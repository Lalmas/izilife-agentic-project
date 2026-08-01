# izilife — Socle technique des agents

> Charger aussi : izilife-global.md, dev/architecture.md

## postIngestJson() — à créer dans Scraper.php

Ajouter dans App\Controllers\Scraper, protégée par scope `agent:ingest`.

```php
public function postIngestJson()
{
    // Scope check
    if ($deny = $this->denyServiceAgentWithoutScope('agent:ingest')) {
        return $deny;
    }

    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    if (!$data || empty($data['type'])) {
        return $this->response->setStatusCode(400)
            ->setJSON(['success' => false, 'error' => 'Missing type']);
    }

    $type   = $data['type'];   // place|shop|event|experience|equipment|circuit|deal|promo_code|local_habit
    $source = $data['source'] ?? 'agent';
    $fields = $data['fields'] ?? [];

    // Router vers le bon model staging selon $type
    switch ($type) {
        case 'event':
            $id = $this->scraping_event_tmp_model->insert([...]);
            break;
        case 'experience':
            $id = $this->scraping_experience_tmp_model->insert([...]);
            break;
        case 'place':
        case 'shop':
            $id = $this->scrapingUnmappedPoi_model->insert([...]);
            break;
        // ...
    }

    return $this->response->setJSON([
        'success' => true,
        'type'    => $type,
        'tmp_id'  => $id,
        'source'  => $source,
    ]);
}
```

Types supportés : `place`, `shop`, `event`, `experience`, `equipment`,
`circuit`, `deal`, `promo_code`, `local_habit`

---

## Classe Agent PHP — à créer

Fichier : `app/Libraries/Agents/Agent.php`

```php
namespace App\Libraries\Agents;

use App\Libraries\OpenAI_lib;
use App\Libraries\AIClient_lib;

abstract class Agent
{
    protected string $mdPath;
    protected string $llmProvider;
    protected string $agentMode;

    public function __construct(string $mdPath)
    {
        $this->mdPath      = $mdPath;
        $this->llmProvider = getenv('LLM_PROVIDER') ?: 'gpt';
        $this->agentMode   = getenv('AGENT_MODE')   ?: 'test';
    }

    protected function getSystemPrompt(): string
    {
        return file_get_contents($this->mdPath);
    }

    // Appel indépendant — pas d'historique entre les items
    protected function callLLM(string $userPrompt): array
    {
        // switcher selon $this->llmProvider
        // retourne le JSON parsé (jamais le texte brut)
    }

    protected function pushToIzilife(string $type, array $fields, string $source): array
    {
        // POST vers postIngestJson()
        // Headers : Authorization: Bearer {service_token}
        // retourne {success, type, tmp_id}
    }

    protected function isTestMode(): bool
    {
        return $this->agentMode === 'test';
    }

    abstract public function run(array $input): array;
}
```

---

## Variable LLM (dans config ou .env)
```
LLM_PROVIDER=gpt          # gpt | claude | mistral
AGENT_MODE=test            # test | production
```

```php
const LLM_MODELS = [
    'gpt'     => 'gpt-4o',
    'claude'  => 'claude-sonnet-4-20250514',
    'mistral' => 'mistral-large-latest',
];
```

---

## Mode test
```php
if ($this->isTestMode()) {
    // Traiter max 3 items
    // Logger sans pusher vers izilife
    // Retourner le JSON résultat en sortie
    echo json_encode($result);
    exit;
}
```

---

## Principe des appels en boucle
- 1 item = 1 appel LLM indépendant (contexte remis à zéro)
- System prompt = contenu du .md de l'agent (getSystemPrompt())
- User prompt = données de l'item uniquement
- Réponse attendue : JSON structuré uniquement — jamais de texte libre
- Pas d'historique entre les items — jamais

---

## Modèles staging existants à réutiliser
```php
App\Models\Scraping\ScrapingEventTmp_model
  ->insert([...])
  ->urlRecentlyScraped($url, $days)    // dédup
  ->fileRecentlyScraped($fingerprint, $days)  // dédup image

App\Models\Scraping\ScrapingExperienceTmp_model
  ->insert([...])
  ->urlRecentlyScraped($url, $days)

App\Models\Scraping\ScrapingUnmappedPoi_model
  ->insert([...])   // pour les lieux/shops
```

---

## Score de remplissage
```php
helper('completion_score');
$score = LQ_refresh_completion_score('place', $place_id);
// Types : place, shop, event, experience, equipment, circuit, selection
```
