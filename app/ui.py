"""
Delt UI-lag for Havbruksløftets Evidensrom.

Holder all custom CSS og små HTML-hjelpere samlet ett sted, slik at
sidene (app.py og rom-sidene) kan dele visuell identitet uten å duplisere
styling eller drive skjør DOM-targeting rundt i koden.

Designtokens er hentet fra HTML-mockupen (mockup/index.html,
mockup/tema-villaks.html) som er visuell fasit.
"""

from __future__ import annotations

from html import escape

import streamlit as st

# ── Designtokens (speiler mockupen) ────────────────────────────────────────────

ACCENT = "#005f73"

_BASE_CSS = """
<style>
:root{
  --hl-ink:#15232b;
  --hl-muted:#5b6b75;
  --hl-line:#d5dee6;
  --hl-accent:#005f73;
  --hl-accent-soft:#e6f2f5;
  --hl-soft:#f4f7fa;
  --hl-surface:#ffffff;
  --hl-radius:14px;
  --hl-shadow:0 1px 2px rgba(21,35,43,.04), 0 8px 24px rgba(21,35,43,.05);
  --hl-ok:#1e5a35; --hl-ok-bg:#e5f3ea;
  --hl-warn:#6a5218; --hl-warn-bg:#f6f0dd;
}

/* Romslig, sentrert innholdsbredde (mockup ~1240px) */
.block-container{
  max-width:1240px;
  margin-left:auto; margin-right:auto;
  padding-top:1.6rem; padding-bottom:4rem;
}

/* Dempet Streamlit-topplinje så vår egen brand-linje får ro */
[data-testid="stHeader"]{background:transparent;}

/* Typografi */
h1,h2,h3{ letter-spacing:-.02em; color:var(--hl-ink); }
h1{ line-height:1.14; }

/* Kort: hvite flater mot lys blågrå bakgrunn */
[data-testid="stVerticalBlockBorderWrapper"]{
  background:var(--hl-surface);
  border:1px solid var(--hl-line);
  border-radius:var(--hl-radius);
  box-shadow:var(--hl-shadow);
}
/* Feature-kort (aktivt rom) og dempet "kommer"-kort via sentinel-markører */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div .hl-feature-marker){
  border-left:4px solid var(--hl-accent);
}
[data-testid="stVerticalBlockBorderWrapper"]:has(> div .hl-soon-marker){
  background:var(--hl-soft);
}

/* Brand-topplinje */
.hl-topbar{
  display:flex; align-items:center; justify-content:space-between;
  gap:16px; flex-wrap:wrap;
  padding:6px 0 14px; margin-bottom:6px;
  border-bottom:1px solid var(--hl-line);
}
.hl-brand{ display:flex; align-items:center; gap:11px; }
.hl-mark{
  width:34px; height:34px; border-radius:9px;
  background:var(--hl-accent); color:#fff;
  display:grid; place-items:center;
  font-size:.78rem; font-weight:700; letter-spacing:-.02em;
}
.hl-brand-text{ display:flex; flex-direction:column; line-height:1.2; }
.hl-brand-text strong{ font-size:.98rem; color:var(--hl-ink); }
.hl-brand-text span{ font-size:.74rem; font-weight:500; color:var(--hl-muted); }
.hl-brand-right{ font-size:.82rem; color:var(--hl-muted); }

/* Hero */
.hl-eyebrow{
  font-size:.8rem; font-weight:600; letter-spacing:.05em;
  text-transform:uppercase; color:var(--hl-accent);
  margin:2px 0 8px;
}
.hl-h1{
  font-size:clamp(2rem,3vw,2.6rem);
  letter-spacing:-.03em; line-height:1.12;
  margin:0 0 12px; color:var(--hl-ink);
}
.hl-lede{ color:var(--hl-muted); font-size:1.08rem; margin:0; max-width:44rem; }

/* Etiketter / smått */
.hl-label{ font-size:.85rem; font-weight:600; color:var(--hl-muted); margin:6px 0 2px; }
.hl-note{ font-size:.8rem; color:var(--hl-muted); margin:0 0 4px; }
.hl-crumb{ font-size:.82rem; color:var(--hl-muted); margin:2px 0 10px; }
.hl-muted{ color:var(--hl-muted); }

/* Seksjonshode med tag-pill */
.hl-section-head{
  display:flex; align-items:baseline; justify-content:space-between;
  gap:12px; flex-wrap:wrap; margin:6px 0 10px;
}
.hl-section-head h2{ font-size:1.4rem; margin:0; }
.hl-tag{
  display:inline-block; font-size:.7rem; font-weight:700;
  letter-spacing:.04em; text-transform:uppercase;
  color:var(--hl-accent); background:var(--hl-accent-soft);
  padding:4px 10px; border-radius:999px; white-space:nowrap;
}

/* Statusmerker (rom-kort) */
.hl-status{
  display:inline-block; font-size:.72rem; font-weight:600;
  padding:3px 10px; border-radius:999px;
}
.hl-status-on{ background:var(--hl-ok-bg); color:var(--hl-ok); }
.hl-status-soon{ background:var(--hl-warn-bg); color:var(--hl-warn); }

/* Rom-kort tekst */
.hl-room-title{ font-size:1.2rem; letter-spacing:-.02em; margin:10px 0 6px; color:var(--hl-ink); }
.hl-room-desc{ color:var(--hl-muted); font-size:.96rem; margin:0; }
.hl-room-meta{
  margin-top:14px; padding-top:12px; border-top:1px solid var(--hl-line);
  font-size:.82rem; color:var(--hl-muted);
}

/* Kompakt stats-panel (rom-hero) */
.hl-stats{ display:grid; grid-template-columns:1fr 1fr; gap:14px 12px; }
.hl-stat strong{ display:block; font-size:1.35rem; letter-spacing:-.02em; color:var(--hl-accent); }
.hl-stat span{ font-size:.8rem; color:var(--hl-muted); }

/* Figurtekst */
.hl-figcap{ font-size:.82rem; color:var(--hl-muted); margin-top:8px; line-height:1.4; }

/* Placeholder (mangler kildedata) */
.hl-placeholder{
  background:var(--hl-soft); border:1px dashed #b7c2cc; color:var(--hl-muted);
  padding:10px 12px; margin:8px 0 0; font-size:.9rem; border-radius:10px;
}

/* Nummerert kunnskapskjede (B) */
.hl-chain{ margin:12px 0 0; padding:0; list-style:none; counter-reset:step; }
.hl-chain li{
  position:relative; padding:8px 0 8px 34px;
  border-left:2px solid var(--hl-accent-soft); margin-left:10px; font-size:.94rem;
}
.hl-chain li::before{
  counter-increment:step; content:counter(step);
  position:absolute; left:-12px; top:7px; width:22px; height:22px;
  border-radius:50%; background:var(--hl-accent); color:#fff;
  font-size:.72rem; font-weight:700; display:grid; place-items:center;
}

/* Paper-chips (C + kilder) */
.hl-papers{ margin:12px 0 0; display:flex; flex-wrap:wrap; gap:6px; }
.hl-paper{
  font-family:ui-monospace,Consolas,monospace; font-size:.72rem;
  background:var(--hl-accent-soft); color:var(--hl-accent);
  border-radius:6px; padding:3px 8px;
}
.hl-caveat{ font-size:.86rem; color:var(--hl-muted); font-style:italic; margin:10px 0 0; }

/* Footer */
.hl-footer{
  margin-top:34px; padding-top:16px; border-top:1px solid var(--hl-line);
  font-size:.82rem; color:var(--hl-muted);
}
</style>
"""


def inject_css() -> None:
    """Injiser den delte CSS-en. Kall én gang tidlig på hver side."""
    st.markdown(_BASE_CSS, unsafe_allow_html=True)


def brand_header(subtitle: str, right: str = "") -> None:
    """Brand-topplinje som speiler mockupens topbar."""
    right_html = f'<span class="hl-brand-right">{escape(right)}</span>' if right else ""
    st.markdown(
        f"""
<div class="hl-topbar">
  <div class="hl-brand">
    <span class="hl-mark">HL</span>
    <span class="hl-brand-text">
      <strong>Havbruksløftets Evidensrom</strong>
      <span>{escape(subtitle)}</span>
    </span>
  </div>
  {right_html}
</div>
""",
        unsafe_allow_html=True,
    )


def section_header(label: str, tag: str) -> None:
    """Seksjonshode med tittel til venstre og tag-pill til høyre."""
    st.markdown(
        f'<div class="hl-section-head"><h2>{escape(label)}</h2>'
        f'<span class="hl-tag">{escape(tag)}</span></div>',
        unsafe_allow_html=True,
    )


def paper_chips(doc_ids: list[str]) -> None:
    """Rad med monospace paper-chips (korpus-ID-er)."""
    if not doc_ids:
        return
    chips = "".join(f'<span class="hl-paper">{escape(d)}</span>' for d in doc_ids)
    st.markdown(f'<div class="hl-papers">{chips}</div>', unsafe_allow_html=True)
