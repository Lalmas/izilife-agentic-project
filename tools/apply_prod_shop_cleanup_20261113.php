<?php
declare(strict_types=1);

$envFile = 'C:/xampp/htdocs/izilife-admin/.env';
$token = '';
foreach (file($envFile, FILE_IGNORE_NEW_LINES) ?: [] as $line) {
    if (preg_match('/^\s*AGENT_SECRET_TOKEN\s*=/', $line)) {
        $token = trim(substr($line, strpos($line, '=') + 1), " \t\n\r\0\x0B\"'");
        break;
    }
}
if ($token === '') throw new RuntimeException('AGENT_SECRET_TOKEN absent ou vide.');

$url = 'https://www.izilife.co/izilife-admin/scraper/agentMaintainLocation';

function applyLocation(string $url, string $token, array $payload): array
{
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => ['X-Agent-Token: ' . $token],
        CURLOPT_POSTFIELDS => http_build_query(['payload' => json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)]),
        CURLOPT_TIMEOUT => 90,
        CURLOPT_CONNECTTIMEOUT => 20,
    ]);
    $body = curl_exec($ch);
    $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    $decoded = json_decode((string) $body, true);
    if ($body === false || $status < 200 || $status >= 300 || !is_array($decoded) || empty($decoded['success'])) {
        throw new RuntimeException('HTTP ' . $status . ': ' . ($error ?: (string) $body));
    }
    return $decoded;
}

$closed = [
    'club-discotheque',
    'paulo-lea',
    'club-la-renardiere',
    's-club',
    'scoob4y',
    'la-taniheire',
    'we-love-prod-events-la-decadente',
    'umih-lille-metropole-organisation-professionnelle-patronale-de-l-hotellerie-restauration',
    'planck',
    'la-cav',
    'deli-club',
    'o-paradiz',
    'viabar-barman-evenementiel-atelier-cocktails-drinks-specialist',
];

$jobs = [
    ['scope_type' => 'SHOP', 'scope_ref' => 'le-bus-magique', 'category_refs' => ['bar', 'cafe']],
    ['scope_type' => 'SHOP', 'scope_ref' => 'le-network', 'category_refs' => ['discotheque']],
    ['scope_type' => 'SHOP', 'scope_ref' => 'mojito-pub-lille', 'city_ref' => 'tournai'],
];
foreach ($closed as $ref) {
    $jobs[] = [
        'scope_type' => 'SHOP',
        'scope_ref' => $ref,
        'closed_state_ref' => 'ferme-definitivement',
        'is_active' => 0,
        'listable' => 0,
    ];
}

$results = [];
foreach ($jobs as $payload) {
    try {
        $result = applyLocation($url, $token, $payload);
        $results[] = ['ref' => $payload['scope_ref'], 'ok' => true, 'result' => $result];
        echo "OK\t{$payload['scope_ref']}\t" . json_encode($result, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . PHP_EOL;
    } catch (Throwable $e) {
        $results[] = ['ref' => $payload['scope_ref'], 'ok' => false, 'error' => $e->getMessage()];
        echo "ERROR\t{$payload['scope_ref']}\t{$e->getMessage()}" . PHP_EOL;
    }
}

$errors = array_filter($results, static fn(array $row): bool => !$row['ok']);
exit($errors ? 1 : 0);
