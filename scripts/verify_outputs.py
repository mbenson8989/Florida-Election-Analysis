"""Check every number in the rendered PDF, CSV and wiki county table against PASS 2 values (independent of the build code)."""
import json, csv, re, datetime
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP, getcontext
import pdfplumber
getcontext().prec=60
P=json.load(open('/workspace/florida/data/pass2.json')); K=P['counties']
def Fr(v): return Fraction(v) if isinstance(v,str) else Fraction(v)
def q(v,nd): v=Fr(v); return (Decimal(v.numerator)/Decimal(v.denominator)).quantize(Decimal(1).scaleb(-nd),rounding=ROUND_HALF_UP)
def norm(s): return re.sub(r'[^a-z]','',s.lower())
name={norm(k):k for k in K}
def keyof(nm): 
    n=norm(nm); return n if n in K else name.get(n)
mism=[]; checks=0
def eq(label,got,exp):
    global checks; checks+=1
    if got!=exp: mism.append((label,got,exp))
# PDF
txt=''
with pdfplumber.open('/workspace/florida/pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf') as pdf:
    pages=[p.extract_text() for p in pdf.pages]
def nums(s): return [Decimal(x.replace(',','').replace('+','')) for x in s.split()]
t1=t2=0; order=[]
for pi,pg in enumerate(pages):
    for line in pg.splitlines():
        m=re.match(r'^([A-Z][A-Za-z\.\- ]+?) ((?:[+\-]?[\d,\.]+ ){10,14}[+\-]?[\d,\.]+)$',line.strip())
        if not m: continue
        nm=m.group(1); v=nums(m.group(2)); k=keyof(nm) if nm!='STATEWIDE' else None
        if nm=='STATEWIDE': continue
        r=K[k]
        if len(v)==14:
            t1+=1; order.append(k)
            exp=[q(r['R22'],2),q(r['R26'],2),r['demreg22'],r['demreg26'],r['demreg_chg'],q(r['demreg_chg_pct'],2),r['dem22'],r['dem26'],r['dem_chg'],q(r['dem_chg_pct'],2),r['ballots22'],r['ballots26'],r['ballots_chg'],q(r['ballots_chg_pct'],2)]
        elif len(v)==11:
            t2+=1
            S22,S26,R22,R26=Fr(r['S22']),Fr(r['S26']),Fr(r['R22']),Fr(r['R26'])
            exp=[q(S22,2),q(S26,2),q(S26-S22,2),q(R22,2),q(R26,2),q(R26-R22,2),q(r['G22'],2),q(r['G26'],2),q(r['dG'],2),r['totreg22'],r['totreg26']]
        else: mism.append(('pdf-shape',nm,len(v))); continue
        for i,(g,e) in enumerate(zip(v,exp)): eq(f'PDF {nm} col{i+1}',g,Decimal(e))
exp_order=sorted(K,key=lambda k:(-Fr(K[k]['R26']),K[k]['county'] if 'county' in K[k] else k))
eq('PDF table1 rows',t1,67); eq('PDF table2 rows',t2,67); eq('PDF sort by R26 desc',order==sorted(order,key=lambda k:-Fr(K[k]['R26'])),True)
# CSV full precision
rows=list(csv.reader(open('/workspace/florida/data/florida_governor_2022_2026_by_county.csv')))
hdr=rows[1]; body=[dict(zip(hdr,r)) for r in rows[2:]]
mapf={'dem_reg_share_2022_pct':'R22','dem_reg_share_2026_pct':'R26','dem_share_of_ballots_2022_pct':'S22','dem_share_of_ballots_2026_pct':'S26','G_2022':'G22','G_2026':'G26','delta_G':'dG','reg_share_drop':'drop','residual_regloss_dG_minus_drop':'resid_regloss','implied_extra_votes_regloss':'implied_regloss','fit_residual':'fit_resid','implied_votes_fit_residual':'implied_fit','surplus_fit_predicted_S_2022':'sfit_pred22','surplus_fit_residual_2022':'sfit_res22','surplus_fit_predicted_S_2026':'sfit_pred26','surplus_fit_residual_2026':'sfit_res26'}
mapi={'dem_reg_2022':'demreg22','dem_reg_2026':'demreg26','dem_gov_votes_2022':'dem22','dem_gov_votes_2026':'dem26','ballots_cast_2022':'ballots22','ballots_cast_2026':'ballots26','total_reg_2022':'totreg22','total_reg_2026':'totreg26'}
nc=0
for b in body:
    if b['county']=='STATEWIDE': continue
    nc+=1; r=K[keyof(b['county'])]
    for c,f in mapf.items(): eq(f'CSV {b["county"]} {c}',Decimal(b[c]),q(r[f],20))
    for c,f in mapi.items(): eq(f'CSV {b["county"]} {c}',int(b[c]),r[f])
eq('CSV county rows',nc,67)
# Wiki Reverse-Math all-67 table
wk=open('/workspace/florida/wiki/Reverse-Math.md').read().split('### All 67 counties')[1]
nw=0
def sgn(x,nd=2): v=q(x,nd); return ('+' if v>0 else '−' if v<0 else '')+f'{abs(v):.{nd}f}'
for line in wk.splitlines():
    if not line.startswith('| ') or line.startswith('| County') : continue
    c=[x.strip() for x in line.strip('|').split('|')]; k=keyof(c[0]); 
    if not k: continue
    r=K[k]; nw+=1
    exp=[c[0],f"{r['ballots26']:,}",f"{r['demreg22']:,} → {r['demreg26']:,}",f"{r['dem22']:,} → {r['dem26']:,}",f"{r['ballots22']:,} → {r['ballots26']:,}",f"{q(r['S22'],2):.2f}% → {q(r['S26'],2):.2f}%",f"{q(r['R22'],2):.2f}% → {q(r['R26'],2):.2f}%",sgn(r['dG']),sgn(r['resid_regloss'])]
    iv=q(r['implied_regloss'],0); exp.append(('+' if iv>0 else '−' if iv<0 else '')+f'{abs(int(iv)):,}')
    for i,(g,e) in enumerate(zip(c,exp)): eq(f'WIKI {c[0]} col{i}',g,e)
eq('WIKI rows',nw,67)
# Locked page: surplus form only, values from PASS 2
import os, hashlib
SFP=P['surplus_fit']; lk=open('/workspace/florida/wiki/Locked-Florida-Formula.md').read()
def p2(x,nd): return f"{q(x,nd):.{nd}f}"
for y in ('22','26'):
    d=SFP[y]; b=Fr(d['offset'])
    eq(f'LOCKED eq 20{y}',f"**20{y}: S = {p2(d['multiplier'],2)} × (D/100) {'+' if b>=0 else '−'} {p2(abs(b),2)}**" in lk,True)
    eq(f'LOCKED exact 20{y}',f"20{y} m = {p2(d['multiplier'],15)}, b = {p2(d['offset'],15)}, R² = {p2(d['R2'],15)}" in lk,True)
    eq(f'LOCKED table R2/MAR 20{y}',f"| {p2(d['R2'],6)} | {p2(d['mean_abs_resid'],6)} |" in lk,True)
eq('LOCKED has no ΔG equation','ΔG =' not in lk and 'ΔG ≈' not in lk and 'registration-share drop)' not in lk,True)
lt=lk.split('## All 67 counties against the line')[1].split('## Rules')[0]; nl=0
for line in lt.splitlines():
    if not line.startswith('| ') or line.startswith('| County'): continue
    c=[x.strip() for x in line.strip('|').split('|')]; k=keyof(c[0])
    if not k: continue
    r=K[k]; nl+=1
    exp=[c[0],f"{q(r['R22'],2):.2f}",sgn(r['G22']),sgn(r['sfit_pred22']),sgn(r['sfit_res22']),f"{q(r['R26'],2):.2f}",sgn(r['G26']),sgn(r['sfit_pred26']),sgn(r['sfit_res26'])]
    for i2,(g,e) in enumerate(zip(c,exp)): eq(f'LOCKED {c[0]} col{i2}',g,e)
eq('LOCKED rows',nl,67)
# README (wiki page and repo README.md): values and hashes
rw=open('/workspace/florida/wiki/README.md').read(); rr=open('/workspace/florida/README.md').read()
eq('README repo == wiki body',rw.startswith(rr),True)
st2={k:sum(K[c][k] for c in K) for k in ('dem22','dem26','ballots22','ballots26','demreg22','demreg26','totreg22','totreg26')}
S22=Fraction(100*st2['dem22'],st2['ballots22']); S26=Fraction(100*st2['dem26'],st2['ballots26']); R22=Fraction(100*st2['demreg22'],st2['totreg22']); R26=Fraction(100*st2['demreg26'],st2['totreg26'])
eq('README shares',f"went from {p2(S22,2)}% in 2022 to {p2(S26,2)}% in 2026, while the Democratic share of registration went from {p2(R22,2)}% to {p2(R26,2)}%" in rr,True)
eq('README surplus',f"grew from {sgn(S22-R22)} to {sgn(S26-R26)} points" in rr,True)
eq('README all counties G rose',all(Fr(K[c]['G26'])>Fr(K[c]['G22']) for c in K),True)
eq('README all counties demreg fell',all(K[c]['demreg26']<K[c]['demreg22'] for c in K),True)
eq('README totreg fall',f"fell by {st2['totreg22']-st2['totreg26']:,} between" in rr,True)
for y in ('22','26'):
    d=SFP[y]; eq(f'README line 20{y}',f"S = {p2(d['multiplier'],2)} × (D/100) + {p2(d['offset'],2)}" in rr,True)
man=json.load(open('/workspace/florida/MANIFEST.json'))
for m_ in man:
    h=hashlib.sha256(open('/workspace/florida/'+m_['file'],'rb').read()).hexdigest()
    eq(f"README hash {m_['file']}",f"| `{m_['file']}` | {m_['url']} | `{h}` |" in rr,True); eq(f"MANIFEST hash {m_['file']}",m_['sha256'],h)
for f_ in ['pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf','data/florida_governor_2022_2026_by_county.csv']:
    h=hashlib.sha256(open('/workspace/florida/'+f_,'rb').read()).hexdigest(); eq(f'README hash {f_}',f"| `{f_}` | `{h}` |" in rr,True)
eq('README raw file count',len(man),len([x for x in os.listdir('/workspace/florida/raw')]))
for need in ['https://moebenson.substack.com/p/the-burden-just-flipped','dos.fl.gov','results.elections.myflorida.com','floridaelectionwatch.gov','USB batch-acceptance overrides','absentee batch chain-of-custody gap','Ghost voters fed with real voter data','Cloud-layer number swaps','sha256sum','UNOFFICIAL']:
    eq(f'README contains {need}',need in rr,True)
# every wiki page: unofficial 2026 label; sidebar order; Cedar link
for f in sorted(os.listdir('/workspace/florida/wiki')):
    s_=open('/workspace/florida/wiki/'+f).read()
    eq(f'unofficial marker in {f}','unofficial' in s_.lower(),True)
# grep for retired strings across every published text file except raw/
bad=['cedar-county-election-analysis','back-room','backroom','back room','who-holds-the-keys','who holds the keys']
for root,_,fs in os.walk('/workspace/florida'):
    if '/raw' in root or '/.git' in root: continue
    for fn in fs:
        if not fn.endswith(('.md','.csv','.json','.txt','.py','.sh')) or fn=='VERIFY_LOG.txt' or root.endswith('scripts') and fn in ('verify_outputs.py','patch_wiki_v2.py'): continue
        t=open(os.path.join(root,fn),errors='ignore').read().lower()
        for b_ in bad: eq(f'no "{b_}" in {os.path.relpath(os.path.join(root,fn),"/workspace/florida")}',b_ in t,False)
pdftxt=''.join(pg.extract_text() or '' for pg in pdfplumber.open('/workspace/florida/pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf').pages).lower()
eq('PDF unofficial','unofficial' in pdftxt,True); eq('PDF not certified-results label','certified nov 17' not in pdftxt,True)
sb=open('/workspace/florida/wiki/_Sidebar.md').read()
order=[m.group(1) for m in re.finditer(r'^\d+\. \[([^\]]+)\]',sb,flags=re.M)]
eq('Sidebar order',order,['Home','Cedar County Audit (Nebraska)','Floor and Ceiling Counties','Bottom-Up Reverse Math','Locked Florida Formula','Graphs','Florida County PDF Information','Resources'])
CED='https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit'
eq('Cedar link sidebar',CED in sb,True); eq('Cedar link home',CED in open('/workspace/florida/wiki/Home.md').read(),True); eq('Cedar link README',CED in rr,True)
eq('PDF link sidebar','https://raw.githubusercontent.com/mbenson8989/Florida-Election-Analysis/main/pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf' in sb,True)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
out=[f'== OUTPUT CHECK vs PASS 2 values (scripts/verify_outputs.py), run {now}',f'  PDF rows: table1 {t1}, table2 {t2}; CSV county rows {nc}; wiki Reverse-Math county rows {nw}; Locked rows {nl}',f'  checks {checks}; mismatches {len(mism)}']+[f'  MISMATCH {x}' for x in mism[:50]]
open('/workspace/florida/VERIFY_LOG.txt','a').write('\n'.join(out)+'\n\n'); print('\n'.join(out))
import sys; sys.exit(1 if mism else 0)
