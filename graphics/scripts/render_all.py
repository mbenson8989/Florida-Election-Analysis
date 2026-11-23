import json, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
G="/usr/share/fonts/truetype/sand-box/google/"
BC=G+"Barlow Condensed/BarlowCondensed-Black.ttf"; BCB=G+"Barlow Condensed/BarlowCondensed-Bold.ttf"
SS=G+"Source Sans 3/SourceSans3-VariableFont_wght.ttf"
def F(size,w):
    f=ImageFont.truetype(SS,size); f.set_variation_by_axes([w]); return f
def T(p,s): return ImageFont.truetype(p,s)
A=json.load(open('flip_passA.json'))[:10]; B=json.load(open('flip_passB.json'))[:10]
assert A==B, "pass mismatch - do not render"
BG=(8,14,28); RED=(200,16,46); WHITE=(255,255,255); GOLD=(212,175,90); GREY=(160,170,190); BLUE=(120,170,230); ORANGE=(245,130,32)
c=lambda n:f"{n:,}"
used={}
def flip(d):
    W,H=1080,1350; img=Image.new("RGB",(W,H),BG); dr=ImageDraw.Draw(img); M=70
    vals=[]
    def txt(xy,s,f,fill): dr.text(xy,s,font=f,fill=fill); vals.append(s)
    txt((M,58),f"F L O R I D A   ·   F L I P   # {d['rank']}   O F   6 7",T(BCB,34),GOLD)
    name=d['county'].upper()+" COUNTY"; sz=140
    while dr.textlength(name,font=T(BC,sz))>W-2*M: sz-=4
    txt((M,98),name,T(BC,sz),WHITE)
    dr.rectangle([M,108+sz+8,M+150,108+sz+14],fill=GOLD)
    def block(y,label,big,col,a,b,sub):
        txt((M,y),label,T(BCB,42),WHITE)
        fb=T(BC,170); txt((M-4,y+34),big,fb,col); bw=dr.textlength(big,font=fb)
        fs=F(42,700); x=M+bw+36; yy=y+34+40
        txt((x,yy),a,fs,GREY); txt((x,yy+52),b,fs,WHITE)
        txt((M,y+226),sub,F(32,600),GREY)
    y0=108+sz+40
    block(y0,"DEMOCRATIC REGISTRATION",f"DOWN {c(-d['reg_chg'])}",BLUE,f"2022: {c(d['reg22'])}",f"2026: {c(d['reg26'])}",
          f"Share of registered voters: {d['D22']}% → {d['D26']}%  (−{d['drop_pts']} pts)")
    block(y0+270,"DEMOCRATIC GOVERNOR VOTES",f"UP {c(d['votes_chg'])}",RED,f"2022: {c(d['votes22'])}",f"2026: {c(d['votes26'])}",
          f"Share of ballots cast: {d['V22']}% → {d['V26']}%  (+{d['V_gain']} pts)")
    y=y0+548; dr.rectangle([M,y,W-M,y+236],outline=RED,width=3); dr.rectangle([M+3,y+3,W-M-3,y+233],fill=(40,10,18))
    txt((M+28,y+16),"THE FLIP (ΔG)",T(BCB,40),GOLD)
    txt((M+28,y+56),f"{d['dG']} PTS",T(BC,118),RED)
    f2=F(32,700); rx=W-M-28
    for i,s in enumerate([f"Surplus G 2022: {d['G22']}",f"Surplus G 2026: {d['G26']}"]):
        dr.text((rx-dr.textlength(s,font=f2),y+60+i*48),s,font=f2,fill=WHITE); vals.append(s)
    txt((M+28,y+180),f"Implied extra votes: +{c(d['implied'])}",F(34,700),ORANGE)
    txt((M,y+252),"Registration fell. Votes rose. Same county.",F(40,700),WHITE)
    ff=F(21,500); fy=H-172
    for s in ["Surplus G = Dem governor votes ÷ ballots cast × 100 − Dem registration share. Flip ΔG = G2026 − G2022.",
              "Ranked by ΔG of 67 counties. Implied extra votes = (ΔG − registration-share drop) × 2026 ballots ÷ 100.",
              "Hypothesis analysis, not a finding of fraud. Computed from unrounded values; verified twice.",
              "Source: Florida Division of Elections; 2026 certified Nov 17.",
              "github.com/mbenson8989/Florida-Election-Analysis/wiki/Resources"]:
        assert dr.textlength(s,font=ff)<W-2*M+20, s
        dr.text((M,fy),s,font=ff,fill=GREY); fy+=30
    fn=f"FL_Flip_{d['rank']:02d}_{d['county'].replace(' ','_')}.png"
    img.save("../flip/"+fn,dpi=(300,300)); used[fn]=vals
for d in A: flip(d)
json.dump(used,open('flip_rendered_values.json','w'),indent=1)

# ---------- Guarantee Clause ----------
NAVY=(18,38,82); ORG=(184,78,10); INK=(40,30,20)
PF=G+"Playfair Display/"; import glob
def serif(sz,bold=False,it=False):
    p=G+"Libre Baskerville/LibreBaskerville-"+("Italic-" if it else "")+"VariableFont_wght.ttf"
    f=T(p,sz); f.set_variation_by_axes([700 if bold else 400]); return f
def SC(sz): return T(glob.glob(G+"Cormorant SC/*Bold.ttf")[0],sz) if glob.glob(G+"Cormorant SC/*Bold.ttf") else serif(sz,True)
def parchment(W,H):
    random.seed(4); img=Image.new("RGB",(W,H),(238,224,190)); px=img.load()
    n=Image.effect_noise((W//4,H//4),40).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    base=Image.new("RGB",(W,H),(240,227,194)); dark=Image.new("RGB",(W,H),(226,206,164))
    img=Image.composite(base,dark,n.point(lambda v:min(255,v+70)))
    fine=Image.effect_noise((W,H),18).convert("RGB"); img=Image.blend(img,fine,0.06)
    # vignette
    v=Image.new("L",(W,H),0); vd=ImageDraw.Draw(v)
    vd.rectangle([0,0,W,H],fill=255)
    for i in range(25): vd.rectangle([i*2,i*2,W-i*2,H-i*2],outline=int(255*i/25))
    v=v.filter(ImageFilter.GaussianBlur(40))
    img=Image.composite(img,Image.new("RGB",(W,H),(196,168,122)),v)
    return img
def palm(dr,x,y,h,col):
    # sabal palm silhouette: curved trunk + tapered fronds
    pts=[];w0=h*0.035
    for i in range(41):
        t=i/40; px=x+math.sin(t*1.2)*h*0.08; py=y-t*h; pts.append((px,py,w0*(1-0.35*t)))
    L=[(p[0]-p[2],p[1]) for p in pts]; R=[(p[0]+p[2],p[1]) for p in pts[::-1]]
    dr.polygon(L+R,fill=col); tx,ty=pts[-1][0],pts[-1][1]
    for k in range(13):
        a=math.radians(-200+k*(220/12)); ln=h*(0.30+0.06*math.cos(k)); poly=[]
        for s in range(21):
            t=s/20; droop=t*t*ln*0.45*(1 if abs(math.cos(a))>0.3 else 0.5)
            cx=tx+math.cos(a)*ln*t; cy=ty+math.sin(a)*ln*t+droop; wd=h*0.022*math.sin(math.pi*min(1,t*1.15))+1
            poly.append((cx,cy,wd))
        top=[(p[0],p[1]-p[2]) for p in poly]; bot=[(p[0],p[1]+p[2]) for p in poly[::-1]]
        dr.polygon(top+bot,fill=col)
def wrap(dr,s,f,maxw):
    out=[];cur=""
    for w in s.split():
        t=(cur+" "+w).strip()
        if dr.textlength(t,font=f)<=maxw: cur=t
        else: out.append(cur); cur=w
    out.append(cur); return out
QUOTE=("The United States shall guarantee to every State in this Union a Republican Form of Government, "
       "and shall protect each of them against Invasion; and on Application of the Legislature, or of the "
       "Executive (when the Legislature cannot be convened) against domestic Violence.")
EOQ=("“The Federal Government has an unavoidable duty under Article II of the Constitution of the United States "
     "to enforce Federal law, which includes preventing violations of Federal criminal law and maintaining "
     "public confidence in election outcomes.”")
def gc(W,H,fn,wide):
    img=parchment(W,H); ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    palm(od,W-170 if not wide else W-200,H-40,H*0.62 if not wide else H*0.80,(18,38,82,38))
    palm(od,W-60 if not wide else W-80,H-40,H*0.48 if not wide else H*0.62,(18,38,82,28))
    img=Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"); dr=ImageDraw.Draw(img)
    # double rule border, navy + orange
    dr.rectangle([24,24,W-25,H-25],outline=NAVY,width=6); dr.rectangle([38,38,W-39,H-39],outline=ORG,width=2)
    M=80 if not wide else 90; y=74
    s="U.S. CONSTITUTION  ·  ARTICLE IV, SECTION 4"; f=SC(34 if not wide else 30); dr.text((M,y),s,font=f,fill=ORG); y+=52
    if wide:
        colw=W*0.56-M
    else: colw=W-2*M
    fh=serif(50 if not wide else 52,True)
    for i,part in enumerate(["Did you know? It’s NOT your job to prove our elections are free and fair.",
                             "The Guarantee Clause puts that on the government."]):
        for ln in wrap(dr,part,fh,colw):
            dr.text((M,y),ln,font=fh,fill=NAVY if i==0 else ORG); y+=fh.size+16
        y+=10
    dr.rectangle([M,y+6,M+140,y+10],fill=NAVY); y+=34
    if wide: qx=W*0.56+30; qy=100; qw=W-qx-M-60
    else: qx=M; qy=y; qw=colw
    fq=serif(25 if not wide else 23,it=True)
    for ln in wrap(dr,"“"+QUOTE+"”",fq,qw): dr.text((qx,qy),ln,font=fq,fill=INK); qy+=fq.size+11
    dr.text((qx,qy+4),"— Article IV, § 4, U.S. Constitution",font=serif(21),fill=INK); qy+=48
    if wide: ex,ey,ew=qx,qy+14,qw
    else: ex,ey,ew=M,qy+10,colw
    dr.text((ex,ey),"EXECUTIVE ORDER 14399",font=SC(32 if not wide else 28),fill=NAVY); ey+=44
    dr.text((ex,ey),"Signed March 31, 2026  ·  91 FR 17125",font=serif(22,True),fill=ORG); ey+=38
    fe=serif(22 if not wide else 20)
    for ln in wrap(dr,EOQ+" (Sec. 1)",fe,ew): dr.text((ex,ey),ln,font=fe,fill=INK); ey+=fe.size+9
    foot="FLORIDA ELECTION ANALYSIS  ·  moebenson.substack.com/p/the-burden-just-flipped"
    ff=serif(17); dr.text((M,H-74),foot,font=ff,fill=NAVY)
    img.save("../guarantee/"+fn,dpi=(300,300)); return ey
print(gc(1080,1080,"FL_Guarantee_Clause_1080x1080.png",False), gc(1600,900,"FL_Guarantee_Clause_1600x900.png",True))
