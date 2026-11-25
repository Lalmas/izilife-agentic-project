from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
from openpyxl import load_workbook
from datetime import date,timedelta
from calendar import monthrange
p=Path(__file__).parent
src=p/'Curation - Démarchage - sauvegarde.xlsm'
dst=p/'Curation - Démarchage - calendrier récurrent.xlsm'
s='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
q=lambda t:'{'+s+'}'+t
def add(e,t,**attrs): return E.SubElement(e,q(t),**attrs)
with ZipFile(src) as z: parts={n:z.read(n) for n in z.namelist()}
files=['xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml','xl/worksheets/sheet7.xml','xl/styles.xml']
wb,rels,ct,ws,styles=[E.fromstring(parts[n]) for n in files]
sheet=E.Element(q('worksheet'),nsmap={None:s})
cols=add(sheet,'cols')
for a,b,w in [(1,1,48),(2,4,16),(5,5,48),(6,8,18),(9,24,14)]:
    add(cols,'col',min=str(a),max=str(b),width=str(w),customWidth='1',**({'hidden':'1'} if a==9 else {}))
sd=add(sheet,'sheetData')
md=ws.find(q('sheetData'))
def cell(data,addr,val,formula=None,style=None):
    n=''.join(filter(str.isdigit,addr))
    row=data.find(q('row')+'[@r="'+n+'"]')
    if row is None:
        row=E.Element(q('row'),r=n)
        nxt=next((e for e in data if int(e.get('r'))>int(n)),None)
        if nxt is None:data.append(row)
        else:nxt.addprevious(row)
    c=row.find(q('c')+'[@r="'+addr+'"]')
    if c is None:
        c=E.Element(q('c'),r=addr)
        key=lambda v:(len(v.rstrip('0123456789')),v.rstrip('0123456789'))
        nxt=next((e for e in row if key(e.get('r'))>key(addr)),None)
        if nxt is None:row.append(c)
        else:nxt.addprevious(c)
    for e in list(c):c.remove(e)
    c.attrib.pop('t',None)
    if style is not None:c.set('s',str(style))
    if formula:
        if isinstance(val,str):c.set('t','str')
        add(c,'f').text=formula
        add(c,'v').text=str(val)
    elif isinstance(val,str):
        c.set('t','inlineStr');add(add(c,'is'),'t').text=val
    else:add(c,'v').text=str(val)
base=load_workbook(src,read_only=True,data_only=True)['Ev - Campagne - Choix']
names=[base[f'A{i}'].value for i in range(2,21)]
assert len(set(names))==19 and None not in names
names[17-1]='Journées européennes du patrimoine'
specs=['black','cyber','12/6','12/25','12/31','winter','mardi','2/14','grand','3/8','mothers','fathers','6/21','summer','7/14','7/21','heritage','10/31','museum']
for col,title in zip('ABCDEFGH',['Campagne','Prochain début','Prochaine fin','Ordre','Campagne à corriger','Année','Début officiel','Fin officielle']):
    cell(sd,col+'1',title)
for i,msg in enumerate(['Saisir une exception dans E2:H20, une ligne par campagne et année.','Recopier le nom exact de A. Saisir l’année et le début officiel.','Pour une date unique, laisser Fin officielle vide.','Nuit des musées : estimation au samedi le plus proche du 18 mai.','Patrimoine : troisième week-end de septembre.','Soldes du Nord : durée nationale standard, sauf décision exceptionnelle.'],23):
    cell(sd,'E'+str(i),msg)
for col,title in zip('ABC',['Campagne annuelle','Dates','État']):cell(md,col+'1',title)
today=date(2026,11,15)
serial=lambda d:(d-date(1899,12,30)).days
def easter(y):
    a=y%19;b,c=divmod(y,100);d,e=divmod(b,4)
    h=(19*a+b-d-(b-(b+8)//25+1)//3+15)%30
    i,k=divmod(c,4);l=(32+2*e+2*i-h-k)%7
    return date(y,3,22)+timedelta(days=h+l-7*((a+11*h+22*l)//451))
def adddays(d,n):return d+timedelta(days=n)
def expression(kind,y,e):
    D=lambda m,d:f'DATE({y},{m},{d})'
    after=lambda d,w:f'{d}+MOD({w}-WEEKDAY({d},2),7)'
    before=lambda d,w:f'{d}-MOD(WEEKDAY({d},2)-{w},7)'
    winter=after(D(1,1),3);summer=before(D(6,30),3); mothers=before(D(5,31),7)
    if '/' in kind:return D(*kind.split('/'))
    return dict(black=after(D(11,1),4)+'+22',cyber=after(D(11,1),4)+'+25',
      winter=f'IF(DAY({winter}+7)>12,{winter},{winter}+7)',summer=f'{summer}-IF(DAY({summer})>28,7,0)',
      mardi=e+'-47',grand=after(D(3,1),7),mothers=f'{mothers}+IF({mothers}={e}+49,7,0)',
      fathers=after(D(6,1),7)+'+14',heritage=after(D(9,15),6),museum=after(D(5,15),6))[kind]
def actual(k,y):
    D=lambda m,d:date(y,m,d)
    after=lambda d,w:adddays(d,(w-d.weekday())%7)
    before=lambda d,w:adddays(d,-((d.weekday()-w)%7))
    if '/' in k:return D(*map(int,k.split('/')))
    w=after(D(1,1),2);a=before(D(6,30),2);m=before(D(5,31),6)
    return dict(black=adddays(after(D(11,1),3),22),cyber=adddays(after(D(11,1),3),25),
      winter=adddays(w,7) if w.day+7<=12 else w,summer=adddays(a,-7) if a.day>28 else a,
      mardi=adddays(easter(y),-47),grand=after(D(3,1),6),
      mothers=adddays(m,7) if m==adddays(easter(y),49) else m,
      fathers=adddays(after(D(6,1),6),14),heritage=after(D(9,15),5),museum=after(D(5,15),5))[k]
for c,y in zip('PQR',[2025,2026,2027]):
    off=y-today.year
    formulas=['YEAR(TODAY())'+(f'{off:+}' if off else ''),'MOD(@2,19)','INT(@2/100)','MOD(@2,100)','INT(@4/4)','MOD(@4,4)','INT((@4+8)/25)','INT((@4-@8+1)/3)','MOD(19*@3+@4-@6-@9+15,30)','INT(@5/4)','MOD(@5,4)','MOD(32+2*@7+2*@11-@10-@12,7)','INT((@3+11*@10+22*@13)/451)','DATE(@2,3,22+@10+@13-7*@14)']
    for n,f in enumerate(formulas,2):cell(sd,c+str(n),y if n==2 else serial(easter(y)) if n==15 else 0,f.replace('@',c))
epoch_from=lambda d,n:(d.year*12+d.month-1+n)
def shift(d,n):
    y,m=divmod(epoch_from(d,n),12)
    return date(y,m+1,min(d.day,monthrange(y,m+1)[1]))
results=[]
for i,(n,k) in enumerate(zip(names,specs),2):
    cell(sd,f'A{i}',n)
    duration=27 if k in ('summer','winter') else 1 if k in ('12/31','heritage') else 0
    dates=[]
    for year,c,sc,ec in zip([2025,2026,2027],'PQR','JLN','KMO'):
        y=c+'$2'
        start=actual(k,year);end=adddays(start,duration)
        dates.append((start,end))
        crit=f'$E$2:$E$20,A{i},$F$2:$F$20,{y}'
        ov=f'SUMIFS($G$2:$G$20,{crit})';oe=f'SUMIFS($H$2:$H$20,{crit})'
        cell(sd,f'{sc}{i}',serial(start),f'IF({ov}>0,{ov},{expression(k,y,c+"$15")})')
        cell(sd,f'{ec}{i}',serial(end),f'IF({oe}>={sc}{i},{oe},IF({ov}>0,{sc}{i},{sc}{i}+{duration}))')
    start,end=next(x for x in dates if x[1]>=today)
    forecast=k in ('museum','heritage')
    results.append((start,i,end,n,forecast))
    cell(sd,f'B{i}',serial(start),f'IF(K{i}>=TODAY(),J{i},IF(M{i}>=TODAY(),L{i},N{i}))')
    cell(sd,f'C{i}',serial(end),f'IF(K{i}>=TODAY(),K{i},IF(M{i}>=TODAY(),M{i},O{i}))')
    cell(sd,f'D{i}',serial(start)*100+i,f'B{i}*100+ROW()')
    if forecast:cell(sd,f'I{i}','Prévision',f'IF(COUNTIFS($E$2:$E$20,A{i},$G$2:$G$20,B{i})>0,"","Prévision")')
for j,(st,i,en,n,forecast) in enumerate(sorted(results),2):
    ref="'Règles campagnes'!"
    ix=f'MOD(SMALL({ref}$D$2:$D$20,ROWS($A$2:A{j})),100)-1'
    idx=lambda c:f'INDEX({ref}{c}$2:{c}$20,{ix})'
    b,c,flag=map(idx,'BCI')
    label=st.strftime('%d/%m/%Y')
    if st!=en:label+=' au '+en.strftime('%d/%m/%Y')
    if forecast:label+=' (prévision)'
    status='En cours' if st<=today else 'À finaliser' if today>=shift(st,-1) else 'À préparer' if today>=shift(st,-2) else 'À venir'
    cell(md,f'A{j}',n,idx('A'))
    cell(md,f'B{j}',label,f'TEXT({b},"dd/mm/yyyy")&IF({c}={b},""," au "&TEXT({c},"dd/mm/yyyy"))&IF({flag}="Prévision"," (prévision)","")')
    cell(md,f'C{j}',status,f'IF({b}<=TODAY(),"En cours",IF(TODAY()>=EDATE({b},-1),"À finaliser",IF(TODAY()>=EDATE({b},-2),"À préparer","À venir")))')
xf=styles.find(q('cellXfs'))
date_style=str(len(xf))
add(xf,'xf',numFmtId='14',fontId='0',fillId='0',borderId='0',xfId='0',applyNumberFormat='1')
xf.set('count',str(len(xf)))
for row in range(2,21):
    for c in 'BC':sd.find(f'.//{q("c")}[@r="{c}{row}"]').set('s',date_style)
    for c in 'GH':cell(sd,f'{c}{row}','',style=date_style)
dx=styles.find(q('dxfs'))
if dx is None:
    dx=E.Element(q('dxfs'));styles.find(q('cellStyles')).addnext(dx)
cf=E.Element(q('conditionalFormatting'),sqref='A2:C20')
for j,(color,status) in enumerate([('FFD9EAD3','À finaliser'),('FFFCE5CD','À préparer')],1):
    rule=add(cf,'cfRule',type='expression',dxfId=str(len(dx)),priority=str(j))
    add(rule,'formula').text=f'$C2="{status}"'
    fill=add(add(add(dx,'dxf'),'fill'),'patternFill',patternType='solid')
    add(fill,'bgColor',rgb=color)
dx.set('count',str(len(dx)));md.addnext(cf)
new=add(wb.find(q('sheets')),'sheet',name='Règles campagnes',sheetId='18')
new.set('{'+r+'}id','rId22')
def same(parent,tag,**attrs):E.SubElement(parent,E.QName(parent).namespace and '{'+E.QName(parent).namespace+'}'+tag,**attrs)
same(rels,'Relationship',Id='rId22',Type=r+'/worksheet',Target='worksheets/sheet18.xml')
same(ct,'Override',PartName='/xl/worksheets/sheet18.xml',ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml')
for name,xml in zip(files+['xl/worksheets/sheet18.xml'],[wb,rels,ct,ws,styles,sheet]):
    parts[name]=E.tostring(xml,encoding='utf-8',xml_declaration=True,standalone=True)
with ZipFile(dst,'w',ZIP_DEFLATED) as z:
    for k,v in parts.items():z.writestr(k,v)
out=load_workbook(dst,data_only=True)
view=out['Ev - Campagne - Choix']
assert view['A2'].value=='Black Friday' and view['C2'].value=='À finaliser'
assert any('15/05/2027' in view[f'B{i}'].value for i in range(2,21))
assert any('18/09/2027 au 19/09/2027' in view[f'B{i}'].value for i in range(2,21))
assert len(view.conditional_formatting)==1
assert actual('mardi',2027)==date(2027,2,9)
with ZipFile(src) as before, ZipFile(dst) as after:
    assert after.testzip() is None
    assert all(before.read(n)==after.read(n) for n in before.namelist() if n not in files)
print('Workbook verified: 19 campaigns, chronological display, ranges and conditional formatting.')
