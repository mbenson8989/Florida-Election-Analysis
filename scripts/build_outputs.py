"""Build CSV, PDF, charts and wiki markdown from pass-1 data (pass 2 must match exactly; checked again here)."""
import json, csv, os, datetime
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec=50
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
BASE='/workspace/florida'
p1=json.load(open(f'{BASE}/data/pass1.json')); p2=json.load(open(f'{BASE}/data/pass2.json'))
for k in p1['counties']:
    for f,v in p2['counties'][k].items(): assert F(str(p1['counties'][k][f]))==F(str(v)),(k,f)
def dec(x): x=F(str(x)); return Decimal(x.numerator)/Decimal(x.denominator)
def rnd(x,nd): return dec(x).quantize(Decimal(1).scaleb(-nd),rounding=ROUND_HALF_UP)
def full(x): return format(dec(x).quantize(Decimal('1e-20'),rounding=ROUND_HALF_UP),'f')
def sg(x,nd=2):
    v=rnd(x,nd); s=f'{abs(v):,.{nd}f}'
    return ('+' if v>0 else '−' if v<0 else '')+s
def ci(n): return f'{n:,}'
def sci(n): return ('+' if n>0 else '−' if n<0 else '')+f'{abs(n):,}'
C={k:{a:(F(b) if isinstance(b,str) and '/' in b else b) for a,b in v.items()} for k,v in p1['counties'].items()}
for r in C.values():
    for f in ['S22','S26','R22','R26','G22','G26','dG','drop','resid_regloss','implied_regloss','dem_chg_pct','ballots_chg_pct','demreg_chg_pct','fit_pred','fit_resid','implied_fit','sfit_pred22','sfit_res22','sfit_pred26','sfit_res26','DR_over_ballots22','DR_over_ballots26','gov_over_ballots22','gov_over_ballots26']:
        r[f]=F(str(r[f]))
    r['totreg_chg_pct']=F(100*r['totreg_chg'],r['totreg22'])
SF={y:{k:F(v) for k,v in d.items()} for y,d in p1['surplus_fit'].items()}
for y in SF: 
    for k in SF[y]: assert SF[y][k]==F(p2['surplus_fit'][y][k])
FIT={k:(F(v) if isinstance(v,str) else v) for k,v in p1['fit'].items()}
c,m,R2,n=FIT['constant'],FIT['multiplier'],FIT['R2'],FIT['n']
S=p1['state_sums']
st=dict(S); H=F(100)
st['S22']=H*S['dem22']/S['ballots22']; st['S26']=H*S['dem26']/S['ballots26']; st['R22']=H*S['demreg22']/S['totreg22']; st['R26']=H*S['demreg26']/S['totreg26']
st['G22']=st['S22']-st['R22']; st['G26']=st['S26']-st['R26']; st['dG']=st['G26']-st['G22']; st['drop']=st['R22']-st['R26']
st['dem_chg']=S['dem26']-S['dem22']; st['ballots_chg']=S['ballots26']-S['ballots22']; st['demreg_chg']=S['demreg26']-S['demreg22']; st['totreg_chg']=S['totreg26']-S['totreg22']
st['dem_chg_pct']=H*st['dem_chg']/S['dem22']; st['ballots_chg_pct']=H*st['ballots_chg']/S['ballots22']; st['demreg_chg_pct']=H*st['demreg_chg']/S['demreg22']; st['totreg_chg_pct']=H*st['totreg_chg']/S['totreg22']
st['resid_regloss']=st['S26']-st['S22']; st['implied_pooled']=S['dem26']-st['S22']*S['ballots26']/H
st['rep_chg']=S['rep26']-S['rep22']
rows=list(C.values())
by_reg26=sorted(rows,key=lambda r:(-r['R26'],r['county']))
by_dG=sorted(rows,key=lambda r:r['dG'])
by_size=sorted(rows,key=lambda r:(-r['ballots26'],r['county']))
ceiling=by_dG[::-1][:5]; floorG=by_dG[:5]
floor_base=sorted(rows,key=lambda r:r['R22'])[:5]; ceil_base=sorted(rows,key=lambda r:-r['R22'])[:5]
fr_sorted=sorted(rows,key=lambda r:r['fit_resid'])
loss=[r for r in rows if r['loss']]
imp_total=sum(r['implied_regloss'] for r in loss)
imp_fit_total=sum(r['implied_fit'] for r in rows); imp_fit_pos=sum(r['implied_fit'] for r in rows if r['implied_fit']>0)
med=sorted(r['dG'] for r in rows); median=(med[32]+med[33])/2 if n%2==0 else med[n//2]
mean=sum(r['dG'] for r in rows)/n
# standard errors (float, display only)
import math
xs=[float(r['drop']) for r in rows]; ys=[float(r['dG']) for r in rows]; mx=sum(xs)/n
sse=sum((float(r['fit_resid']))**2 for r in rows); s2=sse/(n-2); sxx=sum((x-mx)**2 for x in xs)
se_m=math.sqrt(s2/sxx); se_c=math.sqrt(s2*(1/n+mx*mx/sxx)); t975=1.997729654  # t(0.975, df=65)
resid_sd=math.sqrt(s2)
now=datetime.datetime.now().astimezone()
BUILT=now.strftime('%b %d %Y %I:%M %p CST').replace(' 0',' ')
os.makedirs(f'{BASE}/data',exist_ok=True); os.makedirs(f'{BASE}/pdf',exist_ok=True); os.makedirs(f'{BASE}/charts',exist_ok=True); os.makedirs(f'{BASE}/wiki',exist_ok=True)
# ---------------- CSV (full precision) ----------------
cols=['county','dem_reg_share_2022_pct','dem_reg_share_2026_pct','dem_reg_share_change_pts','dem_reg_2022','dem_reg_2026','dem_reg_change','dem_reg_change_pct',
      'total_reg_2022','total_reg_2026','total_reg_change','total_reg_change_pct',
      'dem_gov_votes_2022','dem_gov_votes_2026','dem_votes_change','dem_votes_change_pct','rep_gov_votes_2022','rep_gov_votes_2026','all_gov_votes_2022','all_gov_votes_2026',
      'ballots_cast_2022','ballots_cast_2026','ballots_change','ballots_change_pct',
      'dem_share_of_ballots_2022_pct','dem_share_of_ballots_2026_pct','G_2022','G_2026','delta_G','reg_share_drop','dem_reg_count_fell',
      'residual_regloss_dG_minus_drop','implied_extra_votes_regloss','fit_predicted_dG','fit_residual','implied_votes_fit_residual',
      'surplus_fit_predicted_S_2022','surplus_fit_residual_2022','surplus_fit_predicted_S_2026','surplus_fit_residual_2026',
      'D_plus_R_over_ballots_2022','D_plus_R_over_ballots_2026','gov_votes_over_ballots_2022','gov_votes_over_ballots_2026']
def csvrow(r):
    return [r['county'],full(r['R22']),full(r['R26']),full(r['R26']-r['R22']),r['demreg22'],r['demreg26'],r['demreg_chg'],full(r['demreg_chg_pct']),
            r['totreg22'],r['totreg26'],r['totreg_chg'],full(r['totreg_chg_pct']),
            r['dem22'],r['dem26'],r['dem_chg'],full(r['dem_chg_pct']),r['rep22'],r['rep26'],r['govtot22'],r['govtot26'],
            r['ballots22'],r['ballots26'],r['ballots_chg'],full(r['ballots_chg_pct']),
            full(r['S22']),full(r['S26']),full(r['G22']),full(r['G26']),full(r['dG']),full(r['drop']),'yes' if r['loss'] else 'no',
            full(r['resid_regloss']),full(r['implied_regloss']),full(r['fit_pred']),full(r['fit_resid']),full(r['implied_fit']),
            *( [full(r['sfit_pred22']),full(r['sfit_res22']),full(r['sfit_pred26']),full(r['sfit_res26'])] if 'sfit_pred22' in r else ['','','','']),
            full(r['DR_over_ballots22']),full(r['DR_over_ballots26']),full(r['gov_over_ballots22']),full(r['gov_over_ballots26'])]
with open(f'{BASE}/data/florida_governor_2022_2026_by_county.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['# Florida Governor 2022 (official) vs 2026* (unofficial; Florida Division of Elections Florida Election Watch county returns). Sorted by 2026 Democratic registration share, descending. Values at 20 decimal places, computed from exact rationals; pass 1 and pass 2 match exactly.'])
    w.writerow(cols)
    for r in by_reg26: w.writerow(csvrow(r))
    sr=dict(county='STATEWIDE',R22=st['R22'],R26=st['R26'],demreg22=S['demreg22'],demreg26=S['demreg26'],demreg_chg=st['demreg_chg'],demreg_chg_pct=st['demreg_chg_pct'],
            totreg22=S['totreg22'],totreg26=S['totreg26'],totreg_chg=st['totreg_chg'],totreg_chg_pct=st['totreg_chg_pct'],dem22=S['dem22'],dem26=S['dem26'],dem_chg=st['dem_chg'],dem_chg_pct=st['dem_chg_pct'],
            rep22=S['rep22'],rep26=S['rep26'],govtot22=S['govtot22'],govtot26=S['govtot26'],ballots22=S['ballots22'],ballots26=S['ballots26'],ballots_chg=st['ballots_chg'],ballots_chg_pct=st['ballots_chg_pct'],
            S22=st['S22'],S26=st['S26'],G22=st['G22'],G26=st['G26'],dG=st['dG'],drop=st['drop'],loss=S['demreg26']<S['demreg22'],resid_regloss=st['resid_regloss'],implied_regloss=st['implied_pooled'],
            fit_pred=c+m*st['drop'],fit_resid=st['dG']-(c+m*st['drop']),implied_fit=(st['dG']-(c+m*st['drop']))*S['ballots26']/H,
            DR_over_ballots22=F(S['dem22']+S['rep22'],S['ballots22']),DR_over_ballots26=F(S['dem26']+S['rep26'],S['ballots26']),gov_over_ballots22=F(S['govtot22'],S['ballots22']),gov_over_ballots26=F(S['govtot26'],S['ballots26']))
    w.writerow(csvrow(sr))
STATE_ROW=sr
summary=dict(built=now.isoformat(timespec='seconds'),n=n,constant=full(c),multiplier=full(m),R2=full(R2),se_constant=se_c,se_multiplier=se_m,resid_sd=resid_sd,
  ceiling_dG=[(r['county'],full(r['dG'])) for r in ceiling],floor_dG=[(r['county'],full(r['dG'])) for r in floorG],
  floor_baseline=[(r['county'],full(r['R22'])) for r in floor_base],fit_resid_min=(fr_sorted[0]['county'],full(fr_sorted[0]['fit_resid'])),fit_resid_max=(fr_sorted[-1]['county'],full(fr_sorted[-1]['fit_resid'])),
  implied_regloss_total_loss_counties=full(imp_total),implied_pooled_statewide=full(st['implied_pooled']),implied_fit_sum=full(imp_fit_total),implied_fit_positive_sum=full(imp_fit_pos),
  median_dG=full(median),mean_dG=full(mean),statewide=dict(S22=full(st['S22']),S26=full(st['S26']),R22=full(st['R22']),R26=full(st['R26']),G22=full(st['G22']),G26=full(st['G26']),dG=full(st['dG']),drop=full(st['drop'])))
from scipy import stats as SS
SFS={}
for y in ['22','26']:
    d=SF[y]; s2=float(d['sse'])/(n-2); se_m_=math.sqrt(s2/float(d['sxx']))
    xm=sum(float(r['R'+y])/100 for r in rows)/n; se_b_=math.sqrt(s2*(1/n+xm*xm/float(d['sxx'])))
    tt=float(d['multiplier'])/se_m_; pv=2*SS.t.sf(abs(tt),n-2); tc=SS.t.ppf(0.975,n-2)
    mx_=max(rows,key=lambda r:abs(r['sfit_res'+y]))
    SFS[y]=dict(multiplier=full(d['multiplier']),offset=full(d['offset']),R2=full(d['R2']),mean_abs_resid=full(d['mean_abs_resid']),se_multiplier=se_m_,se_offset=se_b_,
               ci_multiplier=[float(d['multiplier'])-tc*se_m_,float(d['multiplier'])+tc*se_m_],t=tt,p_value=pv,resid_sd=math.sqrt(s2),t_crit=tc,
               max_resid_county=mx_['county'],max_resid=full(mx_['sfit_res'+y]),n=n)
summary['surplus_fit']=SFS
summary['certification_2026']='*2026 figures are unofficial (Florida Election Watch county returns).'
summary['delta_G_fit_note']='Descriptive only; not the locked formula. The locked formula is the surplus form S = m x (D/100) + b.'
json.dump(summary,open(f'{BASE}/data/summary.json','w'),indent=1)
# ---------------- Charts ----------------
FL='#1f4e79'; OR='#e8761e'; GR='#2e8b57'
cn={r['county'] for r in ceiling}; fn={r['county'] for r in floorG}
def col(r): return OR if r['county'] in cn else GR if r['county'] in fn else FL
fig,ax=plt.subplots(figsize=(11,7.5))
ax.scatter([float(r['drop']) for r in rows],[float(r['dG']) for r in rows],c=[col(r) for r in rows],s=[max(18,min(300,r['ballots26']/2500)) for r in rows],alpha=.8,edgecolor='k',lw=.4)
xx=[0,max(float(r['drop']) for r in rows)+0.5]; ax.plot(xx,[float(c+m*F(x)) for x in xx],'r--',lw=1.6,label=f'Descriptive trend line (not the locked formula): ΔG = {rnd(c,2)} + {rnd(m,3)} × drop, R² = {rnd(R2,3)}, n = {n}')
for r in rows:
    if r['county'] in cn|fn or abs(r['fit_resid'])>3 or r['ballots26']>500000: ax.annotate(f"{r['county']} {sg(r['dG'])}",(float(r['drop']),float(r['dG'])),fontsize=7.5,xytext=(4,3),textcoords='offset points')
ax.set_xlim(-0.3,max(xs)+2.2); ax.set_xlabel('Democratic registration-share drop, 2022 → 2026 (points)'); ax.set_ylabel('ΔG = G 2026 − G 2022 (points)')
ax.set_title('Florida governor: ΔG vs registration-share drop, 67 counties (descriptive)\n*2026 unofficial. Orange = ceiling (5 highest ΔG), green = floor (5 lowest ΔG); dot size ∝ 2026 ballots',fontsize=10.5)
ax.legend(loc='upper left'); ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(f'{BASE}/charts/FL_DeltaG_vs_Registration_Drop_Fit.png',dpi=150); plt.close(fig)
fig,ax=plt.subplots(figsize=(11,13)); srt=by_dG
ax.barh(range(n),[float(r['dG']) for r in srt],color=[col(r) for r in srt]); ax.set_yticks(range(n)); ax.set_yticklabels([r['county'] for r in srt],fontsize=7.5)
for i,r in enumerate(srt): ax.text(float(r['dG'])+0.15,i,sg(r['dG']),va='center',fontsize=6.5)
ax.axvline(float(median),color='r',ls='--',lw=1,label=f'County median {sg(median)}'); ax.axvline(float(st['dG']),color='k',ls=':',lw=1,label=f'Statewide pooled {sg(st["dG"])}')
ax.set_xlabel('ΔG (points); *2026 unofficial'); ax.set_title('Florida governor ΔG by county, lowest to highest (*2026 unofficial)\nOrange = ceiling (5 highest), green = floor (5 lowest)',fontsize=10.5); ax.legend(loc='lower right'); ax.grid(axis='x',alpha=.3)
fig.tight_layout(); fig.savefig(f'{BASE}/charts/FL_DeltaG_by_County.png',dpi=150); plt.close(fig)
fig,ax=plt.subplots(figsize=(8,11))
for r in rows: ax.plot([0,1],[float(r['G22']),float(r['G26'])],color=col(r),alpha=.8 if r['county'] in cn|fn else .35,lw=1.6 if r['county'] in cn|fn else .8)
for r in ceiling+floorG: ax.text(1.02,float(r['G26']),f"{r['county']} ({sg(r['dG'])})",fontsize=7,va='center')
ax.set_xticks([0,1]); ax.set_xticklabels(['G 2022','G 2026']); ax.set_xlim(-.1,1.45); ax.set_ylabel('G = Dem share of ballots − Dem registration share (points)')
ax.set_title(f'Florida county slope chart, G 2022 → G 2026 (*2026 unofficial)\nG rose in {sum(r["dG"]>0 for r in rows)} of 67 counties',fontsize=10.5); ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(f'{BASE}/charts/FL_Slope_G2022_to_G2026.png',dpi=150); plt.close(fig)
fig,ax=plt.subplots(figsize=(13,6)); srt=by_size; x=range(n)
ax.bar([i-.2 for i in x],[float(r['DR_over_ballots22'])*100 for r in srt],.4,label='2022',color='#8aa9c9'); ax.bar([i+.2 for i in x],[float(r['DR_over_ballots26'])*100 for r in srt],.4,label='2026',color=FL)
ax.axhline(100,color='r',lw=1.2,label='100% = ballots cast'); ax.set_ylim(90,101); ax.set_xticks(list(x)); ax.set_xticklabels([r['county'] for r in srt],rotation=90,fontsize=6.5)
ax.set_ylabel('(Dem + Rep governor votes) ÷ ballots cast, %'); ax.set_title('Texas-style over-ballot check, all 67 counties by 2026 ballots (largest first). No county reaches 100% (*2026 unofficial)',fontsize=10)
ax.legend(); fig.tight_layout(); fig.savefig(f'{BASE}/charts/FL_Over_Ballot_Check.png',dpi=150); plt.close(fig)
fig,ax=plt.subplots(figsize=(13,6)); srt=by_size
ax.bar(range(n),[float(r['resid_regloss']) for r in srt],color=[col(r) for r in srt]); ax.set_xticks(range(n)); ax.set_xticklabels([r['county'] for r in srt],rotation=90,fontsize=6.5)
ax.set_ylabel('Residual = ΔG − registration-share drop (points)'); ax.set_title('Residual after the registration-loss step, all 67 counties (all lost registered Democrats), by 2026 ballots (*2026 unofficial)',fontsize=10); ax.grid(axis='y',alpha=.3)
fig.tight_layout(); fig.savefig(f'{BASE}/charts/FL_Residual_Bars_by_Ballots.png',dpi=150); plt.close(fig)
for y,yy in [('22','2022'),('26','2026')]:
    d=SF[y]; fig,ax=plt.subplots(figsize=(11,7.5))
    X=[float(r['R'+y]) for r in rows]; Y=[float(r['G'+y]) for r in rows]
    ax.scatter(X,Y,s=[max(18,min(300,r['ballots'+y]/2500)) for r in rows],color=FL,alpha=.75,edgecolor='k',lw=.4)
    xx=[min(X)-2,max(X)+2]; ax.plot(xx,[float(d['multiplier'])*v/100+float(d['offset']) for v in xx],'r--',lw=1.6,label=f"S = {rnd(d['multiplier'],2)} × (D/100) {'+' if d['offset']>=0 else '−'} {abs(rnd(d['offset'],2))}   (R² = {rnd(d['R2'],3)}, n = {n})")
    for r in sorted(rows,key=lambda r:-abs(r['sfit_res'+y]))[:8]+sorted(rows,key=lambda r:-r['ballots'+y])[:4]:
        ax.annotate(f"{r['county']} {sg(r['sfit_res'+y])}",(float(r['R'+y]),float(r['G'+y])),fontsize=7.5,xytext=(4,3),textcoords='offset points')
    ax.axhline(0,color='grey',lw=.8); ax.set_xlabel(f'D = Democratic registration share {yy} (%)'); ax.set_ylabel(f'S = surplus {yy} = Dem share of ballots − D (points)')
    ax.set_title(f"Florida surplus form, {yy}: S vs D, 67 counties, OLS fit (Florida data only)" + ("\n*2026 unofficial" if y=='26' else "\n2022 official")+"; labels show residual (actual − fitted S); dot size ∝ ballots",fontsize=10.5)
    ax.legend(loc='upper left'); ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(f'{BASE}/charts/FL_Surplus_S_vs_D_{yy}.png',dpi=150); plt.close(fig)
    fig,ax=plt.subplots(figsize=(11,13)); srt=sorted(rows,key=lambda r:r['sfit_res'+y])
    ax.barh(range(n),[float(r['sfit_res'+y]) for r in srt],color=[OR if r['sfit_res'+y]>0 else GR for r in srt]); ax.set_yticks(range(n)); ax.set_yticklabels([r['county'] for r in srt],fontsize=7.5)
    for i,r in enumerate(srt): ax.text(float(r['sfit_res'+y])+(0.2 if r['sfit_res'+y]>=0 else -0.2),i,sg(r['sfit_res'+y]),va='center',ha='left' if r['sfit_res'+y]>=0 else 'right',fontsize=6.5)
    ax.axvline(0,color='k',lw=.8); ax.set_xlabel('Residual = actual S − fitted S (points)')
    ax.set_title(f"Florida surplus-form residuals, {yy} (S = {rnd(d['multiplier'],2)} × (D/100) {'+' if d['offset']>=0 else '−'} {abs(rnd(d['offset'],2))}); mean |residual| {rnd(d['mean_abs_resid'],2)} pts" + ("\n*2026 unofficial" if y=='26' else "\n2022 official"),fontsize=10.5)
    ax.grid(axis='x',alpha=.3); fig.tight_layout(); fig.savefig(f'{BASE}/charts/FL_Surplus_Residuals_{yy}.png',dpi=150); plt.close(fig)
json.dump(dict(built=BUILT),open(f'{BASE}/data/build_meta.json','w'))
import pickle; pickle.dump(dict(SF=SF,SFS=SFS,C=C,st=st,S=S,FIT=FIT,se_c=se_c,se_m=se_m,resid_sd=resid_sd,t975=t975,BUILT=BUILT,median=median,mean=mean,imp_total=imp_total,imp_fit_total=imp_fit_total,imp_fit_pos=imp_fit_pos,STATE_ROW=STATE_ROW),open(f'{BASE}/data/build_state.pkl','wb'))
print('built',BUILT); print(json.dumps(summary,indent=1)[:3000])
