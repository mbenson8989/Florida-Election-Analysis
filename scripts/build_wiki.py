import pickle, json
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec=50
B=pickle.load(open('/workspace/florida/data/build_state.pkl','rb'))
C,st,S,FIT,BUILT=B['C'],B['st'],B['S'],B['FIT'],B['BUILT']
SF=B['SF']; SFS=B['SFS']
c,m,R2,n=FIT['constant'],FIT['multiplier'],FIT['R2'],FIT['n']
def dec(x): x=F(x); return Decimal(x.numerator)/Decimal(x.denominator)
def rnd(x,nd): return dec(x).quantize(Decimal(1).scaleb(-nd),rounding=ROUND_HALF_UP)
def p(x,nd=2): return f'{rnd(x,nd):.{nd}f}'
def sg(x,nd=2): v=rnd(x,nd); return ('+' if v>0 else '−' if v<0 else '')+f'{abs(v):.{nd}f}'
def ci(x): return f'{x:,}'
def sci(x): return ('+' if x>0 else '−' if x<0 else '')+f'{abs(x):,}'
def iv(x): v=rnd(x,0); return ('+' if v>0 else '−' if v<0 else '')+f'{abs(int(v)):,}'
REPO='https://github.com/mbenson8989/Florida-Election-Analysis'; WIKI=REPO+'/wiki'; RAWU='https://raw.githubusercontent.com/mbenson8989/Florida-Election-Analysis/main'
CEDAR='https://github.com/mbenson8989/Nebraska-Election-Analysis-/wiki/Cedar-Audit'
SUBSTACK='https://moebenson.substack.com/p/the-burden-just-flipped'
PDFU=RAWU+'/pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf'
rows=list(C.values()); by_dG=sorted(rows,key=lambda r:r['dG']); ceiling=by_dG[::-1][:5]; floorG=by_dG[:5]
by_size=sorted(rows,key=lambda r:(-r['ballots26'],r['county'])); floor_base=sorted(rows,key=lambda r:r['R22'])[:5]; ceil_base=sorted(rows,key=lambda r:-r['R22'])[:5]
fr=sorted(rows,key=lambda r:r['fit_resid']); median=B['median']; mean=B['mean']
imp_total=B['imp_total']; imp_fit_total=B['imp_fit_total']; imp_fit_pos=B['imp_fit_pos']
se_c,se_m,t=B['se_c'],B['se_m'],B['t975']
BANNER=("> **\*2026 figures are UNOFFICIAL.** They are the Florida Division of Elections (DOS) Florida Election Watch county returns for the Nov 3, 2026 general election. 2022 figures are DOS official results.\n>\n"
        "> **Race: Governor.** 2022: Charlie Crist (D) vs. Ron DeSantis (R); 2026: David Jolly (D) vs. Byron Donalds (R). Votes are votes for the Democratic governor ticket, not a count of registered Democrats who voted. Registration is the DOS book-closing count of active registered voters by party (Oct 11, 2022; Oct 5, 2026). Ballots cast are the DOS county voter-turnout figures. These pages measure a pattern; they make no claim about intent, fraud or cause.\n")
NAV=[('Home','Home'),('README','README'),('Floor and Ceiling','Floor-and-Ceiling'),('Reverse Math','Reverse-Math'),('Graphs','Graphs'),('Florida County PDF Information','Florida-County-PDF-Information'),('Locked Florida Formula','Locked-Florida-Formula')]
def rel(skip):
    return '\n---\n**Related:** '+' · '.join(f'[{a}]({WIKI}/{b})' for a,b in NAV if b!=skip)+f' · [Cedar County Audit (Nebraska)]({CEDAR})\n'
pages={}
# ---------- Sidebar
pages['_Sidebar.md']=f"""**Florida Election Analysis**

Governor 2022 vs 2026. *2026 figures are unofficial.

1. [Home]({WIKI}/Home)
2. [README: start here]({WIKI}/README)
3. [Cedar County Audit (Nebraska)]({CEDAR})
4. [Floor and Ceiling]({WIKI}/Floor-and-Ceiling)
5. [Reverse Math]({WIKI}/Reverse-Math)
6. [Graphs]({WIKI}/Graphs)
7. [Florida County PDF Information]({WIKI}/Florida-County-PDF-Information) · **[Open the county PDF]({PDFU})**
8. [Locked Florida Formula]({WIKI}/Locked-Florida-Formula)

[Data, scripts and verification log]({REPO})
"""
lc=len([r for r in rows if r['loss']])
st_fit=c+m*st['drop']
# ---------- Home
pages['Home.md']=f"""# Florida 2022 vs 2026 Governor Race: ΔG Method

**Version 1, built {BUILT}. DRAFT, held for approval; not published.**

{BANNER}
Method developed by Morissa Benson. It began with the **[Cedar County Audit]({CEDAR})** in Nebraska: a small county where Democratic governor votes rose while Democratic registration fell. This wiki applies the same county-by-county arithmetic to all 67 Florida counties using Florida Division of Elections (DOS) numbers only. Florida has party registration, so the baseline is the Democratic share of registered voters; no workaround is needed. The Florida constant is computed from Florida data only; no other state's constant is reused.

## Contents

1. [README]({WIKI}/README): a plain-language guide for first-time readers
2. [Cedar County Audit]({CEDAR}) (Nebraska wiki): where the method began
3. [Floor and Ceiling]({WIKI}/Floor-and-Ceiling): floor and ceiling counties and the Texas-style over-ballot check
4. [Reverse Math]({WIKI}/Reverse-Math): the largest county, then the ten largest, then all 67 counties, solved backward for implied extra votes
5. [Graphs]({WIKI}/Graphs): surplus-form fits, ΔG by county, slope chart, residual bars, over-ballot check
6. [Florida County PDF Information]({WIKI}/Florida-County-PDF-Information): all 67 counties in one downloadable PDF (registration, votes and ballots, 2022 vs 2026)
7. [Locked Florida Formula]({WIKI}/Locked-Florida-Formula): the surplus-form equation S = m × (D/100) + b for 2022 and 2026, a fill-in worksheet and a worked example

## Statewide at a glance

| Measure | 2022 (official) | 2026* (unofficial) | Change |
|---|---|---|---|
| Democratic registration (DOS book closing) | {ci(S['demreg22'])} | {ci(S['demreg26'])} | {sci(st['demreg_chg'])} ({sg(st['demreg_chg_pct'])}%) |
| Total active registration | {ci(S['totreg22'])} | {ci(S['totreg26'])} | {sci(st['totreg_chg'])} ({sg(st['totreg_chg_pct'])}%) |
| Democratic governor votes (Crist 2022, Jolly 2026) | {ci(S['dem22'])} | {ci(S['dem26'])} | {sci(st['dem_chg'])} ({sg(st['dem_chg_pct'])}%) |
| Republican governor votes (DeSantis 2022, Donalds 2026) | {ci(S['rep22'])} | {ci(S['rep26'])} | {sci(st['rep_chg'])} |
| All governor votes | {ci(S['govtot22'])} | {ci(S['govtot26'])} | {sci(S['govtot26']-S['govtot22'])} |
| Total ballots cast (DOS county turnout) | {ci(S['ballots22'])} | {ci(S['ballots26'])} | {sci(st['ballots_chg'])} ({sg(st['ballots_chg_pct'])}%) |
| **S** = Dem votes ÷ ballots cast | {p(st['S22'])}% | {p(st['S26'])}% | {sg(st['S26']-st['S22'])} pts |
| **R** = Dem registration share | {p(st['R22'])}% | {p(st['R26'])}% | {sg(st['R26']-st['R22'])} pts |
| **G** = S − R | {sg(st['G22'])} | {sg(st['G26'])} | **ΔG {sg(st['dG'])}** |

## Key findings

- **ΔG is positive in all 67 counties**, from {sg(by_dG[0]['dG'])} ({by_dG[0]['county']}) to {sg(by_dG[-1]['dG'])} ({by_dG[-1]['county']}); county median {sg(median)}, mean {sg(mean)}.
- **Democratic registration share fell in all 67 counties**, and the Democratic registration **count** fell in {lc} of 67 (no non-loss counties).
- **Locked Florida formula (surplus form, FL data only):** 2022: S = {p(SF['22']['multiplier'],2)} × (D/100) + {p(SF['22']['offset'],2)} (R² = {p(SF['22']['R2'],3)}); 2026: S = {p(SF['26']['multiplier'],2)} × (D/100) + {p(SF['26']['offset'],2)} (R² = {p(SF['26']['R2'],3)}). Both are weak fits; see [Locked Florida Formula]({WIKI}/Locked-Florida-Formula).\n- **Descriptive ΔG trend (not the locked formula):** across counties, ΔG rises with the registration-share drop: ΔG ≈ {p(c)} + {p(m,3)} × drop (R² = {p(R2,3)}).
- **Ceiling (highest ΔG):** {', '.join(f"{r['county']} {sg(r['dG'])}" for r in ceiling)}. **Floor (lowest ΔG):** {', '.join(f"{r['county']} {sg(r['dG'])}" for r in floorG)}.
- **Baseline floor (most Republican registration, lowest 2022 Dem registration share):** {', '.join(f"{r['county']} {p(r['R22'])}%" for r in floor_base)}.
- **Solved backward (hypothesis):** the registration-loss residuals add up to **{iv(imp_total)} implied extra votes** across the {lc} loss counties ({iv(st['implied_pooled'])} on the pooled statewide numbers). These are the votes a hypothesis of added or switched votes would have to account for, not votes shown to be improper.
- **Over-ballot checks:** counties where Democratic governor votes, Democratic + Republican votes, or all governor votes exceed ballots cast: **2022: 0; 2026: 0.**

## Verification

Every figure for all 67 counties was computed in **two independent passes** from the raw DOS files, with separately written code and different parsers and, where DOS publishes the same numbers twice, different source documents (2022 votes: tab extract vs. county detail report; 2026 votes: tab results file vs. pipe-delimited files; 2022 registration: party-by-county PDF vs. party-by-race PDF; 2026 registration: Excel vs. PDF). Every value was compared as an exact fraction: **2,479 county-figure checks (67 counties × 37 fields) plus 4 fit checks, 0 mismatches.** County sums match all 16 DOS statewide totals checked, and the 2026 county votes match the Election Watch by-county page in all 134 checks. Log: [VERIFY_LOG.txt]({REPO}/blob/main/VERIFY_LOG.txt).

## Read this before using the numbers

- **A residual is not evidence of altered votes.** Candidate choice, crossover voting by Republicans and NPA voters, turnout differences, and registration-list maintenance all move these numbers. The arithmetic cannot separate them.
- **Total active registration also fell** ({sci(st['totreg_chg'])} statewide; lower in {sum(1 for r in rows if r['totreg_chg']<0)} of 67 counties) between the two book closings, so registration changes partly reflect voter-list maintenance, not only voters leaving the party.
- **2026 is unofficial.** 2026 figures are the Florida Election Watch county returns (see the note at the top). If DOS posts corrected or certified returns, the pipeline in the repository rebuilds every number.

## Sources

| Data | Source |
|---|---|
| 2022 governor results by county (official) | DOS results.elections.myflorida.com: ResultsExtract (tab) and DetailRpt (Governor), Nov 8, 2022 General |
| 2026 governor results by county (unofficial*) | DOS Florida Election Watch downloads: 20261103_ElecResultsFL.txt and pipe-delimited Info/Votes files; ContestResultsByCounty/160000 |
| 2022 ballots cast | DOS TurnoutRpt, Nov 8, 2022 General (official) |
| 2026 ballots cast | DOS Florida Election Watch County Reporting Status, "Voter Turnout" |
| 2022 registration by party | DOS book closing Oct 11, 2022: party by county (PDF) and party by county by race (PDF) |
| 2026 registration by party | DOS book closing Oct 5, 2026: party by county (Excel and PDF) |

Full list with URLs, download times and SHA-256 hashes: [MANIFEST.md]({REPO}/blob/main/MANIFEST.md).
{rel('Home')}"""
# ---------- Reverse Math
big=by_size[0]
def line(r): return f"| {r['county']} | {ci(r['ballots26'])} | {ci(r['demreg22'])} → {ci(r['demreg26'])} | {ci(r['dem22'])} → {ci(r['dem26'])} | {ci(r['ballots22'])} → {ci(r['ballots26'])} | {p(r['S22'])}% → {p(r['S26'])}% | {p(r['R22'])}% → {p(r['R26'])}% | {sg(r['dG'])} | {sg(r['resid_regloss'])} | {iv(r['implied_regloss'])} |"
HDR="| County | Ballots 2026 | Dem reg 2022 → 2026 | Dem gov votes 2022 → 2026 | Ballots 2022 → 2026 | S 2022 → 2026 | R 2022 → 2026 | ΔG | Residual | Implied extra votes |\n|---|---|---|---|---|---|---|---|---|---|"
def grp(rs):
    d22=sum(r['dem22'] for r in rs); d26=sum(r['dem26'] for r in rs); b22=sum(r['ballots22'] for r in rs); b26=sum(r['ballots26'] for r in rs)
    g22=sum(r['demreg22'] for r in rs); g26=sum(r['demreg26'] for r in rs); t22=sum(r['totreg22'] for r in rs); t26=sum(r['totreg26'] for r in rs)
    S22=F(100*d22,b22); S26=F(100*d26,b26); R22=F(100*g22,t22); R26=F(100*g26,t26); dG=(S26-S22)-(R26-R22)
    return S22,S26,R22,R26,dG,sum(r['dG'] for r in rs)/len(rs),min(r['dG'] for r in rs),max(r['dG'] for r in rs),sum(r['implied_regloss'] for r in rs if r['loss']),sum(1 for r in rs if r['loss'])
def gline(name,rs):
    S22,S26,R22,R26,dG,mn,lo,hi,imp,nl=grp(rs)
    return f"| {name} | {len(rs)} | {p(S22)}% → {p(S26)}% | {p(R22)}% → {p(R26)}% | {sg(S26-S22)} | {sg(R26-R22)} | {sg(dG)} | {sg(mn)} ({sg(lo)} to {sg(hi)}) | {iv(imp)} ({nl} loss counties) |"
pages['Reverse-Math.md']=f"""# Reverse Math

{BANNER}
The same arithmetic at three levels, from one county up to the whole state. Denominator: total ballots cast (DOS county turnout). Counties are ordered by 2026 ballots cast, largest first (DOS data only; no outside population source is used).

## Step 1: {big['county']} County (largest by ballots cast)

| Step | Value |
|---|---|
| Democratic vote share (S) | {p(big['S22'])}% (2022) → {p(big['S26'])}% (2026): **{sg(big['S26']-big['S22'])} points** |
| Democratic registration share (R) | {p(big['R22'])}% → {p(big['R26'])}%: **{sg(big['R26']-big['R22'])} points** |
| ΔG = vote-share growth − registration-share change | {p(big['S26']-big['S22'])} − ({sg(big['R26']-big['R22'])}) = **{sg(big['dG'])} points** |
| Reverse step: ΔG − registration-share loss | {p(big['dG'])} − {p(big['drop'])} = **{p(big['resid_regloss'])}** (the residual) |
| Solved backward: implied extra votes | {ci(big['dem26'])} − {p(big['S22'],4)}% × {ci(big['ballots26'])} = **about {iv(big['implied_regloss'])}** |

## Step 2: the ten largest counties

{HDR}
""" + '\n'.join(line(r) for r in by_size[:10]) + f"""

## Step 3: all 67 counties

| Group | Counties | Pooled S | Pooled R | Vote-share growth | Reg-share change | Pooled ΔG | County mean ΔG (range) | Implied extra votes |
|---|---|---|---|---|---|---|---|---|
{gline('Ten largest counties',by_size[:10])}
{gline('Other 57 counties',by_size[10:])}
{gline('All 67 counties',rows)}

ΔG is positive in all 67 counties; Democratic registration share fell in all 67, and the Democratic registration count fell in all 67, so every county runs the residual step. The residual (ΔG − registration-share drop) equals the vote-share growth S2026 − S2022; it is positive in {sum(r['resid_regloss']>0 for r in rows)} of 67 counties.

### All 67 counties, largest to smallest (2026 ballots cast)

{HDR}
""" + '\n'.join(line(r) for r in by_size) + f"""

Implied extra votes = residual × 2026 ballots ÷ 100 = D2026 − S2022 × ballots2026, computed from unrounded values and rounded to whole votes for display. Statewide total across the 67 loss counties: **{iv(imp_total)}** (exact {p(imp_total,6)}).
{rel('Reverse-Math')}"""
# ---------- Locked formula (surplus form only)
SF=B['SF']; SFS=B['SFS']
def sfrow(y,yy):
    d=SF[y]; q=SFS[y]
    return f"| {yy} | {n} | **S = {p(d['multiplier'],2)} × (D/100) {'+' if d['offset']>=0 else '−'} {p(abs(d['offset']),2)}** | {p(d['multiplier'],6)} ({q['se_multiplier']:.2f}) | {q['ci_multiplier'][0]:+.2f} to {q['ci_multiplier'][1]:+.2f} | {q['p_value']:.3f} | {p(d['offset'],6)} ({q['se_offset']:.2f}) | {p(d['R2'],6)} | {p(d['mean_abs_resid'],6)} | {q['resid_sd']:.2f} | {q['max_resid_county']} ({sg(F(q['max_resid']))}) |"
w=sorted(rows,key=lambda r:(-r['ballots26'],r['county']))[0]
def lrow(r): return f"| {r['county']} | {p(r['R22'])} | {sg(r['G22'])} | {sg(r['sfit_pred22'])} | {sg(r['sfit_res22'])} | {p(r['R26'])} | {sg(r['G26'])} | {sg(r['sfit_pred26'])} | {sg(r['sfit_res26'])} |"
s22=SF['22']; s26=SF['26']
pages['Locked-Florida-Formula.md']=f"""# Locked Florida Formula

{BANNER}
## Florida's equation in final form

### Surplus Equation (Florida, fitted from Florida's own 67 counties)

**2022: S = {p(s22['multiplier'],2)} × (D/100) {'+' if s22['offset']>=0 else '−'} {p(abs(s22['offset']),2)}**

**2026: S = {p(s26['multiplier'],2)} × (D/100) {'+' if s26['offset']>=0 else '−'} {p(abs(s26['offset']),2)}**

Where:
- S = Surplus, in percentage points: Democratic governor votes ÷ total ballots cast × 100, minus D
- D = Democratic registration share, as a percent of total active registration (0–100 scale, DOS book closing), not a headcount of registered Democrats
- m = Multiplier coefficient (the first number): how much S changes per 100 points of D, i.e. per one whole unit of D/100
- b = Constant offset (the second number), in percentage points: the S the line gives at D = 0

Each state fits its own multiplier and offset by graphing that state's counties. These are ordinary least squares fits, each of the 67 counties weighted equally, fitted separately for each year (the statewide total row is not part of the fit). No other state's numbers are used.

| Year | Counties | Equation | Multiplier m (SE) | 95% CI for m | p-value for m | Offset b (SE) | R² | Mean absolute residual (pts) | Residual SD (pts) | Largest residual |
|---|---|---|---|---|---|---|---|---|---|---|
{sfrow('22','2022 (official)')}
{sfrow('26','2026* (unofficial)')}

Exact values (from exact fractions of the raw counts): 2022 m = {p(s22['multiplier'],15)}, b = {p(s22['offset'],15)}, R² = {p(s22['R2'],15)}; 2026 m = {p(s26['multiplier'],15)}, b = {p(s26['offset'],15)}, R² = {p(s26['R2'],15)}.

## Is the fit tight enough to lock?

**Plain verdict: no, not as a predictive constant.** The numbers above are Florida's correctly fitted surplus-form values, and they are verified to the decimal, but registration share explains very little of the county-to-county surplus in Florida:

- **R² is {p(s22['R2'],3)} in 2022 and {p(s26['R2'],3)} in 2026.** D explains about {p(100*s22['R2'],0)}% and {p(100*s26['R2'],0)}% of the spread in S.
- **The typical miss is large:** the average county sits {p(s22['mean_abs_resid'],2)} points (2022) and {p(s26['mean_abs_resid'],2)} points (2026) off the line; the largest misses are {SFS['22']['max_resid_county']} ({sg(F(SFS['22']['max_resid']))}, 2022) and {SFS['26']['max_resid_county']} ({sg(F(SFS['26']['max_resid']))}, 2026).
- **The multiplier is not stable.** In 2022 it is negative and not distinguishable from zero (p = {SFS['22']['p_value']:.2f}; 95% CI {SFS['22']['ci_multiplier'][0]:+.1f} to {SFS['22']['ci_multiplier'][1]:+.1f}). In 2026 it is positive (p = {SFS['26']['p_value']:.3f}; 95% CI {SFS['26']['ci_multiplier'][0]:+.1f} to {SFS['26']['ci_multiplier'][1]:+.1f}). The sign flips between the two years.
- **Compared with the other state wikis:** surplus-form R² was 0.880 / 0.808 in South Carolina and 0.65 / 0.63 in Texas (both use a primary-vote proxy because they have no party registration), 0.304 / 0.681 in Kansas, and 0.15 / 0.04 in North Carolina (2022 / 2026), where the North Carolina page also called the forward fit too weak to be a stable constant. Florida sits at the North Carolina end. The Pennsylvania page publishes no surplus-form fit. Florida's descriptive ΔG-versus-registration-drop relationship (on other pages, not part of this formula) is much tighter, R² {p(R2,4)}.

Use the equations to place a county against Florida's own line, not to predict a county's surplus.

## The worksheet (surplus terms)

| Line | Item | 2022 | 2026 |
|---|---|---|---|
| 1 | Democratic governor votes | ______ | ______ |
| 2 | Total ballots cast (DOS county turnout) | ______ | ______ |
| 3 | Democratic share of ballots = line 1 ÷ line 2 × 100 | ______ | ______ |
| 4 | Democratic registered voters (DOS book closing) | ______ | ______ |
| 5 | Total active registered voters, all parties (same report) | ______ | ______ |
| 6 | D = line 4 ÷ line 5 × 100 | ______ | ______ |
| 7 | S (surplus) = line 3 − line 6 | ______ | ______ |
| 8 | Fitted S = m × (line 6 ÷ 100) + b (2022: m {p(s22['multiplier'],2)}, b {p(s22['offset'],2)}; 2026: m {p(s26['multiplier'],2)}, b {p(s26['offset'],2)}) | ______ | ______ |
| 9 | Residual = line 7 − line 8 (above the line if positive) | ______ | ______ |

## Worked example: {w['county']} (largest county by ballots cast)

| Line | Item | 2022 | 2026 |
|---|---|---|---|
| 1 | Democratic governor votes | {ci(w['dem22'])} | {ci(w['dem26'])} |
| 2 | Total ballots cast | {ci(w['ballots22'])} | {ci(w['ballots26'])} |
| 3 | Democratic share of ballots | {p(w['S22'])} | {p(w['S26'])} |
| 4 | Democratic registered | {ci(w['demreg22'])} | {ci(w['demreg26'])} |
| 5 | Total registered | {ci(w['totreg22'])} | {ci(w['totreg26'])} |
| 6 | D | {p(w['R22'])} | {p(w['R26'])} |
| 7 | S | {sg(w['G22'])} | {sg(w['G26'])} |
| 8 | Fitted S | {sg(w['sfit_pred22'])} | {sg(w['sfit_pred26'])} |
| 9 | Residual | {sg(w['sfit_res22'])} | {sg(w['sfit_res26'])} |

Computed at full precision, then rounded for display.

## All 67 counties against the line

Largest to smallest by 2026 ballots cast.

| County | D 2022 | S 2022 | Fitted S 2022 | Residual 2022 | D 2026 | S 2026 | Fitted S 2026 | Residual 2026 |
|---|---|---|---|---|---|---|---|---|
""" + '\n'.join(lrow(r) for r in sorted(rows,key=lambda r:(-r['ballots26'],r['county']))) + f"""

## Rules for using this formula

1. **Use Florida's own line.** The starting point is different in every state; compare Florida counties with Florida's equation and range, not another state's.
2. **Read the residual, not the prediction.** With R² this low, the line says where a typical Florida county sits; the residual says how far a county sits from it.
3. **Always pull out the ceiling and floor counties** (see [Floor and Ceiling]({WIKI}/Floor-and-Ceiling)).

![Surplus form 2022]({RAWU}/charts/FL_Surplus_S_vs_D_2022.png)

![Surplus form 2026]({RAWU}/charts/FL_Surplus_S_vs_D_2026.png)

*S against D for all 67 counties, with the fitted line for each year. Residual bars for each year are on [Graphs]({WIKI}/Graphs).*
{rel('Locked-Florida-Formula')}"""

# ---------- Floor and ceiling
def fcl(r,g): return f"| {r['county']} | {g} | {ci(r['ballots26'])} | {sg(r['G22'])} | {sg(r['G26'])} | {sg(r['dG'])} | {p(r['R22'])}% → {p(r['R26'])}% | {ci(r['demreg22'])} → {ci(r['demreg26'])} ({sg(r['demreg_chg_pct'],1)}%) | {ci(r['dem22'])} → {ci(r['dem26'])} | {sg(r['fit_resid'])} | {iv(r['implied_regloss'])} |"
fc=[(r,'Ceiling') for r in ceiling]+[(r,'Floor (ΔG)') for r in floorG]
for r in floor_base:
    if r not in floorG: fc.append((r,'Baseline floor'))
fc=sorted(fc,key=lambda x:-x[0]['ballots26'])
def ob(y):
    g=max(rows,key=lambda r:r[f'gov_over_ballots{y}']); dr=max(rows,key=lambda r:r[f'DR_over_ballots{y}']); dm=max(rows,key=lambda r:F(r[f'dem{y}'],r[f'ballots{y}']))
    cnt=lambda f: sum(1 for r in rows if f(r))
    return (cnt(lambda r:r[f'dem{y}']>r[f'ballots{y}']),cnt(lambda r:r[f'dem{y}']+r[f'rep{y}']>r[f'ballots{y}']),cnt(lambda r:r[f'govtot{y}']>r[f'ballots{y}']),
            f"{p(100*dr[f'DR_over_ballots{y}'])}% ({dr['county']})",f"{p(100*g[f'gov_over_ballots{y}'])}% ({g['county']})",f"{p(100*F(dm[f'dem{y}'],dm[f'ballots{y}']))}% ({dm['county']})")
o22,o26=ob('22'),ob('26')
top5_26=sorted(rows,key=lambda r:-r['DR_over_ballots26'])[:5]
pages['Floor-and-Ceiling.md']=f"""# Floor and Ceiling

{BANNER}
## How to read floor and ceiling counties

- **The ceiling** is the county with the highest ΔG in the state: **{ceiling[0]['county']}, {sg(ceiling[0]['dG'])}**. **Ceiling counties** are the five highest ΔG: {', '.join(f"{r['county']} {sg(r['dG'])}" for r in ceiling)}.
- **The floor** is the county with the lowest ΔG: **{floorG[0]['county']}, {sg(floorG[0]['dG'])}**. **Floor counties by ΔG** (Pennsylvania wiki convention): {', '.join(f"{r['county']} {sg(r['dG'])}" for r in floorG)}. No Florida county has a negative ΔG, so the floor is the smallest rise, not a decline.
- **Baseline floor** (North Carolina wiki convention: most Republican baseline, five lowest 2022 Democratic registration shares): {', '.join(f"{r['county']} {p(r['R22'])}% (ΔG {sg(r['dG'])})" for r in floor_base)}. Nassau is on both floor lists.
- **Baseline ceiling** (highest 2022 Democratic registration share): {', '.join(f"{r['county']} {p(r['R22'])}%" for r in ceil_base)}.
- **Farthest from the descriptive ΔG trend line** (trend residual = actual ΔG − ({p(c)} + {p(m,3)} × drop); descriptive, not the locked formula): lowest **{fr[0]['county']} {sg(fr[0]['fit_resid'])}**, highest **{fr[-1]['county']} {sg(fr[-1]['fit_resid'])}**. Five highest: {', '.join(f"{r['county']} {sg(r['fit_resid'])}" for r in fr[::-1][:5])}. Five lowest: {', '.join(f"{r['county']} {sg(r['fit_resid'])}" for r in fr[:5])}.
- **Non-loss counties:** none. Registered Democrats fell in all 67 counties.
- **Registration fell and votes fell too:** none. Democratic governor votes rose in all 67 counties.
- **Ballots fell, Democratic votes rose** ({sum(1 for r in rows if r['ballots_chg']<0)} counties): {', '.join(r['county'] for r in sorted(rows,key=lambda r:-r['ballots26']) if r['ballots_chg']<0)}.

## Ceiling and floor detail

Largest to smallest by 2026 ballots cast.

| County | Group | Ballots 2026 | G 2022 | G 2026 | ΔG | Dem reg share 2022 → 2026 | Dem reg 2022 → 2026 | Dem gov votes 2022 → 2026 | ΔG trend residual | Implied extra votes |
|---|---|---|---|---|---|---|---|---|---|---|
""" + '\n'.join(fcl(r,g) for r,g in fc) + f"""

**Ceiling profile.** All five ceiling counties began 2022 with a negative G (Democratic vote share of ballots behind Democratic registration share): {', '.join(f"{r['county']} {sg(r['G22'])}" for r in ceiling)}. Liberty and Calhoun have the two largest registration-share drops in the state ({p(C['liberty']['drop'])} and {p(C['calhoun']['drop'])} points) and sit almost on the descriptive ΔG trend line (trend residuals {sg(C['liberty']['fit_resid'])} and {sg(C['calhoun']['fit_resid'])}); Hendry, Hardee and DeSoto sit well above it ({sg(C['hendry']['fit_resid'])}, {sg(C['hardee']['fit_resid'])}, {sg(C['desoto']['fit_resid'])}).

**Floor profile.** The ΔG floor counties are Sumter (central Florida), Charlotte, Citrus and Sarasota (Gulf coast) and Nassau (northeast); all five sit below the descriptive ΔG trend line.

## Texas-style over-ballot check

Any county where governor votes exceed total ballots cast (DOS county turnout).

| Year | Counties checked | Dem votes > ballots | Dem + Rep > ballots | All governor votes > ballots | Highest (D + R) ÷ ballots | Highest all governor votes ÷ ballots | Highest Dem ÷ ballots |
|---|---|---|---|---|---|---|---|
| 2022 (official) | 67 | **{o22[0]}** | **{o22[1]}** | **{o22[2]}** | {o22[3]} | {o22[4]} | {o22[5]} |
| 2026* (unofficial) | 67 | **{o26[0]}** | **{o26[1]}** | **{o26[2]}** | {o26[3]} | {o26[4]} | {o26[5]} |

**No over-ballot anomalies in either year.** Highest five (D + R) ÷ ballots in 2026:

| County | 2022 | 2026 |
|---|---|---|
""" + '\n'.join(f"| {r['county']} | {p(100*r['DR_over_ballots22'])}% | {p(100*r['DR_over_ballots26'])}% |" for r in top5_26) + f"""

![Ceiling and floor on the descriptive ΔG trend]({RAWU}/charts/FL_DeltaG_vs_Registration_Drop_Fit.png)

![ΔG by county]({RAWU}/charts/FL_DeltaG_by_County.png)

*All 67 counties, ΔG lowest to highest. Orange: ceiling (5 highest). Green: floor (5 lowest).*
{rel('Floor-and-Ceiling')}"""
# ---------- Graphs
SF=B['SF']; SFS=B['SFS']
pages['Graphs.md']=f"""# Graphs

{BANNER}
## 1. Locked surplus form, 2022: S vs D with the fitted line

![Surplus form 2022]({RAWU}/charts/FL_Surplus_S_vs_D_2022.png)

*S = {p(SF['22']['multiplier'],2)} × (D/100) + {p(SF['22']['offset'],2)} (R² = {p(SF['22']['R2'],3)}, n = 67). Labels show each county's residual.*

## 2. Locked surplus form, 2026: S vs D with the fitted line

![Surplus form 2026]({RAWU}/charts/FL_Surplus_S_vs_D_2026.png)

*S = {p(SF['26']['multiplier'],2)} × (D/100) + {p(SF['26']['offset'],2)} (R² = {p(SF['26']['R2'],3)}, n = 67).*

## 3. Surplus-form residuals by county

![Surplus residuals 2022]({RAWU}/charts/FL_Surplus_Residuals_2022.png)

*2022: mean absolute residual {p(SF['22']['mean_abs_resid'],2)} points; largest {SFS['22']['max_resid_county']} ({sg(F(SFS['22']['max_resid']))}).*

![Surplus residuals 2026]({RAWU}/charts/FL_Surplus_Residuals_2026.png)

*2026: mean absolute residual {p(SF['26']['mean_abs_resid'],2)} points; largest {SFS['26']['max_resid_county']} ({sg(F(SFS['26']['max_resid']))}).*

## 4. ΔG vs registration-share drop (descriptive)

![ΔG vs drop]({RAWU}/charts/FL_DeltaG_vs_Registration_Drop_Fit.png)

*Descriptive trend line, not the locked formula: ΔG ≈ {p(c)} + {p(m,3)} × drop (R² = {p(R2,3)}). Orange: ceiling (5 highest ΔG); green: floor (5 lowest ΔG).*

## 5. ΔG by county

![ΔG by county]({RAWU}/charts/FL_DeltaG_by_County.png)

*All 67 counties, lowest to highest. Floor {floorG[0]['county']} {sg(floorG[0]['dG'])}; ceiling {ceiling[0]['county']} {sg(ceiling[0]['dG'])}. Red dashed: county median {sg(median)}; black dotted: statewide pooled {sg(st['dG'])}.*

## 6. County slope chart, G 2022 → G 2026

![Slope chart]({RAWU}/charts/FL_Slope_G2022_to_G2026.png)

*Each line is one county. G (the surplus S) rose in 67 of 67 counties.*

## 7. Residual after the registration-loss step

![Residual bars]({RAWU}/charts/FL_Residual_Bars_by_Ballots.png)

*Residual = ΔG − registration-share drop (= change in Democratic share of ballots) for all 67 loss counties, by 2026 ballots cast.*

## 8. Texas-style over-ballot check

![Over-ballot check]({RAWU}/charts/FL_Over_Ballot_Check.png)

*(Democratic + Republican governor votes) ÷ ballots cast, every county, 2022 and 2026. No county reaches 100% (2022: 0, 2026: 0).*
{rel('Graphs')}"""
# ---------- PDF info
SR=B['STATE_ROW']
pages['Florida-County-PDF-Information.md']=f"""# Florida County PDF Information

{BANNER}
This 4-page PDF covers all 67 Florida counties, 2022 vs 2026, governor race. Same layout as the other state wikis: two tables, statewide totals row at the bottom of each. A CSV with every value at full precision accompanies it.

**[Download the Florida 67-County PDF]({RAWU}/pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf)** · [CSV]({RAWU}/data/florida_governor_2022_2026_by_county.csv)

## Sort order

Counties are sorted by **2026 Democratic share of registration** (Democratic active registered voters ÷ all active registered voters, DOS book closing Oct 5, 2026), highest first. {sorted(rows,key=lambda r:-r['R26'])[0]['county']} is first ({p(sorted(rows,key=lambda r:-r['R26'])[0]['R26'])}%); {sorted(rows,key=lambda r:r['R26'])[0]['county']} is last ({p(sorted(rows,key=lambda r:r['R26'])[0]['R26'])}%). The last row of each table is the statewide total.

## Table 1 columns (pages 1–2)

| Column | Meaning |
|---|---|
| County | County name |
| Dem Reg Share 2022 % / 2026 % | Democratic registered ÷ all active registered, DOS book closing Oct 11, 2022 / Oct 5, 2026 |
| Dem Reg 2022 / 2026 | Registered Democrats, same reports |
| Reg Change # / % | 2026 minus 2022, and that change as a percent of 2022 |
| Dem Gov Votes 2022 / 2026 | Votes for the Democratic governor ticket (Crist 2022; Jolly 2026) |
| Vote Change # / % | 2026 minus 2022, and as a percent of 2022 |
| Ballots Cast 2022 / 2026 | Total ballots cast in the county (DOS county turnout) |
| Ballot Change # / % | 2026 minus 2022, and as a percent of 2022 |

## Table 2 columns (pages 3–4)

| Column | Meaning |
|---|---|
| Dem Share of Ballots 2022 % / 2026 % | Democratic governor votes ÷ total ballots cast |
| Change (pts) | 2026 share minus 2022 share, percentage points |
| Dem Reg Share 2022 % / 2026 % | as above, and the point change |
| G 2022 / G 2026 / ΔG | G = Dem share of ballots − Dem registration share; ΔG = G 2026 − G 2022 |
| Total Reg 2022 / 2026 | All active registered voters, all parties |

Percents and point changes are rounded half-up to two decimals from exact values.

## Statewide totals row

| Dem Reg Share 2022 → 2026 | Dem Reg 2022 → 2026 | Reg Change | Dem Gov Votes 2022 → 2026 | Vote Change | Ballots 2022 → 2026 | Ballot Change |
|---|---|---|---|---|---|---|
| {p(st['R22'])}% → {p(st['R26'])}% | {ci(S['demreg22'])} → {ci(S['demreg26'])} | {sci(st['demreg_chg'])} ({sg(st['demreg_chg_pct'])}%) | {ci(S['dem22'])} → {ci(S['dem26'])} | {sci(st['dem_chg'])} ({sg(st['dem_chg_pct'])}%) | {ci(S['ballots22'])} → {ci(S['ballots26'])} | {sci(st['ballots_chg'])} ({sg(st['ballots_chg_pct'])}%) |

## Verification

Every number in the PDF was re-checked against the Pass 2 values (re-parsed from the raw DOS files with a separate parser) by extracting the text of the PDF and comparing each cell to the independently rounded value; see the PDF check in [VERIFY_LOG.txt]({REPO}/blob/main/VERIFY_LOG.txt).

## Sources

DOS results.elections.myflorida.com (2022 official), DOS Florida Election Watch and its download files (2026*, unofficial), DOS book-closing registration reports for each general election. Full list: [MANIFEST.md]({REPO}/blob/main/MANIFEST.md).
{rel('Florida-County-PDF-Information')}"""
# ---------- README (plain-language guide; also written as repo README.md)
import hashlib, os as _os
def _sha(path): return hashlib.sha256(open(path,'rb').read()).hexdigest()
_man=json.load(open('/workspace/florida/MANIFEST.json'))
_hash_rows='\n'.join(f"| `{r['file']}` | {r['url']} | `{_sha('/workspace/florida/'+r['file'])}` |" for r in _man)
_out_rows='\n'.join(f"| `{f}` | `{_sha('/workspace/florida/'+f)}` |" for f in ['pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf','data/florida_governor_2022_2026_by_county.csv'])
SF=B['SF']
README=f"""# Florida Election Analysis: a plain-language guide

**Start here if this is your first time.** This page explains, without the math, what this project is, where every number came from, and how to check it yourself.

> **\*2026 figures are UNOFFICIAL.** They are the Florida Division of Elections (DOS) Florida Election Watch county returns for the Nov 3, 2026 general election. 2022 figures are the state's official results.

## What is this?

This project compares the 2022 and 2026 races for Governor of Florida, county by county, for all 67 counties. It asks one simple question:

> **Did the Democratic candidate's share of the ballots change by more or less than the Democratic Party's share of registered voters?**

If a party loses registered voters but its candidate's share of the vote goes up, those two numbers have moved apart. This project measures how far apart, in every county.

It is part of a state-by-state series that uses the same method, which Morissa Benson developed in Nebraska. It began with her [Cedar County Audit]({CEDAR}). Each state uses only its own numbers.

## Where the numbers came from

**Every number comes directly from the Florida Division of Elections' official websites:**

- **dos.fl.gov**: the book-closing reports showing how many active registered voters each party had in each county (Oct 11, 2022 and Oct 5, 2026)
- **results.elections.myflorida.com**: the official 2022 governor results and 2022 ballots cast, county by county
- **floridaelectionwatch.gov**: the 2026 governor results and 2026 ballots cast, county by county (*2026 unofficial)

Nothing was estimated, and no other source was mixed in.

**You can check the underlying data yourself.** The sidebar links to the **Florida County PDF**, a table of all 67 counties showing registered Democrats, Democratic votes and ballots cast in both years, with the changes. [Open the county PDF here]({PDFU}).

## What reverse-factoring does, in plain terms

For each county, in each year, Morissa compares two percentages:

1. **The Democratic share of the ballots**: of everyone who cast a ballot, what percent voted for the Democratic governor candidate.
2. **The Democratic share of registration**: of everyone registered, what percent are registered Democrats.

**The difference between them is the "surplus."** If Democrats are 30% of registered voters but the Democratic candidate gets 48% of the ballots, the surplus is 18 points. Then she compares 2022 with 2026 to see how much the surplus grew or shrank, and works backward ("reverse-factoring") to ask how many votes that change represents.

**What Florida shows:**

- Statewide, the Democratic share of ballots went from {p(st['S22'])}% in 2022 to {p(st['S26'])}% in 2026, while the Democratic share of registration went from {p(st['R22'])}% to {p(st['R26'])}%.
- So the statewide surplus grew from {sg(st['G22'])} to {sg(st['G26'])} points.
- The surplus grew in all 67 counties, and every county had fewer registered Democrats in 2026 than in 2022.
- There were no counties where votes added up to more than the ballots cast, in either year.

## How Morissa derived the numbers

- **County by county.** All 67 counties were computed one at a time from the state's own files.
- **Checked twice, independently.** Two separate programs, written differently and reading the numbers from different copies of the state's reports where the state publishes them twice, computed every figure from scratch. Every number had to match exactly, to the last decimal, before anything was published. County totals were also checked against the state's own statewide totals.
- **Florida's own line.** She graphed every county's surplus against its Democratic registration share and fitted a straight line through the points: **S = m × (D/100) + b**. Here D is the Democratic share of registration, **m** (the multiplier) says how much the surplus tends to change as the Democratic share of registration changes, and **b** (the offset) is where the line starts. For Florida, the 2022 line is S = {p(SF['22']['multiplier'],2)} × (D/100) + {p(SF['22']['offset'],2)} and the 2026 line is S = {p(SF['26']['multiplier'],2)} × (D/100) + {p(SF['26']['offset'],2)}. In Florida, registration share explains little of the difference between counties, so the line is a loose fit. The [Locked Florida Formula]({WIKI}/Locked-Florida-Formula) page shows exactly how loose.

## This is a hypothesis, not a settled fact

These numbers measure a **pattern**. They do not prove fraud, error or intent by anyone. Ordinary things can also move them: people voting across party lines, changes in who turned out, people moving, and voter-roll cleanups (Florida's total active registration fell by {ci(-st['totreg_chg'])} between the two reports).

Morissa's view is that election manipulation, if it exists, would be **multifaceted**: several methods working together, not a single trick. This analysis is **one lens** on that question. Her hypothesis, which is not proven, names four possible pieces:

1. **USB batch-acceptance overrides**: update media used to make systems accept batches they otherwise would not
2. **An absentee batch chain-of-custody gap**: absentee ballot batches moving without a complete custody record
3. **Ghost voters fed with real voter data**: registrations that use real people's information
4. **Cloud-layer number swaps**: totals changed in the reporting layer after counting

Each of these is a hypothesis to be tested with records, not a finding of this project. For the story behind the numbers and why she thinks these pieces fit together, read her write-up: **[The Burden Just Flipped]({SUBSTACK})**.

## Where to go next

| Page | What you'll find |
|---|---|
| [Home]({WIKI}/Home) | Overview and statewide numbers |
| [Cedar County Audit]({CEDAR}) | Where the method began (Nebraska) |
| [Floor and Ceiling]({WIKI}/Floor-and-Ceiling) | The counties at the top and bottom |
| [Reverse Math]({WIKI}/Reverse-Math) | One county, then the ten largest, then all 67 |
| [Graphs]({WIKI}/Graphs) | All charts |
| [Florida County PDF Information]({WIKI}/Florida-County-PDF-Information) | The downloadable 67-county table |
| [Locked Florida Formula]({WIKI}/Locked-Florida-Formula) | Florida's surplus equation and a fill-in worksheet |

## Hash verification: proving the files are unchanged

Every file the state published that this project used is saved, unchanged, in the [`raw/`]({REPO}/tree/main/raw) folder of the repository. Each one has a **SHA-256 fingerprint**: a 64-character code that changes completely if even one character of the file changes. If your fingerprint matches the one below, your copy is identical to the one used here.

**How to check:** download the file from the repository, then run `sha256sum <file>` (Mac or Linux) or `Get-FileHash <file> -Algorithm SHA256` (Windows PowerShell) and compare. The state sometimes updates files at the same address, so a fresh download from the state site can differ from the copy saved on the date listed in [MANIFEST.md]({REPO}/blob/main/MANIFEST.md).

| File in `raw/` | Source | SHA-256 |
|---|---|---|
{_hash_rows}

Published outputs:

| File | SHA-256 |
|---|---|
{_out_rows}

## Disclaimers

1. **This measures a pattern, not a cause.** It makes no claim about intent, fraud or wrongdoing by any person, office or party.
2. **Votes are not voters.** "Democratic votes" counts votes for the Democratic governor ticket, not registered Democrats who voted.
3. **Florida only.** No other state's numbers are used in any Florida figure.
"""
pages['README.md']=README+rel('README')
open('/workspace/florida/README.md','w').write(README.replace('](raw/','](raw/'))
for fn,txt in pages.items(): open(f'/workspace/florida/wiki/{fn}','w').write(txt)
print('wiki pages',list(pages))
