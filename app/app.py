"""
Havbruksløftets Evidensrom — forside (romvelger).

Run from repo root:
    streamlit run app/app.py --server.fileWatcherType none
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ui import brand_header, inject_css

st.set_page_config(
    page_title="Havbruksløftets Evidensrom",
    page_icon="🌊",
    layout="wide",
)

inject_css()

# Rolig blågrå toning bak hero, kun på forsiden (speiler mockup/index.html).
st.markdown(
    """
<style>
.stApp{
  background:
    radial-gradient(ellipse 80% 46% at 8% -12%, #c5dde4 0%, transparent 55%),
    radial-gradient(ellipse 55% 38% at 92% -6%, #d8e8ef 0%, transparent 52%),
    #eef3f7;
}
</style>
""",
    unsafe_allow_html=True,
)

brand_header("Kuraterte korpus · synlig uenighet")

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="max-width:44rem; margin:22px 0 30px;">
  <p class="hl-eyebrow">Havbruksløftet · AP1</p>
  <h1 class="hl-h1">Havbruksløftets Evidensrom</h1>
  <p class="hl-lede">
    Velg et evidensrom. Hvert rom kartlegger hva akademiske publikasjoner sier om et tema.
    Korpuset er kuratert, og faglig uenighet skjules ikke.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Aktive rom ───────────────────────────────────────────────────────────────
st.markdown('<p class="hl-label">Aktive evidensrom</p>', unsafe_allow_html=True)

active_cols = st.columns(2)
with active_cols[0]:
    with st.container(border=True):
        st.markdown(
            """
<div class="hl-feature-marker"></div>
<span class="hl-status hl-status-on">Aktiv</span>
<h3 class="hl-room-title">Lakselus og dødelighet hos ville laksefisk</h3>
<p class="hl-room-desc">
  Hva akademiske publikasjoner sier om hvor mye lakselus fra oppdrett
  bidrar til dødelighet hos villaks. Hvor evidensen er uenig, og hvor datahullene er.
</p>
<div class="hl-room-meta">27 artikler · 1997-2026</div>
""",
            unsafe_allow_html=True,
        )
        st.page_link(
            "pages/1_Lakselus_og_villaks.py",
            label="Åpne rom →",
            icon="📗",
        )

with active_cols[1]:
    with st.container(border=True):
        st.markdown(
            """
<div class="hl-feature-marker"></div>
<span class="hl-status hl-status-on">Utkast</span>
<h3 class="hl-room-title">Areal og havbruk</h3>
<p class="hl-room-desc">
  Havbrukets krav på sjøareal. A skiller merdareal, lokalitetsareal og
  planareal. B viser det delte styringssystemet. C og D viser åpne
  spørsmål i forvaltningen og i forskningen. Villaks hører hjemme når
  den er lokk på vekst. Utkast.
</p>
<div class="hl-room-meta">39 dokumenter · utkast</div>
""",
            unsafe_allow_html=True,
        )
        st.page_link(
            "pages/2_Areal_og_havbruk.py",
            label="Åpne rom →",
            icon="📘",
        )

# ── Kommende rom (sekundært) ─────────────────────────────────────────────────
st.markdown(
    '<p class="hl-label" style="margin-top:26px;">Kommende evidensrom</p>',
    unsafe_allow_html=True,
)

COMING = [
    (
        "Lakselus, velferd og avlusning hos oppdrettslaks",
        "Hvordan lus og avlusingsmetoder påvirker velferd og overlevelse hos oppdrettslaks. "
        "Korpuset er under oppbygging. Ingen artikler er lagt inn ennå.",
        "0 artikler · stub",
        "soon_welfare",
    ),
    (
        "Produksjonsdødelighet hos oppdrettslaks",
        "Dødelighet i produksjon fra sykdom, håndtering, miljø og system. "
        "Gir bredere kontekst for funn som handler spesielt om lus.",
        "0 artikler · stub",
        "soon_mortality",
    ),
]

cols = st.columns(len(COMING))
for col, (title, desc, meta, key) in zip(cols, COMING):
    with col:
        with st.container(border=True):
            st.markdown(
                f"""
<div class="hl-soon-marker"></div>
<span class="hl-status hl-status-soon">Under oppbygging</span>
<h3 class="hl-room-title" style="font-size:1.05rem;">{title}</h3>
<p class="hl-room-desc" style="font-size:.9rem;">{desc}</p>
<div class="hl-room-meta">{meta}</div>
""",
                unsafe_allow_html=True,
            )
            st.button("Kommer", disabled=True, key=key, width="stretch")

# ── Footer / proveniens ──────────────────────────────────────────────────────
st.markdown(
    """
<div class="hl-footer">
  Metode: Honest Broker (Pielke 2007). Vi viser evidensen, usikkerheten og den faglige
  uenigheten. Vi lager ikke en kunstig konsensus.<br>
  Korpus: <a href="https://github.com/hakonbakke/ap1-curated-corpora">hakonbakke/ap1-curated-corpora</a>.
  Finansiert av FHF / Havbruksløftet AP1. Kan på sikt inngå i Bluetalk.
</div>
""",
    unsafe_allow_html=True,
)
