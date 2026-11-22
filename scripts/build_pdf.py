import pickle, sys
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec=50
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
B=pickle.load(open('/workspace/florida/data/build_state.pkl','rb'))
C,st,S,BUILT=B['C'],B['st'],B['S'],B['BUILT']
def dec(x): x=F(x); return Decimal(x.numerator)/Decimal(x.denominator)
def rnd(x,nd): return dec(x).quantize(Decimal(1).scaleb(-nd),rounding=ROUND_HALF_UP)
def p2(x): v=rnd(x,2); return f'{v:.2f}'
def sp2(x): v=rnd(x,2); return ('+' if v>0 else '' )+f'{v:.2f}'
def ci(n): return f'{n:,}'
def sci(n): return ('+' if n>0 else '')+f'{n:,}'
rows=sorted(C.values(),key=lambda r:(-r['R26'],r['county']))
SR=B['STATE_ROW']
ss=getSampleStyleSheet(); small=ParagraphStyle('s',parent=ss['Normal'],fontSize=7.5,leading=9.5)
title=ParagraphStyle('t',parent=ss['Title'],fontSize=13,leading=16)
NOTE=("<b>2026 figures: certified Nov 17, 2026</b> by the Elections Canvassing Commission (label per Morissa Benson's decision, based on the Florida Election Watch "
      "'Official Election Results' label and news reports of the Nov 17 certification). 2022 figures are DOS official results. Governor race: Crist (D) 2022, Jolly (D) 2026. "
      "Registration = DOS book-closing active registered voters (Oct 11, 2022; Oct 5, 2026). Ballots cast = DOS county voter turnout. "
      "Sorted by 2026 Democratic share of registration, highest first; statewide total in the last row. Percents and point changes rounded half-up to 2 decimals from exact values; "
      "change % = change ÷ 2022 value. Full-precision values are in the CSV.")
h1=['County','Dem Reg\nShare\n2022 %','Dem Reg\nShare\n2026 %','Dem Reg\n2022','Dem Reg\n2026','Reg\nChange #','Reg\nChange %','Dem Gov\nVotes 2022','Dem Gov\nVotes 2026','Vote\nChange #','Vote\nChange %','Ballots\nCast 2022','Ballots\nCast 2026','Ballot\nChange #','Ballot\nChange %']
def t1(r): return [r['county'],p2(r['R22']),p2(r['R26']),ci(r['demreg22']),ci(r['demreg26']),sci(r['demreg_chg']),sp2(r['demreg_chg_pct']),ci(r['dem22']),ci(r['dem26']),sci(r['dem_chg']),sp2(r['dem_chg_pct']),ci(r['ballots22']),ci(r['ballots26']),sci(r['ballots_chg']),sp2(r['ballots_chg_pct'])]
h2=['County','Dem Share of\nBallots 2022 %','Dem Share of\nBallots 2026 %','Change\n(pts)','Dem Reg\nShare 2022 %','Dem Reg\nShare 2026 %','Change\n(pts)','G 2022','G 2026','ΔG','Total Reg\n2022','Total Reg\n2026']
def t2(r): return [r['county'],p2(r['S22']),p2(r['S26']),sp2(r['S26']-r['S22']),p2(r['R22']),p2(r['R26']),sp2(r['R26']-r['R22']),sp2(r['G22']),sp2(r['G26']),sp2(r['dG']),ci(r['totreg22']),ci(r['totreg26'])]
SR2=dict(SR); SR2['county']='STATEWIDE'
def mk(h,data,cw):
    t=Table([h]+data,colWidths=cw,repeatRows=1)
    sty=[('FONT',(0,0),(-1,-1),'Helvetica',6.6),('FONT',(0,0),(-1,0),'Helvetica-Bold',6.4),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1f4e79')),('TEXTCOLOR',(0,0),(-1,0),colors.white),
         ('ALIGN',(1,0),(-1,-1),'RIGHT'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),0.25,colors.HexColor('#999999')),('TOPPADDING',(0,0),(-1,-1),1.2),('BOTTOMPADDING',(0,0),(-1,-1),1.2),
         ('FONT',(0,-1),(-1,-1),'Helvetica-Bold',6.6),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#dde6f0'))]
    for i in range(1,len(data)):
        if i%2==0: sty.append(('BACKGROUND',(0,i),(-1,i),colors.HexColor('#f3f6fa')))
    t.setStyle(TableStyle(sty)); return t
def onpage(cv,doc):
    cv.saveState(); cv.setFont('Helvetica',7); cv.drawString(0.4*inch,0.3*inch,f'Florida 67-County Democratic Registration and Governor Vote Change, 2022 vs 2026   |   2026 certified Nov 17, 2026   |   Built {BUILT}   |   Page {doc.page}'); cv.restoreState()
doc=SimpleDocTemplate('/workspace/florida/pdf/Florida_67_County_Democratic_Registration_and_Vote_Change.pdf',pagesize=landscape(letter),leftMargin=0.35*inch,rightMargin=0.35*inch,topMargin=0.4*inch,bottomMargin=0.45*inch,
    title='Florida 67-County Democratic Registration and Governor Vote Change, 2022 vs 2026 (2026 certified Nov 17, 2026)',author='Morissa Benson method; prepared for review')
el=[Paragraph('Florida 67 Counties: Democratic Registration, Governor Votes and Ballots Cast, 2022 vs 2026 (2026 certified Nov 17, 2026)',title),Paragraph(NOTE,small),Spacer(1,4),
    Paragraph('<b>Table 1.</b> Democratic registration, Democratic governor votes and total ballots cast, raw numbers and percent change.',small),Spacer(1,3)]
cw1=[0.95*inch]+[0.48*inch]*2+[0.66*inch]*2+[0.6*inch,0.5*inch]+[0.66*inch]*2+[0.6*inch,0.5*inch]+[0.66*inch]*2+[0.6*inch,0.5*inch]
el.append(mk(h1,[t1(r) for r in rows]+[t1(SR2)],cw1)); el.append(PageBreak())
el+= [Paragraph('<b>Table 2.</b> Shares and the gap G = Democratic share of ballots cast − Democratic share of registration (points); ΔG = G 2026 − G 2022 (descriptive). Same sort order. 2026 certified Nov 17, 2026.',small),Spacer(1,3)]
cw2=[1.0*inch]+[0.82*inch]*2+[0.62*inch]+[0.75*inch]*2+[0.6*inch]+[0.62*inch]*3+[0.8*inch]*2
el.append(mk(h2,[t2(r) for r in rows]+[t2(SR2)],cw2))
doc.build(el,onFirstPage=onpage,onLaterPages=onpage)
print('pdf ok')
