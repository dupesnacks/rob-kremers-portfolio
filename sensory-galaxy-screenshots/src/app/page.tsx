"use client";

import { useState, useRef } from "react";
import { toPng } from "html-to-image";

const EXPORT_W = 1125;
const EXPORT_H = 2436;

const SCREENSHOTS = [
  { id: "explorePlanets", file: "exploreplanets.png", dualPhone: false },
  { id: "explorerSelection", file: "explorerselection.png", dualPhone: false },
  { id: "exploringJourney", file: "exploringjourney.png", dualPhone: false },
  { id: "foodExploration", file: "foodexploration.png", dualPhone: false },
  { id: "goalFood", file: "goal food.png", dualPhone: false },
  { id: "setupFoods", file: "setup foods.png", dualPhone: false },
];

const DEFAULT_CAPTIONS: Record<string, { headline: string; subheading: string }> = {
  "explorePlanets": { headline: "", subheading: "" },
  "explorerSelection": { headline: "", subheading: "" },
  "exploringJourney": { headline: "", subheading: "" },
  "foodExploration": { headline: "", subheading: "" },
  "goalFood": { headline: "", subheading: "" },
  "setupFoods": { headline: "", subheading: "" },
};

function ExportCard({ id, file, dualPhone }: { id: string; file: string; dualPhone: boolean }) {
  const [headline, setHeadline] = useState(DEFAULT_CAPTIONS[id].headline);
  const [subheading, setSubheading] = useState(DEFAULT_CAPTIONS[id].subheading);
  const canvasRef = useRef<HTMLDivElement>(null);

  const handleExport = async () => {
    if (!canvasRef.current) return;

    const element = canvasRef.current;
    element.style.position = "absolute";
    element.style.left = "0";
    element.style.top = "0";
    element.style.zIndex = "9999";

    try {
      await toPng(element, { width: EXPORT_W, height: EXPORT_H, pixelRatio: 1 });
      const dataUrl = await toPng(element, { width: EXPORT_W, height: EXPORT_H, pixelRatio: 1 });
      const link = document.createElement("a");
      link.download = `${id}-${EXPORT_W}x${EXPORT_H}.png`;
      link.href = dataUrl;
      link.click();
    } catch (e) {
      console.error("Export failed:", e);
    } finally {
      element.style.position = "absolute";
      element.style.left = "-9999px";
      element.style.top = "-9999px";
      element.style.zIndex = "auto";
    }
  };

  return (
    <div style={{ padding: "15px", background: "white", borderRadius: "8px", marginBottom: "15px" }}>
      {/* Hidden export canvas */}
      <div
        ref={canvasRef}
        style={{
          width: EXPORT_W,
          height: EXPORT_H,
          background: "linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(102, 126, 234, 0.1))",
          padding: "50px 30px 50px",
          boxSizing: "border-box",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          fontFamily: "system-ui, sans-serif",
          color: "white",
          position: "absolute",
          left: "-9999px",
          top: "-9999px",
          gap: "40px",
          overflow: "hidden",
        }}
      >
        {/* Text - fills available space */}
        <div style={{ textAlign: "center", flex: "1 1 auto" }}>
          <h1 style={{ fontSize: "100px", fontWeight: "800", color: "#00d9ff", margin: "0 0 30px 0", lineHeight: "0.95", letterSpacing: "-3px" }}>
            {headline}
          </h1>
          <p style={{ fontSize: "52px", fontWeight: "600", margin: 0, color: "rgba(255,255,255,0.85)", letterSpacing: "-1px", lineHeight: "1.1" }}>
            {subheading}
          </p>
        </div>

        {/* Phones */}
        <div style={{ display: "flex", justifyContent: "center", gap: dualPhone ? "60px" : "0", width: "100%", flex: "0 1 auto" }}>
          <img
            src={`/screenshots/${file}`}
            alt=""
            style={{
              width: dualPhone ? "48%" : "80%",
              height: "auto",
              borderRadius: "35px",
              border: "14px solid #1a1a2e",
              boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
              display: "block",
            }}
          />
          {dualPhone && (
            <img
              src={`/screenshots/${file}`}
              alt=""
              style={{
                width: "48%",
                height: "auto",
                borderRadius: "35px",
                border: "14px solid #1a1a2e",
                boxShadow: "0 20px 60px rgba(0,0,0,0.5)",
                display: "block",
              }}
            />
          )}
        </div>
      </div>

      {/* Visible preview */}
      <div style={{ display: "flex", gap: "12px", marginBottom: "12px" }}>
        <div style={{ width: dualPhone ? "120px" : "100px" }}>
          <img src={`/screenshots/${file}`} alt="" style={{ width: "100%", borderRadius: "12px", border: "1px solid #ddd" }} />
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: "11px", color: "#666", marginBottom: "4px" }}>Headline</div>
          <input
            value={headline}
            onChange={(e) => setHeadline(e.target.value)}
            style={{ width: "100%", padding: "6px", fontSize: "12px", marginBottom: "8px", border: "1px solid #ddd", borderRadius: "4px", boxSizing: "border-box" }}
          />
          <div style={{ fontSize: "11px", color: "#666", marginBottom: "4px" }}>Subheading</div>
          <input
            value={subheading}
            onChange={(e) => setSubheading(e.target.value)}
            style={{ width: "100%", padding: "6px", fontSize: "12px", border: "1px solid #ddd", borderRadius: "4px", boxSizing: "border-box" }}
          />
          {dualPhone && <div style={{ fontSize: "10px", color: "#999", marginTop: "8px" }}>✓ Dual phone export</div>}
        </div>
      </div>

      <button
        onClick={handleExport}
        style={{
          width: "100%",
          padding: "8px",
          background: "linear-gradient(135deg, #00d9ff, #667eea)",
          color: "white",
          border: "none",
          borderRadius: "4px",
          fontWeight: "600",
          cursor: "pointer",
          fontSize: "12px",
        }}
      >
        Export
      </button>
    </div>
  );
}

export default function Page() {
  const [layout, setLayout] = useState<"1" | "2" | "3">("2");

  return (
    <div style={{ padding: "30px 20px", maxWidth: "1200px", margin: "0 auto", fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ fontSize: "24px", marginBottom: "8px" }}>Sensory Galaxy Screenshots</h1>
      <p style={{ color: "#666", marginBottom: "20px", fontSize: "14px" }}>Edit captions and export at 1125x2436px</p>

      <div style={{ marginBottom: "20px", display: "flex", gap: "12px" }}>
        <select
          value={layout}
          onChange={(e) => setLayout(e.target.value as "1" | "2" | "3")}
          style={{
            padding: "6px 10px",
            border: "1px solid #ddd",
            borderRadius: "4px",
            fontSize: "12px",
          }}
        >
          <option value="1">1 Column</option>
          <option value="2">2 Columns</option>
          <option value="3">3 Columns</option>
        </select>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: layout === "1" ? "1fr" : layout === "2" ? "1fr 1fr" : "1fr 1fr 1fr",
          gap: "15px",
        }}
      >
        {SCREENSHOTS.map((ss) => (
          <ExportCard key={ss.id} id={ss.id} file={ss.file} dualPhone={ss.dualPhone} />
        ))}
      </div>
    </div>
  );
}
