param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$packagePath = Join-Path $PSScriptRoot 'cryotera_lille_services_eap_approved.json'
$package = Get-Content -LiteralPath $packagePath -Raw -Encoding UTF8 | ConvertFrom-Json
$base = 'https://www.izilife.co/izilife-admin'
$headers = @{ 'X-Agent-Token' = $env:IZILIFE_AGENT_TOKEN }
if (-not $headers['X-Agent-Token']) { throw 'IZILIFE_AGENT_TOKEN absent.' }
$ref = $package.target.scope_ref
$lookupBody = @{ items = @(@{ type = 'SHOP'; string_id = $ref }); include_graph = $true } | ConvertTo-Json -Depth 6
function Read-Graph {
    $result = Invoke-RestMethod -Uri "$base/scraper/agentInternalDataV0Lookup" -Method Post -Headers $headers -ContentType 'application/json' -Body $lookupBody
    if ($result.items[0].status -ne 'found') { throw 'Fiche Cryotera absente.' }
    return $result.items[0].graph
}
$graph = Read-Graph
if (-not (@($graph.eap)[0].PSObject.Properties.Name -contains 'service_name')) {
    throw 'Le BO production ne publie pas encore service_name dans son export EAP : livrer CurationSyncExport_model avant de lancer cette réparation.'
}
$services = @($package.objects | Where-Object { $_.kind -eq 'element_service' -and $_.review_status -eq 'approved' })
$eaps = @($package.objects | Where-Object { $_.kind -eq 'eap' -and $_.review_status -eq 'approved' })
if ($services.Count -ne 7 -or $eaps.Count -ne 22 -or @($graph.services).Count -ne 7 -or @($graph.eap).Count -ne 22) { throw 'Comptage inattendu : arrêt avant écriture.' }
$serviceNames = @($services | ForEach-Object { $_.item.name } | Sort-Object)
$existingServiceNames = @($graph.services | ForEach-Object { $_.name } | Sort-Object)
$eapNames = @($eaps | ForEach-Object { $_.item.name } | Sort-Object)
$existingEapNames = @($graph.eap | ForEach-Object { $_.name } | Sort-Object)
if ((Compare-Object $serviceNames $existingServiceNames) -or (Compare-Object $eapNames $existingEapNames)) { throw 'Les noms existants ne correspondent pas exactement au paquet.' }
foreach ($obj in $eaps) {
    $row = @($graph.eap | Where-Object { $_.name -ceq $obj.item.name })
    if ($row.Count -ne 1 -or [decimal]$row[0].price -ne [decimal]$obj.item.price -or -not $obj.item.service_name) { throw "EAP différent ou sans Service : $($obj.item.name)" }
}
Write-Output ("Précontrôle : {0} Services existants et {1} EAP existants ; liens visibles : {2}." -f $services.Count,$eaps.Count,@($graph.eap | Where-Object service_name).Count)
if (-not $Apply) { return }
foreach ($obj in $services) {
    $payload = @{ kind = 'element_service'; scope_type = 'SHOP'; scope_ref = $ref; source_url = $obj.source_url; item = $obj.item } | ConvertTo-Json -Depth 20 -Compress
    $result = Invoke-RestMethod -Uri "$base/scraper/agentIngestSiteItem" -Method Post -Headers $headers -Body @{ payload = $payload }
    if (-not $result.success -or $result.created -or -not $result.updated) { throw "Service non corrigé : $($obj.item.name)" }
}
foreach ($obj in $eaps) {
    $payload = @{ kind = 'eap'; scope_type = 'SHOP'; scope_ref = $ref; source_url = $obj.source_url; item = $obj.item } | ConvertTo-Json -Depth 20 -Compress
    $result = Invoke-RestMethod -Uri "$base/scraper/agentIngestSiteItem" -Method Post -Headers $headers -Body @{ payload = $payload }
    if (-not $result.success -or $result.created -or -not $result.updated) { throw "EAP non rattaché : $($obj.item.name)" }
}
$after = Read-Graph
$linked = @($after.eap | Where-Object service_name)
$published = @($after.services | Where-Object { $_.status -eq '2' -and $_.is_active -eq '1' })
$wrong = @($after.eap | Where-Object { $name = $_.name; $expected = @($eaps | Where-Object { $_.item.name -ceq $name })[0].item.service_name; $_.service_name -cne $expected })
Write-Output ("Après correction : Services publiés {0}/7 ; EAP liés au bon Service {1}/22 ; EAP actifs {2}/22." -f $published.Count,(22-$wrong.Count),@($after.eap | Where-Object { $_.is_active -eq '1' }).Count)
if ($published.Count -ne 7 -or $linked.Count -ne 22 -or $wrong.Count -ne 0) { throw 'Vérification finale incomplète.' }
