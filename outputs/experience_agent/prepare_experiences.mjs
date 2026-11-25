import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "file:///C:/Users/alcamara/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const dir = "C:/Users/alcamara/Documents/agentic_Workspace/outputs/experience_agent";
const input = `${dir}/experiences_source.xlsx`;
const output = `${dir}/experiences.xlsx`;

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const sheet = workbook.worksheets.getItem("Experiences");

const before = await workbook.render({
  sheetName: "Experiences",
  range: "F78:AK84",
  scale: 1,
  format: "png",
});
await fs.writeFile(`${dir}/before.png`, new Uint8Array(await before.arrayBuffer()));

const updates = {
  80: {
    F: "activite-collective", H: "sport", I: "libre-et-gratuit",
    N: 2, O: 1, AF: "oui", AI: "pending", AK: null,
  },
  81: {
    F: "croisiere-en-bateau", H: "loisirs", I: "acces-payant",
    J: "uniquement-site-externe", L: "De 0 à 30 € selon tarif", M: 30,
    O: 1, AF: "oui", AI: "pending", AK: null,
  },
  82: {
    F: "croisiere-en-bateau", H: "loisirs", I: "acces-payant",
    J: "uniquement-site-externe", L: "À partir de 12 € par adulte", M: 12,
    N: 90, O: 2, AF: "oui", AG: "non", AI: "pending", AK: null,
  },
  83: {
    F: "croisiere-en-bateau", H: "loisirs", I: "acces-payant",
    J: "reservation-conseillee", L: "À partir de 9,50 € selon formule", M: 9.5,
    N: 1, O: 1, AF: "oui", AI: "pending", AK: null,
  },
  84: {
    F: "croisiere-en-bateau", H: "loisirs", I: "acces-payant",
    J: "uniquement-par-telephone", L: "Visite guidée à partir de 9 €", M: 9,
    N: 1, O: 1, AF: "oui", AI: "pending", AK: null,
  },
};

for (const [row, cells] of Object.entries(updates)) {
  for (const [column, value] of Object.entries(cells)) {
    sheet.getRange(`${column}${row}`).values = [[value]];
  }
}

workbook.recalculate();

const check = await workbook.inspect({
  kind: "region",
  sheetId: "Experiences",
  range: "A80:AK84",
  maxChars: 12000,
});
console.log(check.ndjson);

const formulas = await workbook.inspect({
  kind: "formula",
  sheetId: "Experiences",
  range: "A80:AK84",
  maxChars: 2000,
  options: { maxResults: 20 },
});
console.log(formulas.ndjson);

const after = await workbook.render({
  sheetName: "Experiences",
  range: "F78:AK84",
  scale: 1,
  format: "png",
});
await fs.writeFile(`${dir}/after.png`, new Uint8Array(await after.arrayBuffer()));

const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(output);
