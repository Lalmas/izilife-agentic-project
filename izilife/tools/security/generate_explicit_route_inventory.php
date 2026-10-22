<?php

declare(strict_types=1);

/**
 * Generate a source-only inventory of explicitly declared routes.
 * This does not bootstrap CodeIgniter and never reads .env or database config.
 */
$foRoot = dirname(__DIR__, 2);
$apps = [
    'FO' => $foRoot,
    'BO' => dirname($foRoot) . DIRECTORY_SEPARATOR . 'izilife-admin',
    'Partner' => dirname($foRoot) . DIRECTORY_SEPARATOR . 'izilife-partner-admin',
];
$verbs = 'get|post|put|patch|delete|options|head|match|add';
$routeCounts = [];
$routeDrafts = [];

foreach ($apps as $appName => $root) {
    $routesPath = $root . DIRECTORY_SEPARATOR . 'app' . DIRECTORY_SEPARATOR . 'Config'
        . DIRECTORY_SEPARATOR . 'Routes.php';
    if (! is_file($routesPath)) {
        throw new RuntimeException("Missing route file for {$appName}: {$routesPath}");
    }
    $routeLines = file($routesPath, FILE_IGNORE_NEW_LINES);
    $routeGroups = [];
    $insideBlockComment = false;
    $groupedRouteDefinitions = [];
    $routeCount = 0;
    foreach ($routeLines as $index => $line) {
        $trimmed = trim($line);
        if ($insideBlockComment) {
            if (str_contains($trimmed, '*/')) {
                $insideBlockComment = false;
            }
            continue;
        }
        if (str_starts_with($trimmed, '/*')) {
            if (! str_contains($trimmed, '*/')) {
                $insideBlockComment = true;
            }
            continue;
        }
        if ($trimmed === '' || str_starts_with($trimmed, '//') || str_starts_with($trimmed, '#')) {
            if (preg_match('/^\}\s*\);/', $trimmed) === 1 && $routeGroups !== []) {
                array_pop($routeGroups);
            }
            continue;
        }
        if (preg_match('/\$routes->group\(\s*[\'\"](?<prefix>[^\'\"]*)[\'\"]/i', $line, $groupMatch) === 1) {
            preg_match('/[\'\"]filter[\'\"]\s*=>\s*[\'\"](?<filter>[^\'\"]+)[\'\"]/', $line, $filterMatch);
            $routeGroups[] = [
                'prefix' => trim($groupMatch['prefix'], '/'),
                'filter' => $filterMatch['filter'] ?? null,
            ];
        }
        $pattern = '/\$routes->(?<verb>' . $verbs . ')\s*\(\s*[\'\"](?<uri>[^\'\"]+)[\'\"]\s*,\s*[\'\"](?<target>[^\'\"]+)[\'\"](?<tail>.*?)\);\s*$/i';
        if (preg_match($pattern, $line, $match) === 1) {
            $routeCount++;
            $verb = strtoupper($match['verb']);
            $prefixes = array_map(static fn (array $group): string => $group['prefix'], $routeGroups);
            $uriParts = array_values(array_filter([...$prefixes, trim($match['uri'], '/')], static fn (string $part): bool => $part !== ''));
            $uri = implode('/', $uriParts);
            $controller = explode('::', $match['target'], 2)[0];
            $filters = array_values(array_unique(array_filter(array_map(
                static fn (array $group): ?string => $group['filter'],
                $routeGroups
            ))));
            if (preg_match('/[\'\"]filter[\'\"]\s*=>\s*[\'\"](?<filter>[^\'\"]+)[\'\"]/', $match['tail'], $routeFilter) === 1) {
                $filters[] = $routeFilter['filter'];
            }
            $filters = array_values(array_unique($filters));
            $options = $match['tail'];
            if ($filters !== [] && preg_match('/[\'\"]filter[\'\"]\s*=>/', $options) !== 1) {
                $options = ", ['filter' => '" . implode(',', $filters) . "']";
            }
            $definition = sprintf("\$routes->%s('%s', '%s'%s);", strtolower($match['verb']), $uri, $match['target'], $options);
            $groupedRouteDefinitions[$controller][] = $definition;
        }
        if (preg_match('/^\}\s*\);/', $trimmed) === 1 && $routeGroups !== []) {
            array_pop($routeGroups);
        }
    }
    // Verified active BO forms use these legacy URIs, while the controller
    // methods are post-prefixed under improved auto-routing. Include the
    // explicit POST aliases in the grouped draft even though the live route
    // file does not declare them yet.
    if ($appName === 'BO') {
        $verifiedMissingRoutes = [
            "\$routes->post('scraper/confirmEvent/(:num)/(:num)', 'Scraper::postConfirmEvent/\$1/\$2', ['filter' => 'csrf']);",
            "\$routes->post('scraper/classifyPoi/(:num)/(:num)', 'Scraper::postClassifyPoi/\$1/\$2', ['filter' => 'csrf']);",
        ];
        foreach ($verifiedMissingRoutes as $definition) {
            if (! in_array($definition, $groupedRouteDefinitions['Scraper'] ?? [], true)) {
                $groupedRouteDefinitions['Scraper'][] = $definition;
            }
        }
    }
    $routeDrafts[$appName] = $groupedRouteDefinitions;
    $routeCounts[$appName] = $routeCount;
}

$draftHeader = "<?php\n\nuse CodeIgniter\\Router\\RouteCollection;\n\n/** @var RouteCollection \$routes */\n\n// REVIEW DRAFT: grouped by controller from existing explicit declarations.\n// Auto-routing remains enabled; this file alone is not a complete migration.\n";
foreach ($routeDrafts as $appName => $controllers) {
    ksort($controllers, SORT_NATURAL | SORT_FLAG_CASE);
    $draft = $draftHeader;
    foreach ($controllers as $controller => $definitions) {
        $shortName = substr($controller, strrpos($controller, '\\') !== false ? strrpos($controller, '\\') + 1 : 0);
        $draft .= "\n// {$shortName}\n" . implode("\n", $definitions) . "\n";
    }
    $draftPath = $foRoot . DIRECTORY_SEPARATOR . 'docs' . DIRECTORY_SEPARATOR . 'qa'
        . DIRECTORY_SEPARATOR . 'Routes_' . $appName . '_GROUPED_DRAFT.php';
    file_put_contents($draftPath, $draft);
}

$ajaxLinesByApp = [];
$ajaxCounts = [];
$staticApis = ['fetch', 'XMLHttpRequest constructor', 'jQuery AJAX', 'Axios'];
$staticScopeNote = 'Static source candidates only: verify the rendered URL and method before using as a runtime test. Paths are generated through app helpers; never hard-code a local subdirectory prefix. FO controller names previously identified as inactive are flagged and excluded from the active test set pending owner confirmation.';
$ajaxPattern = '/\bfetch\s*\(|\bnew\s+XMLHttpRequest\s*\(|\$\.(?:ajax|getJSON|get|post)\s*\(|\baxios\.(?:get|post|put|patch|delete)\s*\(/i';
foreach ($apps as $appName => $root) {
    $ajaxLinesByApp[$appName] = [
        '# ' . $appName . ' — AJAX/HTTP call sites',
        '',
        $staticScopeNote,
        '',
        '| Scope | Method (inferred) | API | Endpoint expression | Source |',
        '|---|---|---|---|---|',
    ];
    $ajaxCount = 0;
    $scanRoots = [
        $root . DIRECTORY_SEPARATOR . 'app' . DIRECTORY_SEPARATOR . 'Views',
        $root . DIRECTORY_SEPARATOR . 'statics' . DIRECTORY_SEPARATOR . 'js',
    ];
    foreach ($scanRoots as $scanRoot) {
        if (! is_dir($scanRoot)) {
            continue;
        }
        $iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($scanRoot, FilesystemIterator::SKIP_DOTS));
        foreach ($iterator as $file) {
            if (! $file->isFile() || ! in_array(strtolower($file->getExtension()), ['php', 'js'], true)) {
                continue;
            }
            $sourceLines = file($file->getPathname(), FILE_IGNORE_NEW_LINES);
            foreach ($sourceLines as $index => $sourceLine) {
                if (preg_match_all($ajaxPattern, $sourceLine, $matches, PREG_OFFSET_CAPTURE) === 0) {
                    continue;
                }
                foreach ($matches[0] as $match) {
                    $token = strtolower($match[0]);
                    $callType = strtolower($match[0]);
                    $api = str_contains($token, 'xmlhttprequest') ? 'XMLHttpRequest'
                        : (str_contains($token, 'fetch') ? 'fetch' : (str_contains($token, 'axios') ? 'axios' : 'jQuery'));
                    $contextLines = array_slice($sourceLines, $index, 24);
                    $contextLines[0] = substr($contextLines[0], $match[1]);
                    foreach ($contextLines as $contextIndex => $contextLine) {
                        if ($contextIndex > 0 && preg_match('/^\s*\}\s*\)\s*;?/', $contextLine) === 1) {
                            $contextLines = array_slice($contextLines, 0, $contextIndex + 1);
                            break;
                        }
                    }
                    $context = implode("\n", $contextLines);
                    $method = 'inspect';
                    $endpoint = 'computed/dynamic — inspect source';
                    if (str_contains($callType, 'xmlhttprequest')) {
                        $method = 'inspect xhr.open()';
                        if (preg_match('/\.open\s*\(\s*[\'\"](GET|POST|PUT|PATCH|DELETE)[\'\"]\s*,\s*([^,\)]+)/i', $context, $endpointMatch) === 1) {
                            $method = strtoupper($endpointMatch[1]);
                            $endpoint = trim($endpointMatch[2]);
                        }
                    } elseif (str_contains($callType, 'fetch')) {
                        $method = 'GET*';
                        if (preg_match('/\bfetch\s*\(\s*([^,\)]+)/i', $context, $endpointMatch) === 1) {
                            $endpoint = trim($endpointMatch[1]);
                        }
                        if (preg_match('/\bmethod\s*:\s*[\'\"](GET|POST|PUT|PATCH|DELETE)/i', $context, $methodMatch) === 1) {
                            $method = strtoupper($methodMatch[1]);
                        }
                    } elseif (preg_match('/\$\.(?<verb>getJSON|get|post)\s*\(\s*([^,\)]+)/i', $match[0] . substr($sourceLine, $match[1] + strlen($match[0])), $endpointMatch) === 1) {
                        $method = strtolower($endpointMatch['verb']) === 'post' ? 'POST' : 'GET';
                        $endpoint = trim($endpointMatch[2]);
                    } elseif (preg_match('/\baxios\.(?<verb>get|post|put|patch|delete)\s*\(\s*([^,\)]+)/i', $match[0] . substr($sourceLine, $match[1] + strlen($match[0])), $endpointMatch) === 1) {
                        $method = strtoupper($endpointMatch['verb']);
                        $endpoint = trim($endpointMatch[2]);
                    } else {
                        if (preg_match('/\b(?:method|type)\s*:\s*[\'\"](GET|POST|PUT|PATCH|DELETE)/i', $context, $methodMatch) === 1) {
                            $method = strtoupper($methodMatch[1]);
                        }
                        if (preg_match('/\burl\s*:\s*([^,\r\n]+)/i', $context, $endpointMatch) === 1) {
                            $endpoint = trim($endpointMatch[1]);
                        }
                    }
                    $relative = substr($file->getPathname(), strlen($root) + 1);
                    $inactiveFoSource = $appName === 'FO' && preg_match(
                        '#(?:^|/)(?:activity|author|authors|book|books|borrow|izikids|kidactivity|kidcontent|magazine|outing|outings|reading|space|spaces)(?:/|\\.|$)#i',
                        str_replace(DIRECTORY_SEPARATOR, '/', $relative)
                    ) === 1;
                    $inactiveFoEndpoint = $appName === 'FO' && preg_match(
                        '#(?:^|/)(?:activity|author|book|borrow|izikids|kidactivity|kidcontent|magazine|outing|reading|space)/#i',
                        trim($endpoint, "'\"` ")
                    ) === 1;
                    $scope = ($inactiveFoSource || $inactiveFoEndpoint)
                        ? 'Inactive candidate — exclude pending confirmation'
                        : 'Reachability unverified';
                    $safe = static fn (string $value): string => str_replace(['|', '`'], ['\\|', '\\`'], $value);
                    $ajaxLinesByApp[$appName][] = sprintf('| %s | %s | %s | `%s` | `%s:%d` |', $scope, $method, $api,
                        $safe($endpoint), $safe(str_replace(DIRECTORY_SEPARATOR, '/', $relative)), $index + 1);
                    $ajaxCount++;
                }
            }
        }
    }
    $ajaxCounts[$appName] = $ajaxCount;
    $ajaxPath = $foRoot . DIRECTORY_SEPARATOR . 'docs' . DIRECTORY_SEPARATOR . 'qa'
        . DIRECTORY_SEPARATOR . 'AJAX_CALLSITES_' . $appName . '.md';
    file_put_contents($ajaxPath, implode(PHP_EOL, $ajaxLinesByApp[$appName]) . PHP_EOL);
}
foreach ($apps as $appName => $_) {
    fwrite(STDOUT, sprintf("%s: %d explicit routes grouped; %d AJAX/HTTP call-site candidates\n", $appName, $routeCounts[$appName], $ajaxCounts[$appName]));
}
