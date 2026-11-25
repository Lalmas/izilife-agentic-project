<?php
declare(strict_types=1);

$token = '';
foreach (file('C:/xampp/htdocs/izilife-admin/.env', FILE_IGNORE_NEW_LINES) ?: [] as $line) {
    if (preg_match('/^\s*AGENT_SECRET_TOKEN\s*=/', $line)) {
        $token = trim(substr($line, strpos($line, '=') + 1), " \t\n\r\0\x0B\"'");
        break;
    }
}
if ($token === '') throw new RuntimeException('AGENT_SECRET_TOKEN absent ou vide.');

$payload = [
    'scope_type' => 'PLACE',
    'scope_ref' => 'parc-de-jeux',
    'closed_state_ref' => 'ferme-definitivement',
    'is_active' => 0,
    'listable' => 0,
];
$ch = curl_init('https://www.izilife.co/izilife-admin/scraper/agentMaintainLocation');
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
echo json_encode($decoded, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . PHP_EOL;
