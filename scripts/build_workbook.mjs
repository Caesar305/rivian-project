import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
await fs.mkdir(`${root}/work`, {recursive:true});
const db=JSON.parse(await fs.readFile(`${root}/outputs/dimension_database.json`,'utf8'));
const wb=Workbook.create();
const configs=[];
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
function sheet(name,title,subtitle,headers,rows,widths){
 const s=wb.worksheets.add(name); const end=col(headers.length-1); const last=rows.length+4;
 s.showGridLines=false;
 s.getRange(`A1:${end}${last}`).format.font.name='Arial';
 s.getRange(`A1:${end}${last}`).format.font.size=11;
 s.getRange('A1').values=[[title]];s.getRange('A1').format.font.size=16;s.getRange('A1').format.font.bold=true;
 s.getRange('A2').values=[[subtitle]];s.getRange('A2').format.font.italic=true;
 s.getRange(`A4:${end}4`).values=[headers];
 s.getRange(`A4:${end}4`).format.fill='#334155';s.getRange(`A4:${end}4`).format.font.color='#FFFFFF';s.getRange(`A4:${end}4`).format.font.bold=true;
 s.getRange(`A4:${end}4`).format.wrapText=true;s.getRange(`A4:${end}4`).format.rowHeight=34;
 s.getRange(`A5:${end}${last}`).values=rows;
 s.getRange(`A5:${end}${last}`).format.wrapText=true;s.getRange(`A5:${end}${last}`).format.verticalAlignment='top';
 widths.forEach((w,i)=>s.getRange(`${col(i)}1:${col(i)}${last}`).format.columnWidth=w);
 rows.forEach((r,i)=>{
  const lines=Math.max(...r.map((x,j)=>typeof x==='string'?Math.ceil(x.length/Math.max(5,widths[j]-3)):1));
  s.getRange(`A${i+5}:${end}${i+5}`).format.rowHeight=Math.max(34,lines*15+10);
  if(i%2===1)s.getRange(`A${i+5}:${end}${i+5}`).format.fill='#F1F5F9';
 });
 s.freezePanes.freezeRows(4);s.freezePanes.freezeColumns(2);
 s.tables.add(`A4:${end}${last}`,true,name.replaceAll(' ','')+'Table');
 configs.push({name,last,end});return s;
}
const d=sheet('Dimensions','R1S source dimension register','2023 target · Published claims are reference-only. A classification does not authorize cabin geometry.',
 ['ID','Dimension','Reported value','Unit','Length mm','Length in','Class','Confidence','Measurement type','Configuration','Source ID','Source URL','Model/year scope','Notes','Use in geometry','Uncertainty mm'],
 db.dimensions.map(x=>[x.id,x.name,x.value,x.unit,null,null,x.classification,x.confidence,x.measurement_type,x.configuration,x.source_id,x.source_url,x.model_year_scope,x.notes,'No',x.uncertainty_mm]),
 [10,42,14,9,14,14,9,12,31,37,12,65,42,58,18,16]);
for(let i=0;i<db.dimensions.length;i++){
 const r=i+5;
 d.getRange(`E${r}`).formulas=[[`=IF(D${r}="mm",C${r},IF(D${r}="in",C${r}*25.4,IF(D${r}="ft",C${r}*304.8,"")))`]];
 d.getRange(`F${r}`).formulas=[[`=IF(E${r}="","",E${r}/25.4)`]];
}
d.getRange(`C5:F${db.dimensions.length+4}`).setNumberFormat('0.00');
d.getRange(`H5:H${db.dimensions.length+4}`).setNumberFormat('0');

const first=sheet('First measurements','First vehicle measurements','Enter three reset readings in mm. See START_HERE.md for exact endpoints. Blank means unmeasured.',
 ['ID','Measurement','Reading 1 mm','Reading 2 mm','Reading 3 mm','Second span mm','Height reference','Configuration','Endpoint photo IDs','Tool','Notes'],
 db.first_measurements.map(x=>[x.id,x.name,null,null,null,null,null,null,null,null,null]),
 [10,47,16,16,16,18,37,36,38,24,58]);
first.getRange('C5:K12').format.fill='#FFF7DF';first.getRange('C5:F12').setNumberFormat('0.0');

const st=sheet('Stations','Cabin cross-section observations','Target Z levels are sampling instructions. Record actual XYZ in the approved datum; do not split width equally.',
 ['Station','Landmark','Sample','Target Z mm','Measured X mm','Measured Z mm','Left Y mm','Right Y mm','Width mm','Width in','Configuration','Photo/point IDs'],
 db.station_observations.map(x=>[x.station,x.landmark,x.sample,x.target_z_mm,null,null,null,null,null,null,null,null]),
 [11,38,15,16,17,17,16,16,16,16,36,40]);
for(let i=0;i<db.station_observations.length;i++){
 const r=i+5;
 st.getRange(`I${r}`).formulas=[[`=IF(COUNT(G${r}:H${r})<2,"",G${r}-H${r})`]];
 st.getRange(`J${r}`).formulas=[[`=IF(COUNT(I${r})=0,"",I${r}/25.4)`]];
}
st.getRange(`E5:H${db.station_observations.length+4}`).format.fill='#FFF7DF';
st.getRange(`D5:J${db.station_observations.length+4}`).setNumberFormat('0.0');

const v=sheet('Validation','Planned independent validation','No model exists. Supply source/class, matched configuration and uncertainty before accepting a tolerance check.',
 ['ID','Check','Real mm','Model mm','Difference mm','Error %','Tolerance mm','Uncertainty mm','Result','Real in','Model in','Source / photo','Confidence','Class','Configuration','Point IDs / algorithm'],
 db.validation_plan.map(x=>[x.id,x.name,null,null,null,null,x.tolerance_mm,null,null,null,null,null,null,null,null,null]),
 [10,49,15,15,18,15,17,19,31,15,15,52,13,10,35,60]);
for(let i=0;i<db.validation_plan.length;i++){
 const r=i+5;
 v.getRange(`E${r}`).formulas=[[`=IF(COUNT(C${r}:D${r})<2,"",D${r}-C${r})`]];
 v.getRange(`F${r}`).formulas=[[`=IF(OR(COUNT(C${r}:D${r})<2,C${r}=0),"",E${r}/C${r})`]];
 v.getRange(`I${r}`).formulas=[[`=IF(COUNT(C${r}:D${r})<2,"NOT MEASURED",IF(OR(L${r}="",M${r}="",N${r}="",O${r}="",P${r}=""),"NEEDS PROVENANCE",IF(N${r}="D","UNVERIFIED SOURCE",IF(COUNT(H${r})=0,"NEEDS UNCERTAINTY",IF(H${r}<0,"INVALID UNCERTAINTY",IF(ABS(E${r})+H${r}<=G${r},"WITHIN TOLERANCE","REVIEW REQUIRED"))))))`]];
 v.getRange(`J${r}`).formulas=[[`=IF(COUNT(C${r})=0,"",C${r}/25.4)`]];
 v.getRange(`K${r}`).formulas=[[`=IF(COUNT(D${r})=0,"",D${r}/25.4)`]];
}
v.getRange('C5:E44').setNumberFormat('0.0');v.getRange('F5:F44').setNumberFormat('0.0%');v.getRange('G5:H44').setNumberFormat('0.0');v.getRange('J5:K44').setNumberFormat('0.00');
for(const range of ['C5:D44','H5:H44','L5:P44'])v.getRange(range).format.fill='#FFF7DF';
v.getRange('N5:N44').dataValidation={rule:{type:'list',values:['A','B','C','D']}};
v.getRange('M5:M44').dataValidation={rule:{type:'list',values:['1','2','3','4','5']}};

const rq=sheet('Requirements','Owner design requirements','These values are desired component envelopes, not measured vehicle dimensions.',
 ['Requirement','Minimum','Maximum','Unit','Minimum mm','Maximum mm','Minimum in','Maximum in','Source','Notes'],
 db.owner_design_requirements.map(x=>[x.name,x.min_value,x.max_value,x.unit,null,null,null,null,'Owner brief',x.notes]),
 [43,15,15,10,18,18,18,18,18,65]);
for(let i=0;i<db.owner_design_requirements.length;i++){
 const r=i+5;
 for(const [target,src] of [['E','B'],['F','C']])rq.getRange(`${target}${r}`).formulas=[[`=IF(D${r}="mm",${src}${r},IF(D${r}="in",${src}${r}*25.4,""))`]];
 rq.getRange(`G${r}`).formulas=[[`=IF(E${r}="","",E${r}/25.4)`]];
 rq.getRange(`H${r}`).formulas=[[`=IF(F${r}="","",F${r}/25.4)`]];
}
rq.getRange('B5:H16').setNumberFormat('0.00');

sheet('Sources','Source and access register','Research 9 September 2026. Retain publication/model scope. Missing URLs identify the supplied brief.',
 ['ID','Source','URL','Model/year scope','Access status','Accessed','Notes'],
 db.sources.map(x=>[x.id,x.name,x.url,x.model_year_scope,x.access_status,x.accessed_date,x.notes]),
 [10,54,78,49,43,16,76]);

// Meaningful formula tests on one future validation row, then restore all blanks.
v.getRange('C5:D5').values=[[100,104]];v.getRange('H5').values=[[1]];
v.getRange('L5:P5').values=[['test fixture',5,'B','TEST','p1–p2; span']];
if(v.getRange('I5').values[0][0]!=='WITHIN TOLERANCE')throw Error('Tolerance boundary failed');
v.getRange('D5').values=[[105]];
if(v.getRange('I5').values[0][0]!=='REVIEW REQUIRED')throw Error('Uncertainty guard failed');
v.getRange('C5').values=[[0]];
if(v.getRange('F5').values[0][0]!=='')throw Error('Zero denominator guard failed');
v.getRange('N5').values=[['D']];
if(v.getRange('I5').values[0][0]!=='UNVERIFIED SOURCE')throw Error('Source gate failed: '+JSON.stringify(v.getRange('I5').values));
v.getRange('C5:D5').values=[[null,null]];v.getRange('H5').values=[[null]];v.getRange('L5:P5').values=[[null,null,null,null,null]];
if(v.getRange('I5').values[0][0]!=='NOT MEASURED')throw Error('Blank restore failed');
const dimValues=d.getRange(`E5:F${db.dimensions.length+4}`).values;
db.dimensions.forEach((x,i)=>{if(x.value_mm!==null && Math.abs(dimValues[i][0]-x.value_mm)>1e-6)throw Error('Conversion mismatch '+x.id);});
console.log((await wb.inspect({kind:'table',range:'Dimensions!A4:H8',include:'values,formulas',tableMaxRows:5,tableMaxCols:8,maxChars:2500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:50},summary:'Formula errors',maxChars:2000})).ndjson);
for(const c of configs){
 const p=await wb.render({sheetName:c.name,range:`A1:${c.name==='Sources'?'G':c.name==='Dimensions'?'H':c.name==='First measurements'?'F':c.name==='Validation'?'I':'J'}${Math.min(c.last,9)}`,scale:1,format:'png'});
 await fs.writeFile(`${root}/work/preview_${c.name.replaceAll(' ','_')}.png`,new Uint8Array(await p.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(`${root}/outputs/R1S_dimension_register.xlsx`);
const sidecar=`${root}/outputs/R1S_dimension_register.xlsx.inspect.ndjson`;
try { await fs.rename(sidecar,`${root}/work/workbook_inspection.ndjson`); } catch(e) { if(e.code!=='ENOENT')throw e; }
console.log('Workbook exported; formula tests and 69 conversion checks passed.');
