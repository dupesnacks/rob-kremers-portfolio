import { useState, useEffect, useCallback, useRef } from "react";

// ═══════════════════════════════════════════════════════════
// API CONFIG — Change this to your backend URL
// ═══════════════════════════════════════════════════════════
const API_BASE = "http://localhost:8000";

// ═══════════════════════════════════════════════════════════
// API CLIENT
// ═══════════════════════════════════════════════════════════
async function api(path, opts = {}) {
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...opts,
      headers: { "Content-Type": "application/json", ...opts.headers },
    });
    if (!res.ok) throw new Error(`${res.status}`);
    return await res.json();
  } catch (e) {
    console.warn(`API ${path} failed:`, e.message);
    return null;
  }
}

async function fetchBias() { return api("/api/bias"); }
async function fetchOutfits(limit = 22) { return api(`/api/outfits?limit=${limit}`); }
async function fetchTickers(limit = 50) { return api(`/api/tickers?limit=${limit}`); }
async function fetchSignals(limit = 50) { return api(`/api/signals?limit=${limit}`); }
async function fetchHealth() { return api("/api/health"); }
async function fetchTickerDetail(sym) { return api(`/api/ticker/${sym}`); }
async function triggerScan(mode = "light", tickers, timeframes) {
  let url = `/api/scan?mode=${mode}`;
  if (tickers) url += `&tickers=${tickers}`;
  if (timeframes) url += `&timeframes=${timeframes}`;
  return api(url, { method: "POST" });
}
async function fetchScanStatus() { return api("/api/scan/status"); }

// ═══════════════════════════════════════════════════════════
// MOCK DATA (fallback when backend is offline)
// ═══════════════════════════════════════════════════════════
const pick = a => a[Math.floor(Math.random() * a.length)];
const rnd = (a, b) => a + Math.random() * (b - a);

function mockOutfits() {
  const data = [
    { rank:1, sequence:"Base 2/NVDA", key:"base2", category:"core", smas:[16,32,64,128,256,512], total:1615, long:769, short:846, ls_ratio:0.91, slope:"Falling", struct_bias:"Bearish", key_smas:"16/32/64/128/256/512", price_pos:"Below", bias:"Neutral", dom_tkr:"UPRO" },
    { rank:2, sequence:"Waring's Problem", key:"waring", category:"core", smas:[19,37,73,143,279,548], total:1578, long:749, short:829, ls_ratio:0.90, slope:"Falling", struct_bias:"Bullish", key_smas:"19/37/73/143/279/548", price_pos:"Above", bias:"Neutral", dom_tkr:"SDOW" },
    { rank:3, sequence:"Time (144)", key:"time144", category:"core", smas:[18,36,72,144,288,576], total:1568, long:746, short:822, ls_ratio:0.91, slope:"Falling", struct_bias:"Bullish", key_smas:"18/36/72/144/288/576", price_pos:"Above", bias:"Neutral", dom_tkr:"SDOW" },
    { rank:4, sequence:"AN (11s)", key:"an11", category:"angel", smas:[11,44,88,111,444,888], total:1463, long:712, short:751, ls_ratio:0.95, slope:"Falling", struct_bias:"Bearish", key_smas:"11/44/88/111/444/888", price_pos:"Below", bias:"Neutral", dom_tkr:"SOXS" },
    { rank:5, sequence:"Time (365)", key:"time365", category:"core", smas:[23,46,91,183,365,730], total:1353, long:653, short:700, ls_ratio:0.93, slope:"Falling", struct_bias:"Bearish", key_smas:"23/46/91/183/365/730", price_pos:"Below", bias:"Neutral", dom_tkr:"SQQQ" },
    { rank:6, sequence:"US President (47)", key:"pres47", category:"political", smas:[24,47,94,188,376,752], total:1345, long:653, short:692, ls_ratio:0.94, slope:"Falling", struct_bias:"Neutral", key_smas:"24/47/94/188/376/752", price_pos:"Above", bias:"Neutral", dom_tkr:"SDOW" },
    { rank:7, sequence:"AN (22s)", key:"an22", category:"angel", smas:[22,55,77,222,555,777], total:1335, long:637, short:698, ls_ratio:0.91, slope:"Falling", struct_bias:"Neutral", key_smas:"22/55/77/222/555/777", price_pos:"Below", bias:"Neutral", dom_tkr:"UPRO" },
    { rank:8, sequence:"S&P", key:"sp", category:"system", smas:[10,50,200], total:1034, long:510, short:524, ls_ratio:0.97, slope:"Falling", struct_bias:"Bearish", key_smas:"10/50/200", price_pos:"Below", bias:"Neutral", dom_tkr:"SQQQ" },
    { rank:9, sequence:"NAS", key:"nas", category:"system", smas:[20,100,250], total:862, long:388, short:474, ls_ratio:0.82, slope:"Falling", struct_bias:"Neutral", key_smas:"20/100/250", price_pos:"Below", bias:"Neutral", dom_tkr:"UPRO" },
    { rank:10, sequence:"DJI", key:"dji", category:"system", smas:[30,60,90,300,600,900], total:1169, long:553, short:616, ls_ratio:0.90, slope:"Falling", struct_bias:"N/A", key_smas:"30/60/90/300/600/900", price_pos:"N/A", bias:"Neutral", dom_tkr:"SPY" },
  ];
  return data.map(d => ({ ...d, seq: d.sequence, cat: d.category, struct: d.struct_bias, pricePos: d.price_pos, domTkr: d.dom_tkr, ls: d.ls_ratio }));
}

function mockTickers() {
  const data = [
    { rank:1, ticker:"UVIX", total:1733, long:244, short:1489, ls_ratio:0.16, dom_outfit:"Waring's Problem", dom_outfit_key:"waring", key_smas:"19/37/73/143/279/548", slope:"Falling", struct_bias:"Neutral", price_pos:"Above", bias:"Exhaustion" },
    { rank:2, ticker:"BITO", total:1729, long:1686, short:43, ls_ratio:39.21, dom_outfit:"Base 2/NVDA", dom_outfit_key:"base2", key_smas:"16/32/64/128/256/512", slope:"Rising", struct_bias:"Bullish", price_pos:"Above", bias:"Exhaustion" },
    { rank:3, ticker:"IWM", total:1729, long:1586, short:143, ls_ratio:11.09, dom_outfit:"Base 2/NVDA", dom_outfit_key:"base2", key_smas:"16/32/64/128/256/512", slope:"Rising", struct_bias:"Neutral", price_pos:"Below", bias:"Exhaustion" },
    { rank:4, ticker:"SOXS", total:1727, long:99, short:1628, ls_ratio:0.06, dom_outfit:"Base 2/NVDA", dom_outfit_key:"base2", key_smas:"16/32/64/128/256/512", slope:"Falling", struct_bias:"Bearish", price_pos:"Below", bias:"Exhaustion" },
    { rank:5, ticker:"TSLA", total:1024, long:658, short:366, ls_ratio:1.80, dom_outfit:"Base 2/NVDA", dom_outfit_key:"base2", key_smas:"16/32/64/128/256/512", slope:"Falling", struct_bias:"Bullish", price_pos:"Above", bias:"Exhaustion" },
  ];
  return data.map(d => ({ ...d, domOutfit: d.dom_outfit, domKey: d.dom_outfit_key, keySmas: d.key_smas, struct: d.struct_bias, pricePos: d.price_pos, ls: d.ls_ratio, sigs: Math.floor(rnd(0,5)) }));
}

function mockSignals() {
  return [{ id: "mock-0", type: { key: "sma_touch", label: "SMA Touch", color: "#b388ff", icon: "◇" }, ticker: "—", outfit: "No data", tf: "—", sma: "—", price: 0, smaVal: 0, delta: 0, stop: null, time: new Date() }];
}

// ═══════════════════════════════════════════════════════════
// NORMALIZE API → UI (backend uses snake_case, UI uses camelCase)
// ═══════════════════════════════════════════════════════════
function normalizeOutfit(d) {
  return {
    rank: d.rank, seq: d.sequence, key: d.key, cat: d.category,
    smas: d.smas, total: d.total, long: d.long, short: d.short,
    ls: d.ls_ratio, slope: d.slope, struct: d.struct_bias,
    keySmas: d.key_smas, pricePos: d.price_pos, bias: d.bias,
    domTkr: d.dom_tkr,
  };
}

function normalizeTicker(d) {
  return {
    rank: d.rank, ticker: d.ticker, total: d.total, long: d.long,
    short: d.short, ls: d.ls_ratio, domOutfit: d.dom_outfit,
    domKey: d.dom_outfit_key, keySmas: d.key_smas, slope: d.slope,
    struct: d.struct_bias, pricePos: d.price_pos, bias: d.bias,
    sigs: d.active_signals || 0,
  };
}

const SIGNAL_COLOR = {
  precision_buy: { label: "Precision Buy", color: "#00e676", icon: "▲" },
  auto_short: { label: "Auto Short", color: "#ff1744", icon: "▼" },
  hard_stop: { label: "Hard Stop", color: "#ff9100", icon: "⊘" },
  optimized_buy: { label: "Optimized Buy", color: "#00e5ff", icon: "◆" },
  sma_touch: { label: "SMA Touch", color: "#b388ff", icon: "◇" },
  crossover: { label: "Crossover", color: "#ffd600", icon: "✕" },
  long: { label: "Long Hit", color: "#00e676", icon: "▲" },
  short: { label: "Short Hit", color: "#ff1744", icon: "▼" },
};

function normalizeSignal(d, i) {
  const typeInfo = SIGNAL_COLOR[d.side] || SIGNAL_COLOR.sma_touch;
  return {
    id: `sig-${i}-${d.timestamp || Date.now()}`,
    type: typeInfo, ticker: d.ticker, outfit: d.outfit_name,
    tf: d.timeframe, sma: `MA${d.sma_period}`,
    price: d.ohlc_value, smaVal: d.sma_value, delta: d.delta,
    stop: null, time: new Date(d.timestamp || Date.now()),
  };
}

// ═══════════════════════════════════════════════════════════
// COLORS & STYLING
// ═══════════════════════════════════════════════════════════
const C = {
  bg: "#06090f", bgCard: "#0c1119", bgAlt: "#101724", bgHover: "#141e30",
  bgHeader: "#080c14", border: "#162033", borderHi: "#1e3050",
  text: "#b8c4d8", textDim: "#4e5c74", textBright: "#e4eaf4", textWhite: "#f4f6fa",
  green: "#00e676", greenBg: "rgba(0,230,118,0.06)", greenBd: "rgba(0,230,118,0.2)",
  red: "#ff1744", redBg: "rgba(255,23,68,0.06)", redBd: "rgba(255,23,68,0.2)",
  yellow: "#ffd600", yellowBg: "rgba(255,214,0,0.06)", yellowBd: "rgba(255,214,0,0.2)",
  blue: "#448aff", blueBg: "rgba(68,138,255,0.06)", blueBd: "rgba(68,138,255,0.2)",
  cyan: "#00e5ff", cyanDim: "rgba(0,229,255,0.12)", cyanBd: "rgba(0,229,255,0.25)",
  orange: "#ff9100", purple: "#b388ff",
};
const mono = "'JetBrains Mono', 'Fira Code', monospace";

// ═══════════════════════════════════════════════════════════
// SMALL COMPONENTS
// ═══════════════════════════════════════════════════════════
function Chip({ value, lg }) {
  const m = { Bearish:[C.redBg,C.redBd,C.red], Bullish:[C.greenBg,C.greenBd,C.green], Neutral:[C.yellowBg,C.yellowBd,C.yellow], Exhaustion:[C.blueBg,C.blueBd,C.blue], "N/A":["transparent",C.border,C.textDim] };
  const [bg,bd,c] = m[value]||m["N/A"];
  return <span style={{ display:"inline-block", padding:lg?"4px 12px":"2px 7px", borderRadius:"3px", background:bg, border:`1px solid ${bd}`, color:c, fontSize:lg?"11px":"9.5px", fontWeight:700, fontFamily:mono, letterSpacing:"0.4px", textTransform:"uppercase" }}>{value}</span>;
}
function Slope({ v }) { const u=v==="Rising"; return <span style={{ color:u?C.green:C.red, fontFamily:mono, fontSize:"10px", fontWeight:700 }}>{u?"▲":"▼"} {v}</span>; }
function Rank({ n }) { const top=n<=3; const cols={1:C.cyan,2:C.blue,3:C.purple}; const c=cols[n]||C.textDim; return <span style={{ display:"inline-flex", alignItems:"center", justifyContent:"center", width:"24px", height:"24px", borderRadius:"4px", fontSize:"10px", fontWeight:800, fontFamily:mono, background:top?`${c}15`:"transparent", color:c, border:`1px solid ${top?`${c}40`:C.border}` }}>{n}</span>; }
function Bar({ long, total }) { const p=total>0?(long/total)*100:50; return <div style={{ display:"flex", alignItems:"center", gap:"5px", width:"80px" }}><div style={{ flex:1, height:"3px", background:`${C.red}25`, borderRadius:"2px", overflow:"hidden" }}><div style={{ width:`${p}%`, height:"100%", borderRadius:"2px", background:p>60?C.green:p<40?C.red:C.yellow, transition:"width 0.4s" }}/></div><span style={{ fontSize:"8px", color:C.textDim, fontFamily:mono, width:"24px", textAlign:"right" }}>{p.toFixed(0)}%</span></div>; }
function Cat({ c }) { const m={ system:[C.cyan,"SYS"], core:[C.blue,"CORE"], angel:[C.purple,"AN"], political:[C.orange,"POL"], dual:[C.green,"DUAL"] }; const [col,lbl]=m[c]||m.core; return <span style={{ fontSize:"7.5px", fontWeight:800, fontFamily:mono, letterSpacing:"0.8px", padding:"1px 4px", borderRadius:"2px", background:`${col}12`, color:col }}>{lbl}</span>; }
function Dot({ c, pulse }) { return <span style={{ display:"inline-block", width:"6px", height:"6px", borderRadius:"50%", background:c, boxShadow:`0 0 5px ${c}55`, animation:pulse?"pulse 2s ease-in-out infinite":"none" }} />; }

function Feed({ signals }) {
  return <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, height:"100%", display:"flex", flexDirection:"column" }}>
    <div style={{ padding:"10px 14px", borderBottom:`1px solid ${C.border}`, display:"flex", justifyContent:"space-between", alignItems:"center", background:C.bgHeader }}>
      <div style={{ display:"flex", alignItems:"center", gap:"7px" }}><Dot c={C.green} pulse /><span style={{ fontSize:"10px", fontWeight:700, fontFamily:mono, color:C.textBright, letterSpacing:"0.7px" }}>SIGNAL FEED</span></div>
      <span style={{ fontSize:"8px", fontFamily:mono, color:C.textDim }}>{signals.length}</span>
    </div>
    <div style={{ flex:1, overflowY:"auto", padding:"2px 0" }}>
      {signals.map((s,i) => (
        <div key={s.id} style={{ padding:"8px 14px", borderBottom:`1px solid ${C.border}06`, display:"flex", gap:"8px", alignItems:"flex-start", animation:`fadeIn 0.25s ease ${i*0.02}s both`, transition:"background 0.12s" }}
          onMouseEnter={e=>e.currentTarget.style.background=C.bgHover} onMouseLeave={e=>e.currentTarget.style.background="transparent"}>
          <div style={{ width:"24px", height:"24px", borderRadius:"5px", flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center", background:`${s.type.color}10`, border:`1px solid ${s.type.color}25`, color:s.type.color, fontSize:"11px", fontWeight:700 }}>{s.type.icon}</div>
          <div style={{ flex:1, minWidth:0 }}>
            <div style={{ display:"flex", alignItems:"center", gap:"5px", marginBottom:"2px", flexWrap:"wrap" }}>
              <span style={{ fontFamily:mono, fontSize:"11px", fontWeight:700, color:C.textWhite }}>{s.ticker}</span>
              <span style={{ fontFamily:mono, fontSize:"8px", fontWeight:700, color:s.type.color, letterSpacing:"0.4px", padding:"0px 4px", borderRadius:"2px", background:`${s.type.color}12` }}>{s.type.label.toUpperCase()}</span>
              <span style={{ fontFamily:mono, fontSize:"9px", color:C.textDim }}>{s.tf}</span>
            </div>
            <div style={{ fontFamily:mono, fontSize:"9.5px", color:C.text, lineHeight:1.4 }}>
              {s.sma} at <span style={{ color:C.textBright, fontWeight:600 }}>{s.price}</span>
              {" "}[<span style={{ color:s.delta>=0?C.green:C.red, fontWeight:600 }}>{s.delta>=0?"+":""}{s.delta}</span>]
              <span style={{ color:C.textDim }}> · {s.outfit}</span>
            </div>
          </div>
          <span style={{ fontFamily:mono, fontSize:"8px", color:C.textDim, flexShrink:0 }}>
            {s.time.toLocaleTimeString([], { hour:"2-digit", minute:"2-digit", second:"2-digit" })}
          </span>
        </div>
      ))}
    </div>
  </div>;
}

function Modal({ ticker, data, signals, onClose }) {
  if (!data) return null;
  const ts = signals.filter(s => s.ticker === ticker).slice(0, 10);
  return <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.88)", zIndex:1000, display:"flex", alignItems:"center", justifyContent:"center", backdropFilter:"blur(10px)", animation:"fadeIn 0.15s ease" }} onClick={onClose}>
    <div style={{ background:C.bgCard, border:`1px solid ${C.borderHi}`, borderRadius:"10px", width:"min(780px, 92vw)", maxHeight:"85vh", overflow:"auto", animation:"slideUp 0.2s ease" }} onClick={e=>e.stopPropagation()}>
      <div style={{ padding:"18px 22px", borderBottom:`1px solid ${C.border}`, display:"flex", justifyContent:"space-between", alignItems:"center", background:C.bgHeader, borderRadius:"10px 10px 0 0" }}>
        <div style={{ display:"flex", alignItems:"center", gap:"12px" }}>
          <span style={{ fontFamily:mono, fontSize:"24px", fontWeight:800, color:C.textWhite }}>{ticker}</span>
          <Chip value={data.bias} lg /><Slope v={data.slope} />
        </div>
        <button onClick={onClose} style={{ background:C.bg, border:`1px solid ${C.border}`, borderRadius:"5px", color:C.textDim, cursor:"pointer", padding:"5px 9px", fontSize:"12px", fontFamily:mono }}>ESC</button>
      </div>
      <div style={{ padding:"18px 22px" }}>
        <div style={{ display:"grid", gridTemplateColumns:"repeat(4, 1fr)", gap:"8px", marginBottom:"16px" }}>
          {[["TOTAL",data.total,C.textWhite],["LONG",data.long,C.green],["SHORT",data.short,C.red],["L/S",data.ls,data.ls>1?C.green:C.red]].map(([l,v,c])=>(
            <div key={l} style={{ background:C.bg, border:`1px solid ${C.border}`, borderRadius:"5px", padding:"10px 12px" }}>
              <div style={{ fontSize:"8px", fontWeight:700, letterSpacing:"1px", color:C.textDim, fontFamily:mono, marginBottom:"3px" }}>{l}</div>
              <div style={{ fontSize:"18px", fontWeight:800, color:c, fontFamily:mono }}>{typeof v==="number"&&v>99?v.toLocaleString():v}</div>
            </div>
          ))}
        </div>
        <div style={{ background:C.bg, border:`1px solid ${C.border}`, borderRadius:"5px", padding:"12px", marginBottom:"12px" }}>
          <div style={{ fontSize:"8px", fontWeight:700, letterSpacing:"1px", color:C.textDim, fontFamily:mono, marginBottom:"6px" }}>DOMINANT OUTFIT</div>
          <div style={{ fontFamily:mono, fontSize:"13px", fontWeight:700, color:C.purple, marginBottom:"3px" }}>{data.domOutfit}</div>
          <div style={{ fontFamily:mono, fontSize:"10px", color:C.textDim }}>{data.keySmas}</div>
        </div>
        <div style={{ background:C.bg, border:`1px solid ${C.border}`, borderRadius:"5px", padding:"12px" }}>
          <div style={{ fontSize:"8px", fontWeight:700, letterSpacing:"1px", color:C.textDim, fontFamily:mono, marginBottom:"8px" }}>RECENT HITS</div>
          {ts.length===0 ? <div style={{ fontFamily:mono, fontSize:"10px", color:C.textDim }}>No recent hits for {ticker}</div>
          : ts.map(s=>(
            <div key={s.id} style={{ display:"flex", alignItems:"center", gap:"7px", padding:"4px 0", borderBottom:`1px solid ${C.border}06`, fontFamily:mono, fontSize:"10px" }}>
              <span style={{ color:s.type.color, fontWeight:700, width:"12px" }}>{s.type.icon}</span>
              <span style={{ color:C.textDim, width:"26px" }}>{s.tf}</span>
              <span style={{ color:C.text }}>{s.sma}</span>
              <span style={{ color:C.textBright, fontWeight:600 }}>{s.price}</span>
              <span style={{ color:s.delta>=0?C.green:C.red }}>[{s.delta>=0?"+":""}{s.delta}]</span>
              <span style={{ color:C.textDim, marginLeft:"auto" }}>{s.time.toLocaleTimeString([], { hour:"2-digit", minute:"2-digit" })}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>;
}

function TH({ children, align, onClick, active, dir }) {
  return <th onClick={onClick} style={{ textAlign:align||"left", padding:"8px 8px", fontSize:"8.5px", fontWeight:700, letterSpacing:"0.8px", textTransform:"uppercase", color:active?C.cyan:C.textDim, borderBottom:`2px solid ${active?C.cyan+"50":C.borderHi}`, background:C.bgHeader, fontFamily:mono, whiteSpace:"nowrap", cursor:onClick?"pointer":"default", userSelect:"none", position:"sticky", top:0, zIndex:2 }}>{children}{active?(dir==="asc"?" ↑":" ↓"):""}</th>;
}
function TD({ children, align, color, fw }) {
  return <td style={{ textAlign:align||"left", padding:"6px 8px", fontSize:"10.5px", fontFamily:mono, color:color||C.text, fontWeight:fw||400, borderBottom:`1px solid ${C.border}06`, whiteSpace:"nowrap" }}>{children}</td>;
}

// ═══════════════════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════════════════
export default function App() {
  const [tab, setTab] = useState("outfits");
  const [oData, setOData] = useState([]);
  const [tData, setTData] = useState([]);
  const [sigs, setSigs] = useState([]);
  const [bias, setBias] = useState(null);
  const [upd, setUpd] = useState(new Date());
  const [live, setLive] = useState(false); // Default manual
  const [filter, setFilter] = useState("");
  const [selTk, setSelTk] = useState(null);
  const [sCol, setSCol] = useState("rank");
  const [sDir, setSDir] = useState("asc");
  const [feed, setFeed] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [connected, setConnected] = useState(false);
  const [scanMode, setScanMode] = useState("light"); // light or full
  const ref = useRef(null);
  const pollRef = useRef(null);

  // ─── Load data from API (or fallback to mock) ───
  const loadData = useCallback(async () => {
    const [oRes, tRes, sRes, bRes] = await Promise.all([
      fetchOutfits(), fetchTickers(), fetchSignals(), fetchBias(),
    ]);

    if (oRes && Array.isArray(oRes) && oRes.length > 0) {
      setOData(oRes.map(normalizeOutfit));
      setConnected(true);
    } else if (oData.length === 0) {
      setOData(mockOutfits());
      setConnected(false);
    }

    if (tRes && Array.isArray(tRes) && tRes.length > 0) {
      setTData(tRes.map(normalizeTicker));
    } else if (tData.length === 0) {
      setTData(mockTickers());
    }

    if (sRes && Array.isArray(sRes) && sRes.length > 0) {
      setSigs(sRes.map(normalizeSignal));
    } else if (sigs.length === 0) {
      setSigs(mockSignals());
    }

    if (bRes) setBias(bRes);

    setUpd(new Date());
  }, []);

  // ─── Initial load ───
  useEffect(() => { loadData(); }, []);

  // ─── Auto-refresh when live ───
  useEffect(() => {
    if (live) ref.current = setInterval(loadData, 15000); // 15s poll
    return () => clearInterval(ref.current);
  }, [live, loadData]);

  // ─── Trigger scan ───
  const doScan = useCallback(async () => {
    setScanning(true);
    const res = await triggerScan(scanMode);
    if (!res) {
      // Backend offline — just show mock data
      setOData(mockOutfits());
      setTData(mockTickers());
      setSigs(mockSignals());
      setScanning(false);
      setUpd(new Date());
      return;
    }

    // Poll for scan completion
    pollRef.current = setInterval(async () => {
      const status = await fetchScanStatus();
      if (status && !status.is_scanning) {
        clearInterval(pollRef.current);
        setScanning(false);
        await loadData(); // Refresh with new scan results
      }
    }, 2000);

    // Safety timeout (5 min max)
    setTimeout(() => {
      clearInterval(pollRef.current);
      setScanning(false);
      loadData();
    }, 300000);
  }, [scanMode, loadData]);

  const sort = col => {
    if (sCol === col) setSDir(d => d === "asc" ? "desc" : "asc");
    else { setSCol(col); setSDir("desc"); }
  };

  const doSort = useCallback(data => [...data].sort((a, b) => {
    let av = a[sCol], bv = b[sCol];
    if (typeof av === "string") return sDir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
    return sDir === "asc" ? (av||0) - (bv||0) : (bv||0) - (av||0);
  }), [sCol, sDir]);

  const fO = doSort(oData.filter(d => (d.seq||"").toLowerCase().includes(filter.toLowerCase())));
  const fT = doSort(tData.filter(d => (d.ticker||"").toLowerCase().includes(filter.toLowerCase())));
  const selData = tData.find(d => d.ticker === selTk);

  const bearN = oData.filter(d => d.bias === "Bearish").length;
  const bullN = oData.filter(d => d.bias === "Bullish").length;
  const ovBias = bias?.overall || (bearN > bullN ? "Bearish" : bullN > bearN ? "Bullish" : "Neutral");
  const bCol = ovBias === "Bearish" ? C.red : ovBias === "Bullish" ? C.green : C.yellow;
  const top = oData[0];

  return (
    <div style={{ minHeight: "100vh", background: C.bg, color: C.text, fontFamily: "'Segoe UI', sans-serif" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');
        @keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
        @keyframes fadeIn{from{opacity:0;transform:translateY(2px)}to{opacity:1;transform:translateY(0)}}
        @keyframes slideUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
        *{box-sizing:border-box;scrollbar-width:thin;scrollbar-color:${C.borderHi} transparent}
        *::-webkit-scrollbar{width:4px;height:4px}
        *::-webkit-scrollbar-thumb{background:${C.borderHi};border-radius:2px}
        input::placeholder{color:${C.textDim}}
        body{margin:0;overflow:hidden}
      `}</style>

      {selTk && <Modal ticker={selTk} data={selData} signals={sigs} onClose={() => setSelTk(null)} />}

      {/* HEADER */}
      <header style={{ borderBottom:`1px solid ${C.border}`, padding:"0 20px", height:"48px", display:"flex", alignItems:"center", justifyContent:"space-between", background:C.bgHeader, position:"sticky", top:0, zIndex:100 }}>
        <div style={{ display:"flex", alignItems:"center", gap:"10px" }}>
          <span style={{ fontFamily:mono, fontSize:"14px", fontWeight:800, color:C.textWhite, display:"flex", alignItems:"center", gap:"7px" }}>
            <span style={{ background:`linear-gradient(135deg,${C.cyan},${C.blue})`, WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent", fontSize:"16px" }}>◆</span>
            SMA OUTFITS
          </span>
          <span style={{ fontFamily:mono, fontSize:"8px", fontWeight:600, color:connected?C.green:C.textDim, letterSpacing:"0.8px", padding:"1px 6px", background:C.bgAlt, borderRadius:"2px", border:`1px solid ${connected?C.greenBd:C.border}` }}>
            {connected ? "● CONNECTED" : "○ MOCK DATA"}
          </span>
        </div>
        <div style={{ display:"flex", alignItems:"center", gap:"8px" }}>
          <input placeholder="Filter..." value={filter} onChange={e => setFilter(e.target.value)}
            style={{ background:C.bg, border:`1px solid ${C.border}`, borderRadius:"4px", padding:"5px 8px 5px 24px", color:C.text, fontSize:"10px", fontFamily:mono, width:"170px", outline:"none" }}
            onFocus={e=>e.target.style.borderColor=C.cyan} onBlur={e=>e.target.style.borderColor=C.border} />

          <button onClick={() => setFeed(!feed)} style={{ background:feed?C.cyanDim:C.bg, border:`1px solid ${feed?C.cyanBd:C.border}`, borderRadius:"4px", padding:"5px 8px", cursor:"pointer", color:feed?C.cyan:C.textDim, fontSize:"9px", fontFamily:mono, fontWeight:700 }}>FEED</button>

          {/* Scan mode toggle */}
          <button onClick={() => setScanMode(m => m === "light" ? "full" : "light")} style={{
            background:C.bg, border:`1px solid ${C.border}`, borderRadius:"4px", padding:"5px 8px",
            cursor:"pointer", color:scanMode === "full" ? C.orange : C.textDim, fontSize:"9px", fontFamily:mono, fontWeight:700,
          }}>{scanMode === "light" ? "LIGHT" : "FULL"}</button>

          {/* Scan button */}
          <button onClick={doScan} disabled={scanning} style={{
            display:"flex", alignItems:"center", gap:"5px",
            background:scanning?"rgba(255,145,0,0.06)":C.bg,
            border:`1px solid ${scanning?C.orange+"44":C.border}`,
            borderRadius:"4px", padding:"5px 10px", cursor:scanning?"wait":"pointer",
            color:scanning?C.orange:C.cyan, fontSize:"9px", fontFamily:mono, fontWeight:700,
            opacity:scanning?0.7:1,
          }}>{scanning ? "⟳ SCANNING..." : "▶ SCAN"}</button>

          <button onClick={() => setLive(!live)} style={{
            display:"flex", alignItems:"center", gap:"5px",
            background:live?C.greenBg:C.bg, border:`1px solid ${live?C.greenBd:C.border}`,
            borderRadius:"4px", padding:"5px 8px", cursor:"pointer",
            color:live?C.green:C.textDim, fontSize:"9px", fontFamily:mono, fontWeight:700,
          }}><Dot c={live?C.green:C.textDim} pulse={live} />{live ? "AUTO 15s" : "MANUAL"}</button>

          <span style={{ fontFamily:mono, fontSize:"9px", color:C.textDim }}>{upd.toLocaleTimeString()} EST</span>
        </div>
      </header>

      <div style={{ display:"flex", height:"calc(100vh - 48px)" }}>
        <div style={{ flex:1, overflow:"auto", padding:"14px 18px" }}>
          {/* Bias strip */}
          <div style={{ display:"flex", gap:"8px", marginBottom:"12px", animation:"fadeIn 0.3s ease" }}>
            <div style={{ background:C.bgCard, border:`1px solid ${bCol}20`, borderLeft:`3px solid ${bCol}`, borderRadius:"5px", padding:"10px 16px", display:"flex", alignItems:"center", gap:"12px" }}>
              <div>
                <div style={{ fontFamily:mono, fontSize:"8px", fontWeight:700, letterSpacing:"1px", color:C.textDim, marginBottom:"3px" }}>OVERALL INSTITUTIONAL BIAS</div>
                <Chip value={ovBias} lg />
              </div>
            </div>
            {[
              { l:"DOM OUTFIT", v:bias?.dominant_outfit || top?.seq, s:bias?.key_smas || top?.keySmas, c:C.textWhite },
              { l:"STRUCT BIAS", v:bias?.struct_bias || top?.struct, c:(v=>(v==="Bearish"?C.red:v==="Bullish"?C.green:C.yellow))(bias?.struct_bias || top?.struct) },
              { l:"PRICE POS", v:bias?.price_position || top?.pricePos, c:(v=>(v==="Below"?C.red:v==="Above"?C.green:C.yellow))(bias?.price_position || top?.pricePos) },
              { l:"SESSION", v:`${upd.toLocaleDateString("en-US",{month:"numeric",day:"numeric",year:"2-digit"})}`, s:connected?"Live via Polygon":"Mock data", c:C.cyan },
            ].map(b => (
              <div key={b.l} style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:"5px", padding:"10px 14px", flex:1, minWidth:"100px" }}>
                <div style={{ fontFamily:mono, fontSize:"8px", fontWeight:700, letterSpacing:"1px", color:C.textDim, marginBottom:"3px" }}>{b.l}</div>
                <div style={{ fontFamily:mono, fontSize:"15px", fontWeight:800, color:b.c, lineHeight:1.1 }}>{b.v || "—"}</div>
                {b.s && <div style={{ fontFamily:mono, fontSize:"8px", color:C.textDim, marginTop:"1px" }}>{b.s}</div>}
              </div>
            ))}
          </div>

          {/* Tabs */}
          <div style={{ display:"flex", gap:"2px", marginBottom:"8px", background:C.bgCard, borderRadius:"5px", padding:"2px", border:`1px solid ${C.border}`, width:"fit-content" }}>
            {[["outfits","OUTFIT RANKING",oData.length],["tickers","TICKER RANKING (SMA 1-999)",tData.length]].map(([k,l,n])=>(
              <button key={k} onClick={()=>{setTab(k);setSCol("rank");setSDir("asc")}} style={{
                background:tab===k?C.cyanDim:"transparent", border:tab===k?`1px solid ${C.cyanBd}`:"1px solid transparent",
                borderRadius:"3px", padding:"5px 14px", cursor:"pointer", color:tab===k?C.cyan:C.textDim,
                fontSize:"9px", fontWeight:700, letterSpacing:"0.7px", fontFamily:mono, display:"flex", alignItems:"center", gap:"5px",
              }}>{l}<span style={{ fontSize:"8px", padding:"0 4px", borderRadius:"2px", background:tab===k?`${C.cyan}18`:C.border }}>{n}</span></button>
            ))}
          </div>

          {/* Table */}
          <div style={{ background:C.bgCard, border:`1px solid ${C.border}`, borderRadius:"6px", overflow:"hidden" }}>
            <div style={{ overflowX:"auto", maxHeight:"calc(100vh - 230px)" }}>
              <table style={{ width:"100%", borderCollapse:"collapse" }}>
                <thead>
                  {tab==="outfits" ? (
                    <tr>
                      <TH onClick={()=>sort("rank")} active={sCol==="rank"} dir={sDir}>#</TH>
                      <TH>Cat</TH>
                      <TH onClick={()=>sort("seq")} active={sCol==="seq"} dir={sDir}>Sequence</TH>
                      <TH align="right" onClick={()=>sort("total")} active={sCol==="total"} dir={sDir}>Total</TH>
                      <TH align="right" onClick={()=>sort("long")} active={sCol==="long"} dir={sDir}>Long</TH>
                      <TH align="right" onClick={()=>sort("short")} active={sCol==="short"} dir={sDir}>Short</TH>
                      <TH align="right" onClick={()=>sort("ls")} active={sCol==="ls"} dir={sDir}>L/S</TH>
                      <TH>Ratio</TH>
                      <TH onClick={()=>sort("slope")} active={sCol==="slope"} dir={sDir}>Slope</TH>
                      <TH onClick={()=>sort("struct")} active={sCol==="struct"} dir={sDir}>Struct</TH>
                      <TH>Key SMAs</TH>
                      <TH onClick={()=>sort("pricePos")} active={sCol==="pricePos"} dir={sDir}>Price</TH>
                      <TH onClick={()=>sort("bias")} active={sCol==="bias"} dir={sDir}>Bias</TH>
                      <TH>Dom Tkr</TH>
                    </tr>
                  ) : (
                    <tr>
                      <TH onClick={()=>sort("rank")} active={sCol==="rank"} dir={sDir}>#</TH>
                      <TH onClick={()=>sort("ticker")} active={sCol==="ticker"} dir={sDir}>Ticker</TH>
                      <TH align="right" onClick={()=>sort("total")} active={sCol==="total"} dir={sDir}>Total</TH>
                      <TH align="right" onClick={()=>sort("long")} active={sCol==="long"} dir={sDir}>Long</TH>
                      <TH align="right" onClick={()=>sort("short")} active={sCol==="short"} dir={sDir}>Short</TH>
                      <TH align="right" onClick={()=>sort("ls")} active={sCol==="ls"} dir={sDir}>L/S</TH>
                      <TH>Ratio</TH>
                      <TH>Dom Outfit</TH>
                      <TH onClick={()=>sort("slope")} active={sCol==="slope"} dir={sDir}>Slope</TH>
                      <TH onClick={()=>sort("struct")} active={sCol==="struct"} dir={sDir}>Struct</TH>
                      <TH>Key SMAs</TH>
                      <TH onClick={()=>sort("pricePos")} active={sCol==="pricePos"} dir={sDir}>Price</TH>
                      <TH onClick={()=>sort("bias")} active={sCol==="bias"} dir={sDir}>Bias</TH>
                      <TH align="right" onClick={()=>sort("sigs")} active={sCol==="sigs"} dir={sDir}>Sigs</TH>
                    </tr>
                  )}
                </thead>
                <tbody>
                  {tab==="outfits" ? fO.map((r,i)=>(
                    <tr key={r.key||i} style={{ animation:`fadeIn 0.15s ease ${i*0.012}s both`, transition:"background 0.1s" }}
                      onMouseEnter={e=>e.currentTarget.style.background=C.bgHover} onMouseLeave={e=>e.currentTarget.style.background="transparent"}>
                      <TD align="center"><Rank n={r.rank} /></TD>
                      <TD><Cat c={r.cat} /></TD>
                      <TD color={C.textWhite} fw={700}>{r.seq}</TD>
                      <TD align="right" color={C.textWhite} fw={700}>{(r.total||0).toLocaleString()}</TD>
                      <TD align="right" color={C.green}>{(r.long||0).toLocaleString()}</TD>
                      <TD align="right" color={C.red}>{(r.short||0).toLocaleString()}</TD>
                      <TD align="right" color={r.ls>1?C.green:C.red} fw={600}>{r.ls}</TD>
                      <TD><Bar long={r.long} total={r.total} /></TD>
                      <TD><Slope v={r.slope} /></TD>
                      <TD><Chip value={r.struct} /></TD>
                      <TD color={C.textDim}>{r.keySmas}</TD>
                      <TD color={r.pricePos==="Below"?C.red:r.pricePos==="Above"?C.green:C.yellow} fw={600}>{r.pricePos}</TD>
                      <TD><Chip value={r.bias} /></TD>
                      <TD color={C.cyan} fw={600}>{r.domTkr}</TD>
                    </tr>
                  )) : fT.map((r,i)=>(
                    <tr key={r.ticker||i} style={{ animation:`fadeIn 0.15s ease ${i*0.01}s both`, transition:"background 0.1s", cursor:"pointer" }}
                      onClick={()=>setSelTk(r.ticker)}
                      onMouseEnter={e=>e.currentTarget.style.background=C.bgHover} onMouseLeave={e=>e.currentTarget.style.background="transparent"}>
                      <TD align="center"><Rank n={r.rank} /></TD>
                      <TD color={C.cyan} fw={700}>{r.ticker}</TD>
                      <TD align="right" color={C.textWhite} fw={700}>{(r.total||0).toLocaleString()}</TD>
                      <TD align="right" color={C.green}>{(r.long||0).toLocaleString()}</TD>
                      <TD align="right" color={C.red}>{(r.short||0).toLocaleString()}</TD>
                      <TD align="right" color={r.ls>1?C.green:C.red} fw={600}>{r.ls}</TD>
                      <TD><Bar long={r.long} total={r.total} /></TD>
                      <TD color={C.purple} fw={600}>{r.domOutfit}</TD>
                      <TD><Slope v={r.slope} /></TD>
                      <TD><Chip value={r.struct} /></TD>
                      <TD color={C.textDim}>{r.keySmas}</TD>
                      <TD color={r.pricePos==="Below"?C.red:r.pricePos==="Above"?C.green:C.yellow} fw={600}>{r.pricePos}</TD>
                      <TD><Chip value={r.bias} /></TD>
                      <TD align="right" color={r.sigs>3?C.orange:C.textDim} fw={600}>{r.sigs}</TD>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div style={{ display:"flex", justifyContent:"space-between", padding:"6px 2px", fontFamily:mono, fontSize:"8px", color:C.textDim }}>
            <span>SMA 1-999 | {tab==="outfits"?fO.length:fT.length} rows | {connected?"Live":"Mock"} | Scan: {scanMode}</span>
            <span>{connected ? `API: ${API_BASE}` : "Backend offline — showing mock data"} | github.com/raultrades/SMA-outfits</span>
          </div>
        </div>

        {feed && <div style={{ width:"320px", borderLeft:`1px solid ${C.border}`, flexShrink:0, animation:"fadeIn 0.15s ease" }}>
          <Feed signals={sigs} />
        </div>}
      </div>
    </div>
  );
}
