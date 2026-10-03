"""
HTML report writer — produces a professional, self-contained HTML report
with a dark terminal aesthetic suitable for sharing, archiving, or
attaching to engagement deliverables.

No external dependencies — everything (CSS, layout) is embedded so the
file opens anywhere and works offline.
"""

import html
from datetime import datetime, timezone


# ──────────────────────────────────────────────────────────────────────
# Color mapping (matches CLI)
# ──────────────────────────────────────────────────────────────────────

VERDICT_META = {
    "vulnerable":  {"label": "VULNERABLE",  "color": "#ff4444", "icon": "✕"},
    "uncertain":   {"label": "UNCERTAIN",   "color": "#ffaa33", "icon": "?"},
    "likely_safe": {"label": "LIKELY SAFE", "color": "#00ff9d", "icon": "✓"},
    "error":       {"label": "ERROR",       "color": "#888888", "icon": "!"},
}


# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

def _esc(text):
    """HTML-escape and coerce to string."""
    if text is None:
        return ""
    return html.escape(str(text))


def _truncate(text, n=400):
    """Truncate long text with an ellipsis marker."""
    if text is None:
        return ""
    s = str(text)
    if len(s) <= n:
        return s
    return s[:n] + " …[truncated]"


def _confidence_bar(confidence):
    """Render a small confidence bar (0.0–1.0)."""
    pct = max(0, min(100, int(round(confidence * 100))))
    color = "#ff4444" if pct >= 60 else ("#ffaa33" if pct >= 20 else "#00ff9d")
    return (
        f'<div class="conf-bar">'
        f'  <div class="conf-fill" style="width:{pct}%;background:{color}"></div>'
        f'</div>'
        f'<span class="conf-num">{confidence:.2f}</span>'
    )


def _render_finding(r):
    meta = VERDICT_META.get(r["verdict"], VERDICT_META["error"])
    response = r.get("response_text") or ""
    reasons = r.get("reasons", [])
    reasons_html = "".join(f"<li>{_esc(x)}</li>" for x in reasons) or "<li>—</li>"

    return f"""
    <div class="finding verdict-{_esc(r['verdict'])}">
      <div class="finding-header">
        <div class="finding-id">{_esc(r['id'])}</div>
        <div class="finding-cat">{_esc(r['category'])}</div>
        <div class="finding-verdict" style="color:{meta['color']}">
          [{meta['icon']}] {meta['label']}
        </div>
      </div>

      <div class="finding-conf">
        <span class="conf-label">confidence</span>
        {_confidence_bar(r.get('confidence', 0.0))}
        <span class="conf-elapsed">{_esc(r.get('elapsed_seconds', 0))}s</span>
      </div>

      <div class="finding-block">
        <div class="block-label">Payload</div>
        <pre class="block-pre payload">{_esc(_truncate(r.get('payload_text', ''), 500))}</pre>
      </div>

      <div class="finding-block">
        <div class="block-label">Response</div>
        <pre class="block-pre response">{_esc(_truncate(response, 800)) or '(empty)'}</pre>
      </div>

      <div class="finding-block">
        <div class="block-label">Detection signals</div>
        <ul class="reasons">{reasons_html}</ul>
      </div>
    </div>
    """


# ──────────────────────────────────────────────────────────────────────
# Main writer
# ──────────────────────────────────────────────────────────────────────

def write_html_report(results, summary, target_name, output_path):
    """Write a full HTML report. Returns the output path."""

    # Partition results by verdict for grouped display
    by_verdict = {"vulnerable": [], "uncertain": [], "likely_safe": [], "error": []}
    for r in results:
        by_verdict.setdefault(r["verdict"], []).append(r)

    # Order: vulnerable first (most important), then uncertain, then safe, then errors
    display_order = ["vulnerable", "uncertain", "likely_safe", "error"]
    findings_html = ""
    for verdict in display_order:
        group = by_verdict.get(verdict, [])
        if not group:
            continue
        meta = VERDICT_META[verdict]
        findings_html += f"""
        <div class="group">
          <h3 class="group-title" style="border-color:{meta['color']};color:{meta['color']}">
            [{meta['icon']}] {meta['label']} — {len(group)} finding{'s' if len(group) != 1 else ''}
          </h3>
          {''.join(_render_finding(r) for r in group)}
        </div>
        """

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DIVYASTRA Report — {_esc(target_name)}</title>
<style>
  :root {{
    --bg:       #0a0a0f;
    --surface:  #13131c;
    --surface2: #1a1a26;
    --border:   #222232;
    --text:     #e8e8f0;
    --text-dim: #8080a8;
    --accent:   #00ff9d;
    --red:      #ff4444;
    --orange:   #ffaa33;
    --green:    #00ff9d;
    --gray:     #888888;
    --mono: 'SF Mono', 'Consolas', 'Monaco', 'Courier New', monospace;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: var(--mono);
    font-size: 13px;
    line-height: 1.6;
    padding: 40px 20px;
  }}
  .container {{ max-width: 1000px; margin: 0 auto; }}

  /* Header */
  header {{
    border: 1px solid var(--border);
    border-top: 3px solid var(--accent);
    background: var(--surface);
    padding: 28px 32px;
    margin-bottom: 24px;
  }}
  header h1 {{
    margin: 0 0 8px 0;
    font-size: 22px;
    letter-spacing: 2px;
    color: var(--accent);
  }}
  header .subtitle {{
    color: var(--text-dim);
    font-size: 12px;
    margin-bottom: 16px;
  }}
  header .meta-row {{
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
    font-size: 12px;
    color: var(--text-dim);
  }}
  header .meta-row strong {{ color: var(--text); }}

  /* Summary cards */
  .summary-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-bottom: 32px;
  }}
  .summary-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 18px 20px;
    text-align: center;
  }}
  .summary-card .num {{
    font-size: 28px;
    font-weight: 700;
    display: block;
    margin-bottom: 6px;
  }}
  .summary-card .lbl {{
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-dim);
  }}
  .summary-card.total    .num {{ color: var(--text); }}
  .summary-card.vuln     .num {{ color: var(--red); }}
  .summary-card.uncertain .num {{ color: var(--orange); }}
  .summary-card.safe     .num {{ color: var(--green); }}
  .summary-card.error    .num {{ color: var(--gray); }}

  /* Group */
  .group {{ margin-bottom: 40px; }}
  .group-title {{
    font-size: 14px;
    letter-spacing: 1px;
    padding-bottom: 10px;
    margin: 0 0 20px 0;
    border-bottom: 1px solid;
  }}

  /* Finding card */
  .finding {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--border);
    padding: 20px 24px;
    margin-bottom: 16px;
  }}
  .finding.verdict-vulnerable  {{ border-left-color: var(--red); }}
  .finding.verdict-uncertain   {{ border-left-color: var(--orange); }}
  .finding.verdict-likely_safe {{ border-left-color: var(--green); }}
  .finding.verdict-error       {{ border-left-color: var(--gray); }}

  .finding-header {{
    display: flex;
    gap: 16px;
    align-items: baseline;
    flex-wrap: wrap;
    margin-bottom: 14px;
  }}
  .finding-id {{
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
  }}
  .finding-cat {{
    font-size: 11px;
    color: var(--text-dim);
    padding: 2px 10px;
    background: var(--surface2);
    border: 1px solid var(--border);
    letter-spacing: 1px;
  }}
  .finding-verdict {{
    font-size: 11px;
    letter-spacing: 1px;
    margin-left: auto;
    font-weight: 700;
  }}

  .finding-conf {{
    display: flex;
    gap: 12px;
    align-items: center;
    margin-bottom: 16px;
    font-size: 11px;
    color: var(--text-dim);
  }}
  .conf-label {{ letter-spacing: 1px; text-transform: uppercase; }}
  .conf-bar {{
    flex: 1;
    height: 4px;
    background: var(--surface2);
    max-width: 200px;
    position: relative;
  }}
  .conf-fill {{ height: 100%; }}
  .conf-num {{ color: var(--text); }}
  .conf-elapsed {{ margin-left: auto; }}

  .finding-block {{ margin-bottom: 14px; }}
  .block-label {{
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 6px;
  }}
  .block-pre {{
    background: #06060b;
    border: 1px solid var(--border);
    padding: 12px 14px;
    margin: 0;
    font-family: var(--mono);
    font-size: 12px;
    line-height: 1.55;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
    overflow-x: auto;
    max-height: 320px;
    overflow-y: auto;
  }}
  .block-pre.payload {{ border-left: 2px solid var(--orange); }}
  .block-pre.response {{ border-left: 2px solid var(--accent); }}

  .reasons {{
    margin: 0;
    padding-left: 20px;
    font-size: 12px;
    color: var(--text);
  }}
  .reasons li {{ margin-bottom: 4px; }}

  /* Footer */
  footer {{
    margin-top: 48px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
    font-size: 11px;
    color: var(--text-dim);
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }}
  footer .brand {{ color: var(--accent); letter-spacing: 2px; }}

  @media (max-width: 640px) {{
    body {{ padding: 20px 12px; font-size: 12px; }}
    header {{ padding: 20px; }}
    .finding {{ padding: 16px; }}
    .finding-verdict {{ margin-left: 0; width: 100%; }}
  }}
</style>
</head>
<body>
<div class="container">

  <header>
    <h1>⚔ DIVYASTRA — Prompt Injection Vulnerability Report</h1>
    <div class="subtitle">Automated AI/LLM red-teaming assessment</div>
    <div class="meta-row">
      <div><strong>Target</strong> · {_esc(target_name)}</div>
      <div><strong>Generated</strong> · {generated}</div>
      <div><strong>Payloads</strong> · {summary['total']}</div>
      <div><strong>Tool</strong> · DIVYASTRA v2.0.0</div>
    </div>
  </header>

  <div class="summary-grid">
    <div class="summary-card total">    <span class="num">{summary['total']}</span>       <span class="lbl">Total</span></div>
    <div class="summary-card vuln">     <span class="num">{summary['vulnerable']}</span>  <span class="lbl">Vulnerable</span></div>
    <div class="summary-card uncertain"><span class="num">{summary['uncertain']}</span>   <span class="lbl">Uncertain</span></div>
    <div class="summary-card safe">     <span class="num">{summary['likely_safe']}</span><span class="lbl">Likely Safe</span></div>
    <div class="summary-card error">    <span class="num">{summary['error']}</span>       <span class="lbl">Errors</span></div>
  </div>

  {findings_html}

  <footer>
    <div class="brand">DIVYASTRA — The Divine Weapon for AI Security</div>
    <div>Generated by Nilanjan Chowdhury · github.com/CalculusGuy/DIVYASTRA</div>
  </footer>

</div>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc)

    return output_path
