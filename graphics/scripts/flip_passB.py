# Pass B: independent Decimal(60) computation, different code path; also checks CSV derived columns
import csv, json
from decimal import Decimal as Dc, getcontext, ROUND_HALF_EVEN
getcontext().prec=60
L=list(csv.reader(l for l in open('../../data/florida_governor_2022_2026_by_county.csv') if not l.lstrip('"').startswith('#')))
h=L[0]; idx={k:j for j,k in enumerate(h)}
res=[]
for row in L[1:]:
    if row[0]=='STATEWIDE': continue
    g=lambda k:Dc(row[idx[k]])
    d22=g('dem_reg_2022')/g('total_reg_2022')*100; d26=g('dem_reg_2026')/g('total_reg_2026')*100
    v22=g('dem_gov_votes_2022')/g('ballots_cast_2022')*100; v26=g('dem_gov_votes_2026')/g('ballots_cast_2026')*100
    dg=(v26-d26)-(v22-d22)
    # cross-check CSV derived cols to 15 dp
    for mine,col in [(d22,'dem_reg_share_2022_pct'),(d26,'dem_reg_share_2026_pct'),(dg,'delta_G'),(d22-d26,'reg_share_drop')]:
        assert abs(mine-g(col))<Dc('1e-15'),(row[0],col)
    imp=(dg-(d22-d26))*g('ballots_cast_2026')/100
    assert abs(imp-g('implied_extra_votes_regloss'))<Dc('1e-12')
    q=lambda x:x.quantize(Dc('0.01'),ROUND_HALF_EVEN)
    res.append((dg,dict(county=row[0],D22=str(q(d22)),D26=str(q(d26)),drop_pts=str(q(d22-d26)),
      reg22=int(row[idx['dem_reg_2022']]),reg26=int(row[idx['dem_reg_2026']]),reg_chg=int(row[idx['dem_reg_change']]),
      V22=str(q(v22)),V26=str(q(v26)),V_gain=str(q(v26-v22)),
      votes22=int(row[idx['dem_gov_votes_2022']]),votes26=int(row[idx['dem_gov_votes_2026']]),votes_chg=int(row[idx['dem_votes_change']]),
      G22=f"{q(v22-d22):+}",G26=f"{q(v26-d26):+}",dG=f"{q(dg):+}",implied=int(imp.quantize(Dc(1),ROUND_HALF_EVEN)))))
assert len(res)==67
res.sort(key=lambda t:t[0],reverse=True)
out=[]
for n,(k,d) in enumerate(res,1): d['rank']=n; out.append(d)
json.dump(out,open('flip_passB.json','w'),indent=1)
