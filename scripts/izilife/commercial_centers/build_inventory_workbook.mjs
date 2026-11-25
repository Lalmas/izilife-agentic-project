import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const artifactToolUrl = pathToFileURL(
  "C:/Users/alcamara/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs",
).href;
const { SpreadsheetFile, Workbook } = await import(artifactToolUrl);

const inputPath = process.argv[2];
const outputPath = process.argv[3];
const previewDir = process.argv[4];

if (!inputPath || !outputPath || !previewDir) {
  throw new Error("Usage: node build_inventory_workbook.mjs inventory.json output.xlsx preview_dir");
}

const inventory = JSON.parse(await fs.readFile(inputPath, "utf8"));
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

const workbook = Workbook.create();
const summary = workbook.worksheets.add("Synthèse");
const commerces = workbook.worksheets.add("Commerces");
const services = workbook.worksheets.add("Services_CC");

const fontFamily = "Aptos";
const dark = "#17324D";
const blue = "#2F75B5";
const lightBlue = "#D9EAF7";
const green = "#D9EAD3";
const amber = "#FFF2CC";
const red = "#F4CCCC";
const grey = "#E7E6E6";

for (const sheet of [summary, commerces, services]) {
  sheet.showGridLines = false;
  sheet.getRange("A1:Z300").format.font = { name: fontFamily, size: 10 };
}

function actionForCommerce(row) {
  if (!row.inside_center) return "CONTRÔLE SEULEMENT — NE PAS RATTACHER";
  if (row.center === "AUSHOPPING V2") return "BLOQUÉ : centre V2 modélisé en SHOP";
  if (row.match_status === "EXISTANT_A_RATTACHER") return "Vérifier in_on_place puis rattacher à Lillenium (PLACE 82)";
  if (row.match_status === "PROBABLE_A_VALIDER") return "Valider la correspondance avant rattachement";
  if (row.match_status === "AMBIGU_A_REVOIR") return "Choisir la bonne fiche iziLife";
  return "Confirmer l'absence avant création";
}

function candidateText(candidate) {
  if (!candidate) return "";
  return `${candidate.name || ""} [${candidate.type || ""}]`;
}

function otherCandidates(row) {
  const extras = (row.candidates || []).slice(1).map((candidate) =>
    `${candidate.name} (${candidate.string_id}, score ${candidate.score})`,
  );
  if (row.center_model_warning) extras.unshift(row.center_model_warning);
  if (row.candidates?.length) extras.push("in_on_place non exposé par l'API de lecture actuelle");
  return extras.join(" | ");
}

const commerceHeaders = [
  "Centre", "Périmètre", "Type source", "Nom source", "Catégories source", "URL source",
  "État rapprochement", "Candidat iziLife", "string_id candidat", "Score", "Motif",
  "Ville ID", "Actif", "Listable", "in_on_place actuel", "Action proposée",
  "Décision humaine", "Autres candidats / alerte",
];
const commerceRows = inventory.commerces.map((row) => {
  const first = row.candidates?.[0];
  return [
    row.center,
    row.inside_center ? "DANS LE CENTRE" : "PROXIMITÉ — CONTRÔLE",
    row.source_kind,
    row.name,
    (row.source_categories || []).join(", "),
    row.source_url,
    row.match_status,
    candidateText(first),
    first?.string_id || "",
    first?.score ?? "",
    first?.reason || "",
    first?.city_id ?? "",
    first?.is_active ?? "",
    first?.listable ?? "",
    row.current_in_on_place ?? "NON EXPOSÉ",
    actionForCommerce(row),
    "À DÉCIDER",
    otherCandidates(row),
  ];
});

commerces.getRangeByIndexes(0, 0, commerceRows.length + 1, commerceHeaders.length).values = [commerceHeaders, ...commerceRows];
commerces.freezePanes.freezeRows(1);
commerces.freezePanes.freezeColumns(4);
commerces.getRange(`A1:R${commerceRows.length + 1}`).format.wrapText = true;
commerces.getRange("A1:R1").format = {
  fill: dark,
  font: { name: fontFamily, size: 10, bold: true, color: "#FFFFFF" },
  verticalAlignment: "center",
  wrapText: true,
};
commerces.getRange("A1:R1").format.rowHeight = 34;
commerces.tables.add(`A1:R${commerceRows.length + 1}`, true, "CommercesTable").style = "TableStyleMedium2";
commerces.getRange(`Q2:Q${commerceRows.length + 1}`).dataValidation = {
  rule: { type: "list", values: ["À DÉCIDER", "CONFIRMER RATTACHEMENT", "CONFIRMER CRÉATION", "EXCLURE", "À REVOIR"] },
};
commerces.getRange(`G2:G${commerceRows.length + 1}`).conditionalFormats.add("containsText", { text: "EXISTANT", format: { fill: green } });
commerces.getRange(`G2:G${commerceRows.length + 1}`).conditionalFormats.add("containsText", { text: "PROBABLE", format: { fill: amber } });
commerces.getRange(`G2:G${commerceRows.length + 1}`).conditionalFormats.add("containsText", { text: "AMBIGU", format: { fill: amber } });
commerces.getRange(`G2:G${commerceRows.length + 1}`).conditionalFormats.add("containsText", { text: "ABSENT", format: { fill: red } });
commerces.getRange(`B2:B${commerceRows.length + 1}`).conditionalFormats.add("containsText", { text: "PROXIMITÉ", format: { fill: grey, font: { color: "#666666" } } });

const commerceWidths = [18, 20, 15, 28, 24, 42, 24, 30, 28, 9, 30, 10, 9, 9, 16, 42, 24, 52];
commerceWidths.forEach((width, index) => {
  commerces.getRangeByIndexes(0, index, commerceRows.length + 1, 1).format.columnWidth = width;
});
commerces.getRange(`A2:R${commerceRows.length + 1}`).format.verticalAlignment = "top";

function actionForService(row) {
  if (row.match_status === "REFERENTIEL_TROUVE") return "Valider l'ajout au centre";
  return "Classer : ObjectOnPublicPlace, Equipment, Service ou Hobby";
}

const serviceHeaders = [
  "Centre", "Nom source", "Description", "URL source", "Type proposé", "Référence proposée",
  "État référentiel", "Action proposée", "Décision humaine", "Notes",
];
const serviceRows = inventory.services.map((row) => [
  row.center,
  row.name,
  row.description || "",
  row.source_url,
  row.proposed_object_type,
  row.proposed_ref,
  row.match_status,
  actionForService(row),
  "À DÉCIDER",
  row.proposed_object_type === "A_CLASSER" ? "Aucun type inventé automatiquement" : "Correspondance issue des référentiels SQL existants",
]);

services.getRangeByIndexes(0, 0, serviceRows.length + 1, serviceHeaders.length).values = [serviceHeaders, ...serviceRows];
services.freezePanes.freezeRows(1);
services.freezePanes.freezeColumns(2);
services.getRange(`A1:J${serviceRows.length + 1}`).format.wrapText = true;
services.getRange("A1:J1").format = {
  fill: dark,
  font: { name: fontFamily, size: 10, bold: true, color: "#FFFFFF" },
  verticalAlignment: "center",
  wrapText: true,
};
services.getRange("A1:J1").format.rowHeight = 34;
services.tables.add(`A1:J${serviceRows.length + 1}`, true, "ServicesCCTable").style = "TableStyleMedium4";
services.getRange(`I2:I${serviceRows.length + 1}`).dataValidation = {
  rule: { type: "list", values: ["À DÉCIDER", "CONFIRMER OBJET", "CONFIRMER ÉQUIPEMENT", "CONFIRMER SERVICE", "CONFIRMER HOBBY", "EXCLURE", "À REVOIR"] },
};
services.getRange(`G2:G${serviceRows.length + 1}`).conditionalFormats.add("containsText", { text: "TROUVE", format: { fill: green } });
services.getRange(`G2:G${serviceRows.length + 1}`).conditionalFormats.add("containsText", { text: "CONFIRMER", format: { fill: amber } });
const serviceWidths = [18, 28, 62, 42, 34, 28, 24, 42, 24, 38];
serviceWidths.forEach((width, index) => {
  services.getRangeByIndexes(0, index, serviceRows.length + 1, 1).format.columnWidth = width;
});
services.getRange(`A2:J${serviceRows.length + 1}`).format.verticalAlignment = "top";

summary.mergeCells("A1:H2");
summary.getRange("A1").values = [["Inventaire des centres commerciaux — Lillenium et Aushopping V2"]];
summary.getRange("A1:H2").format = {
  fill: dark,
  font: { name: fontFamily, size: 18, bold: true, color: "#FFFFFF" },
  verticalAlignment: "center",
};
summary.getRange("A3:H3").merge();
summary.getRange("A3").values = [["Lecture seule · aucune création ni modification de production · 30 octobre 2026"]];
summary.getRange("A3:H3").format = { fill: lightBlue, font: { name: fontFamily, size: 10, italic: true, color: dark } };

summary.getRange("A5:B5").values = [["Indicateur", "Valeur"]];
summary.getRange("A6:A14").values = [
  ["Commerces recensés"],
  ["Dans les centres"],
  ["Proximité — contrôle seulement"],
  ["Existants (correspondance forte)"],
  ["Probables à valider"],
  ["Ambigus à revoir"],
  ["Absents à confirmer"],
  ["Services / objets recensés"],
  ["Référentiels déjà trouvés"],
];
summary.getRange("B6:B14").formulas = [
  [`=COUNTA(Commerces!D2:D${commerceRows.length + 1})`],
  [`=COUNTIF(Commerces!B2:B${commerceRows.length + 1},"DANS LE CENTRE")`],
  [`=COUNTIF(Commerces!B2:B${commerceRows.length + 1},"PROXIMITÉ — CONTRÔLE")`],
  [`=COUNTIFS(Commerces!B2:B${commerceRows.length + 1},"DANS LE CENTRE",Commerces!G2:G${commerceRows.length + 1},"EXISTANT_A_RATTACHER")`],
  [`=COUNTIFS(Commerces!B2:B${commerceRows.length + 1},"DANS LE CENTRE",Commerces!G2:G${commerceRows.length + 1},"PROBABLE_A_VALIDER")`],
  [`=COUNTIFS(Commerces!B2:B${commerceRows.length + 1},"DANS LE CENTRE",Commerces!G2:G${commerceRows.length + 1},"AMBIGU_A_REVOIR")`],
  [`=COUNTIFS(Commerces!B2:B${commerceRows.length + 1},"DANS LE CENTRE",Commerces!G2:G${commerceRows.length + 1},"ABSENT_A_CONFIRMER")`],
  [`=COUNTA(Services_CC!B2:B${serviceRows.length + 1})`],
  [`=COUNTIF(Services_CC!G2:G${serviceRows.length + 1},"REFERENTIEL_TROUVE")`],
];
summary.getRange("A5:B5").format = { fill: blue, font: { name: fontFamily, bold: true, color: "#FFFFFF" } };
summary.getRange("A5:B14").format.borders = { preset: "all", style: "thin", color: "#B8C2CC" };
summary.getRange("B6:B14").format.font = { name: fontFamily, size: 12, bold: true, color: dark };

summary.getRange("D5:H5").merge();
summary.getRange("D5").values = [["Décisions structurantes"]];
summary.getRange("D5:H5").format = { fill: blue, font: { name: fontFamily, bold: true, color: "#FFFFFF" } };
summary.getRange("D6:H10").merge(true);
summary.getRange("D6:D10").values = [
  ["Lillenium : cible production confirmée comme PLACE `lillenium` (ID 82). Le rattachement Shop.in_on_place est techniquement possible après validation ligne par ligne."],
  ["Aushopping V2 : cible production actuellement modélisée comme SHOP `aushopping-v2`. Shop.in_on_place exige une PLACE : aucun rattachement ne doit être appliqué avant décision de modèle."],
  ["Les 31 fiches dites de proximité sont conservées pour contrôle, mais exclues de toute proposition de rattachement automatique."],
  ["La route de lecture production confirme les fiches candidates mais n'expose pas leur in_on_place actuel. La colonne reste donc NON EXPOSÉ ; il faudra le contrôler avant écriture."],
  ["Hobbies détectés : 0. Les pages fournies ne justifient pas d'en inventer ; les services non classés restent à arbitrer."],
];
summary.getRange("D6:H10").format = { wrapText: true, verticalAlignment: "top" };
summary.getRange("D6:H10").format.borders = { preset: "all", style: "thin", color: "#B8C2CC" };

summary.getRange("A17:H17").merge();
summary.getRange("A17").values = [["Sources officielles analysées"]];
summary.getRange("A17:H17").format = { fill: blue, font: { name: fontFamily, bold: true, color: "#FFFFFF" } };
summary.getRange("A18:B22").values = [
  ["Lillenium — boutiques", "https://www.lillenium-lille.com/nos-boutiques/"],
  ["Lillenium — services", "https://www.lillenium-lille.com/nos-services/"],
  ["Aushopping V2 — magasins", "https://v2.aushopping.com/magasins"],
  ["Aushopping V2 — restaurants", "https://v2.aushopping.com/restaurants"],
  ["Aushopping V2 — services", "https://v2.aushopping.com/services"],
];
summary.getRange("A18:B22").format.borders = { preset: "all", style: "thin", color: "#B8C2CC" };
summary.getRange("A18:B22").format.wrapText = true;

summary.getRange("A24:H24").merge();
summary.getRange("A24").values = [["Mode d'emploi"]];
summary.getRange("A24:H24").format = { fill: blue, font: { name: fontFamily, bold: true, color: "#FFFFFF" } };
summary.getRange("A25:H27").merge(true);
summary.getRange("A25:A27").values = [
  ["1. Filtrer `Commerces` par centre et état de rapprochement ; confirmer le candidat ou la création dans `Décision humaine`."],
  ["2. Filtrer `Services_CC` ; valider le référentiel proposé ou choisir entre ObjectOnPublicPlace, Equipment, Service et Hobby."],
  ["3. Après validation seulement, générer un plan d'écriture idempotent. Ce classeur n'effectue aucune écriture."],
];
summary.getRange("A25:H27").format = { wrapText: true, verticalAlignment: "top" };

summary.freezePanes.freezeRows(3);
summary.getRange("A1:H27").format.wrapText = true;
summary.getRange("A1:A27").format.columnWidth = 34;
summary.getRange("B1:B27").format.columnWidth = 18;
for (const col of ["C", "D", "E", "F", "G", "H"]) summary.getRange(`${col}1:${col}27`).format.columnWidth = 18;
summary.getRange("D1:D27").format.columnWidth = 28;
summary.getRange("A3:H3").format.rowHeight = 26;
summary.getRange("D6:H10").format.rowHeight = 46;
summary.getRange("A25:H27").format.rowHeight = 34;

workbook.recalculate();

for (const sheetName of ["Synthèse", "Commerces", "Services_CC"]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  const fileName = sheetName.replace(/[^A-Za-z0-9_-]+/g, "_") + ".png";
  await fs.writeFile(path.join(previewDir, fileName), new Uint8Array(await preview.arrayBuffer()));
}

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);

const formulaCheck = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  maxChars: 3000,
});
const summaryInspect = await workbook.inspect({
  kind: "table",
  sheetId: "Synthèse",
  range: "A1:H27",
  include: "values,formulas",
  maxChars: 5000,
});

console.log(JSON.stringify({ outputPath, previewDir, formulaCheck: formulaCheck.ndjson, summary: summaryInspect.ndjson }));
