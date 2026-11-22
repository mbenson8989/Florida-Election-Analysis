import json, re, sys, datetime
from fractions import Fraction
from decimal import Decimal, getcontext
from bs4 import BeautifulSoup
sys.path.insert(0,'/workspace/florida/scripts'); from common_fields import FIELDS_INT, FIELDS_FRAC
getcontext().prec=40
p1=json.load(open('data/pass1.json')); p2=json.load(open('data/pass2.json'))
def fr(s): return Fraction(s) if isinstance(s,str) else Fraction(s)
def dec(f): return Decimal(f.numerator)/Decimal(f.denominator)
log=[]; mism=[]
K1,K2=sorted(p1['counties']),sorted(p2['counties'])
log.append(f'county count pass1={len(K1)} pass2={len(K2)} keys identical={K1==K2}')
checks=0
for k in K1:
    a,b=p1['counties'][k],p2['counties'][k]
    for f in FIELDS_INT:
        checks+=1
        if a[f]!=b[f]: mism.append((k,f,a[f],b[f]))
    for f in FIELDS_FRAC:
        checks+=1
        x,y=fr(a[f]),fr(b[f])
        # exact rational equality AND identical 40-significant-digit decimal string
        if x!=y or str(dec(x))!=str(dec(y)): mism.append((k,f,str(dec(x)),str(dec(y))))
    checks+=1
    if a['loss']!=(b['demreg26']<b['demreg22']): mism.append((k,'loss',a['loss'],None))
fitchecks=0
for f in ['constant','multiplier','R2']:
    fitchecks+=1
    if fr(p1['fit'][f])!=fr(p2['fit'][f]): mism.append(('FIT',f,p1['fit'][f],p2['fit'][f]))
for y in ['22','26']:
    for f in ['n','multiplier','offset','R2','mean_abs_resid','sxx','sse']:
        fitchecks+=1
        if fr(p1['surplus_fit'][y][f])!=fr(p2['surplus_fit'][y][f]): mism.append(('SURPLUS'+y,f,p1['surplus_fit'][y][f],p2['surplus_fit'][y][f]))
fitchecks+=1
if p1['fit']['n']!=p2['fit']['n']: mism.append(('FIT','n',p1['fit']['n'],p2['fit']['n']))
log.append(f'county-figure checks={checks} ({len(K1)} counties x {len(FIELDS_INT)+len(FIELDS_FRAC)+1} fields); fit checks={fitchecks}; mismatches={len(mism)}')
# State totals: county sums vs DOE-reported statewide figures
S=p1['state_sums']; R1=p1['state_reported_in_parsed_files']; R2=p2['reported']
gov26=open('raw/few_governor_statewide_2026.html').read()
t=re.sub(r'<script.*?</script>','',gov26,flags=re.S); t=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'(&nbsp;|\s)+',' ',t)
jolly=int(re.search(r'David Jolly and Gwen Graham DEM ([\d,]+)',t).group(1).replace(',',''))
donalds=int(re.search(r'Byron Donalds and Bryan Avila REP ([\d,]+)',t).group(1).replace(',',''))
tot26=int(re.search(r'Total ([\d,]+)',t).group(1).replace(',',''))
# 2026 county HTML (third source) totals row + per-county check
s=BeautifulSoup(open('raw/few_gov_by_county_2026.html').read(),'html.parser')
html26={}
for tr in s.find_all('tr'):
    c=[td.get_text(' ',strip=True) for td in tr.find_all(['td','th'])]
    if len(c)==11 and re.fullmatch(r'[\d,]+',c[1]):
        vals=[int(x.replace(',','')) for x in c[1:]]
        html26[re.sub(r'[^a-z]','',c[0].lower().replace('total',''))or'total']=vals
st=[]
def chk(label,a,b): st.append((label,a,b,a==b))
chk('2022 Dem gov votes: county sum vs DOE DetailRpt Total',S['dem22'],R2['total22']['dem'])
chk('2022 Rep gov votes: county sum vs DOE DetailRpt Total',S['rep22'],R2['total22']['rep'])
chk('2022 all gov votes: county sum vs DOE DetailRpt Total',S['govtot22'],R2['total22']['all'])
chk('2022 ballots cast: county sum vs DOE TurnoutRpt Total',S['ballots22'],R1['ballots22'])
chk('2022 Dem registration: county sum vs book-closing Total',S['demreg22'],R1['demreg22'])
chk('2022 total registration: county sum vs book-closing Total',S['totreg22'],R1['totreg22'])
chk('2022 total registration: book-closing vs TurnoutRpt Voter Reg Total',R1['totreg22'],R1['totreg22_turnoutrpt'])
chk('2026 Dem gov votes: county sum vs Election Watch statewide',S['dem26'],jolly)
chk('2026 Rep gov votes: county sum vs Election Watch statewide',S['rep26'],donalds)
chk('2026 all gov votes: county sum vs Election Watch statewide Total',S['govtot26'],tot26)
chk('2026 Dem gov votes: county sum vs Election Watch by-county Total row',S['dem26'],html26['total'][1])
chk('2026 all gov votes: county sum vs by-county Total row',S['govtot26'],sum(html26['total']))
chk('2026 ballots cast: county sum vs CountyReportingStatus TOTAL',S['ballots26'],R1['ballots26'])
chk('2026 Dem registration: county sum vs book-closing Total',S['demreg26'],R1['demreg26'])
chk('2026 total registration: county sum vs book-closing Total',S['totreg26'],R1['totreg26'])
chk('2026 total registration: book-closing vs CountyReportingStatus Eligible Active TOTAL',R1['totreg26'],R1['totreg26_status'])
# cross-source per county, 2026 HTML vs tab file
xs=0; xd=[]
for k in K1:
    h=html26[re.sub(r'[^a-z]','',k)]
    xs+=2
    if h[1]!=p1['counties'][k]['dem26']: xd.append((k,'dem',h[1],p1['counties'][k]['dem26']))
    if sum(h)!=p1['counties'][k]['govtot26']: xd.append((k,'all',sum(h),p1['counties'][k]['govtot26']))
ok_state=all(x[3] for x in st)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
lines=[f'Florida governor 2022 vs 2026 - verification log, run {now}','']
lines+=['== PASS 1 (scripts/pass1_compute.py) vs PASS 2 (scripts/pass2_verify.py), separate parsers and partly separate source documents']+log
lines+=[f'  MISMATCH {m}' for m in mism]
lines+=['','== STATE TOTALS (county sums vs DOE-reported statewide totals)']+[f"  {'OK ' if ok else 'BAD'} {l}: {a:,} vs {b:,}" for l,a,b,ok in st]
lines+=['',f'== CROSS-SOURCE 2026 Election Watch ContestResultsByCounty HTML vs results tab file: {xs} checks, differences {len(xd)} {xd}']
lines+=[f"== 2026 pipe Votes file governor record status codes: {p2['pipe_status']} (I = Incomplete per DOS layout)"]
lines+=['',f'RESULT: {"CLEAN" if not mism and ok_state and not xd and len(K1)==67 else "NOT CLEAN"}']
open('VERIFY_LOG.txt','a').write('\n'.join(lines)+'\n\n')
print('\n'.join(lines))
sys.exit(0 if (not mism and ok_state and not xd and len(K1)==67) else 1)
