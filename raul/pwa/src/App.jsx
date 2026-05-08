import { useState, useEffect, useCallback, useRef } from "react";

// ═══════════════════════════════════════════════════════════
// API CONFIG
// ═══════════════════════════════════════════════════════════
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function api(path) {
  try {
    const res = await fetch(`${API_BASE}${path}`);
    if (!res.ok) throw new Error(`${res.status}`);
    return await res.json();
  } catch (e) {
    console.warn(`API ${path}:`, e.message);
    return null;
  }
}

async function triggerScan(mode = "light") {
  try {
    const res = await fetch(`${API_BASE}/api/scan?mode=${mode}`, { method: "POST" });
    if (!res.ok) throw new Error(`${res.status}`);
    return await res.json();
  } catch (e) {
    console.warn("Scan failed:", e.message);
    return null;
  }
}

// ═══════════════════════════════════════════════════════════
// COLORS
// ═══════════════════════════════════════════════════════════
const GREEN = "#00e676";
const RED = "#ff1744";
const YELLOW = "#ffd740";
const WHITE = "#e0e0e0";
const DIM = "#555";
const CYAN = "#00e5ff";
const PURPLE = "#b388ff";
const ORANGE = "#ff9100";
const MAGENTA = "#f06292";
const BG = "#0a0a0a";
const BG_EXPAND = "#0e0e0e";
const LINE = "#333";
const FONT = "'JetBrains Mono', 'Fira Code', 'Consolas', monospace";

function biasColor(v) {
  if (!v || v === "N/A") return DIM;
  if (v === "Bullish") return GREEN;
  if (v === "Bearish") return RED;
  if (v === "Neutral") return YELLOW;
  if (v === "Exhaustion") return CYAN;
  return DIM;
}
function slopeColor(v) { return v === "Rising" ? GREEN : v === "Falling" ? RED : DIM; }
function momentumColor(v) { return v === "Rising" ? GREEN : v === "Falling" ? RED : v === "Flat" ? YELLOW : DIM; }
function posColor(v) { return v === "Above" ? GREEN : v === "Below" ? RED : DIM; }
function sideColor(v) { return v === "long" ? GREEN : RED; }
function vixColor(regime) {
  if (regime === "Low") return GREEN;
  if (regime === "Normal") return YELLOW;
  if (regime === "Elevated") return ORANGE;
  if (regime === "Extreme") return RED;
  return DIM;
}
function protocolLabel(p) {
  if (p === "penny_breach") return "PENNY";
  if (p === "point_break") return "POINT";
  if (p === "candle_close") return "CANDLE";
  return p?.toUpperCase() || "—";
}
function protocolColor(p) {
  if (p === "penny_breach") return RED;
  if (p === "point_break") return ORANGE;
  if (p === "candle_close") return YELLOW;
  return DIM;
}

// ═══════════════════════════════════════════════════════════
// SEPARATOR
// ═══════════════════════════════════════════════════════════
const SEP = "═".repeat(160);

// ═══════════════════════════════════════════════════════════
// COLORED TEXT COMPONENT
// ═══════════════════════════════════════════════════════════
function T({ children, c = WHITE, w, align = "left", bold }) {
  return (
    <span style={{
      color: c, width: w, display: "inline-block", textAlign: align,
      flexShrink: 0, fontWeight: bold ? 700 : 400,
      overflow: "hidden", textOverflow: "ellipsis",
      paddingRight: "6px", boxSizing: "border-box",
    }}>
      {children}
    </span>
  );
}

// ═══════════════════════════════════════════════════════════
// WEIGHT BAR
// ═══════════════════════════════════════════════════════════
function WeightBar({ weight, maxWeight, side }) {
  const pct = maxWeight > 0 ? Math.min((weight / maxWeight) * 100, 100) : 0;
  const color = side === "long" ? GREEN : RED;
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: "4px", width: "80px" }}>
      <span style={{
        display: "inline-block", width: "50px", height: "4px",
        background: "#1a1a1a", borderRadius: "2px", overflow: "hidden",
      }}>
        <span style={{
          display: "block", height: "100%", borderRadius: "2px",
          width: `${pct}%`, background: color,
        }} />
      </span>
      <span style={{ fontSize: "10px", color: DIM }}>{weight.toFixed(1)}</span>
    </span>
  );
}

// ═══════════════════════════════════════════════════════════
// TICKER DETAIL — expanded view showing SMA program acting on ticker
// ═══════════════════════════════════════════════════════════
function TickerDetail({ ticker }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api(`/api/ticker/${ticker}`).then(res => {
      if (!cancelled) { setData(res); setLoading(false); }
    });
    return () => { cancelled = true; };
  }, [ticker]);

  if (loading) return (
    <div style={{ padding: "8px 0 8px 44px", color: DIM }}>
      Loading {ticker} signals...
    </div>
  );

  if (!data || !data.signals || data.signals.length === 0) return (
    <div style={{ padding: "8px 0 8px 44px", color: DIM }}>
      No active SMA signals for {ticker}
    </div>
  );

  const signals = data.signals;
  const maxW = Math.max(...signals.map(s => s.weight));
  const longW = signals.filter(s => s.side === "long").reduce((a, s) => a + s.weight, 0);
  const shortW = signals.filter(s => s.side === "short").reduce((a, s) => a + s.weight, 0);
  const longCount = signals.filter(s => s.side === "long").length;
  const shortCount = signals.filter(s => s.side === "short").length;
  const netSide = longW > shortW ? "long" : "short";
  const netColor = netSide === "long" ? GREEN : RED;
  const netLabel = netSide === "long" ? "▲ LONG BIAS" : "▼ SHORT BIAS";

  const byOutfit = {};
  signals.forEach(s => {
    if (!byOutfit[s.outfit]) byOutfit[s.outfit] = [];
    byOutfit[s.outfit].push(s);
  });

  return (
    <div style={{ background: BG_EXPAND, borderTop: `1px solid ${LINE}`, borderBottom: `1px solid ${LINE}`, padding: "8px 0" }}>
      <div style={{ display: "flex", whiteSpace: "nowrap", padding: "2px 0 6px 44px", gap: "24px" }}>
        <span>
          <span style={{ color: DIM }}>SMA PROGRAM ON </span>
          <span style={{ color: CYAN, fontWeight: 700 }}>{ticker}</span>
        </span>
        <span>
          <span style={{ color: DIM }}>Net: </span>
          <span style={{ color: netColor, fontWeight: 700 }}>{netLabel}</span>
        </span>
        <span>
          <span style={{ color: GREEN }}>▲ {longCount} long</span>
          <span style={{ color: DIM }}> ({longW.toFixed(1)}w) </span>
          <span style={{ color: RED }}>▼ {shortCount} short</span>
          <span style={{ color: DIM }}> ({shortW.toFixed(1)}w)</span>
        </span>
        <span>
          <span style={{ color: DIM }}>DOM: </span>
          <span style={{ color: PURPLE }}>{data.dominant_outfit}</span>
        </span>
        <span>
          <span style={{ color: DIM }}>L/S: </span>
          <span style={{ color: data.ls_ratio > 1.5 ? GREEN : data.ls_ratio < 0.67 ? RED : YELLOW }}>
            {data.ls_ratio?.toFixed(2)}
          </span>
        </span>
      </div>

      <div style={{ display: "flex", whiteSpace: "nowrap", padding: "2px 0 2px 44px", color: DIM, fontSize: "10px", borderBottom: `1px solid #1a1a1a` }}>
        <T w="60px" c={DIM}>SIDE</T>
        <T w="150px" c={DIM}>OUTFIT</T>
        <T w="50px" c={DIM}>TF</T>
        <T w="70px" c={DIM}>SMA</T>
        <T w="90px" c={DIM} align="right">PRICE</T>
        <T w="90px" c={DIM} align="right">SMA_VAL</T>
        <T w="80px" c={DIM} align="right">DELTA</T>
        <T w="50px" c={DIM}>OHLC</T>
        <T w="90px" c={DIM}>WEIGHT</T>
      </div>

      {signals.map((s, i) => (
        <div key={i} style={{ display: "flex", whiteSpace: "nowrap", padding: "1px 0 1px 44px", fontSize: "11px" }}>
          <T w="60px" c={sideColor(s.side)} bold>
            {s.side === "long" ? "▲ LONG" : "▼ SHORT"}
          </T>
          <T w="150px" c={PURPLE}>{s.outfit}</T>
          <T w="50px" c={ORANGE}>{s.timeframe}</T>
          <T w="70px" c={WHITE} bold>MA{s.sma_period}</T>
          <T w="90px" c={WHITE} align="right">{s.price?.toFixed(2)}</T>
          <T w="90px" c={DIM} align="right">{s.sma_value?.toFixed(2)}</T>
          <T w="80px" c={s.delta >= 0 ? GREEN : RED} align="right">
            {s.delta >= 0 ? "+" : ""}{s.delta?.toFixed(2)}
          </T>
          <T w="50px" c={DIM}>{s.ohlc}</T>
          <WeightBar weight={s.weight} maxWeight={maxW} side={s.side} />
        </div>
      ))}

      <div style={{ padding: "6px 0 2px 44px", borderTop: `1px solid #1a1a1a`, marginTop: "4px" }}>
        <span style={{ color: DIM, fontSize: "10px" }}>OUTFIT BREAKDOWN: </span>
        {Object.entries(byOutfit).map(([outfit, sigs]) => {
          const oLong = sigs.filter(s => s.side === "long").reduce((a, s) => a + s.weight, 0);
          const oShort = sigs.filter(s => s.side === "short").reduce((a, s) => a + s.weight, 0);
          const oNet = oLong > oShort ? "long" : "short";
          return (
            <span key={outfit} style={{ marginRight: "16px", fontSize: "11px" }}>
              <span style={{ color: PURPLE }}>{outfit}</span>
              <span style={{ color: DIM }}> (</span>
              <span style={{ color: GREEN }}>{oLong.toFixed(1)}L</span>
              <span style={{ color: DIM }}>/</span>
              <span style={{ color: RED }}>{oShort.toFixed(1)}S</span>
              <span style={{ color: DIM }}>) </span>
              <span style={{ color: oNet === "long" ? GREEN : RED }}>
                {oNet === "long" ? "▲" : "▼"}
              </span>
            </span>
          );
        })}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════════════════════
// ACTIVE PROGRAMS SECTION
// ═══════════════════════════════════════════════════════════
function ActiveProgramsSection({ programs, isOpen, onToggle }) {
  const active = (programs || []).filter(p => p.status === "active");
  const terminated = (programs || []).filter(p => p.status === "terminated").slice(0, 10);
  const magnetized = active.filter(p => p.is_magnetized);

  const row = { display: "flex", whiteSpace: "nowrap" };

  return (
    <>
      <div
        onClick={onToggle}
        style={{ color: DIM, fontWeight: 700, padding: "4px 0", cursor: "pointer", userSelect: "none" }}
      >
        <span style={{ color: WHITE }}>
          {"  "}{isOpen ? "▼" : "▸"} ACTIVE PROGRAMS ({active.length})
        </span>
        {magnetized.length > 0 && (
          <span style={{ color: MAGENTA, fontWeight: 400, fontSize: "11px" }}>
            {" "}| {magnetized.length} MAGNETIZED
          </span>
        )}
        {!isOpen && active.length > 0 && (
          <span style={{ color: DIM, fontWeight: 400, fontSize: "11px" }}>
            {" "}— click to expand
          </span>
        )}
      </div>
      <div style={{ color: DIM }}>{SEP}</div>

      {isOpen && (
        <>
          {active.length > 0 && (
            <>
              <div style={{ ...row, color: DIM, fontWeight: 700, borderBottom: `1px solid ${LINE}`, padding: "2px 0", fontSize: "11px" }}>
                <T w="60px">TICKER</T>
                <T w="180px">OUTFIT</T>
                <T w="50px">TF</T>
                <T w="70px">SMA</T>
                <T w="80px">PROTOCOL</T>
                <T w="90px" align="right">ENTRY</T>
                <T w="90px" align="right">SMA_VAL</T>
                <T w="90px" align="right">STOP</T>
                <T w="60px" align="center">SESS</T>
                <T w="90px">TYPE</T>
              </div>

              {active.map((p, i) => (
                <div key={i} style={{ ...row, padding: "1px 0", fontSize: "11px" }}>
                  <T w="60px" c={CYAN} bold>{p.ticker}</T>
                  <T w="180px" c={PURPLE}>{p.outfit_key}</T>
                  <T w="50px" c={ORANGE}>{p.timeframe}</T>
                  <T w="70px" c={WHITE} bold>MA{p.sma_period}</T>
                  <T w="80px" c={protocolColor(p.protocol)}>{protocolLabel(p.protocol)}</T>
                  <T w="90px" c={WHITE} align="right">{p.entry_price?.toFixed(2)}</T>
                  <T w="90px" c={DIM} align="right">{p.sma_value?.toFixed(2)}</T>
                  <T w="90px" c={RED} align="right">{p.stop_level?.toFixed(2)}</T>
                  <T w="60px" c={p.consecutive_sessions >= 2 ? MAGENTA : DIM} align="center">
                    {p.consecutive_sessions}
                  </T>
                  <T w="90px" c={p.is_magnetized ? MAGENTA : GREEN} bold>
                    {p.is_magnetized ? "MAGNETIZED" : "PRECISION"}
                  </T>
                </div>
              ))}
            </>
          )}

          {active.length === 0 && (
            <div style={{ color: DIM, padding: "4px 0 4px 4px" }}>No active programs</div>
          )}

          {/* Recently Terminated */}
          {terminated.length > 0 && (
            <>
              <div style={{ color: DIM, padding: "8px 0 4px 0" }}>{SEP}</div>
              <div style={{ color: DIM, fontWeight: 700, padding: "4px 0", fontSize: "11px" }}>
                {"  "}RECENTLY TERMINATED ({terminated.length})
              </div>

              <div style={{ ...row, color: DIM, fontWeight: 700, borderBottom: `1px solid ${LINE}`, padding: "2px 0", fontSize: "10px" }}>
                <T w="60px">TICKER</T>
                <T w="180px">OUTFIT</T>
                <T w="50px">TF</T>
                <T w="70px">SMA</T>
                <T w="80px">PROTOCOL</T>
                <T w="90px" align="right">ENTRY</T>
                <T w="90px" align="right">STOP</T>
                <T w="140px">TERMINATED</T>
              </div>

              {terminated.map((p, i) => (
                <div key={i} style={{ ...row, padding: "1px 0", fontSize: "10px", opacity: 0.6 }}>
                  <T w="60px" c={WHITE}>{p.ticker}</T>
                  <T w="180px" c={DIM}>{p.outfit_key}</T>
                  <T w="50px" c={DIM}>{p.timeframe}</T>
                  <T w="70px" c={DIM}>MA{p.sma_period}</T>
                  <T w="80px" c={DIM}>{protocolLabel(p.protocol)}</T>
                  <T w="90px" c={DIM} align="right">{p.entry_price?.toFixed(2)}</T>
                  <T w="90px" c={DIM} align="right">{p.stop_level?.toFixed(2)}</T>
                  <T w="140px" c={RED}>{p.terminated_at?.slice(0, 19) || "—"}</T>
                </div>
              ))}
            </>
          )}

          <div style={{ color: DIM, padding: "4px 0" }}>{SEP}</div>
        </>
      )}
    </>
  );
}

// ═══════════════════════════════════════════════════════════
// SNAPSHOTS VIEWER
// ═══════════════════════════════════════════════════════════
function SnapshotsViewer({ isOpen, onToggle }) {
  const [dates, setDates] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedWindow, setSelectedWindow] = useState("all");
  const [snapshots, setSnapshots] = useState([]);
  const [momentum, setMomentum] = useState(null);
  const [loading, setLoading] = useState(false);

  // Load available dates on first open
  useEffect(() => {
    if (isOpen && dates.length === 0) {
      api("/api/snapshots/dates").then(res => {
        if (res && Array.isArray(res)) {
          setDates(res);
          if (res.length > 0) setSelectedDate(res[0].date);
        }
      });
    }
  }, [isOpen, dates.length]);

  // Load snapshots when date/window changes
  useEffect(() => {
    if (!selectedDate) return;
    setLoading(true);
    const wq = selectedWindow !== "all" ? `&window=${selectedWindow}` : "";
    Promise.all([
      api(`/api/snapshots?date=${selectedDate}${wq}`),
      api(`/api/momentum?date=${selectedDate}`),
    ]).then(([snapRes, momRes]) => {
      if (snapRes?.snapshots) setSnapshots(snapRes.snapshots);
      if (momRes?.outfits) setMomentum(momRes.outfits);
      setLoading(false);
    });
  }, [selectedDate, selectedWindow]);

  const row = { display: "flex", whiteSpace: "nowrap" };

  // Group snapshots by window for cleaner display
  const grouped = {};
  (snapshots || []).filter(s => s.ticker === null).forEach(s => {
    if (!grouped[s.time_window]) grouped[s.time_window] = [];
    grouped[s.time_window].push(s);
  });

  const windowLabels = { open: "OPEN (9:30-10:30)", midday: "MIDDAY (11:30-1:00)", close: "CLOSE (3:00-4:00)", full: "FULL DAY" };

  const dateInfo = dates.find(d => d.date === selectedDate);

  return (
    <>
      <div
        onClick={onToggle}
        style={{ color: DIM, fontWeight: 700, padding: "4px 0", cursor: "pointer", userSelect: "none" }}
      >
        <span style={{ color: WHITE }}>
          {"  "}{isOpen ? "▼" : "▸"} SCAN SNAPSHOTS
        </span>
        {dates.length > 0 && (
          <span style={{ color: DIM, fontWeight: 400, fontSize: "11px" }}>
            {" "}| {dates.length} day{dates.length !== 1 ? "s" : ""} of data
          </span>
        )}
        {!isOpen && (
          <span style={{ color: DIM, fontWeight: 400, fontSize: "11px" }}>
            {" "}— click to expand
          </span>
        )}
      </div>
      <div style={{ color: DIM }}>{SEP}</div>

      {isOpen && (
        <>
          {/* Controls */}
          <div style={{ display: "flex", gap: "10px", padding: "6px 0", alignItems: "center", flexWrap: "wrap" }}>
            <span style={{ color: DIM, fontSize: "11px" }}>DATE:</span>
            <select
              value={selectedDate || ""}
              onChange={e => setSelectedDate(e.target.value)}
              style={{
                background: "#111", border: `1px solid ${LINE}`, color: WHITE,
                padding: "3px 8px", fontSize: "11px", fontFamily: FONT,
              }}
            >
              {dates.map(d => (
                <option key={d.date} value={d.date}>
                  {d.date} ({d.windows.join(", ")})
                </option>
              ))}
            </select>

            <span style={{ color: DIM, fontSize: "11px", marginLeft: "8px" }}>WINDOW:</span>
            <span style={{ display: "flex", gap: "2px", border: `1px solid ${LINE}`, borderRadius: "3px", overflow: "hidden" }}>
              {["all", "open", "midday", "close", "full"].map(w => (
                <button key={w} onClick={() => setSelectedWindow(w)} style={{
                  background: selectedWindow === w ? "#1a1a2e" : "transparent",
                  border: "none", borderRight: `1px solid ${LINE}`,
                  color: selectedWindow === w ? CYAN : DIM,
                  padding: "3px 8px", cursor: "pointer", fontSize: "10px", fontFamily: FONT,
                  fontWeight: selectedWindow === w ? 700 : 400,
                }}>{w.toUpperCase()}</button>
              ))}
            </span>

            {dateInfo && (
              <span style={{ color: DIM, fontSize: "10px", marginLeft: "auto" }}>
                {dateInfo.scan_count} snapshots across {dateInfo.windows.length} window{dateInfo.windows.length !== 1 ? "s" : ""}
              </span>
            )}
          </div>

          {loading && <div style={{ color: DIM, padding: "4px 0" }}>Loading snapshots...</div>}

          {!loading && Object.keys(grouped).length === 0 && (
            <div style={{ color: DIM, padding: "4px 0" }}>No snapshots for this date/window</div>
          )}

          {!loading && Object.entries(grouped).map(([win, snaps]) => (
            <div key={win} style={{ marginBottom: "8px" }}>
              <div style={{ color: ORANGE, fontWeight: 700, fontSize: "11px", padding: "4px 0 2px 0" }}>
                {"  "}{windowLabels[win] || win.toUpperCase()}
                <span style={{ color: DIM, fontWeight: 400, fontSize: "10px" }}>
                  {" "}| scanned {snaps[0]?.scanned_at?.slice(11, 19)} UTC | {snaps.length} outfits
                </span>
              </div>

              <div style={{ ...row, color: DIM, fontWeight: 700, borderBottom: `1px solid ${LINE}`, padding: "2px 0", fontSize: "11px" }}>
                <T w="220px">OUTFIT</T>
                <T w="80px" align="right">LONG</T>
                <T w="80px" align="right">SHORT</T>
                <T w="80px" align="right">L/S</T>
                <T w="90px" align="right">WEIGHT</T>
                {momentum && <T w="90px">MOMENTUM</T>}
                {momentum && <T w="80px" align="right">DELTA</T>}
              </div>

              {snaps.sort((a, b) => b.total_weight - a.total_weight).map((s, i) => {
                const mom = momentum?.[s.outfit_key];
                return (
                  <div key={i} style={{ ...row, padding: "1px 0", fontSize: "11px" }}>
                    <T w="220px" c={WHITE}>{s.outfit_key}</T>
                    <T w="80px" c={GREEN} align="right">{s.long_count}</T>
                    <T w="80px" c={RED} align="right">{s.short_count}</T>
                    <T w="80px" c={s.ls_ratio > 1.5 ? GREEN : s.ls_ratio < 0.67 ? RED : YELLOW} align="right">
                      {s.ls_ratio.toFixed(2)}
                    </T>
                    <T w="90px" c={DIM} align="right">{s.total_weight.toFixed(1)}</T>
                    {momentum && (
                      <T w="90px" c={momentumColor(mom?.momentum)} bold>
                        {mom?.momentum || "—"}
                      </T>
                    )}
                    {momentum && (
                      <T w="80px" c={mom?.delta > 0 ? GREEN : mom?.delta < 0 ? RED : DIM} align="right">
                        {mom?.delta != null ? (mom.delta > 0 ? "+" : "") + mom.delta.toFixed(2) : "—"}
                      </T>
                    )}
                  </div>
                );
              })}
            </div>
          ))}

          <div style={{ color: DIM, padding: "4px 0" }}>{SEP}</div>
        </>
      )}
    </>
  );
}

// ═══════════════════════════════════════════════════════════
// SMA REFERENCE TABLE
// ═══════════════════════════════════════════════════════════
function SmaReferenceTable({ isOpen, onToggle }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    if (isOpen && !data) {
      setLoading(true);
      api("/api/sma-table").then(res => {
        if (res) setData(res);
        setLoading(false);
      });
    }
  }, [isOpen, data]);

  const row = { display: "flex", whiteSpace: "nowrap" };
  const filtered = data ? data.filter(t => {
    if (!filter) return true;
    const q = filter.toUpperCase();
    if (t.ticker.includes(q)) return true;
    return t.outfits?.some(o => o.outfit.toUpperCase().includes(q));
  }) : [];

  const withAffinity = filtered.filter(t => t.has_affinity);
  const noAffinity = filtered.filter(t => !t.has_affinity);

  return (
    <>
      <div
        onClick={onToggle}
        style={{ color: DIM, fontWeight: 700, padding: "4px 0", cursor: "pointer", userSelect: "none" }}
      >
        <span style={{ color: WHITE }}>
          {"  "}{isOpen ? "▼" : "▸"} SMA REFERENCE TABLE
        </span>
        {data && (
          <span style={{ color: DIM, fontWeight: 400, fontSize: "11px" }}>
            {" "}| {data.filter(t => t.has_affinity).length} tickers with known outfits
          </span>
        )}
        {!isOpen && (
          <span style={{ color: DIM, fontWeight: 400, fontSize: "11px" }}>
            {" "}— click to expand
          </span>
        )}
      </div>
      <div style={{ color: DIM }}>{SEP}</div>

      {isOpen && (
        <>
          {loading && <div style={{ color: DIM, padding: "4px 0" }}>Loading SMA table...</div>}

          {data && (
            <>
              <div style={{ padding: "4px 0 8px 0" }}>
                <input
                  type="text"
                  placeholder="Filter by ticker or outfit..."
                  value={filter}
                  onChange={e => setFilter(e.target.value)}
                  style={{
                    background: "#111", border: `1px solid ${LINE}`, color: WHITE,
                    padding: "4px 10px", fontSize: "11px", fontFamily: FONT,
                    width: "250px", borderRadius: "3px",
                  }}
                />
                <span style={{ color: DIM, fontSize: "10px", marginLeft: "10px" }}>
                  {withAffinity.length} tickers with confirmed outfits | {noAffinity.length} unassigned
                </span>
              </div>

              {/* Header */}
              <div style={{ ...row, color: DIM, fontWeight: 700, borderBottom: `1px solid ${LINE}`, padding: "2px 0", fontSize: "11px" }}>
                <T w="70px">TICKER</T>
                <T w="200px">OUTFIT</T>
                <T w="100px">CATEGORY</T>
                <T w="500px">SMA PERIODS</T>
              </div>

              {withAffinity.map(t => (
                t.outfits.map((o, i) => (
                  <div key={`${t.ticker}-${o.outfit}`} style={{ ...row, padding: "1px 0", fontSize: "11px" }}>
                    <T w="70px" c={CYAN} bold>{i === 0 ? t.ticker : ""}</T>
                    <T w="200px" c={PURPLE}>{o.outfit}</T>
                    <T w="100px" c={
                      o.category === "Core" ? WHITE :
                      o.category === "System" ? ORANGE :
                      o.category === "Angel" ? YELLOW :
                      o.category === "Political" ? RED :
                      o.category === "Dual" ? MAGENTA : DIM
                    }>{o.category}</T>
                    <T w="500px" c={WHITE}>
                      {o.periods.map((p, j) => (
                        <span key={j}>
                          {j > 0 && <span style={{ color: DIM }}>, </span>}
                          <span style={{ color: p >= 400 ? GREEN : p >= 100 ? YELLOW : WHITE, fontWeight: p >= 400 ? 700 : 400 }}>
                            {p}
                          </span>
                        </span>
                      ))}
                    </T>
                  </div>
                ))
              ))}

              {noAffinity.length > 0 && (
                <>
                  <div style={{ padding: "8px 0 4px 0", color: DIM, fontSize: "11px" }}>
                    {"  "}UNASSIGNED — scan all outfits (no confirmed Raul data):
                  </div>
                  <div style={{ padding: "0 0 4px 4px", color: DIM, fontSize: "11px", lineHeight: "1.8" }}>
                    {noAffinity.map(t => t.ticker).join(", ")}
                  </div>
                </>
              )}
            </>
          )}

          <div style={{ color: DIM, padding: "4px 0" }}>{SEP}</div>
        </>
      )}
    </>
  );
}

// ═══════════════════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════════════════
export default function App() {
  const [outfits, setOutfits] = useState([]);
  const [tickers, setTickers] = useState([]);
  const [bias, setBias] = useState(null);
  const [vix, setVix] = useState(null);
  const [programs, setPrograms] = useState([]);
  const [connected, setConnected] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [scanMode, setScanMode] = useState("light");
  const [lastUpdate, setLastUpdate] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [expanded, setExpanded] = useState(null);
  const [programsOpen, setProgramsOpen] = useState(false);
  const [snapshotsOpen, setSnapshotsOpen] = useState(false);
  const [smaTableOpen, setSmaTableOpen] = useState(false);
  const [window, setWindow] = useState("full");
  const [schedule, setSchedule] = useState(null);
  const [schwabStatus, setSchwabStatus] = useState(null);
  const [alerts, setAlerts] = useState(null);
  const [btc, setBtc] = useState(null);
  const [dataStatus, setDataStatus] = useState(null);
  const intervalRef = useRef(null);
  const pollRef = useRef(null);

  const loadData = useCallback(async () => {
    const wq = window !== "full" ? `?window=${window}` : "";
    const [oRes, tRes, bRes, vRes, pRes, sRes, schRes, aRes, btcRes, dsRes] = await Promise.all([
      api(`/api/outfits${wq}`),
      api(`/api/tickers${wq}`),
      api(`/api/bias${wq}`),
      api("/api/vix"),
      api("/api/programs"),
      api("/api/scan/schedule"),
      api("/api/schwab/status"),
      api("/api/alerts"),
      api("/api/btc"),
      api("/api/data-status"),
    ]);

    if (oRes && Array.isArray(oRes) && oRes.length > 0) {
      setOutfits(oRes);
      setConnected(true);
    } else {
      setConnected(false);
    }

    if (tRes && Array.isArray(tRes)) setTickers(tRes);
    if (bRes) setBias(bRes);
    if (vRes) setVix(vRes);
    if (pRes && Array.isArray(pRes)) setPrograms(pRes);
    if (sRes) setSchedule(sRes);
    if (schRes) setSchwabStatus(schRes);
    if (aRes) setAlerts(aRes);
    if (btcRes) setBtc(btcRes);
    if (dsRes) setDataStatus(dsRes);
    setLastUpdate(new Date());
  }, [window]);

  useEffect(() => { loadData(); }, [loadData]);

  useEffect(() => {
    if (autoRefresh) intervalRef.current = setInterval(loadData, 15000);
    return () => clearInterval(intervalRef.current);
  }, [autoRefresh, loadData]);

  const doScan = useCallback(async () => {
    setScanning(true);
    const res = await triggerScan(scanMode);
    if (!res) { setScanning(false); return; }

    pollRef.current = setInterval(async () => {
      const status = await api("/api/scan/status");
      if (status && !status.in_progress) {
        clearInterval(pollRef.current);
        setScanning(false);
        await loadData();
      }
    }, 2000);

    setTimeout(() => {
      clearInterval(pollRef.current);
      setScanning(false);
      loadData();
    }, 300000);
  }, [scanMode, loadData]);

  const now = lastUpdate
    ? lastUpdate.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", hour12: false })
    : "--:--";
  const dateStr = lastUpdate
    ? lastUpdate.toLocaleDateString("en-US", { year: "numeric", month: "2-digit", day: "2-digit" })
    : "";

  const ovBias = bias?.overall_bias || "Neutral";
  const domOutfit = bias?.dominant_outfit || outfits[0]?.sequence || "—";
  const structBias = bias?.structural_bias || "N/A";
  const pricePos = bias?.price_position || "N/A";
  const keySmas = outfits[0]?.smas || "—";
  const instMomentum = bias?.institutional_momentum;
  const momSummary = bias?.momentum_summary;

  const vixLevel = vix?.vix;
  const vixRegime = vix?.regime || "Unknown";

  const activeCount = programs.filter(p => p.status === "active").length;
  const magCount = programs.filter(p => p.is_magnetized).length;

  const row = { display: "flex", whiteSpace: "nowrap" };

  return (
    <div style={{ fontFamily: FONT, fontSize: "12px", lineHeight: "1.6", background: BG, color: WHITE, minHeight: "100vh", padding: "12px 16px", overflow: "auto" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
        body { margin: 0; background: ${BG}; }
        * { box-sizing: border-box; }
        *::-webkit-scrollbar { width: 6px; height: 6px; }
        *::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
        button { font-family: ${FONT}; }
      `}</style>

      {/* ── CONTROLS ── */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "10px", alignItems: "center", flexWrap: "wrap" }}>
        <button onClick={doScan} disabled={scanning} style={{
          background: scanning ? "#331800" : "#002200",
          border: `1px solid ${scanning ? "#664400" : "#006600"}`,
          color: scanning ? YELLOW : GREEN,
          padding: "4px 12px", cursor: scanning ? "wait" : "pointer", fontSize: "11px",
        }}>
          {scanning ? "⟳ SCANNING..." : `▶ SCAN (${scanMode.toUpperCase()})`}
        </button>
        <button onClick={() => setScanMode(m => m === "light" ? "full" : m === "full" ? "tsla" : "light")} style={{
          background: scanMode === "tsla" ? "#1a0033" : "transparent",
          border: `1px solid ${scanMode === "tsla" ? "#6600aa" : LINE}`,
          color: scanMode === "tsla" ? PURPLE : DIM, padding: "4px 10px", cursor: "pointer", fontSize: "11px",
        }}>MODE: {scanMode.toUpperCase()}</button>
        <button onClick={() => setAutoRefresh(!autoRefresh)} style={{
          background: "transparent", border: `1px solid ${autoRefresh ? "#006600" : LINE}`,
          color: autoRefresh ? GREEN : DIM, padding: "4px 10px", cursor: "pointer", fontSize: "11px",
        }}>{autoRefresh ? "● AUTO 15s" : "○ MANUAL"}</button>
        <button onClick={loadData} style={{
          background: "transparent", border: `1px solid ${LINE}`,
          color: DIM, padding: "4px 10px", cursor: "pointer", fontSize: "11px",
        }}>↻ REFRESH</button>

        {/* Window toggle */}
        <span style={{ display: "flex", gap: "2px", marginLeft: "8px", border: `1px solid ${LINE}`, borderRadius: "3px", overflow: "hidden" }}>
          {[
            { key: "full", label: "FULL DAY" },
            { key: "institutional", label: "INSTITUTIONAL" },
          ].map(w => (
            <button key={w.key} onClick={() => setWindow(w.key)} style={{
              background: window === w.key ? (w.key === "institutional" ? "#1a0033" : "#001a00") : "transparent",
              border: "none",
              borderRight: `1px solid ${LINE}`,
              color: window === w.key ? (w.key === "institutional" ? PURPLE : GREEN) : DIM,
              padding: "4px 10px", cursor: "pointer", fontSize: "10px", fontFamily: FONT,
              fontWeight: window === w.key ? 700 : 400,
            }}>{w.label}</button>
          ))}
        </span>

        {schedule?.current_window && (
          <span style={{ color: ORANGE, fontSize: "10px", marginLeft: "6px" }}>
            ● {schedule.current_window.toUpperCase()} WINDOW
          </span>
        )}

        {alerts && alerts.count > 0 && (
          <span style={{
            fontSize: "10px", marginLeft: "6px", fontWeight: 700,
            color: alerts.critical > 0 ? RED : ORANGE,
            background: alerts.critical > 0 ? "#330000" : "#331a00",
            padding: "2px 8px", borderRadius: "3px",
            border: `1px solid ${alerts.critical > 0 ? "#660000" : "#664400"}`,
          }}>
            {alerts.critical > 0 ? "!!" : "!"} {alerts.count} ALERT{alerts.count !== 1 ? "S" : ""}
          </span>
        )}

        {/* Data freshness indicator */}
        {dataStatus && dataStatus.has_scan_data && (
          <span style={{ fontSize: "10px", color: DIM, marginLeft: "6px", display: "flex", alignItems: "center", gap: "6px" }}>
            <span>Last scan: {dataStatus.last_scan_time?.slice(11, 19)} UTC ({dataStatus.last_scan_mode})</span>
            {dataStatus.windows_captured_today.length > 0 && (
              <span style={{
                color: CYAN,
                border: `1px solid ${LINE}`, padding: "1px 6px", borderRadius: "3px",
              }}>
                {dataStatus.windows_captured_today.map(w => w.toUpperCase()).join(" · ")}
              </span>
            )}
            {dataStatus.has_momentum && (
              <span style={{ color: GREEN }}>MOM:{dataStatus.momentum_outfits}</span>
            )}
          </span>
        )}

        <span style={{ color: DIM, fontSize: "11px", marginLeft: "auto", display: "flex", alignItems: "center", gap: "8px" }}>
          {/* Data source indicator — always visible */}
          <span style={{
            fontSize: "10px",
            color: schwabStatus?.authenticated ? GREEN : RED,
            border: `1px solid ${schwabStatus?.authenticated ? "#006600" : "#660000"}`,
            padding: "2px 8px", borderRadius: "3px",
          }}>
            {schwabStatus?.authenticated ? "● SCHWAB" : schwabStatus ? "!! NO DATA SOURCE" : "..."}
            {schwabStatus?.authenticated && schwabStatus.access_token_expires_in != null && (
              <span style={{ color: DIM }}> {Math.floor(schwabStatus.access_token_expires_in / 60)}m</span>
            )}
          </span>
          {schwabStatus?.data_source_stats && schwabStatus.data_source_stats.schwab > 0 && (
            <span style={{ fontSize: "10px", color: DIM }}>
              S:{schwabStatus.data_source_stats.schwab} F:{schwabStatus.data_source_stats.failed}
            </span>
          )}
          <span>{connected ? `● ${API_BASE}` : "○ NO DATA"}</span>
        </span>
      </div>

      {/* ── BIAS HEADER + VIX ── */}
      <div style={{ color: DIM }}>{SEP}</div>
      <div style={{ padding: "4px 0" }}>
        <div style={{ color: WHITE, fontWeight: 700, marginBottom: "2px" }}>
          {"  "}OVERALL INSTITUTIONAL BIAS | {dateStr} | {now} EST
        </div>
        <div style={{ display: "flex", gap: "48px" }}>
          <div>
            <div style={row}>{"    "}Overall Bias  : <T c={biasColor(ovBias)}>{" "}{ovBias}</T></div>
            <div style={row}>{"    "}Dominant Outfit: <T c={WHITE}>{" "}{domOutfit}</T></div>
            <div style={row}>{"    "}STRUCT_BIAS   : <T c={biasColor(structBias)}>{" "}{structBias}</T></div>
            <div style={row}>{"    "}Key SMAs      : <T c={WHITE}>{" "}{keySmas}</T></div>
            <div style={row}>{"    "}Price Position : <T c={posColor(pricePos)}>{" "}{pricePos}</T></div>
            {instMomentum && (
              <div style={row}>{"    "}Inst Momentum :{" "}
                <T c={instMomentum === "Bullish" ? GREEN : instMomentum === "Bearish" ? RED : YELLOW} bold>
                  {instMomentum}
                </T>
                {momSummary && (
                  <span style={{ color: DIM, fontSize: "10px" }}>
                    {" "}({momSummary.rising}↑ {momSummary.falling}↓ {momSummary.flat}→ of {momSummary.total})
                  </span>
                )}
              </div>
            )}
          </div>
          <div>
            <div style={row}>
              {"    "}VIX           :{" "}
              <T c={vixColor(vixRegime)} bold>
                {vixLevel != null ? vixLevel.toFixed(2) : "—"}
              </T>
              <T c={vixColor(vixRegime)}>
                {" "}{vixRegime}
              </T>
            </div>
            <div style={row}>
              {"    "}Active Progs  : <T c={activeCount > 0 ? GREEN : DIM}>{" "}{activeCount}</T>
            </div>
            <div style={row}>
              {"    "}Magnetized    : <T c={magCount > 0 ? MAGENTA : DIM}>{" "}{magCount}</T>
            </div>
            <div style={{ ...row, color: DIM, fontSize: "10px", marginTop: "2px" }}>
              {"    "}
              {vixRegime === "Low" && "Low VIX = fewer outfit activations"}
              {vixRegime === "Normal" && "Normal VIX = standard outfit activity"}
              {vixRegime === "Elevated" && "Elevated VIX = more outfits active, more risk"}
              {vixRegime === "Extreme" && "Extreme VIX = maximum outfit activation, high risk/opportunity"}
              {vixRegime === "Unknown" && "VIX data unavailable"}
            </div>
          </div>
        </div>
      </div>
      <div style={{ color: DIM }}>{SEP}</div>

      {/* ── BITCOIN PANEL ── */}
      {btc && (
        <>
          <div style={{
            background: "#0a0a14",
            border: `1px solid ${btc.verdict === "Bullish" ? "#006600" : btc.verdict === "Bearish" ? "#660000" : "#333300"}`,
            borderRadius: "4px", padding: "8px 12px", margin: "6px 0",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: "16px", marginBottom: "4px" }}>
              <span style={{ color: ORANGE, fontWeight: 700, fontSize: "13px" }}>₿ BITCOIN</span>
              <span style={{ color: WHITE, fontWeight: 700, fontSize: "15px" }}>
                ${btc.price?.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) || "—"}
              </span>
              <span style={{
                color: btc.verdict === "Bullish" ? GREEN : btc.verdict === "Bearish" ? RED : YELLOW,
                fontWeight: 700, fontSize: "13px",
                background: btc.verdict === "Bullish" ? "#002200" : btc.verdict === "Bearish" ? "#220000" : "#222200",
                padding: "2px 10px", borderRadius: "3px",
              }}>
                {btc.verdict === "Bullish" ? "▲ " : btc.verdict === "Bearish" ? "▼ " : "● "}{btc.verdict.toUpperCase()}
              </span>
              <span style={{ color: DIM, fontSize: "11px" }}>{btc.reason}</span>
              <span style={{ color: DIM, fontSize: "10px", marginLeft: "auto" }}>
                via COINBASE | {btc.total_hits} hit{btc.total_hits !== 1 ? "s" : ""}
              </span>
            </div>

            <div style={{ display: "flex", gap: "24px", fontSize: "11px" }}>
              <div>
                <span style={{ color: DIM }}>Long: </span>
                <span style={{ color: GREEN, fontWeight: 700 }}>{btc.long_weight}w</span>
              </div>
              <div>
                <span style={{ color: DIM }}>Short: </span>
                <span style={{ color: RED, fontWeight: 700 }}>{btc.short_weight}w</span>
              </div>
              {btc.dominant_outfit && (
                <div>
                  <span style={{ color: DIM }}>Dominant: </span>
                  <span style={{ color: PURPLE, fontWeight: 700 }}>{btc.dominant_outfit}</span>
                </div>
              )}
              {btc.key_levels && Object.keys(btc.key_levels).length > 0 && (
                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                  <span style={{ color: DIM }}>Key Levels: </span>
                  {Object.entries(btc.key_levels).slice(0, 5).map(([sma, info]) => (
                    <span key={sma} style={{ marginRight: "4px" }}>
                      <span style={{ color: WHITE, fontWeight: 700 }}>{sma}</span>
                      <span style={{ color: DIM }}>@</span>
                      <span style={{ color: info.side === "long" ? GREEN : RED }}>
                        ${info.value?.toLocaleString()}
                      </span>
                    </span>
                  ))}
                </div>
              )}
            </div>

            {btc.top_hits && btc.top_hits.length > 0 && (
              <div style={{ marginTop: "4px", borderTop: `1px solid #1a1a1a`, paddingTop: "4px" }}>
                <div style={{ display: "flex", gap: "4px", flexWrap: "wrap", fontSize: "10px" }}>
                  {btc.top_hits.slice(0, 6).map((h, i) => (
                    <span key={i} style={{
                      background: "#111", border: `1px solid ${LINE}`, borderRadius: "3px",
                      padding: "1px 6px", display: "inline-flex", gap: "4px", alignItems: "center",
                    }}>
                      <span style={{ color: h.side === "long" ? GREEN : RED, fontWeight: 700 }}>
                        {h.side === "long" ? "▲" : "▼"}
                      </span>
                      <span style={{ color: PURPLE }}>{h.outfit}</span>
                      <span style={{ color: ORANGE }}>{h.timeframe}</span>
                      <span style={{ color: WHITE }}>MA{h.period}</span>
                      <span style={{ color: DIM }}>@${h.sma_value?.toLocaleString()}</span>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </>
      )}

      {/* ── MAJOR SIGNAL ALERTS ── */}
      {alerts && alerts.count > 0 && (
        <>
          <div style={{
            background: alerts.critical > 0 ? "#1a0000" : "#1a0d00",
            border: `1px solid ${alerts.critical > 0 ? "#660000" : "#664400"}`,
            borderRadius: "4px", padding: "8px 12px", margin: "6px 0",
          }}>
            <div style={{ color: alerts.critical > 0 ? RED : ORANGE, fontWeight: 700, fontSize: "13px", marginBottom: "4px" }}>
              {alerts.critical > 0 ? "!! " : "! "}MAJOR SIGNALS DETECTED — {alerts.count} alert{alerts.count !== 1 ? "s" : ""}
              {alerts.critical > 0 && <span style={{ color: RED }}> ({alerts.critical} CRITICAL)</span>}
              {alerts.high > 0 && <span style={{ color: ORANGE }}> ({alerts.high} HIGH)</span>}
            </div>
            {alerts.alerts.slice(0, 15).map((a, i) => (
              <div key={i} style={{ display: "flex", gap: "8px", padding: "3px 0", fontSize: "11px", alignItems: "center" }}>
                <span style={{
                  color: "#0a0a0a",
                  background: a.level === "critical" ? RED : ORANGE,
                  padding: "0 6px", borderRadius: "2px", fontWeight: 700, fontSize: "10px",
                  minWidth: "60px", textAlign: "center",
                }}>
                  {a.level.toUpperCase()}
                </span>
                <span style={{
                  color: CYAN, fontWeight: 700, minWidth: "50px",
                }}>{a.ticker}</span>
                <span style={{
                  color: a.type === "CONFLUENCE" ? MAGENTA :
                         a.type === "AFFINITY_LOCK" ? GREEN :
                         a.type === "HIGH_PERIOD_CLUSTER" ? PURPLE :
                         a.type === "OUTFIT_SURGE" ? YELLOW :
                         a.type === "MAGNETIZED_HIGH" ? ORANGE : WHITE,
                  minWidth: "130px", fontSize: "10px",
                }}>{a.type}</span>
                {a.details?.entry_price != null && (
                  <>
                    <span style={{ color: a.details.side === "long" ? GREEN : RED, fontWeight: 700, minWidth: "42px" }}>
                      {a.details.side === "long" ? "LONG" : "SHORT"}
                    </span>
                    <span style={{ color: WHITE, fontWeight: 700, minWidth: "80px" }}>
                      entry ${a.details.entry_price?.toFixed(2)}
                    </span>
                    <span style={{ color: RED, fontWeight: 700, minWidth: "80px" }}>
                      stop ${a.details.stop_price?.toFixed(2)}
                    </span>
                    <span style={{ color: DIM, fontSize: "10px", minWidth: "50px" }}>
                      {a.details.protocol === "penny_breach" ? "PENNY" :
                       a.details.protocol === "point_break" ? "POINT" :
                       a.details.protocol === "candle_close" ? "CANDLE" : ""}
                    </span>
                  </>
                )}
                <span style={{ color: DIM, fontSize: "10px" }}>{a.summary}</span>
              </div>
            ))}
            {alerts.count > 10 && (
              <div style={{ color: DIM, fontSize: "10px", marginTop: "4px" }}>
                ... and {alerts.count - 10} more alerts
              </div>
            )}
          </div>
        </>
      )}

      {/* ── OUTFIT RANKING (PRIMARY VIEW) ── */}
      <div style={{ color: WHITE, fontWeight: 700, padding: "4px 0" }}>
        {"  "}TOP {Math.min(outfits.length, 20)} OUTFITS BIAS SUMMARY
        {window === "institutional" && (
          <span style={{ color: PURPLE, fontWeight: 400, fontSize: "11px" }}>
            {" "}| INSTITUTIONAL HOUR VIEW
          </span>
        )}
      </div>
      {window === "institutional" && outfits.length === 0 && (
        <div style={{ padding: "8px 0 8px 4px" }}>
          <span style={{ color: YELLOW }}>No institutional hour data yet. </span>
          <span style={{ color: DIM, fontSize: "11px" }}>
            This view requires scan snapshots from midday + close market windows on the same day.
            Switch to{" "}
            <span
              onClick={() => setWindow("full")}
              style={{ color: GREEN, cursor: "pointer", textDecoration: "underline" }}
            >FULL DAY</span>
            {" "}to see all scan results.
          </span>
        </div>
      )}
      <div style={{ color: DIM }}>{SEP}</div>

      <div style={{ ...row, color: DIM, fontWeight: 700, borderBottom: `1px solid ${LINE}`, padding: "2px 0" }}>
        <T w="44px">RANK</T>
        <T w="70px">DOM_TKR</T>
        <T w="200px">SEQUENCE</T>
        <T w="70px" align="right">TOTAL</T>
        <T w="70px" align="right">LONG</T>
        <T w="70px" align="right">SHORT</T>
        <T w="70px" align="right">L/S</T>
        <T w="76px">SLOPE</T>
        <T w="110px">MOMENTUM</T>
        <T w="74px">LEVEL</T>
        <T w="90px">STRUCT_BIAS</T>
        <T w="200px">KEY_SMAS</T>
        <T w="82px">PRICE_POS</T>
        <T w="90px">BIAS</T>
      </div>

      {outfits.slice(0, 20).map((o) => (
        <div key={o.rank} style={{ ...row, padding: "1px 0" }}>
          <T w="44px" c={WHITE}>{o.rank}</T>
          <T w="70px" c={CYAN} bold>{o.dominant_ticker}</T>
          <T w="200px" c={WHITE}>{o.sequence}</T>
          <T w="70px" c={WHITE} align="right" bold>{o.total_count ?? Math.round(o.total)}</T>
          <T w="70px" c={GREEN} align="right">{o.long_count ?? Math.round(o.long)}</T>
          <T w="70px" c={RED} align="right">{o.short_count ?? Math.round(o.short)}</T>
          <T w="70px" c={o.ls_ratio > 1.5 ? GREEN : o.ls_ratio < 0.67 ? RED : YELLOW} align="right">{o.ls_ratio?.toFixed(2)}</T>
          <T w="76px" c={slopeColor(o.slope)}>{o.slope}</T>
          <T w="110px" c={momentumColor(o.momentum)} bold>
            {o.momentum || "—"}
            {o.momentum_delta != null && o.momentum_delta !== 0 && (
              <span style={{ fontSize: "9px", fontWeight: 400 }}>
                {" "}{o.momentum_delta > 0 ? "+" : ""}{o.momentum_delta}
              </span>
            )}
          </T>
          <T w="74px" c={biasColor(o.level)}>{o.level || "—"}</T>
          <T w="90px" c={biasColor(o.structural_bias || o.bias)}>{o.structural_bias || "N/A"}</T>
          <T w="200px" c={DIM}>{o.smas}</T>
          <T w="82px" c={posColor(o.price_position)}>{o.price_position}</T>
          <T w="90px" c={biasColor(o.institutional_bias || o.bias)}>{o.institutional_bias || o.bias}</T>
        </div>
      ))}

      <div style={{ color: DIM, padding: "4px 0" }}>{SEP}</div>

      {/* ── TICKER RANKING (PRIMARY VIEW) ── */}
      <div style={{ color: WHITE, fontWeight: 700, padding: "4px 0" }}>
        {"  "}TICKER RANKING (SMA 1-999) | {dateStr} | {now} EST
      </div>
      <div style={{ color: DIM, fontSize: "10px", padding: "0 0 4px 0" }}>
        {"  "}Click any ticker to see the SMA program acting on it
      </div>
      <div style={{ color: DIM }}>{SEP}</div>

      <div style={{ ...row, color: DIM, fontWeight: 700, borderBottom: `1px solid ${LINE}`, padding: "2px 0" }}>
        <T w="44px">RANK</T>
        <T w="60px">TICKER</T>
        <T w="70px" align="right">TOTAL</T>
        <T w="70px" align="right">LONG</T>
        <T w="70px" align="right">SHORT</T>
        <T w="70px" align="right">L/S</T>
        <T w="200px">DOM_OUTFIT</T>
        <T w="76px">SLOPE</T>
        <T w="110px">MOMENTUM</T>
        <T w="74px">LEVEL</T>
        <T w="90px">STRUCT_BIAS</T>
        <T w="200px">KEY_SMAS</T>
        <T w="82px">PRICE_POS</T>
        <T w="90px">BIAS</T>
      </div>

      {tickers.map((t) => (
        <div key={t.rank}>
          <div
            onClick={() => setExpanded(expanded === t.ticker ? null : t.ticker)}
            style={{
              ...row, padding: "1px 0", cursor: "pointer",
              background: expanded === t.ticker ? "#111" : "transparent",
            }}
          >
            <T w="44px" c={WHITE}>{t.rank}</T>
            <T w="60px" c={CYAN} bold>
              {expanded === t.ticker ? "▼ " : "▸ "}{t.ticker}
            </T>
            <T w="70px" c={WHITE} align="right" bold>{t.total_count ?? Math.round(t.total)}</T>
            <T w="70px" c={GREEN} align="right">{t.long_count ?? Math.round(t.long)}</T>
            <T w="70px" c={RED} align="right">{t.short_count ?? Math.round(t.short)}</T>
            <T w="70px" c={t.ls_ratio > 1.5 ? GREEN : t.ls_ratio < 0.67 ? RED : YELLOW} align="right">{t.ls_ratio?.toFixed(2)}</T>
            <T w="200px" c={WHITE}>{t.dominant_outfit}</T>
            <T w="76px" c={slopeColor(t.slope)}>{t.slope}</T>
            <T w="110px" c={momentumColor(t.outfit_momentum || t.momentum)}>
              {t.outfit_momentum || t.momentum || "—"}
              {t.outfit_momentum_delta != null && t.outfit_momentum_delta !== 0 && (
                <span style={{ fontSize: "9px", fontWeight: 400 }}>
                  {" "}{t.outfit_momentum_delta > 0 ? "+" : ""}{t.outfit_momentum_delta}
                </span>
              )}
            </T>
            <T w="74px" c={biasColor(t.level)}>{t.level || "—"}</T>
            <T w="90px" c={biasColor(t.structural_bias || t.bias)}>{t.structural_bias || "N/A"}</T>
            <T w="200px" c={DIM}>{t.key_smas}</T>
            <T w="82px" c={posColor(t.price_position)}>{t.price_position}</T>
            <T w="90px" c={biasColor(t.institutional_bias || t.bias)}>{t.institutional_bias || t.bias}</T>
          </div>
          {expanded === t.ticker && (
            <TickerDetail ticker={t.ticker} />
          )}
        </div>
      ))}

      <div style={{ color: DIM, padding: "4px 0" }}>{SEP}</div>

      {/* ── ACTIVE PROGRAMS (SECONDARY — collapsible) ── */}
      <ActiveProgramsSection programs={programs} isOpen={programsOpen} onToggle={() => setProgramsOpen(!programsOpen)} />

      {/* ── SNAPSHOTS VIEWER (collapsible) ── */}
      <SnapshotsViewer isOpen={snapshotsOpen} onToggle={() => setSnapshotsOpen(!snapshotsOpen)} />

      {/* ── SMA REFERENCE TABLE (collapsible) ── */}
      <SmaReferenceTable isOpen={smaTableOpen} onToggle={() => setSmaTableOpen(!smaTableOpen)} />

      {/* ── QUICK LINKS ── */}
      <div style={{ color: WHITE, fontWeight: 700, padding: "4px 0" }}>
        {"  "}QUICK LINKS
      </div>
      <div style={{ color: DIM }}>{SEP}</div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "6px 16px", padding: "6px 0" }}>
        {[
          { label: "Health", path: "/api/health", desc: "API status" },
          { label: "Config", path: "/api/config", desc: "Outfits, tickers, timeframes" },
          { label: "Scan Status", path: "/api/scan/status", desc: "Current scan progress" },
          { label: "Schedule", path: "/api/scan/schedule", desc: "Auto-scan windows" },
          { label: "Bias", path: "/api/bias", desc: "Overall institutional bias" },
          { label: "Outfits", path: "/api/outfits", desc: "Outfit rankings (JSON)" },
          { label: "Tickers", path: "/api/tickers", desc: "Ticker rankings (JSON)" },
          { label: "Signals", path: "/api/signals", desc: "Recent signal feed" },
          { label: "Momentum", path: "/api/momentum", desc: "Per-outfit momentum data" },
          { label: "Snapshots", path: "/api/snapshots", desc: "Raw scan snapshots" },
          { label: "Snapshot Dates", path: "/api/snapshots/dates", desc: "Available snapshot dates" },
          { label: "VIX", path: "/api/vix", desc: "Current VIX level" },
          { label: "Bitcoin", path: "/api/btc", desc: "BTC analysis via Coinbase" },
          { label: "SMA Table", path: "/api/sma-table", desc: "Ticker → outfit → SMA reference" },
          { label: "Programs", path: "/api/programs", desc: "Active/terminated programs" },
          { label: "Schwab Status", path: "/api/schwab/status", desc: "Auth status & data source" },
          { label: "Schwab Auth", path: "/api/schwab/auth", desc: "Get OAuth2 login URL" },
        ].map(link => (
          <a
            key={link.path}
            href={`${API_BASE}${link.path}`}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: CYAN, fontSize: "11px", textDecoration: "none",
              padding: "2px 8px", border: `1px solid ${LINE}`, borderRadius: "3px",
              display: "inline-flex", alignItems: "center", gap: "6px",
              background: "transparent",
            }}
            onMouseEnter={e => { e.target.style.background = "#0a1a2a"; e.target.style.borderColor = CYAN; }}
            onMouseLeave={e => { e.target.style.background = "transparent"; e.target.style.borderColor = LINE; }}
            title={link.desc}
          >
            <span>{link.label}</span>
            <span style={{ color: DIM, fontSize: "9px" }}>{link.path}</span>
          </a>
        ))}
      </div>

      {/* Schwab auth helper */}
      {schwabStatus && !schwabStatus.authenticated && (
        <div style={{ padding: "6px 0", fontSize: "11px", background: "#1a0000", border: `1px solid #440000`, borderRadius: "4px", margin: "6px 0", padding: "8px 12px" }}>
          <span style={{ color: RED, fontWeight: 700 }}>Schwab not authenticated — no data available. </span>
          <span style={{ color: WHITE }}>
            Click "Schwab Auth" above, open the URL in your browser, log in,
            then the callback will auto-complete. Schwab tokens expire every 7 days.
          </span>
        </div>
      )}

      <div style={{ color: DIM, padding: "4px 0" }}>{SEP}</div>
      <div style={{ color: DIM, fontSize: "10px", padding: "4px 0" }}>
        SMA 1-999 | {outfits.length} outfits | {tickers.length} tickers | {activeCount} programs
        | {schwabStatus?.authenticated ? "Schwab" : "NO DATA"}
        | {connected ? "Live" : "No data"} | github.com/raultrades/SMA-outfits
      </div>
    </div>
  );
}
