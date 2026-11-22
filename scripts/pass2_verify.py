"""PASS 2: independent re-parse from raw files with different parsers and sources:
 2022 votes  <- DetailRpt HTML (BeautifulSoup)         [pass 1 used the tab extract]
 2026 votes  <- pipe-delimited Info+Votes files         [pass 1 used the tab file]
 ballots     <- BeautifulSoup table parsing             [pass 1 used regex]
 2022 reg    <- by-party-by-RACE PDF via pdfplumber, Dem = Democrat section total, county total = sum of 12 party sections [pass 1: 1-party PDF via pdftotext]
 2026 reg    <- 1-party PDF via pdfplumber              [pass 1: xlsx via openpyxl]
Math: exact rationals, written separately."""
import re, json
from fractions import Fraction
from bs4 import BeautifulSoup
import pdfplumber
RAW='/workspace/florida/raw/'
def ck(s):
    s=s.lower().strip()
    s=s.replace('st.','st').replace('-','').replace(' ','').replace('.','')
    return s
def num(s): return int(s.replace(',','').replace(':','').strip())

# --- 2022 governor votes from the DetailRpt HTML
soup=BeautifulSoup(open(RAW+'fl_gov_detail_20221108.html',encoding='latin-1').read(),'html.parser')
v22={}; hdr=None; total22=None
for tr in soup.find_all('tr'):
    cells=[td.get_text(' ',strip=True).replace('\xa0',' ').strip() for td in tr.find_all(['td','th'],recursive=False)]
    cells=[c for c in cells if c!='']
    if cells and cells[0]=='County' and len(cells)==5: hdr=cells; continue
    if hdr and len(cells)==5 and re.fullmatch(r'[\d,]+',cells[1]):
        vals=[num(c) for c in cells[1:]]
        di=[i for i,h in enumerate(hdr[1:]) if '(DEM)' in h]; ri=[i for i,h in enumerate(hdr[1:]) if '(REP)' in h]
        assert len(di)==1 and len(ri)==1 and 'Crist' in hdr[1+di[0]]
        rec=dict(dem=vals[di[0]],rep=vals[ri[0]],all=sum(vals))
        if cells[0]=='Total': total22=rec
        else: v22[ck(cells[0])]=rec
# --- 2026 governor votes from pipe files
races={};cands={};units={}
for line in open(RAW+'20261103_ElecResultsFL_PipeDlm_Info.txt',encoding='latin-1'):
    f=line.strip().strip('[]').split('|')
    if f[0]=='r': races[f[5]]=f[3]
    elif f[0]=='c': cands[f[6]]=(f[3],f[4],f[5])
    elif f[0]=='u': units[f[4]]=f[3]
gov=[r for r,nm in races.items() if nm.startswith('Governor')]; assert gov==['160000']
dem_id=[c for c,(r,l,fn) in cands.items() if r=='160000' and fn=='Jolly']; rep_id=[c for c,(r,l,fn) in cands.items() if r=='160000' and fn=='Donalds']
assert len(dem_id)==1 and len(rep_id)==1
v26={}; status=set()
for line in open(RAW+'20261103_ElecResultsFL_PipeDlm_Votes.txt',encoding='latin-1'):
    f=line.strip().strip('[]').split('|')
    if f[0]!='V' or f[4]!='160000': continue
    status.add(f[3]); u=ck(units[f[5]]); r=v26.setdefault(u,dict(dem=0,rep=0,all=0))
    r['all']+=int(f[8])
    if f[7]==dem_id[0]: r['dem']+=int(f[8])
    if f[7]==rep_id[0]: r['rep']+=int(f[8])
# --- ballots 2022 (TurnoutRpt) and 2026 (CountyReportingStatus) via BeautifulSoup
def table_rows(path,enc):
    s=BeautifulSoup(open(path,encoding=enc).read(),'html.parser')
    for tr in s.find_all('tr'):
        yield [td.get_text(' ',strip=True).replace('\xa0',' ').strip() for td in tr.find_all(['td','th'])]
bal22={}
for c in table_rows(RAW+'fl_turnout_20221108.html','latin-1'):
    c=[x for x in c if x]
    if len(c)==4 and re.fullmatch(r'[\d,]+',c[1]) and c[3].endswith('%'): bal22[ck(c[0])]=num(c[2])
bal26={}; status26={}
for c in table_rows(RAW+'few_CountyReportingStatus.html','utf-8'):
    if len(c)>=5 and re.fullmatch(r'[\d,]+',c[1] or '-'):
        bal26[ck(c[0])]=num(c[1]); status26[ck(c[0])]=c[3:]
# --- registration 2022: by-race PDF sections
SECTIONS={'Republican','Democrat','Coalition With A Purpose Party','Constitution Party of Florida','Ecology Party of Florida','Green Party','Independent Party of Florida','Libertarian Party of Florida','Party for Socialism and Liberation - Florida',"People's Party",'Reform Party of Florida','No Party Affiliation'}
reg22={}; cur=None
with pdfplumber.open(RAW+'bookclosing_2022gen_3_party_by_county_by_race.pdf') as pdf:
    for p in pdf.pages:
        for l in sorted(p.extract_text_lines(),key=lambda l:(round(l['top']),l['x0'])):
            t=l['text'].strip()
            if t in SECTIONS: cur=t; continue
            m=re.match(r'^([A-Za-z][A-Za-z\.\- ]*?) ((?:[\d,]+ ){8}[\d,]+)$',t)
            if m and cur:
                vals=[num(x) for x in m.group(2).split()]; assert sum(vals[:8])==vals[8]
                d=reg22.setdefault(ck(m.group(1)),{}); assert cur not in d; d[cur]=vals[8]
for k,d in reg22.items(): assert len(d)==12,(k,len(d))
reg22={k:(d['Democrat'],sum(d.values())) for k,d in reg22.items()}
# --- registration 2026: 1-party PDF via pdfplumber
reg26={}
with pdfplumber.open(RAW+'bookclosing_2026gen_1_party_by_county.pdf') as pdf:
    for p in pdf.pages:
        for t in (p.extract_text() or '').splitlines():
            m=re.match(r'^([A-Za-z][A-Za-z\.\- ]*?) ((?:[\d,]+ ){18,19}[\d,]+)$',t.strip())
            if m:
                vals=[num(x) for x in m.group(2).split()]
                # 18 party columns + TOTAL (+ Precincts on county rows)
                if len(vals)==20: vals=vals[:19]
                assert sum(vals[:18])==vals[18],t
                reg26[ck(m.group(1))]=(vals[1],vals[18])
st_reg22=reg22.pop('total'); st_reg26=reg26.pop('total')
st_bal22=bal22.pop('total'); st_bal26=bal26.pop('total'); status26.pop('total',None)
K=sorted(v22)
for nm,d in [('v26',v26),('bal22',bal22),('bal26',bal26),('reg22',reg22),('reg26',reg26)]:
    assert sorted(d)==K,(nm,set(d)^set(K))
assert len(K)==67

def pct(a,b): return Fraction(100*a,b)
out={}
for k in K:
    D22,D26=v22[k]['dem'],v26[k]['dem']; B22,B26=bal22[k],bal26[k]
    DR22,TR22=reg22[k]; DR26,TR26=reg26[k]
    o=dict(dem22=D22,govtot22=v22[k]['all'],rep22=v22[k]['rep'],ballots22=B22,demreg22=DR22,totreg22=TR22,
           dem26=D26,govtot26=v26[k]['all'],rep26=v26[k]['rep'],ballots26=B26,demreg26=DR26,totreg26=TR26,
           dem_chg=D26-D22,ballots_chg=B26-B22,demreg_chg=DR26-DR22,totreg_chg=TR26-TR22)
    o['S22']=pct(D22,B22); o['S26']=pct(D26,B26); o['R22']=pct(DR22,TR22); o['R26']=pct(DR26,TR26)
    o['G22']=Fraction(100*(D22*TR22-DR22*B22),B22*TR22); o['G26']=Fraction(100*(D26*TR26-DR26*B26),B26*TR26)
    o['dG']=(o['S26']-o['S22'])-(o['R26']-o['R22'])
    o['drop']=o['R22']-o['R26']
    o['resid_regloss']=o['S26']-o['S22']          # algebraically = dG - drop
    o['implied_regloss']=Fraction(D26)-o['S22']*B26/100   # NC form: D2026 - S2022 x ballots2026
    o['dem_chg_pct']=pct(D26-D22,D22); o['ballots_chg_pct']=pct(B26-B22,B22); o['demreg_chg_pct']=pct(DR26-DR22,DR22)
    o['DR_over_ballots22']=Fraction(D22+v22[k]['rep'],B22); o['DR_over_ballots26']=Fraction(D26+v26[k]['rep'],B26)
    o['gov_over_ballots22']=Fraction(v22[k]['all'],B22); o['gov_over_ballots26']=Fraction(v26[k]['all'],B26)
    out[k]=o
# regression via normal equations (different formula from pass 1)
n=len(K); X=[out[k]['drop'] for k in K]; Y=[out[k]['dG'] for k in K]
sx=sum(X); sy=sum(Y); sxx=sum(x*x for x in X); sxy=sum(x*y for x,y in zip(X,Y)); syy=sum(y*y for y in Y)
m=(n*sxy-sx*sy)/(n*sxx-sx*sx); c=(sy-m*sx)/n
ssr=sum((y-(c+m*x))**2 for x,y in zip(X,Y)); sst=syy-sy*sy/n; R2=1-ssr/sst
for k in K:
    out[k]['fit_pred']=c+m*out[k]['drop']; out[k]['fit_resid']=out[k]['dG']-out[k]['fit_pred']; out[k]['implied_fit']=out[k]['fit_resid']*out[k]['ballots26']/100
# surplus form via normal equations (n*Sxy - Sx*Sy)/(n*Sxx - Sx^2), R2 = 1 - SSE/SST
sf={}
for yr in ('22','26'):
    D=[Fraction(out[k]['demreg'+yr],out[k]['totreg'+yr]) for k in K]          # D/100 directly as a ratio
    Sv=[out[k]['G'+yr] for k in K]
    a1=sum(D); a2=sum(Sv); a11=sum(d*d for d in D); a12=sum(d*v for d,v in zip(D,Sv)); a22=sum(v*v for v in Sv)
    mm=(n*a12-a1*a2)/(n*a11-a1*a1); bb=(a2-mm*a1)/n
    res=[v-(mm*d+bb) for d,v in zip(D,Sv)]
    for k,r in zip(K,res): out[k]['sfit_res'+yr]=r; out[k]['sfit_pred'+yr]=out[k]['G'+yr]-r
    sse=sum(r*r for r in res); sst=a22-a2*a2/n
    sf[yr]=dict(n=n,multiplier=mm,offset=bb,R2=1-sse/sst,mean_abs_resid=sum(abs(r) for r in res)/n,sxx=a11-a1*a1/n,sse=sse)
ser=lambda v: f'{v.numerator}/{v.denominator}' if isinstance(v,Fraction) else v
json.dump(dict(counties={k:{a:ser(b) for a,b in v.items()} for k,v in out.items()},fit=dict(n=n,constant=ser(c),multiplier=ser(m),R2=ser(R2)),surplus_fit={y:{a:ser(b) for a,b in d.items()} for y,d in sf.items()},
               reported=dict(total22=total22,st_reg22=st_reg22,st_reg26=st_reg26,st_bal22=st_bal22,st_bal26=st_bal26),pipe_status=sorted(status),
               status26={k:v for k,v in status26.items()}),open('/workspace/florida/data/pass2.json','w'),indent=1)
print('PASS2 counties',n,'pipe status',status,'fit',float(c),float(m),float(R2))
