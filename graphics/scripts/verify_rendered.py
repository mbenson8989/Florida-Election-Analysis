# Independent check: every number drawn on each flip card vs values recomputed from the CSV's own derived columns
import csv,json,re
from decimal import Decimal as D, ROUND_HALF_EVEN
rows={r['county']:r for r in csv.DictReader(l for l in open('../../data/florida_governor_2022_2026_by_county.csv') if not l.lstrip('"').startswith('#'))}
del rows['STATEWIDE']
rank=sorted(rows,key=lambda k:D(rows[k]['delta_G']),reverse=True)[:10]
q=lambda x:str(D(x).quantize(D('0.01'),ROUND_HALF_EVEN)); sg=lambda x:('+' if D(x)>=0 else '')+q(x)
R=json.load(open('flip_rendered_values.json')); checks=0; bad=[]
for n,c in enumerate(rank,1):
    r=rows[c]; fn=f"FL_Flip_{n:02d}_{c.replace(' ','_')}.png"; text=" | ".join(R[fn])
    assert int(r['dem_reg_change'])<0 and int(r['dem_votes_change'])>0
    exp=[c.upper(),f"#{n} ".replace("#","# ")+"",f"DOWN {-int(r['dem_reg_change']):,}",f"2022: {int(r['dem_reg_2022']):,}",f"2026: {int(r['dem_reg_2026']):,}",
     f"{q(r['dem_reg_share_2022_pct'])}% → {q(r['dem_reg_share_2026_pct'])}%",f"(−{q(r['reg_share_drop'])} pts)",
     f"UP {int(r['dem_votes_change']):,}",f"2022: {int(r['dem_gov_votes_2022']):,}",f"2026: {int(r['dem_gov_votes_2026']):,}",
     f"{q(r['dem_share_of_ballots_2022_pct'])}% → {q(r['dem_share_of_ballots_2026_pct'])}%",
     f"(+{q(D(r['dem_share_of_ballots_2026_pct'])-D(r['dem_share_of_ballots_2022_pct']))} pts)",
     f"{sg(r['delta_G'])} PTS",f"Surplus G 2022: {sg(r['G_2022'])}",f"Surplus G 2026: {sg(r['G_2026'])}",
     f"Implied extra votes: +{int(D(r['implied_extra_votes_regloss']).quantize(D(1),ROUND_HALF_EVEN)):,}"]
    exp[1]=f"F L I P   # {n}   O F   6 7"
    for e in exp:
        checks+=1
        if e not in text: bad.append((fn,e))
    # every numeric token on card must be in expected set
    nums=set(re.findall(r'\d[\d,]*\.?\d*',text)); allowed=set(re.findall(r'\d[\d,]*\.?\d*'," ".join(exp)))|{'2022','2026','67'}
    extra=nums-allowed
    if extra: bad.append((fn,'unexpected',extra))
print("checks",checks,"mismatches",len(bad),bad)
