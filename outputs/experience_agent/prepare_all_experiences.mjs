import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/alcamara/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const inputPath = "C:/Users/alcamara/Documents/agentic_Workspace/outputs/experience_agent/experiences_all_source.xlsx";
const outputPath = "C:/Users/alcamara/Documents/agentic_Workspace/outputs/experience_agent/experiences_all_ready.xlsx";
const outDir = "C:/Users/alcamara/Documents/agentic_Workspace/outputs/experience_agent";
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));
const ws = wb.worksheets.getItem("Experiences");
const used = ws.getUsedRange(true);
const values = used.values;
const headers = values[0].map(v => String(v ?? "").trim());
const col = Object.fromEntries(headers.map((h, i) => [h, i]));

const before = await wb.render({sheetName:"Experiences", range:"A1:AK18", scale:0.8, format:"png"});
await fs.writeFile(`${outDir}/experiences_before.png`, new Uint8Array(await before.arrayBuffer()));

const slug = (text) => String(text ?? "").normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 150);
const contains = (text, words) => words.some(w => text.includes(w));
const classify = (title, description) => {
  const t = `${title} ${description}`.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  if (contains(t,["jeu de piste","chasse au tresor","escape game"])) return "jeu-de-piste";
  if (contains(t,["degustation","biere","whisky","food tour","gourmand"])) return "balade-gourmande";
  if (contains(t,["atelier","creez","creation","initiation","cours de cuisine","parfum","bijou"])) return "atelier";
  if (contains(t,["running","run club","bootcamp","pratique libre","danse","fitness","club runner","cavale"])) return "activite-collective";
  if (contains(t,["bateau","barque","bacove","croisiere","marais"])) return "croisiere-en-bateau";
  if (contains(t,["visite","tour","decouverte","beffroi","citadelle","bus","2cv","architecture"])) return "visite-guidee";
  return "activite-collective";
};
const commercialPlatforms = new Set(["Funbooker","Babasport","Fever","Viator","GetYourGuide"]);
const eligible = new Set(["NEW_CANDIDATE","TO_VERIFY"]);
let changed = 0;
for (let r = 1; r < values.length; r++) {
  const row = values[r];
  const review = String(row[col.review_status] ?? "").trim();
  if (String(row[col.status] ?? "").toLowerCase() !== "skip" || !eligible.has(review)) continue;
  const title = String(row[col.title] ?? "").trim();
  const desc = String(row[col.description] ?? "").trim();
  const platform = String(row[col.source_platform] ?? "").trim();
  row[col.experience_string_id] = slug(`${title}-${row[col.city_ref] || "lille"}`);
  row[col.experience_type_ref] = classify(title, desc);
  row[col.access_type_ref] = commercialPlatforms.has(platform) ? "acces-payant" : "libre-et-gratuit";
  row[col.booking_needed_ref] = commercialPlatforms.has(platform) ? "uniquement-sur-reservation" : "sans-reservation-possible";
  if (!row[col.duration]) row[col.duration] = 1;
  const unit = String(row[col.duration_measurement_unity_id] ?? "").trim().toLowerCase();
  row[col.duration_measurement_unity_id] = unit === "m" ? 2 : 1;
  row[col.exterior] = row[col.exterior] || "non";
  row[col.with_equipment] = row[col.with_equipment] || "non";
  row[col.equipment_gived] = row[col.equipment_gived] || "non";
  row[col.is_nocturnal] = row[col.is_nocturnal] || "non";
  row[col.noise_level] = row[col.noise_level] ?? 0;
  row[col.participation_mode] = row[col.participation_mode] || (row[col.experience_type_ref] === "activite-collective" ? "open_group" : "individual");
  row[col.is_for_kids] = row[col.is_for_kids] || "non";
  row[col.accessible_for_kids] = row[col.accessible_for_kids] || "non";
  row[col.is_insolite] = row[col.is_insolite] || "non";
  row[col.experience_in_all_city] = row[col.experience_in_all_city] || "oui";
  row[col.place_visit] = row[col.place_visit] || "non";
  row[col.status] = "pending";
  row[col.last_result] = null;
  row[col.notes] = `${row[col.notes] || ""} | Création inactive autorisée le 2026-11-03; champs incomplets préremplis pour validation BO.`.trim();
  ws.getRangeByIndexes(r, 0, 1, headers.length).values = [row];
  changed++;
}

wb.recalculate();
const check = await wb.inspect({kind:"region", sheetId:"Experiences", range:"A1:AK84", maxChars:7000, tableMaxRows:8, tableMaxCols:12});
console.log(check.ndjson);
const errors = await wb.inspect({kind:"match", searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options:{useRegex:true,maxResults:100}, maxChars:3000});
console.log(errors.ndjson);
const after = await wb.render({sheetName:"Experiences", range:"A1:AK18", scale:0.8, format:"png"});
await fs.writeFile(`${outDir}/experiences_after.png`, new Uint8Array(await after.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(outputPath);
console.log(JSON.stringify({changed, outputPath}));
