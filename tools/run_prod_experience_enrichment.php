<?php
declare(strict_types=1);

$envFile = 'C:/xampp/htdocs/izilife-admin/.env';
$env = is_file($envFile) ? file($envFile, FILE_IGNORE_NEW_LINES) : [];
$secretLine = null;
foreach ($env as $line) if (preg_match('/^\s*AGENT_SECRET_TOKEN\s*=/', $line)) { $secretLine=$line; break; }
if ($secretLine === null) {
    throw new RuntimeException('AGENT_SECRET_TOKEN absent du .env local.');
}
$token = trim(substr($secretLine, strpos($secretLine, '=') + 1));
$token = trim($token, " \t\n\r\0\x0B\"'");
if ($token === '') throw new RuntimeException('AGENT_SECRET_TOKEN vide.');
$base = 'https://www.izilife.co/izilife-admin/';
$report = ['started_at'=>date(DATE_ATOM),'staged'=>[],'processed'=>[],'errors'=>[]];

function progress(string $message): void {
    echo '['.date('H:i:s').'] '.$message.PHP_EOL;
    if (function_exists('ob_flush')) @ob_flush();
    flush();
}

function api(string $route, array $payload): array {
    global $token, $base;
    $ch = curl_init($base . $route);
    curl_setopt_array($ch, [
        CURLOPT_POST=>true,
        CURLOPT_RETURNTRANSFER=>true,
        CURLOPT_HTTPHEADER=>['Content-Type: application/json','X-Agent-Token: '.$token],
        CURLOPT_POSTFIELDS=>json_encode($payload, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
        CURLOPT_TIMEOUT=>180,
        CURLOPT_CONNECTTIMEOUT=>20,
    ]);
    $body = curl_exec($ch);
    $status = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    if ($body === false || $status < 200 || $status >= 300) {
        throw new RuntimeException("HTTP $status $route: ".($error ?: mb_substr((string)$body,0,500)));
    }
    $decoded = json_decode((string)$body,true);
    if (!is_array($decoded) || empty($decoded['success'])) throw new RuntimeException("Réponse invalide $route");
    return $decoded;
}

// Toutes les XP actives ayant une URL dans scrapped_from ou scrapping_json.
$after = 0;
do {
    progress("Staging après XP #$after");
    $stage = api('scraper/agentStageExistingExperienceEnrichment', [
        'source_contains'=>'http','after_id'=>$after,'limit'=>200,
    ]);
    foreach (($stage['staged'] ?? []) as $row) $report['staged'][] = $row;
    $after = (int)($stage['next_after_id'] ?? $after);
    $scanned = (int)($stage['scanned'] ?? 0);
    progress('Lot staging: '.$scanned.' scannées, '.count($stage['staged'] ?? []).' préparées');
} while ($scanned > 0);

// Inclut également les existing_backfill restés pending lors d'une relance précédente.
$afterTmp = 0;
do {
    $batch = api('scraper/agentExperienceValidatorCandidates',['after_id'=>$afterTmp,'limit'=>500]);
    $rows = $batch['experiences'] ?? [];
    foreach ($rows as $row) {
        $afterTmp = max($afterTmp,(int)($row['id'] ?? 0));
        $raw = json_decode((string)($row['raw_json'] ?? ''),true);
        if (!is_array($raw) || empty($raw['existing_backfill']['experience_id'])) continue;
        $tmpId=(int)$row['id'];
        try {
            progress("Analyse TMP #$tmpId / XP #".(int)$raw['existing_backfill']['experience_id'].' — '.(string)($row['title'] ?? ''));
            $analysis=api('scraper/agentAnalyzeExperienceTmp',['tmp_id'=>$tmpId,'source_text'=>'']);
            $apply=api('scraper/agentApplyExperienceValidation',[
                'tmp_id'=>$tmpId,'proposal'=>$analysis['proposal'] ?? [],'validate'=>true,'activate'=>true,
            ]);
            $report['processed'][]=[
                'tmp_id'=>$tmpId,
                'experience_id'=>(int)$raw['existing_backfill']['experience_id'],
                'title'=>$row['title'] ?? null,
                'validated'=>(bool)($apply['validation']['validated'] ?? false),
                'blockers'=>$apply['blockers'] ?? [],
            ];
            progress('Résultat TMP #'.$tmpId.': '.(!empty($apply['validation']['validated']) ? 'validée' : 'bloquée'));
        } catch (Throwable $e) {
            $report['errors'][]=['tmp_id'=>$tmpId,'experience_id'=>(int)$raw['existing_backfill']['experience_id'],'error'=>$e->getMessage()];
            progress('Erreur TMP #'.$tmpId.': '.$e->getMessage());
        }
    }
} while (count($rows) === 500);

$report['finished_at']=date(DATE_ATOM);
$report['summary']=[
    'staged'=>count($report['staged']),
    'processed'=>count($report['processed']),
    'validated'=>count(array_filter($report['processed'],fn($r)=>$r['validated'])),
    'blocked'=>count(array_filter($report['processed'],fn($r)=>!$r['validated'])),
    'errors'=>count($report['errors']),
];
file_put_contents(__DIR__.'/../outputs/prod_experience_enrichment_'.date('Ymd_His').'.json',json_encode($report,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
echo json_encode($report['summary'],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),PHP_EOL;
