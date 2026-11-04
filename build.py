"""Builds the TechVestVentures Prediction Market Accuracy Graphs site from focus/prediction-accuracy/2026-11-04/. Modeled on ukrcas-site/build.py."""
import os,sys,shutil,json,glob
sys.path.insert(0,'/workspace/risk-watcher/graphs-site');sys.path.insert(0,'/workspace/risk-watcher');os.chdir(os.path.dirname(os.path.abspath(__file__)))
from common import *
T="TechVestVentures Prediction Market Accuracy Graphs";J="/workspace/risk-watcher/focus/prediction-accuracy/2026-11-04/"
RC='<a href="https://atlantean2.github.io/tvv-daily-risk-alert-digest/" style="color:#FFD400;font-size:.6em;margin-left:14px">TVV RISK CENTER</a>'
R={g["file"]:g for g in json.load(open(J+"records.json"))}
F=lambda n:[f for f in R if f.startswith(f"PMA {n:02d} ")][0]
TABS=[("scorecard","Scorecard","Polymarket and Kalshi prices captured Nov 2, 2026 at 5:02 PM ET, scored against AP calls and market resolutions as of about 1 PM ET Nov 4. House seat results are provisional (Polymarket-resolved; AP had many House races uncalled).",[F(i) for i in (1,2,4)]),
 ("venues","Calibration and Venues","How well prices matched outcomes, and Polymarket against Kalshi on the same races. Samples in the low-price bands are tiny (1 to 5 races).",[F(i) for i in (3,5,7)]),
 ("models","Markets vs Models","Chamber control against the forecast models captured before the vote. Only 2 outcomes, so illustrative only.",[F(6)]),
 ("pending","Pending","Races AP had not called. TVV names no winner until they are called; a later update pass will score them.",[F(8)])]
shutil.rmtree("issues",ignore_errors=True);os.makedirs("issues/img");os.makedirs("assets",exist_ok=True)
assert sorted(f for *_,fs in TABS for f in fs)==sorted(os.path.basename(p) for p in glob.glob(J+"PMA 0*.png"))
tabs=[];src={};n=0
def w(k,lab,body): open(f"issues/{k}.html","w").write(page(T,k,body));tabs.append((k,lab))
for k,lab,note,fs in TABS:
    b=f'<h2 class="desk">{E(lab)}{RC}</h2><p>{E(note)}</p>'
    for f in fs:
        g=R[f];n+=1;out=f"img/{k}-{n:02d}.webp";save_img(J+f,"issues/"+out)
        urls=list(dict.fromkeys(g["sources"]))
        for u in urls: src.setdefault(u,g["title"])
        b+=figure(out,g["title"],g["caption"]+" [Data: Nov 2-4, 2026]",urls)
    w(k,lab,b)
w("sources","Sources",f'<h2 class="desk">Sources ({len(src)} links){RC}</h2><p>All charts were drawn by TechVestVentures from the data linked below.</p><ul class="src">'+"".join(f'<li>{E(l)}: <a href="{E(u)}">{E(u)}</a></li>' for u,l in src.items())+"</ul>")
index(T,tabs,"Sections",cur="predacc");print(n,"charts",len(src),"sources")
