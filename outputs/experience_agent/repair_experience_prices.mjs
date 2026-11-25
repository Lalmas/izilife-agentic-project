import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/alcamara/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const inputPath = "C:/Users/alcamara/Documents/agentic_Workspace/outputs/experience_agent/experiences_after_run.xlsx";
const outputPath = "C:/Users/alcamara/Documents/agentic_Workspace/outputs/experience_agent/experiences_prices_ready.xlsx";
const outDir = "C:/Users/alcamara/Documents/agentic_Workspace/outputs/experience_agent";
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));
const ws = wb.worksheets.getItem("Experiences");
const values = ws.getUsedRange(true).values;
const headers = values[0].map(v => String(v ?? "").trim());
const col = Object.fromEntries(headers.map((h, i) => [h, i]));

const pricesByUrl = new Map([
  ["https://www.funbooker.com/fr/annonce/initiation-au-pilotage-en-ulm-autogire-a-lille-59/voir", [139, "À partir de 139 €"]],
  ["https://www.babasport.fr/activites/8946-fun-city-tour-a-lille-rallye-decouverte-et-insolite-pour-votre-team-building-evg-evjf", [34, "À partir de 34 €"]],
  ["https://feverup.com/m/615539", [16.90, "À partir de 16,90 €"]],
  ["https://www.getyourguide.com/fr-fr/lille-l643/food-tour-du-midi-decouverte-de-lille-t1397865", [57, "À partir de 57 €"]],
  ["Simulateur de chute libre indoor", [64.90, "À partir de 64,90 €"]],
  ["Parcours des 5 sens type Fort Boyard", [21, "À partir de 21 €"]],
  ["Baptême d’ULM à Bondues", [65, "À partir de 65 €"]],
  ["Bubble Foot indoor à Lezennes", [249, "À partir de 249 € par groupe"]],
  ["Atelier DIY cosmétiques naturels et bio", [20, "À partir de 20 €"]],
  ["Initiation à la dégustation de vin à Lille", [64.80, "À partir de 64,80 €"]],
  ["Bootcamp urbain à Lille", [15, "À partir de 15 €"]],
  ["Escape game outdoor avec GoPro à Lille", [18, "À partir de 18 €"]],
  ["Simulateur Airbus A320 à Lesquin", [109, "À partir de 109 €"]],
  ["Fun City Tour – rallye découverte de Lille", [34, "À partir de 34 €"]],
  ["BuzzAttack – expérience jeu télé en direct", [16.90, "À partir de 16,90 €"]],
  ["Visite privée de Lille en 2CV avec champagne", [70.77, "À partir de 70,77 US$ (tarif source)"]],
  ["Visite de Lille en bus", [18, "À partir de 18 €"]],
  ["Tarot, écriture et création de son oracle", [20, "À partir de 20 €"]],
  ["Food tour du midi – découverte de Lille", [57, "À partir de 57 €"]],
  ["Excursion Lille et Valenciennes en train avec un guide", [399, "À partir de 399 € par personne"]],
  ["Visite d’une brasserie historique et dégustation de bières artisanales", [16, "À partir de 16 €"]],
].map(([title, price]) => [title, price]));

const pricesByTitle = new Map([
  ["Simulateur de chute libre indoor", [64.90, "À partir de 64,90 €"]],
  ["Parcours des 5 sens type Fort Boyard", [21, "À partir de 21 €"]],
  ["Baptême d’ULM à Bondues", [65, "À partir de 65 €"]],
  ["Bubble Foot indoor à Lezennes", [249, "À partir de 249 € par groupe"]],
  ["Atelier DIY cosmétiques naturels et bio", [20, "À partir de 20 €"]],
  ["Initiation à la dégustation de vin à Lille", [64.80, "À partir de 64,80 €"]],
  ["Bootcamp urbain à Lille", [15, "À partir de 15 €"]],
  ["Escape game outdoor avec GoPro à Lille", [18, "À partir de 18 €"]],
  ["Simulateur Airbus A320 à Lesquin", [109, "À partir de 109 €"]],
  ["Fun City Tour – rallye découverte de Lille", [34, "À partir de 34 €"]],
  ["BuzzAttack – expérience jeu télé en direct", [16.90, "À partir de 16,90 €"]],
  ["Visite privée de Lille en 2CV avec champagne", [70.77, "À partir de 70,77 US$ (tarif source)"]],
  ["Visite de Lille en bus", [18, "À partir de 18 €"]],
  ["Tarot, écriture et création de son oracle", [20, "À partir de 20 €"]],
  ["Food tour du midi – découverte de Lille", [57, "À partir de 57 €"]],
  ["Excursion Lille et Valenciennes en train avec un guide", [399, "À partir de 399 € par personne"]],
  ["Visite d’une brasserie historique et dégustation de bières artisanales", [16, "À partir de 16 €"]],
]);

const normalize = value => String(value ?? "").normalize("NFC").replace(/\s+/g, " ").trim();
let changed = 0;
for (let r = 1; r < values.length; r++) {
  const row = values[r];
  if (normalize(row[col.status]).toLowerCase() !== "error") continue;
  const title = normalize(row[col.title]);
  const sourceUrl = normalize(row[col.source_url]);
  if (sourceUrl.includes("saut-en-parachute-en-tandem-a-peronne-80")) {
    row[col.status] = "pending";
    row[col.last_result] = null;
    row[col.notes] = `${normalize(row[col.notes])} | Ville de Péronne ajoutée au référentiel production le 2026-11-03.`;
    ws.getRangeByIndexes(r, 0, 1, headers.length).values = [row];
    changed++;
    continue;
  }
  const price = pricesByUrl.get(sourceUrl) || pricesByTitle.get(title);
  if (!price) continue;
  row[col.basic_price] = price[0];
  row[col.price_text] = price[1];
  row[col.status] = "pending";
  row[col.last_result] = null;
  row[col.notes] = `${normalize(row[col.notes])} | Tarif contrôlé sur la source le 2026-11-03.`;
  ws.getRangeByIndexes(r, 0, 1, headers.length).values = [row];
  changed++;
}

wb.recalculate();
const errors = await wb.inspect({kind:"match", searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options:{useRegex:true,maxResults:100}, maxChars:3000});
console.log(errors.ndjson);
const preview = await wb.render({sheetName:"Experiences", range:"A60:O84", scale:0.8, format:"png"});
await fs.writeFile(`${outDir}/experiences_prices_ready.png`, new Uint8Array(await preview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(outputPath);
console.log(JSON.stringify({changed, outputPath}));
