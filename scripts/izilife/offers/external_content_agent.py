"""Agent commun ExternalPromo (ExternalOffer métier), ElementNewsPost et veille."""
from __future__ import annotations
import argparse, hashlib, html, json, mimetypes, os, re, tempfile
from io import BytesIO
import sys
from html.parser import HTMLParser
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
import openpyxl, requests
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

HERE = Path(__file__).resolve().parent
IZILIFE_SCRIPTS = HERE.parent
SCRIPTS_ROOT = IZILIFE_SCRIPTS.parent
for import_root in (IZILIFE_SCRIPTS, SCRIPTS_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from core.paths import IZILIFE_ENVS, external_content_file, normalize_env, normalize_zone
from core.place_resolution import normalize_url
from core.location_identity import resolve_location
from objects.object_agent_common import load_env

OFFER_HEADERS=["SOURCE_URL","SOURCE_TYPE","STATUS","TITRE","DESCRIPTION","SCOPE_TYPE","SCOPE_REF","STARTS_AT","ENDS_AT","USE_LLM_IF_MISSING","RESULTAT","ERREUR"]
NEWS_HEADERS=["SOURCE_URL","SOURCE_TYPE","AUTHOR_TYPE","AUTHOR_REF","STATUS","TITRE","RESUME","CONTENU","DESCRIPTION","IMAGE_URLS","SCOPE_TYPE","SCOPE_REF","POST_TYPE","DISPLAY_MODE","IS_FEATURED","STARTS_AT","ENDS_AT","VISIBILITY","USE_LLM_IF_MISSING","INFORMATIONS_JSON","RESULTAT","ERREUR"]
WATCH_HEADERS=["SOURCE_URL","SOURCE_TYPE","AUTHOR_TYPE","AUTHOR_REF","DESTINATION_TYPE","SCOPE_TYPE","SCOPE_REF","ACTIF","LAST_CHECK","LAST_HASH","STATUS","RESULTAT"]
HISTORY_HEADERS=["PARENT_URL","CONTENT_URL","DESTINATION_TYPE","FIRST_SEEN","LAST_SEEN","STATUS","OBJECT_ID","LAST_RESULT"]
def _style_sheet(ws):
    ws.freeze_panes="A2";ws.auto_filter.ref=f"A1:{openpyxl.utils.get_column_letter(ws.max_column)}1"
    for cell in ws[1]:
        cell.font=Font(bold=True,color="FFFFFF");cell.fill=PatternFill("solid",fgColor="17365D")
    for idx,header in enumerate([str(c.value or "") for c in ws[1]],1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(idx)].width=34 if header in {"SOURCE_URL","IMAGE_URLS","LANDING_URL","AFFILIATE_URL","CONTENT_URL","PARENT_URL"} else 30 if header in {"DESCRIPTION","CONTENU","RESULTAT","ERREUR","LAST_RESULT","INFORMATIONS_JSON"} else 16

def _validation(ws,header,values):
    headers={str(c.value or ""):c.column for c in ws[1]}
    if header not in headers:return
    dv=DataValidation(type="list",formula1='"'+','.join(values)+'"',allow_blank=True);ws.add_data_validation(dv)
    letter=openpyxl.utils.get_column_letter(headers[header]);dv.add(f"{letter}2:{letter}1000")

def init_workbook(path:Path):
    path.parent.mkdir(parents=True,exist_ok=True);wb=openpyxl.Workbook();wb.remove(wb.active)
    for name,headers in (("ExternalOffer",OFFER_HEADERS),("ElementNewsPost",NEWS_HEADERS),("Veille",WATCH_HEADERS),("Historique",HISTORY_HEADERS)):
        ws=wb.create_sheet(name);ws.append(headers);_style_sheet(ws)
        if "SOURCE_TYPE" in headers:_validation(ws,"SOURCE_TYPE",["instagram","facebook","website","manual"])
        if "STATUS" in headers:_validation(ws,"STATUS",["pending","done","dry_run","duplicate","error"])
    _validation(wb["ExternalOffer"],"SCOPE_TYPE",["GLOBAL","CITY","PLACE","SHOP"])
    _validation(wb["ElementNewsPost"],"AUTHOR_TYPE",["PAGE"])
    _validation(wb["ElementNewsPost"],"AUTHOR_REF",["lille-addict"])
    _validation(wb["ElementNewsPost"],"SCOPE_TYPE",["PAGE","PLACE","SHOP","EQUIPMENT","EVENT","EVENT_SERIE","EXPERIENCE","ANNUAL_CELEBRATION","CITY","ADMINISTRATIVE_DIVISION","COUNTRY","PARTNER"])
    _validation(wb["Veille"],"AUTHOR_TYPE",["PAGE"])
    _validation(wb["Veille"],"AUTHOR_REF",["lille-addict"])
    _validation(wb["Veille"],"ACTIF",["oui","non"])
    guide=wb.create_sheet("ModeEmploi");guide.append(["Règle","Détail"])
    for row in [("Saisie simple","Pour Instagram : SOURCE_URL, SOURCE_TYPE=instagram, STATUS=pending, TITRE, DESCRIPTION, SCOPE_TYPE, SCOPE_REF et les dates si connues."),("Image Instagram","Laisser IMAGE_URLS vide : l'image originale est téléchargée automatiquement."),("Champs avancés","Les colonnes commerciales avancées sont masquées et leurs valeurs par défaut sont appliquées automatiquement."),("IA","USE_LLM_IF_MISSING reste non lorsque titre et description sont remplis."),("Dates","Format AAAA-MM-JJ HH:MM.")]:guide.append(row)
    _style_sheet(guide);guide.column_dimensions["A"].width=24;guide.column_dimensions["B"].width=90
    wb.save(path)

def ensure_workbook_schema(path:Path):
    if not path.exists():init_workbook(path);return
    wb=openpyxl.load_workbook(path);changed=False
    for name,headers in (("ExternalOffer",OFFER_HEADERS),("ElementNewsPost",NEWS_HEADERS),("Veille",WATCH_HEADERS),("Historique",HISTORY_HEADERS)):
        if name not in wb.sheetnames:
            ws=wb.create_sheet(name);ws.append(headers);changed=True
        else:ws=wb[name]
        existing=[str(c.value or "").strip().upper() for c in ws[1]]
        for header in headers:
            if header not in existing:ws.cell(1,ws.max_column+1,header);existing.append(header);changed=True
        _style_sheet(ws)
        if "SOURCE_TYPE" in headers:_validation(ws,"SOURCE_TYPE",["instagram","facebook","website","manual"])
        if "STATUS" in headers:_validation(ws,"STATUS",["pending","done","dry_run","duplicate","error"])
        if name in {"ElementNewsPost","Veille"}:
            _validation(ws,"AUTHOR_TYPE",["PAGE"])
            _validation(ws,"AUTHOR_REF",["lille-addict"])
        if name == "ElementNewsPost":
            _validation(ws,"SCOPE_TYPE",["PAGE","PLACE","SHOP","EQUIPMENT","EVENT","EVENT_SERIE","EXPERIENCE","ANNUAL_CELEBRATION","CITY","ADMINISTRATIVE_DIVISION","COUNTRY","PARTNER"])
    if "ModeEmploi" not in wb.sheetnames:
        guide=wb.create_sheet("ModeEmploi");guide.append(["Règle","Détail"]);guide.append(["IA","Parcours déterministe par défaut."]);_style_sheet(guide);changed=True
    # Les validations peuvent évoluer sans ajout de colonne : sauvegarder aussi
    # dans ce cas afin que les classeurs déjà créés reçoivent les nouveaux choix.
    wb.save(path)

def fetch(url):
    r=requests.get(url,timeout=35,headers={"User-Agent":"Mozilla/5.0 iziLife External Content/1.0"});r.raise_for_status()
    try:return r.content.decode("utf-8")
    except UnicodeDecodeError:return r.text

def meta(source,name):
    patterns=[rf'<meta[^>]+(?:property|name)=["\']{re.escape(name)}["\'][^>]+content=["\']([^"\']*)',rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:property|name)=["\']{re.escape(name)}["\']']
    for p in patterns:
        m=re.search(p,source,re.I)
        if m:return re.sub(r"\s+"," ",html.unescape(m.group(1))).strip()
    return ""

def extracted_from_source(url,source):
    title=meta(source,"og:title") or meta(source,"twitter:title")
    desc=meta(source,"og:description") or meta(source,"description")
    image=normalize_url(meta(source,"og:image")); clean=re.sub(r"\s+"," ",re.sub(r'<[^>]+>',' ',source)).strip()
    return {"title":title[:200],"description":desc,"image_url":image,"hash":hashlib.sha256(clean.encode()).hexdigest(),"content":clean[:5000]}

def source_identity(url,info):
    host=urlparse(url).netloc.lower();title=str(info.get("title") or "")
    if "instagram." in host:name=re.sub(r"\s+on Instagram:.*$","",title,flags=re.I).strip(' "“”')
    elif "facebook." in host:name=re.sub(r"\s*[|\-]\s*Facebook.*$","",title,flags=re.I).strip(' "“”')
    else:name=""
    account=""
    match=re.search(r"@([A-Za-z0-9._]+)",title)
    if match:account=match.group(1).lower()
    urls=[url]
    if account:urls.insert(0,f"https://www.instagram.com/{account}/")
    return name,urls

def extracted(url):
    return extracted_from_source(url,fetch(url))

class LinkParser(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a":
            href=dict(attrs).get("href")
            if href:self.links.append(str(href))

def discovered_urls(parent_url,source,destination):
    parser=LinkParser();parser.feed(source);host=urlparse(normalize_url(parent_url)).netloc.lower();out=[]
    instagram="instagram.com" in host
    pattern=r"/(?:p|reel)/[^/]+" if instagram else (r"(?:offre|promo|deal|bon-plan|reduction)" if destination=="EXTERNAL_OFFER" else r"(?:actualit|news|blog|article|evenement|event)")
    for href in parser.links:
        url=normalize_url(urljoin(parent_url,href))
        parsed=urlparse(url)
        if not url or parsed.netloc.lower()!=host or not re.search(pattern,parsed.path,re.I):continue
        if re.search(r"\.(?:jpg|jpeg|png|webp|gif|pdf|zip)$",parsed.path,re.I):continue
        if url not in out:out.append(url)
    return out[:50]

def history_sheet(wb):
    if "Historique" in wb.sheetnames:
        ws=wb["Historique"]
        headers=[str(c.value or "") for c in ws[1]]
        for name in ("OBJECT_ID","LAST_RESULT"):
            if name not in headers:ws.cell(1,ws.max_column+1,name);headers.append(name)
        return ws
    ws=wb.create_sheet("Historique");ws.append(["PARENT_URL","CONTENT_URL","DESTINATION_TYPE","FIRST_SEEN","LAST_SEEN","STATUS","OBJECT_ID","LAST_RESULT"])
    return ws

def history_index(ws):
    return {normalize_url(str(row[1].value or "")):row[0].row for row in ws.iter_rows(min_row=2) if row[1].value}

def queue_candidate(wb,destination,url,source_type,scope_type,scope_ref,author_type="",author_ref=""):
    tab="ExternalOffer" if destination=="EXTERNAL_OFFER" else "ElementNewsPost";ws=wb[tab]
    headers={str(c.value or "").strip().upper():i+1 for i,c in enumerate(ws[1])};row=ws.max_row+1
    values={"SOURCE_URL":url,"SOURCE_TYPE":source_type or "website","AUTHOR_TYPE":author_type,"AUTHOR_REF":author_ref,"SCOPE_TYPE":scope_type,"SCOPE_REF":scope_ref,"STATUS":"pending","RESULTAT":"Découvert par Veille"}
    for key,value in values.items():
        if key in headers:ws.cell(row,headers[key],value)

def post(payload,env):
    cfg=IZILIFE_ENVS[env];token=os.getenv("IZILIFE_AGENT_TOKEN","").strip()
    if not token:return {"success":False,"error":"IZILIFE_AGENT_TOKEN manquant"}
    try:return requests.post(cfg["base_url"].rstrip("/")+"/scraper/agentUpsertExternalContent",json=payload,headers={"X-Agent-Token":token},verify=cfg.get("verify_ssl",True),timeout=120).json()
    except (requests.RequestException,ValueError) as exc:return {"success":False,"error":str(exc)}

def as_bool(value):return str(value or "").strip().lower() in {"1","oui","yes","true","vrai"}

def promo_source_string_id(source_type):
    """ExternalPromoSource décrit le canal métier, pas le réseau d'origine.

    Instagram/Facebook/site sont conservés dans source_url, mais passent par
    la source manuelle tant qu'aucun référentiel dédié n'existe en base.
    """
    value=str(source_type or "manual").strip().lower()
    return value if value in {"manual","dealabs","bonplan"} else "manual"

def ai_complete(kind,current,source_content,env):
    cfg=IZILIFE_ENVS[env];token=os.getenv("IZILIFE_AGENT_TOKEN","").strip()
    if not token:return {"success":False,"error":"IZILIFE_AGENT_TOKEN manquant"}
    payload={"kind":kind,"current":current,"content":source_content,"manual_ai_request":True}
    try:
        response=requests.post(cfg["base_url"].rstrip("/")+"/scraper/agentAnalyzeExternalContent",json=payload,headers={"X-Agent-Token":token},verify=cfg.get("verify_ssl",True),timeout=120)
        data=response.json()
        if response.status_code>=400:return {"success":False,"error":data.get("error",f"HTTP {response.status_code}"),"code":data.get("code")}
        return data
    except (requests.RequestException,ValueError) as exc:return {"success":False,"error":str(exc)}

def image_urls(value):
    return [normalize_url(url) for url in re.split(r"[\n;,|]+",str(value or "")) if normalize_url(url)]

def original_social_media(source_url):
    """Télécharge les médias originaux d'un post social, sans capture ni vignette.

    Cette voie n'est utilisée que quand IMAGE_URLS est vide. Elle réutilise le
    parcours iGram éprouvé par curate_events et ne déclenche ni OCR ni LLM.
    """
    host=urlparse(normalize_url(source_url)).netloc.lower()
    if "instagram.com" not in host:return [],None
    from playwright.sync_api import sync_playwright
    from events.ingest_manual_curate import download_from_igram_world
    temp=tempfile.TemporaryDirectory(prefix="izilife-external-media-")
    output=Path(temp.name)
    with sync_playwright() as playwright:
        try:browser=playwright.chromium.launch(channel="chrome",headless=False)
        except Exception:browser=playwright.chromium.launch(headless=False)
        page=browser.new_page(locale="fr-FR")
        try:files=download_from_igram_world(page,source_url,output,"external-content")
        finally:browser.close()
    return [Path(item) for item in files],temp

def upload_images(kind,object_id,urls,env):
    if not urls:return []
    # Le schéma ExternalPromoMedias ne porte volontairement qu'une image
    # principale par offre. Ne pas télécharger plusieurs fichiers qui se
    # remplaceraient successivement. Les News, elles, restent multi-médias.
    if kind == "EXTERNAL_OFFER":
        urls = urls[:1]
    cfg=IZILIFE_ENVS[env];token=os.getenv("IZILIFE_AGENT_TOKEN","").strip();results=[]
    endpoint="agentAddExternalPromoMedia" if kind=="EXTERNAL_OFFER" else "agentAddElementNewsMedia"
    id_field="external_promo_id" if kind=="EXTERNAL_OFFER" else "element_news_post_id"
    for index,url in enumerate(urls):
        try:
            local=Path(url) if isinstance(url,(str,Path)) else None
            if local and local.is_file():
                content=local.read_bytes();content_type=(mimetypes.guess_type(local.name)[0] or "image/jpeg").lower()
            else:
                response=requests.get(str(url),timeout=45,headers={"User-Agent":"Mozilla/5.0 iziLife Media/1.0"})
                response.raise_for_status();content=response.content;content_type=response.headers.get("Content-Type","").split(";",1)[0].lower()
            if not content_type.startswith("image/"):raise RuntimeError("URL non image")
            if len(content)>20*1024*1024:raise RuntimeError("Image supérieure à 20 Mo")
            extension={"image/jpeg":"jpg","image/png":"png","image/webp":"webp","image/gif":"gif"}.get(content_type,"jpg")
            upload=requests.post(cfg["base_url"].rstrip("/")+f"/scraper/{endpoint}",
                data={id_field:str(object_id),"is_principal":"1" if index==0 else "0","display_order":str(index)},
                files={"media":(f"external-content-{index}.{extension}",BytesIO(content),content_type)},
                headers={"X-Agent-Token":token},verify=cfg.get("verify_ssl",True),timeout=120)
            payload=upload.json();payload["source_url"]=url;results.append(payload)
        except (requests.RequestException,ValueError,RuntimeError) as exc:results.append({"success":False,"source_url":url,"error":str(exc)})
    return results

def sheet_rows(ws):
    headers={str(c.value or "").strip().upper():i for i,c in enumerate(ws[1])}
    for row in ws.iter_rows(min_row=2):
        def get(k):return str(row[headers[k]].value or "").strip() if k in headers else ""
        def put(k,v):ws.cell(row[0].row,headers[k]+1,v)
        yield row[0].row,get,put

def run(path:Path,env:str,dry_run:bool,maximum:int):
    wb=openpyxl.load_workbook(path); handled=0; history=history_sheet(wb); seen=history_index(history)
    for tab,kind in (("ExternalOffer","EXTERNAL_OFFER"),("ElementNewsPost","ELEMENT_NEWS_POST")):
        ws=wb[tab]
        for _,get,put in sheet_rows(ws):
            if handled>=maximum or not get("SOURCE_URL") or get("STATUS").lower() in {"done","duplicate"}:continue
            try:
                manual=json.loads(get("INFORMATIONS_JSON") or "{}")
                manual_title=get("TITRE")
                manual_description=get("DESCRIPTION")
                manual_content=get("CONTENU") or manual_description
                scope_complete=bool(get("SCOPE_TYPE")) and (get("SCOPE_TYPE").upper()=="GLOBAL" or bool(get("SCOPE_REF")))
                need_source=not manual_title or not manual_description or (kind=="ELEMENT_NEWS_POST" and not manual_content) or not scope_complete
                info=extracted(get("SOURCE_URL")) if need_source else {"title":"","description":"","image_url":"","hash":"","content":""}
                payload={"kind":kind,"title":get("TITRE") or info["title"],"description":get("DESCRIPTION") or info["description"],"summary":get("RESUME"),"content":get("CONTENU") or get("DESCRIPTION") or info["description"],
                  "source_url":normalize_url(get("SOURCE_URL")),"author_type":get("AUTHOR_TYPE"),"author_ref":get("AUTHOR_REF"),"scope_type":get("SCOPE_TYPE"),"scope_ref":get("SCOPE_REF"),"source_string_id":promo_source_string_id(get("SOURCE_TYPE"))}|manual
                if not payload.get("scope_ref"):
                    identity_name,identity_urls=source_identity(get("SOURCE_URL"),info)
                    try:location=resolve_location(IZILIFE_ENVS[env]["base_url"],IZILIFE_ENVS[env].get("verify_ssl",True),name=identity_name,urls=identity_urls)
                    except Exception:location=None
                    if location:
                        payload["scope_type"]=location["type"];payload["scope_ref"]=location["string_id"]
                required_missing=not payload.get("title") or (kind=="ELEMENT_NEWS_POST" and not payload.get("content"))
                if required_missing and as_bool(get("USE_LLM_IF_MISSING")) and not dry_run:
                    completed=ai_complete(kind,payload,info["content"],env)
                    if completed.get("success"):
                        for key,value in (completed.get("result") or {}).items():
                            if value and not payload.get(key):payload[key]=value
                    else:
                        raise RuntimeError(completed.get("error","Complément IA impossible"))
                payload|={"starts_at":get("STARTS_AT"),"ends_at":get("ENDS_AT")}
                if kind=="EXTERNAL_OFFER":payload|={"source_url":normalize_url(get("LANDING_URL") or get("SOURCE_URL")),"promo_kind":get("PROMO_KIND") or "deal","code":get("CODE"),"affiliate_url":normalize_url(get("AFFILIATE_URL")),"discount_type":get("DISCOUNT_TYPE") or "unknown","discount_value":get("DISCOUNT_VALUE") or None,"currency":get("CURRENCY") or "EUR","priority":get("PRIORITY") or 0}
                else:payload|={"post_type":get("POST_TYPE") or "NEWS","display_mode":get("DISPLAY_MODE") or "ARTICLE","is_featured":get("IS_FEATURED") or 0,"visibility":get("VISIBILITY") or 1}
                if dry_run:result={"success":True,"dry_run":True,"payload":payload}
                else:
                    result=post(payload,env)
                    object_id=result.get("id") or result.get("external_promo_id") or result.get("element_news_post_id")
                    if result.get("success") and object_id:
                        media=image_urls(get("IMAGE_URLS"));temp_media=None
                        if not media:
                            try:media,temp_media=original_social_media(get("SOURCE_URL"))
                            except Exception as exc:
                                result["media_results"]=[{"success":False,"error":f"Média original non récupéré: {exc}"}]
                        try:
                            if media:result["media_results"]=upload_images(kind,object_id,media,env)
                            elif "media_results" not in result:result["media_results"]=[]
                        finally:
                            if temp_media:temp_media.cleanup()
                final_status="dry_run" if dry_run else "done" if result.get("success") and result.get("created") else "duplicate" if result.get("success") else "error"
                put("STATUS",final_status)
                put("RESULTAT",json.dumps(result,ensure_ascii=False)[:3000]);put("ERREUR","" if result.get("success") else result.get("error",""));handled+=1
                source_key=normalize_url(get("SOURCE_URL"))
                if source_key in seen and not dry_run:
                    history.cell(seen[source_key],6,"imported" if final_status=="done" else final_status)
                    history.cell(seen[source_key],7,result.get("id") or result.get("external_promo_id") or result.get("element_news_post_id") or "")
                    history.cell(seen[source_key],8,json.dumps(result,ensure_ascii=False)[:2000])
            except Exception as exc:put("STATUS","error");put("ERREUR",str(exc));handled+=1
            wb.save(path)
    ws=wb["Veille"]
    for _,get,put in sheet_rows(ws):
        if handled>=maximum or not get("SOURCE_URL") or get("ACTIF").lower() not in {"1","oui","true","yes"}:continue
        try:
            source=fetch(get("SOURCE_URL"));info=extracted_from_source(get("SOURCE_URL"),source);old=get("LAST_HASH");changed=bool(old and old!=info["hash"])
            destination=get("DESTINATION_TYPE").upper() or "ELEMENT_NEWS_POST";now=datetime.now().strftime("%Y-%m-%d %H:%M:%S");new_urls=[]
            for url in discovered_urls(get("SOURCE_URL"),source,destination):
                if url in seen:
                    history.cell(seen[url],5,now);continue
                status="baseline" if not old else "dry_run" if dry_run else "queued"
                history.append([normalize_url(get("SOURCE_URL")),url,destination,now,now,status]);seen[url]=history.max_row
                if old:
                    new_urls.append(url)
                if not dry_run:queue_candidate(wb,destination,url,get("SOURCE_TYPE"),get("SCOPE_TYPE"),get("SCOPE_REF"),get("AUTHOR_TYPE"),get("AUTHOR_REF"))
            put("LAST_CHECK",datetime.now().strftime("%Y-%m-%d %H:%M:%S"));put("LAST_HASH",info["hash"]);put("STATUS","new_content" if changed else "initialized" if not old else "unchanged")
            put("RESULTAT",json.dumps({"title":info["title"] or info["description"][:300],"discovered":len(new_urls),"queued":0 if dry_run else len(new_urls)},ensure_ascii=False));handled+=1
        except Exception as exc:put("STATUS","error");put("RESULTAT",str(exc));handled+=1
        wb.save(path)
    print(json.dumps({"success":True,"handled":handled,"dry_run":dry_run},ensure_ascii=False))

def main():
    p=argparse.ArgumentParser();p.add_argument("--zone",required=True);p.add_argument("--env",default="local",choices=["local","staging","prod"]);p.add_argument("--file");p.add_argument("--init",action="store_true");p.add_argument("--dry-run",action="store_true");p.add_argument("--max",type=int,default=100);a=p.parse_args()
    load_env();env=normalize_env(a.env);path=Path(a.file) if a.file else external_content_file(normalize_zone(a.zone),env)
    if a.init:init_workbook(path);return
    ensure_workbook_schema(path);run(path,env,a.dry_run,a.max)
if __name__=="__main__":main()
