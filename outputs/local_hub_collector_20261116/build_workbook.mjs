import { SpreadsheetFile, Workbook } from 'file:///C:/Program%20Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1112-737-0_26.1112.737.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
import fs from 'node:fs/promises';

const workbook = Workbook.create();
const eps = workbook.worksheets.add('Endpoints');
eps.getRange('A1:N3').values = [
  ['enabled','hub_id','endpoint_id','label','source_url','server_base_url','wait_ms','detail_delay_ms','scrolls','max_details','verify_ssl','status','last_error','processed_at'],
  [1,2,2,'Ville de Seclin','https://www.ville-seclin.fr/agenda','https://www.izilife.co',3000,1500,2,120,1,'PENDING','',''],
  [1,2,4,'Ville de Wattignies','https://www.mairie-wattignies.com/evenements/','https://www.izilife.co',3500,1500,3,120,1,'PENDING','',''],
];
eps.freezePanes.freezeRows(1);
eps.getRange('A1:N1').format = { fill:'#1F4E78', font:{bold:true,color:'#FFFFFF'}, horizontalAlignment:'center' };
eps.getRange('A1:N3').format.autofitColumns();
eps.getRange('D:D').format.columnWidth=24; eps.getRange('E:F').format.columnWidth=42;
eps.getRange('M:M').format.columnWidth=45; eps.getRange('N:N').format.columnWidth=20;
const guide = workbook.worksheets.add('Mode emploi');
guide.getRange('A1:B8').values = [
  ['Collecteur Hub local','Configuration Windows et Mac'],
  ['Principe','Playwright charge localement; le serveur filtre les liens puis conserve nettoyage, lots LLM et EventTmp.'],
  ['Authentification','Le secret reste dans .env sous AGENT_SECRET_TOKEN ou IZILIFE_AGENT_TOKEN. Ne jamais le mettre dans ce classeur.'],
  ['Installation','python -m pip install -r requirements.txt'],
  ['Navigateur','python -m playwright install chromium'],
  ['Lancement','python local_hub_collector.py --workbook local_hub_endpoints.xlsx --env CHEMIN/.env'],
  ['Test ciblé','Ajouter --only-endpoint 2 ou --only-endpoint 4.'],
  ['Mode visible','Ajouter --headed pour voir Chromium.'],
];
guide.getRange('A1:B1').format={fill:'#1F4E78',font:{bold:true,color:'#FFFFFF'}};
guide.getRange('A1:B8').format.wrapText=true; guide.getRange('A:A').format.columnWidth=24; guide.getRange('B:B').format.columnWidth=95;
const file = await SpreadsheetFile.exportXlsx(workbook);
await file.save(new URL('./local_hub_endpoints.xlsx', import.meta.url).pathname.slice(1));
for (const sheetName of ['Endpoints', 'Mode emploi']) {
  const preview = await workbook.render({sheetName, autoCrop:'all', scale:1, format:'png'});
  await fs.writeFile(new URL(`./preview-${sheetName.replace(' ', '-')}.png`, import.meta.url), new Uint8Array(await preview.arrayBuffer()));
}
