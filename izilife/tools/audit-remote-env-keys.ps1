[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $HostName,

    [Parameter(Mandatory = $true)]
    [string] $UserName,

    [Parameter(Mandatory = $true)]
    [ValidateSet('staging', 'production')]
    [string] $Environment,

    [string] $RemoteFoRoot = '/var/www/html/izilife',
    [string] $RemoteBoRoot = '/var/www/html/izilife-admin',
    [string] $RemotePsRoot = '/var/www/html/izilife-partner-admin',
    [string] $PlinkPath = ''
)

$ErrorActionPreference = 'Stop'

function Find-Plink {
    param([string] $RequestedPath)

    if ($RequestedPath -and (Test-Path -LiteralPath $RequestedPath)) {
        return (Resolve-Path -LiteralPath $RequestedPath).Path
    }

    $command = Get-Command plink.exe -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    $usualPath = Join-Path $env:ProgramFiles 'PuTTY\plink.exe'
    if (Test-Path -LiteralPath $usualPath) {
        return $usualPath
    }

    throw 'plink.exe est introuvable. Installez PuTTY ou passez -PlinkPath "C:\chemin\plink.exe".'
}

function Get-EnvKeySet {
    param([string] $Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Fichier local introuvable : $Path"
    }

    $keys = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    foreach ($line in [System.IO.File]::ReadLines($Path)) {
        if ($line -match '^\s*(?![#;])([A-Za-z_][A-Za-z0-9_.-]*)\s*=') {
            [void] $keys.Add($Matches[1])
        }
    }
    return $keys
}

function Quote-Sh {
    param([string] $Value)
    $embeddedQuote = "'" + '"' + "'" + '"' + "'"
    return "'" + $Value.Replace("'", $embeddedQuote) + "'"
}

$tool = Find-Plink -RequestedPath $PlinkPath
$repoRoot = Split-Path -Parent $PSScriptRoot
$htdocsRoot = Split-Path -Parent $repoRoot

$apps = @(
    [pscustomobject]@{ Name = 'FO'; Local = Join-Path $htdocsRoot 'izilife\.env'; Remote = ($RemoteFoRoot.TrimEnd('/') + '/.env') },
    [pscustomobject]@{ Name = 'BO'; Local = Join-Path $htdocsRoot 'izilife-admin\.env'; Remote = ($RemoteBoRoot.TrimEnd('/') + '/.env') },
    [pscustomobject]@{ Name = 'PS'; Local = Join-Path $htdocsRoot 'izilife-partner-admin\.env'; Remote = ($RemotePsRoot.TrimEnd('/') + '/.env') }
)

$remoteParts = @('set -eu')
foreach ($app in $apps) {
    $remotePath = Quote-Sh $app.Remote
    $remoteParts += "printf '__IZILIFE_APP__%s\n' '$($app.Name)'"
    $remoteParts += ('if [ ! -f {0} ]; then printf ''__ENV_FILE_MISSING__\n''; else ci_env=$(sed -nE ''s/^[[:space:]]*CI_ENVIRONMENT[[:space:]]*=[[:space:]]*([^[:space:]#;]+).*/\1/p'' {0} | tail -n 1); printf ''__CI_ENVIRONMENT__%s\n'' "$ci_env"; sed -nE ''s/^[[:space:]]*([A-Za-z_][A-Za-z0-9_.-]*)[[:space:]]*=.*/\1/p'' {0} | sort -u; fi' -f $remotePath)
}
$remoteCommand = $remoteParts -join '; '

Write-Host "Audit $Environment sur $HostName. Saisissez le mot de passe SSH dans l'invite de PuTTY si elle apparaît." -ForegroundColor Cyan
Write-Host 'Aucune valeur .env ne sera renvoyée.' -ForegroundColor DarkGray

$remoteOutput = & $tool -ssh "$UserName@$HostName" $remoteCommand
if ($LASTEXITCODE -ne 0) {
    throw "La connexion ou l'audit SSH a échoué (code $LASTEXITCODE)."
}

$remoteByApp = @{}
$remoteEnvironmentByApp = @{}
$currentApp = $null
foreach ($line in @($remoteOutput)) {
    if ($line -match '^__IZILIFE_APP__(FO|BO|PS)$') {
        $currentApp = $Matches[1]
        $remoteByApp[$currentApp] = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
        continue
    }
    if ($currentApp -and $line -eq '__ENV_FILE_MISSING__') {
        $remoteByApp[$currentApp] = $null
        continue
    }
    if ($currentApp -and $line -match '^__CI_ENVIRONMENT__(.*)$') {
        $remoteEnvironmentByApp[$currentApp] = $Matches[1].Trim()
        continue
    }
    if ($currentApp -and $line -match '^[A-Za-z_][A-Za-z0-9_.-]*$' -and $null -ne $remoteByApp[$currentApp]) {
        [void] $remoteByApp[$currentApp].Add($line)
    }
}

$hasMissing = $false
foreach ($app in $apps) {
    Write-Host "`n[$($app.Name)] $Environment" -ForegroundColor Yellow
    $localKeys = Get-EnvKeySet -Path $app.Local
    $remoteKeys = $remoteByApp[$app.Name]
    if ($null -eq $remoteKeys) {
        Write-Host "ERREUR : fichier distant absent ($($app.Remote))" -ForegroundColor Red
        $hasMissing = $true
        continue
    }

    $actualEnvironment = [string] $remoteEnvironmentByApp[$app.Name]
    if ($actualEnvironment -ne $Environment) {
        Write-Host "ERREUR : CI_ENVIRONMENT=$actualEnvironment, cible demandée=$Environment" -ForegroundColor Red
        $hasMissing = $true
    } else {
        Write-Host "CI_ENVIRONMENT=$actualEnvironment" -ForegroundColor Green
    }

    $missing = @($localKeys | Where-Object { -not $remoteKeys.Contains($_) } | Sort-Object)
    $additional = @($remoteKeys | Where-Object { -not $localKeys.Contains($_) } | Sort-Object)

    if ($missing.Count -eq 0) {
        Write-Host 'Variables locales absentes du serveur : aucune' -ForegroundColor Green
    } else {
        $hasMissing = $true
        Write-Host 'Variables locales absentes du serveur :' -ForegroundColor Red
        $missing | ForEach-Object { Write-Host "  - $_" }
    }

    if ($additional.Count -eq 0) {
        Write-Host 'Variables propres au serveur : aucune' -ForegroundColor Green
    } else {
        Write-Host 'Variables propres au serveur (valeurs non affichées) :' -ForegroundColor DarkYellow
        $additional | ForEach-Object { Write-Host "  - $_" }
    }
}

if ($hasMissing) {
    Write-Host "`nAUDIT INCOMPLET : au moins une variable ou un fichier manque." -ForegroundColor Red
    exit 2
}

Write-Host "`nAUDIT OK : toutes les clés locales existent dans les trois .env $Environment." -ForegroundColor Green
exit 0
