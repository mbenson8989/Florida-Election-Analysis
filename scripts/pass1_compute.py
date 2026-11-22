"""PASS 1: parse raw files (csv module, regex HTML, pdftotext -layout, openpyxl); exact Fraction math."""
import csv, re, subprocess, json, sys
from fractions import Fraction as F
import openpyxl
RAW='/workspace/florida/raw/'
def key(n): return re.sub(r'[^a-z]','',n.lower().replace('saint','st'))
def toint(s): return int(str(s).replace(',','').strip())

# 2022 governor votes: tab extract
d22={}
with open(RAW+'fl_results_20221108_extract.txt',encoding='latin-1',newline='') as fh:
    for row in csv.DictReader(fh,delimiter='\t'):
        if row['RaceCode']!='GOV': continue
        k=key(row['CountyName']); c=d22.setdefault(k,{'name':row['CountyName'],'dem':0,'rep':0,'tot':0,'ndem':0})
        v=toint(row['CanVotes']); c['tot']+=v
        if row['PartyCode']=='DEM': c['dem']+=v; c['ndem']+=1; assert row['CanNameFirst']=='Crist'
        if row['PartyCode']=='REP': c['rep']+=v
# 2026 governor votes: tab file
d26={}
with open(RAW+'20261103_ElecResultsFL.txt',encoding='latin-1',newline='') as fh:
    for row in csv.DictReader(fh,delimiter='\t'):
        if row['RaceCode']!='GOV': continue
        k=key(row['CountyName']); c=d26.setdefault(k,{'name':row['CountyName'].strip(),'dem':0,'rep':0,'tot':0,'ndem':0,'prec':row['Precincts'],'precrep':row['PrecinctsReporting']})
        v=toint(row['CanVotes']); c['tot']+=v
        if row['PartyCode']=='DEM': c['dem']+=v; c['ndem']+=1; assert row['CanNameFirst']=='Jolly'
        if row['PartyCode']=='REP': c['rep']+=v
# 2022 ballots: turnout report, regex on stripped text
t=open(RAW+'fl_turnout_20221108.html',encoding='latin-1').read()
t=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'(&nbsp;|\s)+',' ',t)
b22={}; 
for m in re.finditer(r"([A-Z][A-Za-z\.\- ]+?) ([\d,]+) ([\d,]+) ([\d\.]+)%",t):
    nm=m.group(1).strip()
    if nm.startswith('Turnout'): nm=nm[len('Turnout'):].strip()
    nm=nm.split(' % Turnout ')[-1]
    b22[key(nm)]=(toint(m.group(3)),toint(m.group(2)))
tot22_ballots=b22.pop('total')
# 2026 ballots: county reporting status, regex on table rows
h=open(RAW+'few_CountyReportingStatus.html',encoding='utf-8').read()
h=re.sub(r'<script.*?</script>','',h,flags=re.S)
rows=re.findall(r'<tr[^>]*>(.*?)</tr>',h,flags=re.S)
b26={}
for r in rows:
    cells=[re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',c)).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r,flags=re.S)]
    if len(cells)>=4 and re.fullmatch(r'[\d,]+',cells[1] or 'x'):
        b26[key(cells[0])]=(toint(cells[1]),toint(cells[2]))
tot26_ballots=b26.pop('total')
# 2022 registration: pdftotext -layout of 1-party-by-county
txt=subprocess.run(['pdftotext','-layout',RAW+'bookclosing_2022gen_1_party_by_county.pdf','-'],capture_output=True,text=True).stdout
r22={}
for line in txt.splitlines():
    m=re.match(r'^\s*([A-Za-z][A-Za-z\.\- ]*?)\s{2,}((?:[\d,]+\s+){13}[\d,]+)\s*$',line)
    if m:
        nums=[toint(x) for x in m.group(2).split()]
        # cols: Rep, Dem, CWP, Const, Ecol, Green, Indep, Lib, PSL, People's, Reform, NPA, Total, Precincts
        assert sum(nums[:12])==nums[12], line
        r22[key(m.group(1))]=(nums[1],nums[12])
tot22_reg=r22.pop('total',None) or r22.pop('totals',None)
# 2026 registration: openpyxl
wb=openpyxl.load_workbook(RAW+'bookclosing_2026gen_1_party_by_county.xlsx',data_only=True); ws=wb.active
hdr=None; r26={}
for row in ws.iter_rows(values_only=True):
    if row[0]=='County Name': hdr=[str(x).strip() if x else x for x in row]; continue
    if hdr and row[0]:
        di=hdr.index('Florida Democratic Party'); ti=hdr.index('TOTAL')
        assert sum(row[1:ti])==row[ti]
        r26[key(str(row[0]))]=(row[di],row[ti])
tot26_reg=r26.pop('total')

keys=sorted(d22)
for name,dd in [('d26',d26),('b22',b22),('b26',b26),('r22',r22),('r26',r26)]:
    assert sorted(dd)==keys,(name,set(dd)^set(keys))
assert len(keys)==67
H=F(100)
recs={}
for k in keys:
    a,b=d22[k],d26[k]
    assert a['ndem']==1 and b['ndem']==1
    x=dict(county=a['name'].replace('Desoto','DeSoto'),dem22=a['dem'],govtot22=a['tot'],rep22=a['rep'],ballots22=b22[k][0],demreg22=r22[k][0],totreg22=r22[k][1],
           dem26=b['dem'],govtot26=b['tot'],rep26=b['rep'],ballots26=b26[k][0],demreg26=r26[k][0],totreg26=r26[k][1])
    x['dem_chg']=x['dem26']-x['dem22']; x['ballots_chg']=x['ballots26']-x['ballots22']
    x['demreg_chg']=x['demreg26']-x['demreg22']; x['totreg_chg']=x['totreg26']-x['totreg22']
    S22=H*x['dem22']/x['ballots22']; S26=H*x['dem26']/x['ballots26']
    R22=H*x['demreg22']/x['totreg22']; R26=H*x['demreg26']/x['totreg26']
    x.update(S22=S22,S26=S26,R22=R22,R26=R26,G22=S22-R22,G26=S26-R26)
    x['dG']=x['G26']-x['G22']; x['drop']=R22-R26
    x['loss']=x['demreg26']<x['demreg22']
    x['resid_regloss']=x['dG']-x['drop']
    x['implied_regloss']=x['resid_regloss']*x['ballots26']/H
    x['dem_chg_pct']=H*x['dem_chg']/x['dem22']; x['ballots_chg_pct']=H*x['ballots_chg']/x['ballots22']; x['demreg_chg_pct']=H*x['demreg_chg']/x['demreg22']
    x['DR_over_ballots22']=F(x['dem22']+x['rep22'],x['ballots22']); x['DR_over_ballots26']=F(x['dem26']+x['rep26'],x['ballots26'])
    x['gov_over_ballots22']=F(x['govtot22'],x['ballots22']); x['gov_over_ballots26']=F(x['govtot26'],x['ballots26'])
    x['prec26']=b['prec']; x['precrep26']=b['precrep']
    recs[k]=x
# OLS exact
n=len(recs); xs=[recs[k]['drop'] for k in keys]; ys=[recs[k]['dG'] for k in keys]
mx=sum(xs)/n; my=sum(ys)/n
Sxx=sum((a-mx)**2 for a in xs); Syy=sum((b-my)**2 for b in ys); Sxy=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
m=Sxy/Sxx; c=my-m*mx; R2=Sxy*Sxy/(Sxx*Syy)
for k in keys:
    x=recs[k]; x['fit_pred']=c+m*x['drop']; x['fit_resid']=x['dG']-x['fit_pred']; x['implied_fit']=x['fit_resid']*x['ballots26']/H
fit=dict(n=n,constant=c,multiplier=m,R2=R2)
# Surplus-form fits, S = m*(D/100) + b, S = G (Dem share of ballots - Dem reg share, pts), D = Dem reg share (pts). Centered-moment OLS, exact.
sfit={}
for y in ['22','26']:
    X=[recs[k]['R'+y]/100 for k in keys]; Y=[recs[k]['G'+y] for k in keys]
    ax=sum(X)/n; ay=sum(Y)/n
    sxx=sum((a-ax)**2 for a in X); syy=sum((b-ay)**2 for b in Y); sxy=sum((a-ax)*(b-ay) for a,b in zip(X,Y))
    mm=sxy/sxx; bb=ay-mm*ax
    for k in keys:
        recs[k]['sfit_pred'+y]=mm*recs[k]['R'+y]/100+bb; recs[k]['sfit_res'+y]=recs[k]['G'+y]-recs[k]['sfit_pred'+y]
    sfit[y]=dict(n=n,multiplier=mm,offset=bb,R2=sxy*sxy/(sxx*syy),mean_abs_resid=sum(abs(recs[k]['sfit_res'+y]) for k in keys)/n,sxx=sxx,sse=sum(recs[k]['sfit_res'+y]**2 for k in keys))
state=dict(dem22=sum(r['dem22'] for r in recs.values()),govtot22=sum(r['govtot22'] for r in recs.values()),rep22=sum(r['rep22'] for r in recs.values()),
           ballots22=sum(r['ballots22'] for r in recs.values()),demreg22=sum(r['demreg22'] for r in recs.values()),totreg22=sum(r['totreg22'] for r in recs.values()),
           dem26=sum(r['dem26'] for r in recs.values()),govtot26=sum(r['govtot26'] for r in recs.values()),rep26=sum(r['rep26'] for r in recs.values()),
           ballots26=sum(r['ballots26'] for r in recs.values()),demreg26=sum(r['demreg26'] for r in recs.values()),totreg26=sum(r['totreg26'] for r in recs.values()))
reported=dict(ballots22=tot22_ballots[0],totreg22_turnoutrpt=tot22_ballots[1],demreg22=tot22_reg[0] if tot22_reg else None,totreg22=tot22_reg[1] if tot22_reg else None,
              ballots26=tot26_ballots[0],totreg26_status=tot26_ballots[1],demreg26=tot26_reg[0],totreg26=tot26_reg[1])
def ser(v):
    if isinstance(v,F): return f'{v.numerator}/{v.denominator}'
    return v
json.dump(dict(counties={k:{a:ser(b) for a,b in v.items()} for k,v in recs.items()},fit={a:ser(b) for a,b in fit.items()},surplus_fit={y:{a:ser(b) for a,b in d.items()} for y,d in sfit.items()},state_sums=state,state_reported_in_parsed_files=reported),
          open('/workspace/florida/data/pass1.json','w'),indent=1)
print('PASS1 counties',n,'fit',float(c),float(m),float(R2)); print('state sums',state); print('reported',reported)
