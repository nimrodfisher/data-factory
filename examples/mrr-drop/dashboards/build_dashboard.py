"""BI-engineer station — self-contained MRR & price-change dashboard (no external dependencies).

Every number comes from the marts / analyses / DS outputs passed in by build.py; nothing is typed by hand.
"""
import datetime as dt
import json


def build(con, results, ds, path):
    bridge = results["01_mrr_bridge"].fillna(0)
    rates = results["03_logo_churn_rates"]
    seg = results["04_segment_summary"].fillna(0)
    h, imp, fc, did = ds["headline"], ds["impact"], ds["forecast"], ds["did"]

    aug = bridge[bridge.month_end.astype(str) == "2026-08-31"].iloc[0]
    jul_mrr = float(bridge[bridge.month_end.astype(str) == "2026-07-31"].mrr.iloc[0])
    oct_rate = float(rates[(rates.grp == "SMB Starter · monthly") & (rates.month_end.astype(str) == "2026-10-31")].logo_churn_rate.iloc[0])

    data = {
        "asOf": "2026-10-31",
        "builtAt": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "kpis": [
            {"label": "MRR · Oct 2026", "value": h["mrr_oct"], "fmt": "money", "delta": (h["mrr_oct"] - jul_mrr) / jul_mrr, "deltaLabel": "vs Jul", "good": True},
            {"label": "MRR change · Aug", "value": h["aug_change"], "fmt": "money", "delta": h["aug_change_pct"], "deltaLabel": "vs Jul", "good": False},
            {"label": "Starter monthly churn · Oct", "value": oct_rate, "fmt": "pct", "note": f"baseline {did['treated_pre']:.1%}", "status": "serious"},
            {"label": "Price change net impact", "value": imp["net_run_rate_mrr"], "fmt": "money", "note": "MRR / month at Oct run-rate", "status": "serious" if imp["net_run_rate_mrr"] < 0 else "good"},
            {"label": "Dec 2026 forecast (base)", "value": fc["scenarios"]["base"][1], "fmt": "money", "note": f"80%: {fc['base_80pct'][1][0]/1e6:.2f}–{fc['base_80pct'][1][1]/1e6:.2f}M"},
        ],
        "trend": {
            "x": [str(d)[:10] for d in bridge.month_end] + fc["months"],
            "actual": [round(v) for v in bridge.mrr] + [None, None],
            "forecast": [None] * (len(bridge) - 1) + [round(float(bridge.mrr.iloc[-1]))] + [round(v) for v in fc["scenarios"]["base"]],
            "band": [None] * len(bridge) + [[round(a), round(b)] for a, b in fc["base_80pct"]],
            "events": [{"x": "2026-07-31", "label": "Jul 15 · price change announced"}, {"x": "2026-09-30", "label": "Sep 1 · existing Starter re-priced"}],
        },
        "waterfall": [
            {"label": "Jul", "value": jul_mrr, "total": True},
            {"label": "New", "value": float(aug.new_mrr)},
            {"label": "Expans.", "value": float(aug.expansion_mrr)},
            {"label": "Contr.", "value": float(aug.contraction_mrr)},
            {"label": "Churn", "value": float(aug.churned_mrr)},
            {"label": "Aug", "value": float(aug.mrr), "total": True},
        ],
        "churn": {"x": did["series"]["months"][1:], "treated": did["series"]["treated"][1:], "control": did["series"]["control"][1:]},
        "ledger": [
            {"label": "Re-pricing uplift", "value": imp["repricing_uplift_mrr"]},
            {"label": "Excess churn · Aug", "value": -imp["excess_churned_mrr_by_month"]["2026-08-31"]},
            {"label": "Excess churn · Sep", "value": -imp["excess_churned_mrr_by_month"]["2026-09-30"]},
            {"label": "Excess churn · Oct", "value": -imp["excess_churned_mrr_by_month"]["2026-10-31"]},
            {"label": "Net effect", "value": imp["net_run_rate_mrr"], "total": True},
        ],
        "table": [{"segment": r.segment, "plan": r.plan, "jul": r.mrr_jul, "aug": r.mrr_aug, "oct": r.mrr_oct, "accounts": int(r.accounts_oct)} for r in seg.itertuples()],
    }
    html = TEMPLATE.replace("/*DATA*/null", json.dumps(data, default=float))
    with open(path, "w") as f:
        f.write(html)
    return path


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MRR & Starter price change — Data Factory demo</title>
<style>
.viz-root{color-scheme:light;--surface-0:#f4f3f0;--surface-1:#fcfcfb;--border:#e4e2dc;--text-primary:#0b0b0b;--text-secondary:#52514e;--text-muted:#7a7974;
--grid:#ebe9e4;--series-1:#2a78d6;--series-2:#eb6834;--pos:#2a78d6;--neg:#e34948;--total:#52514e;--serious:#ec835a;--good:#0ca30c;--band:rgba(42,120,214,.14)}
@media (prefers-color-scheme:dark){.viz-root{color-scheme:dark;--surface-0:#111110;--surface-1:#1a1a19;--border:#2e2e2b;--text-primary:#f0efec;--text-secondary:#c3c2b7;
--text-muted:#8f8e86;--grid:#2a2a27;--series-1:#3987e5;--series-2:#d95926;--pos:#3987e5;--neg:#e66767;--total:#c3c2b7;--band:rgba(57,135,229,.2)}}
*{box-sizing:border-box}body{margin:0}
.viz-root{background:var(--surface-0);color:var(--text-primary);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;padding:28px;min-height:100vh}
header{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px;margin-bottom:20px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:15px;margin:0 0 2px}.sub{color:var(--text-secondary);font-size:13px;margin:0 0 10px}
.meta{color:var(--text-muted);font-size:12px;text-align:right}
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:12px}
.card{background:var(--surface-1);border:1px solid var(--border);border-radius:12px;padding:16px}
.kpi .l{color:var(--text-secondary);font-size:12px}.kpi .v{font-size:26px;font-weight:650;margin:4px 0 2px;font-variant-numeric:tabular-nums}
.kpi .d{font-size:12px;color:var(--text-secondary)}.st{display:inline-flex;gap:4px;align-items:center}.st i{font-style:normal;font-weight:700}
.st.serious i{color:var(--serious)}.st.good i{color:var(--good)}
.grid{display:grid;grid-template-columns:2fr 1fr;gap:12px;margin-bottom:12px}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}
svg{display:block;width:100%;height:auto;overflow:visible}svg text{fill:var(--text-muted);font-size:11px}
.legend{display:flex;gap:14px;font-size:12px;color:var(--text-secondary);margin:6px 0 0}.sw{display:inline-block;width:14px;height:3px;border-radius:2px;vertical-align:middle;margin-right:6px}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}th,td{padding:7px 8px;text-align:right;border-bottom:1px solid var(--border)}
th:first-child,td:first-child,th:nth-child(2),td:nth-child(2){text-align:left}th{color:var(--text-secondary);font-weight:600;font-size:12px}
#tip{position:fixed;pointer-events:none;background:var(--surface-1);border:1px solid var(--border);border-radius:8px;padding:8px 10px;font-size:12px;
box-shadow:0 4px 16px rgba(0,0,0,.12);display:none;z-index:9;color:var(--text-primary)}
footer{color:var(--text-muted);font-size:12px;margin-top:8px}
@media (max-width:900px){.kpis{grid-template-columns:repeat(2,1fr)}.grid,.grid2{grid-template-columns:1fr}}
</style></head>
<body><div class="viz-root">
<header><div><h1>Why did MRR drop in August — and did the Starter price change pay off?</h1>
<p class="sub">Clean MRR (test & internal accounts excluded) · Jan 2025 – Oct 2026 · forecast to Dec 2026</p></div>
<div class="meta">Data as of <b id="asof"></b><br>Built <span id="built"></span> by the Data Factory</div></header>
<section class="kpis" id="kpis"></section>
<section class="grid">
  <div class="card"><h2>MRR recovered in September — on price, not on retention</h2><p class="sub">Month-end MRR, USD · dashed = base forecast with 80% interval</p><div id="trend"></div></div>
  <div class="card"><h2>August: churn more than doubled</h2><p class="sub">MRR bridge, Jul → Aug 2026 · axis truncated</p><div id="wf"></div></div>
</section>
<section class="grid2">
  <div class="card"><h2>Starter monthly churn spiked after the announcement</h2><p class="sub">Monthly logo churn rate · re-priced group vs a comparable group that was not re-priced</p><div id="churn"></div>
  <div class="legend"><span><span class="sw" style="background:var(--series-1)"></span>SMB Starter · monthly (re-priced)</span><span><span class="sw" style="background:var(--series-2)"></span>SMB Growth · monthly (comparison)</span></div></div>
  <div class="card"><h2>So far, the price change costs more than it earns</h2><p class="sub">Monthly recurring effect at Oct run-rate, USD (difference-in-differences estimate)</p><div id="ledger"></div></div>
</section>
<section class="card"><h2>MRR by segment & plan</h2><p class="sub">Month-end MRR, USD</p><table id="tbl"></table></section>
<footer>Reference output of the Data Factory demo run · numbers re-derived independently by the Quality Inspector · synthetic data.</footer>
<div id="tip"></div>
</div>
<script>
const DATA=/*DATA*/null;
const $=s=>document.querySelector(s),tip=$('#tip');
const money=v=>(v<0?'−':'')+'$'+(Math.abs(v)>=1e6?(Math.abs(v)/1e6).toFixed(2)+'M':Math.abs(v)>=1e3?(Math.abs(v)/1e3).toFixed(1)+'k':Math.abs(v).toFixed(0));
const pct=v=>(v*100).toFixed(1)+'%';const mon=s=>new Date(s+'T00:00:00Z').toLocaleString('en',{month:'short',year:'2-digit',timeZone:'UTC'});
const showTip=(e,html)=>{tip.innerHTML=html;tip.style.display='block';tip.style.left=Math.min(e.clientX+14,innerWidth-220)+'px';tip.style.top=(e.clientY+14)+'px'};
const hideTip=()=>tip.style.display='none';
const el=(t,a={},p)=>{const n=document.createElementNS('http://www.w3.org/2000/svg',t);for(const k in a)n.setAttribute(k,a[k]);p&&p.appendChild(n);return n};
function scale(d0,d1,r0,r1){return v=>r0+(v-d0)/(d1-d0)*(r1-r0)}
function ticks(min,max,n=4){const s=Math.pow(10,Math.floor(Math.log10((max-min)/n)));const st=[1,2,2.5,5,10].map(m=>m*s).find(x=>(max-min)/x<=n)||s*10;
  const out=[];for(let v=Math.ceil(min/st)*st;v<=max+1e-9;v+=st)out.push(v);return out}
/* KPI tiles */
$('#asof').textContent=DATA.asOf;$('#built').textContent=DATA.builtAt;
$('#kpis').innerHTML=DATA.kpis.map(k=>{const v=k.fmt==='pct'?pct(k.value):money(k.value);
 let d=k.delta!=null?`${k.delta>=0?'▲':'▼'} ${pct(Math.abs(k.delta))} ${k.deltaLabel}`:k.note||'';
 if(k.status)d=`<span class="st ${k.status}"><i>${k.status==='good'?'✓':'!'}</i>${k.status==='good'?'On track':'Needs attention'}</span> · ${k.note}`;
 return `<div class="card kpi"><div class="l">${k.label}</div><div class="v">${v}</div><div class="d">${d}</div></div>`}).join('');
/* line chart */
function line(id,{x,series,band,events,yfmt,ymin}){const W=640,H=260,m={l:56,r:16,t:14,b:26};const svg=el('svg',{viewBox:`0 0 ${W} ${H}`},$(id));
 const vals=series.flatMap(s=>s.values).concat((band||[]).flat()).filter(v=>v!=null);let lo=ymin??Math.min(...vals),hi=Math.max(...vals);const pad=(hi-lo)*.08;lo-=ymin!=null?0:pad;hi+=pad;
 const X=scale(0,x.length-1,m.l,W-m.r),Y=scale(lo,hi,H-m.b,m.t);
 ticks(lo,hi).forEach(t=>{el('line',{x1:m.l,x2:W-m.r,y1:Y(t),y2:Y(t),stroke:'var(--grid)'},svg);el('text',{x:m.l-8,y:Y(t)+4,'text-anchor':'end'},svg).textContent=yfmt(t)});
 x.forEach((d,i)=>{if(i%3===0)el('text',{x:X(i),y:H-6,'text-anchor':'middle'},svg).textContent=mon(d)});
 (events||[]).forEach(ev=>{const i=x.indexOf(ev.x);el('line',{x1:X(i),x2:X(i),y1:m.t,y2:H-m.b,stroke:'var(--text-muted)','stroke-dasharray':'2 3'},svg);
   el('text',{x:X(i)-5,y:H-m.b-8-(events.length-1-events.indexOf(ev))*14,'text-anchor':'end'},svg).textContent=ev.label});
 if(band){let up='',dn='';band.forEach((b,i)=>{if(b){up+=`${up?'L':'M'}${X(i)},${Y(b[1])}`;dn=`L${X(i)},${Y(b[0])}`+dn}});
   const first=band.findIndex(b=>b);el('path',{d:`M${X(first-1)},${Y(series[1].values[first-1])}`+up.replace(/^M/,'L')+dn+'Z',fill:'var(--band)'},svg)}
 series.forEach(s=>{let d='';s.values.forEach((v,i)=>{if(v!=null)d+=`${d?'L':'M'}${X(i)},${Y(v)}`});
   el('path',{d,fill:'none',stroke:s.color,'stroke-width':2,'stroke-dasharray':s.dashed?'5 4':'','stroke-linejoin':'round'},svg);
   const li=s.values.map((v,i)=>v!=null?i:-1).filter(i=>i>=0).pop();if(s.label)el('text',{x:X(li)+6,y:Y(s.values[li])+4,style:'fill:var(--text-secondary)'},svg).textContent=s.label});
 const cross=el('line',{y1:m.t,y2:H-m.b,stroke:'var(--text-muted)',opacity:0},svg);const dots=series.map(s=>el('circle',{r:4,fill:s.color,stroke:'var(--surface-1)','stroke-width':2,opacity:0},svg));
 const hit=el('rect',{x:m.l,y:m.t,width:W-m.l-m.r,height:H-m.t-m.b,fill:'transparent'},svg);
 hit.addEventListener('mousemove',e=>{const r=svg.getBoundingClientRect();const px=(e.clientX-r.left)/r.width*W;const i=Math.max(0,Math.min(x.length-1,Math.round((px-m.l)/(W-m.l-m.r)*(x.length-1))));
   cross.setAttribute('x1',X(i));cross.setAttribute('x2',X(i));cross.setAttribute('opacity',.5);
   let html=`<b>${mon(x[i])}</b>`;series.forEach((s,j)=>{const v=s.values[i];dots[j].setAttribute('opacity',v!=null?1:0);if(v!=null){dots[j].setAttribute('cx',X(i));dots[j].setAttribute('cy',Y(v));
     html+=`<br><span class="sw" style="background:${s.color}"></span>${s.name}: <b>${yfmt(v,true)}</b>`}});
   if(band&&band[i])html+=`<br>80% interval: ${yfmt(band[i][0],true)} – ${yfmt(band[i][1],true)}`;showTip(e,html)});
 hit.addEventListener('mouseleave',()=>{hideTip();cross.setAttribute('opacity',0);dots.forEach(d=>d.setAttribute('opacity',0))})}
/* waterfall (vertical) and ledger (horizontal) */
function waterfall(id,items,{horizontal=false}={}){const W=horizontal?520:420,H=horizontal?230:260,m=horizontal?{l:128,r:70,t:6,b:6}:{l:50,r:8,t:18,b:26};
 const svg=el('svg',{viewBox:`0 0 ${W} ${H}`},$(id));let run=0,lo,hi;let segs=items.map(it=>{let a,b;if(horizontal){a=0;b=it.value}else if(it.total){a=null;b=it.value;run=it.value}else{a=run;b=run+it.value;run=b}return{...it,a,b}});
 if(horizontal){lo=Math.min(0,...segs.map(s=>s.b));hi=Math.max(0,...segs.map(s=>s.b))}
 else{const v=segs.flatMap(s=>[s.a,s.b]).filter(x=>x!=null);lo=Math.min(...v)-(Math.max(...v)-Math.min(...v))*.35;hi=Math.max(...v)+(Math.max(...v)-Math.min(...v))*.08;segs=segs.map(s=>s.a==null?{...s,a:lo}:s)}
 const n=segs.length,band=(horizontal?H-m.t-m.b:W-m.l-m.r)/n,bw=band*.62;
 const V=horizontal?scale(lo,hi,m.l,W-m.r):scale(lo,hi,H-m.b,m.t);
 if(horizontal)el('line',{x1:V(0),x2:V(0),y1:m.t,y2:H-m.b,stroke:'var(--text-muted)'},svg);
 else ticks(lo,hi,4).forEach(t=>{el('line',{x1:m.l,x2:W-m.r,y1:V(t),y2:V(t),stroke:'var(--grid)'},svg);el('text',{x:m.l-6,y:V(t)+4,'text-anchor':'end'},svg).textContent=money(t)});
 segs.forEach((s,i)=>{const c=s.total?'var(--total)':s.value>=0?'var(--pos)':'var(--neg)';const p0=Math.min(V(s.a),V(s.b)),len=Math.max(2,Math.abs(V(s.a)-V(s.b)));
   const r=horizontal?el('rect',{x:p0,y:m.t+i*band+(band-bw)/2,width:len,height:bw,rx:3,fill:c},svg):el('rect',{x:m.l+i*band+(band-bw)/2,y:p0,width:bw,height:len,rx:3,fill:c},svg);
   const lab=(s.value>=0&&!s.total?'+':'')+money(s.value);
   if(horizontal){el('text',{x:m.l-8,y:m.t+i*band+band/2+4,'text-anchor':'end',style:'fill:var(--text-secondary)'},svg).textContent=s.label;
     el('text',{x:W-4,y:m.t+i*band+band/2+4,'text-anchor':'end',style:'fill:var(--text-primary);font-weight:600'},svg).textContent=lab}
   else{el('text',{x:m.l+i*band+band/2,y:H-8,'text-anchor':'middle'},svg).textContent=s.label;el('text',{x:m.l+i*band+band/2,y:p0-5,'text-anchor':'middle',style:'fill:var(--text-primary)'},svg).textContent=lab}
   r.addEventListener('mousemove',e=>showTip(e,`<b>${s.label}</b><br>${lab}`));r.addEventListener('mouseleave',hideTip)})}
const T=DATA.trend;
line('#trend',{x:T.x,series:[{name:'Actual MRR',values:T.actual,color:'var(--series-1)'},{name:'Forecast (base)',values:T.forecast,color:'var(--series-1)',dashed:true}],band:T.band,events:T.events,yfmt:(v,f)=>f?money(v):'$'+(v/1e6).toFixed(1)+'M'});
waterfall('#wf',DATA.waterfall);
line('#churn',{x:DATA.churn.x,series:[{name:'Starter · monthly',values:DATA.churn.treated,color:'var(--series-1)',label:'Starter'},{name:'Growth · monthly',values:DATA.churn.control,color:'var(--series-2)',label:'Growth'}],events:[T.events[0]],yfmt:v=>pct(v),ymin:0});
waterfall('#ledger',DATA.ledger,{horizontal:true});
$('#tbl').innerHTML='<tr><th>Segment</th><th>Plan</th><th>Jul</th><th>Aug</th><th>Oct</th><th>Δ Jul→Aug</th><th>Accounts (Oct)</th></tr>'+DATA.table.map(r=>
 `<tr><td>${r.segment}</td><td>${r.plan}</td><td>${money(r.jul)}</td><td>${money(r.aug)}</td><td>${money(r.oct)}</td><td>${(r.aug-r.jul>=0?'+':'')+money(r.aug-r.jul)}</td><td>${r.accounts.toLocaleString()}</td></tr>`).join('');
</script></body></html>
"""
