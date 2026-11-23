# Pass A: exact rationals from raw count columns
import csv, json
from fractions import Fraction as Fr
rows=[r for r in csv.DictReader(l for l in open('../../data/florida_governor_2022_2026_by_county.csv') if not l.lstrip('"').startswith('#')) if r['county']!='STATEWIDE']
assert len(rows)==67
out=[]
for r in rows:
    i=lambda k:int(r[k])
    D22=Fr(100*i('dem_reg_2022'),i('total_reg_2022')); D26=Fr(100*i('dem_reg_2026'),i('total_reg_2026'))
    V22=Fr(100*i('dem_gov_votes_2022'),i('ballots_cast_2022')); V26=Fr(100*i('dem_gov_votes_2026'),i('ballots_cast_2026'))
    G22=V22-D22; G26=V26-D26; dG=G26-G22; drop=D22-D26
    imp=(dG-drop)*i('ballots_cast_2026')/100
    out.append(dict(county=r['county'],D22=f"{float(D22):.2f}",D26=f"{float(D26):.2f}",drop_pts=f"{float(drop):.2f}",
      reg22=i('dem_reg_2022'),reg26=i('dem_reg_2026'),reg_chg=i('dem_reg_2026')-i('dem_reg_2022'),
      V22=f"{float(V22):.2f}",V26=f"{float(V26):.2f}",V_gain=f"{float(V26-V22):.2f}",
      votes22=i('dem_gov_votes_2022'),votes26=i('dem_gov_votes_2026'),votes_chg=i('dem_gov_votes_2026')-i('dem_gov_votes_2022'),
      G22=f"{float(G22):+.2f}",G26=f"{float(G26):+.2f}",dG=f"{float(dG):+.2f}",implied=round(imp),_k=dG))
out.sort(key=lambda d:-d['_k'])
for n,d in enumerate(out,1): d['rank']=n; d.pop('_k')
json.dump(out,open('flip_passA.json','w'),indent=1)
