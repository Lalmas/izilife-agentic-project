import { FileBlob, SpreadsheetFile } from "file:///C:/Users/alcamara/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const path = "C:/Users/alcamara/Documents/agentic_Workspace/outputs/experience_agent/experiences_final.xlsx";
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const ws = wb.worksheets.getItem("Experiences");
const values = ws.getUsedRange(true).values;
const headers = values[0].map(value => String(value ?? "").trim());
const statusIndex = headers.indexOf("status");
const counts = {};
for (const row of values.slice(1)) {
  const status = String(row[statusIndex] ?? "").trim().toLowerCase();
  counts[status || "blank"] = (counts[status || "blank"] ?? 0) + 1;
}
const formulaErrors = await wb.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  maxChars: 3000,
});
console.log(JSON.stringify({ counts, formulaErrors: formulaErrors.ndjson }));
