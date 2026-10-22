import fs from "node:fs/promises";
import { execFileSync } from "node:child_process";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const mysql = "C:/xampp/mysql/bin/mysql.exe";
const outputDir = "C:/xampp/htdocs/izilife/outputs/equipment-characteristics-audit";

function query(sql) {
  const raw = execFileSync(mysql, [
    "-uroot", "--default-character-set=utf8mb4", "--batch", "--raw", "--skip-column-names",
    "-e", `USE izilife2; ${sql}`,
  ], { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 });
  return raw.trim() === "" ? [] : raw.trimEnd().split(/\r?\n/).map((line) => line.split("\t").map((v) => v === "NULL" ? null : v));
}

const definitions = query(`
  SELECT d.id,d.string_id,d.name,d.value_type,d.unit,d.icon,d.storage_mode,d.equipment_column,d.is_active,
         COUNT(ecc.equipment_category_id)
  FROM EquipmentCharacteristicDefinition d
  LEFT JOIN EquipmentCategoryCharacteristic ecc ON ecc.characteristic_id=d.id
  GROUP BY d.id
  ORDER BY d.name
`);

const categories = query(`
  SELECT ec.id,ec.name,ec.string_id,COALESCE(ect.name,''),COUNT(ecc.characteristic_id)
  FROM EquipmentCategory ec
  LEFT JOIN EquipmentCategoryType ect ON ect.id=ec.equipment_category_type_id
  LEFT JOIN EquipmentCategoryCharacteristic ecc ON ecc.equipment_category_id=ec.id
  GROUP BY ec.id
  ORDER BY ec.name
`);

const associations = query(`
  SELECT ec.id,ec.name,ec.string_id,COALESCE(ect.name,''),d.id,d.name,d.string_id,d.value_type,d.unit,
         d.storage_mode,d.equipment_column,ecc.is_required,ecc.default_value,ecc.sort_order
  FROM EquipmentCategoryCharacteristic ecc
  JOIN EquipmentCategory ec ON ec.id=ecc.equipment_category_id
  LEFT JOIN EquipmentCategoryType ect ON ect.id=ec.equipment_category_type_id
  JOIN EquipmentCharacteristicDefinition d ON d.id=ecc.characteristic_id
  ORDER BY ec.name,ecc.sort_order,d.name
`);

const characteristicById = new Map(definitions.map((r) => [String(r[0]), r]));
const associationKeys = new Set(associations.map((r) => `${r[0]}:${r[4]}`));

function expectedContent(type) {
  if (type === "BOOLEAN") return "Oui / Non / Non renseigné";
  if (type === "INTEGER") return "Nombre entier";
  if (type === "DECIMAL") return "Mesure décimale";
  return "Texte libre";
}

function storageField(type, mode, column) {
  if (mode === "EQUIPMENT_COLUMN") return `Equipment.${column}`;
  if (type === "BOOLEAN") return "EquipmentCharacteristicValue.boolean_value";
  if (type === "INTEGER") return "EquipmentCharacteristicValue.integer_value";
  if (type === "DECIMAL") return "EquipmentCharacteristicValue.decimal_value";
  return "EquipmentCharacteristicValue.text_value";
}

const wb = Workbook.create();
const dict = wb.worksheets.add("Caractéristiques");
const matrix = wb.worksheets.add("Matrice");
const links = wb.worksheets.add("Associations");
const font = "Arial";
const green = "#169B62";
const dark = "#24324A";
const pale = "#E9F6EF";
const light = "#F3F6FA";

function title(sheet, title, subtitle, endCol) {
  sheet.showGridLines = false;
  sheet.getRange(`A2:${endCol}2`).merge();
  sheet.getRange("A2").values = [[title]];
  sheet.getRange("A2").format.font = { name: font, size: 16, bold: true, color: dark };
  sheet.getRange(`A3:${endCol}3`).merge();
  sheet.getRange("A3").values = [[subtitle]];
  sheet.getRange("A3").format.font = { name: font, size: 10, italic: true, color: "#64748B" };
  sheet.getRange(`A4:${endCol}4`).format.borders = { bottom: { style: "thin", color: green } };
}

const dictHeaders = ["ID", "Identifiant", "Libellé", "Icône", "Contenu attendu", "Type technique", "Unité", "Mode de stockage", "Champ utilisé", "Active", "Nb catégories"];
const dictRows = definitions.map((r) => [
  Number(r[0]), r[1], r[2], r[5] ?? "", expectedContent(r[3]), r[3], r[4] ?? "", r[6], storageField(r[3], r[6], r[7]), Number(r[8]) === 1 ? "Oui" : "Non", Number(r[9]),
]);
title(dict, "Dictionnaire des caractéristiques Equipment", `${definitions.length} caractéristiques configurées dans la base locale`, "K");
dict.getRange("A6").write([dictHeaders, ...dictRows]);
dict.tables.add(`A6:K${6 + dictRows.length}`, true, "EquipmentCharacteristicDictionary").style = "TableStyleMedium2";
dict.freezePanes.freezeRows(6);
dict.getRange(`A6:K${6 + dictRows.length}`).format.font = { name: font, size: 10, color: dark };
dict.getRange("A6:K6").format = { fill: dark, font: { name: font, size: 10, bold: true, color: "#FFFFFF" }, wrapText: true, horizontalAlignment: "center", verticalAlignment: "center" };
dict.getRange(`A7:A${6 + dictRows.length}`).format.numberFormat = "0";
dict.getRange(`K7:K${6 + dictRows.length}`).format.numberFormat = "0";
dict.getRange(`A6:K${6 + dictRows.length}`).format.autofitColumns();
dict.getRange("B:B").format.columnWidth = 27;
dict.getRange("C:C").format.columnWidth = 32;
dict.getRange("E:E").format.columnWidth = 28;
dict.getRange("I:I").format.columnWidth = 48;
dict.getRange(`A7:K${6 + dictRows.length}`).format.rowHeight = 21;

function colLetter(n) {
  let s = "";
  while (n > 0) { n--; s = String.fromCharCode(65 + (n % 26)) + s; n = Math.floor(n / 26); }
  return s;
}

const matrixDefs = [...definitions].sort((a, b) => String(a[2]).localeCompare(String(b[2]), "fr"));
const matrixHeaders = ["ID catégorie", "Catégorie", "Identifiant catégorie", "Type", "Nb caractéristiques", ...matrixDefs.map((r) => `${r[5] ?? ""} ${r[2]}`.trim())];
const matrixRows = categories.map((c) => [
  Number(c[0]), c[1], c[2], c[3], Number(c[4]),
  ...matrixDefs.map((d) => associationKeys.has(`${c[0]}:${d[0]}`) ? "Oui" : ""),
]);
const matrixLastCol = colLetter(matrixHeaders.length);
title(matrix, "Matrice Catégories × Caractéristiques", `${categories.length} catégories et ${associations.length} associations. “Oui” signifie que la caractéristique est proposée pour la catégorie.`, "K");
matrix.getRange("A6").write([matrixHeaders, ...matrixRows]);
matrix.tables.add(`A6:${matrixLastCol}${6 + matrixRows.length}`, true, "EquipmentCategoryCharacteristicMatrix").style = "TableStyleMedium2";
matrix.freezePanes.freezeRows(6);
matrix.freezePanes.freezeColumns(5);
matrix.getRange(`A6:${matrixLastCol}${6 + matrixRows.length}`).format.font = { name: font, size: 9, color: dark };
matrix.getRange(`A6:${matrixLastCol}6`).format = { fill: dark, font: { name: font, size: 9, bold: true, color: "#FFFFFF" }, wrapText: true, horizontalAlignment: "center", verticalAlignment: "center" };
matrix.getRange(`F7:${matrixLastCol}${6 + matrixRows.length}`).format.horizontalAlignment = "center";
matrix.getRange(`F7:${matrixLastCol}${6 + matrixRows.length}`).conditionalFormats.add("containsText", { text: "Oui", format: { fill: pale, font: { bold: true, color: green } } });
matrix.getRange("A:A").format.columnWidth = 12;
matrix.getRange("B:B").format.columnWidth = 30;
matrix.getRange("C:C").format.columnWidth = 30;
matrix.getRange("D:D").format.columnWidth = 22;
matrix.getRange("E:E").format.columnWidth = 17;
matrix.getRange(`F:${matrixLastCol}`).format.columnWidth = 15;
matrix.getRange(`A7:${matrixLastCol}${6 + matrixRows.length}`).format.rowHeight = 20;
matrix.getRange(`A6:${matrixLastCol}6`).format.rowHeight = 55;

const assocHeaders = ["ID catégorie", "Catégorie", "Identifiant catégorie", "Type catégorie", "ID caractéristique", "Caractéristique", "Identifiant caractéristique", "Contenu attendu", "Type technique", "Unité", "Mode de stockage", "Champ utilisé", "Obligatoire", "Valeur par défaut", "Ordre"];
const assocRows = associations.map((r) => [
  Number(r[0]), r[1], r[2], r[3], Number(r[4]), r[5], r[6], expectedContent(r[7]), r[7], r[8] ?? "", r[9], storageField(r[7], r[9], r[10]), Number(r[11]) === 1 ? "Oui" : "Non", r[12] ?? "", Number(r[13]),
]);
title(links, "Liste détaillée des associations", `${associations.length} lignes filtrables pour contrôler précisément chaque catégorie`, "O");
links.getRange("A6").write([assocHeaders, ...assocRows]);
links.tables.add(`A6:O${6 + assocRows.length}`, true, "EquipmentCategoryCharacteristicLinks").style = "TableStyleMedium2";
links.freezePanes.freezeRows(6);
links.getRange(`A6:O${6 + assocRows.length}`).format.font = { name: font, size: 9, color: dark };
links.getRange("A6:O6").format = { fill: dark, font: { name: font, size: 9, bold: true, color: "#FFFFFF" }, wrapText: true, horizontalAlignment: "center", verticalAlignment: "center" };
links.getRange("A:A").format.columnWidth = 12;
links.getRange("B:B").format.columnWidth = 30;
links.getRange("C:C").format.columnWidth = 28;
links.getRange("D:D").format.columnWidth = 22;
links.getRange("E:E").format.columnWidth = 16;
links.getRange("F:F").format.columnWidth = 30;
links.getRange("G:G").format.columnWidth = 28;
links.getRange("H:H").format.columnWidth = 27;
links.getRange("K:K").format.columnWidth = 23;
links.getRange("L:L").format.columnWidth = 48;
links.getRange(`A7:O${6 + assocRows.length}`).format.rowHeight = 20;

dict.tabColor = green;
matrix.tabColor = "#2563EB";
links.tabColor = "#64748B";

wb.recalculate();
await fs.mkdir(outputDir, { recursive: true });
for (const [sheetName, range, file] of [
  ["Caractéristiques", "A1:K25", "preview-characteristics.png"],
  ["Matrice", `A1:${colLetter(Math.min(matrixHeaders.length, 14))}18`, "preview-matrix.png"],
  ["Associations", "A1:O22", "preview-associations.png"],
]) {
  const image = await wb.render({ sheetName, range, scale: 1, format: "png" });
  await fs.writeFile(`${outputDir}/${file}`, new Uint8Array(await image.arrayBuffer()));
}

const inspection = await wb.inspect({ kind: "table", range: "Caractéristiques!A1:K15", include: "values,formulas", tableMaxRows: 15, tableMaxCols: 11 });
console.log(inspection.ndjson);
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" });
console.log(errors.ndjson);

const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(`${outputDir}/controle-caracteristiques-equipment.xlsx`);
console.log(`OUTPUT=${outputDir}/controle-caracteristiques-equipment.xlsx`);
