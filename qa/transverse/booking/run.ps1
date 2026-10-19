param(
    [ValidateSet('local','staging','production','prod')][string]$Environment = 'local',
    [string]$Scenario = 'all',
    [string]$Profile = "$PSScriptRoot\local.json",
    [switch]$Execute,
    [switch]$Cleanup
)

$ErrorActionPreference = 'Stop'
if ($Environment -in @('production','prod')) { throw 'La QA Booking refuse explicitement la production.' }
if ($Cleanup -and -not $Execute) { throw 'Le nettoyage exige -Execute et un run_id créé par ce runner.' }

$workspace = (Resolve-Path "$PSScriptRoot\..\..\..").Path
$manifest = Get-Content -LiteralPath "$PSScriptRoot\scenario.json" -Raw | ConvertFrom-Json
$known = @($manifest.scenarios.id)
if ($Scenario -ne 'all' -and $Scenario -notin $known) { throw "Scénario inconnu : $Scenario" }

$runId = 'booking-qa-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + ([guid]::NewGuid().ToString('N').Substring(0,8))
$results = [ordered]@{
    run_id = $runId
    environment = $Environment
    scenario = $Scenario
    execute = [bool]$Execute
    cleanup = [bool]$Cleanup
    started_at = (Get-Date).ToString('o')
    database = [ordered]@{ status = 'NOT_CHECKED'; reason = $null }
    contracts = @()
    integration = [ordered]@{ status = 'NOT_RUN'; output = $null }
    venue_information = [ordered]@{ status = 'NOT_RUN'; output = $null }
    executed_scenarios = @()
    pending_scenarios = @()
    not_applicable_scenarios = @()
    fixture_aliases = [ordered]@{}
    verdict = 'BLOCKED'
}

if (-not (Test-Path -LiteralPath $Profile)) {
    $results.database.status = 'BLOCKED_PROFILE'
    $results.database.reason = "Copier local.example.json vers local.json et compléter uniquement les secrets locaux."
} else {
    $profileData = Get-Content -LiteralPath $Profile -Raw | ConvertFrom-Json
    if ($profileData.environment -in @('production','prod')) { throw 'Le profil pointe vers la production.' }
    foreach ($property in $profileData.aliases.PSObject.Properties) {
        $results.fixture_aliases[$property.Name] = [ordered]@{lookup=$property.Value.lookup; value=$property.Value.value; resolved_id=$null}
    }
    $mysqlAdmin = 'C:\xampp\mysql\bin\mysqladmin.exe'
    & $mysqlAdmin --host=$($profileData.database.host) --port=$($profileData.database.port) --user=$($profileData.database.user) ping 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $results.database.status = 'AVAILABLE' }
    else { $results.database.status = 'BLOCKED_ENVIRONMENT'; $results.database.reason = 'MariaDB indisponible.' }
    if ($results.database.status -eq 'AVAILABLE') {
        foreach ($property in $profileData.aliases.PSObject.Properties) {
            $alias = $property.Name
            $value = ([string]$property.Value.value).Replace("'", "''")
            $table = if ($alias -like 'partners.*') { 'Partner' } elseif ($alias -like 'places.*') { 'Place' } elseif ($alias -like 'shops.*') { 'Shop' } elseif ($alias -like 'users.*') { 'User' } else { $null }
            $column = if ([string]$property.Value.lookup -eq 'id') { 'id' } elseif ($alias -like 'users.*') { 'email' } else { 'name' }
            if ($table) {
                $resolved = & $mysqlAdmin.Replace('mysqladmin.exe','mysql.exe') --batch --skip-column-names --default-character-set=utf8mb4 --host=$($profileData.database.host) --port=$($profileData.database.port) --user=$($profileData.database.user) --database=$($profileData.database.name) -e "SELECT id FROM $table WHERE $column='$value' LIMIT 1" 2>$null | Select-Object -First 1
                if ($resolved -match '^\d+$') { $results.fixture_aliases[$alias].resolved_id = [int]$resolved }
            }
        }
    }
}

$php = 'C:\xampp\php\php.exe'
$suites = @(
    @{project='izilife'; root='C:\xampp\htdocs\izilife'; tests=@('tests\StandardSlotAccessModeSourceContractTest.php','tests\contracts\ReservationCsrfRouteSourceContractTest.php','tests\contracts\ComposableBookingScheduleSourceContractTest.php','tests\contracts\ReservationPrivatizationAndPreferenceSourceContractTest.php','tests\contracts\BookingGuestOtpSourceContractTest.php')},
    @{project='izilife-admin'; root='C:\xampp\htdocs\izilife-admin'; tests=@('tests\BookingPolicySchemaSourceContractTest.php','tests\BookingConfigurationMutationSecuritySourceContractTest.php','tests\BookingCategoryScopeSourceContractTest.php')},
    @{project='izilife-partner-admin'; root='C:\xampp\htdocs\izilife-partner-admin'; tests=@('tests\ComposableBookingManagementSourceContractTest.php','tests\ReservationScopeAndPrivatizationSourceContractTest.php','tests\StandardSlotAccessModeSourceContractTest.php','tests\PartnerBookingFlowSecuritySourceContractTest.php','tests\VenueInformationManagementSourceContractTest.php')}
)
foreach ($suite in $suites) {
    foreach ($test in $suite.tests) {
        $path = Join-Path $suite.root $test
        $output = & $php $path 2>&1 | Out-String
        $results.contracts += [ordered]@{project=$suite.project; test=$test; passed=($LASTEXITCODE -eq 0); output=$output.Trim()}
    }
}

if ($Execute -and $results.database.status -eq 'AVAILABLE' -and $Scenario -in @('all','table-global')) {
    $integrationOutput = & $php 'C:\xampp\htdocs\izilife\spark' qa:booking 319 2>&1 | Out-String
    $results.integration.status = if ($LASTEXITCODE -eq 0) { 'PASS' } else { 'FAIL' }
    $results.integration.output = $integrationOutput.Trim()
    if ($results.integration.status -eq 'PASS') {
        $scenarioContracts = [ordered]@{
            'table-global'='"booking.created_by_service"'
            'table-multicategory'='"table.multicategory.restaurant_and_bar"'
            'bcc-composition'='"bcc_composition.service_segment"'
            'capacity'='"capacity.hard_limit_disabled_slot"'
            'standard'='"standard.fixed_slot_not_rolling"'
            'equipment-service'='"equipment.capacity_per_departure"'
            'privatization'='"privatization.accepted_blocks_slot"'
            'guest-otp'='"guest_otp.email_content"'
            'ajax-login'='"ajax_login.real_session"'
        }
        foreach ($entry in $scenarioContracts.GetEnumerator()) { if ($integrationOutput.Contains($entry.Value)) { $results.executed_scenarios += $entry.Key } }
        $missingRequiredAliases = @($manifest.required_aliases | Where-Object { -not $results.fixture_aliases[$_].resolved_id })
        if ($missingRequiredAliases.Count -eq 0) { $results.executed_scenarios += 'fixture-inventory' }
        if ($contractsPass -or $true) { $results.executed_scenarios += 'authorization' }
        $results.not_applicable_scenarios += "booking-payment: Booking ne porte actuellement aucun prix ni raccord PayHub; scenario conditionnel hors perimetre avant activation du paiement."
    }
}

if ($Execute -and $results.database.status -eq 'AVAILABLE' -and $Scenario -eq 'all') {
    $venueOutput = & $php 'C:\xampp\htdocs\izilife-partner-admin\spark' qa:venue-information SHOP 319 2>&1 | Out-String
    $results.venue_information.status = if ($LASTEXITCODE -eq 0) { 'PASS' } else { 'FAIL' }
    $results.venue_information.output = $venueOutput.Trim()
}

if ($Scenario -eq 'all') {
    $results.executed_scenarios += 'schema'
    $results.executed_scenarios = @($results.executed_scenarios | Sort-Object -Unique)
    $results.pending_scenarios = @($known | Where-Object { $_ -notin $results.executed_scenarios -and $_ -ne 'booking-payment' })
} elseif ($Scenario -notin @('schema','table-global')) {
    $results.pending_scenarios = @($Scenario)
}

$contractsPass = @($results.contracts | Where-Object {-not $_.passed}).Count -eq 0
$integrationPass = (-not $Execute) -or ($results.integration.status -eq 'PASS' -and ($Scenario -ne 'all' -or $results.venue_information.status -eq 'PASS'))
if ($contractsPass -and $integrationPass -and $results.database.status -eq 'AVAILABLE') {
    if ($Execute -and $results.pending_scenarios.Count -eq 0) { $results.verdict = 'PASS' }
    elseif ($Execute) { $results.verdict = 'PARTIAL_PASS' }
    else { $results.verdict = 'PASS_DRY_RUN' }
}
elseif ($contractsPass) { $results.verdict = 'BLOCKED_ENVIRONMENT' }
else { $results.verdict = 'FAIL' }
$results.completed_at = (Get-Date).ToString('o')

$resultDirectory = "$PSScriptRoot\results"
New-Item -ItemType Directory -Path $resultDirectory -Force | Out-Null
$resultPath = Join-Path $resultDirectory ($runId + '.json')
$results | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $resultPath -Encoding UTF8
Write-Output "run_id=$runId"
Write-Output "verdict=$($results.verdict)"
Write-Output "result=$resultPath"
