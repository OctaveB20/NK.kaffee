"""
ARA by NK – Prototyp der Restaurant-Website (nur Darstellung)
Start: streamlit run app.py
Das Logo (logo.jpg) liegt im selben Ordner wie diese Datei.
"""

import base64
from datetime import datetime
from pathlib import Path

import streamlit as st

try:
    from zoneinfo import ZoneInfo
    BERLIN = ZoneInfo("Europe/Berlin")
except Exception:  # Fallback, falls keine Zeitzonen-Daten vorhanden sind
    BERLIN = None

st.set_page_config(
    page_title="ARA by NK | Korean Street Food in Regensburg",
    page_icon="🍢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# Daten
# --------------------------------------------------------------------------
ADRESSE = "Weiße-Lilien-Straße 6, 93047 Regensburg"
TELEFON_ANZEIGE = "0941 20916513"
TELEFON_LINK = "+4994120916513"
INSTAGRAM = "https://www.instagram.com/nk.kaffee"

OEFFNUNGSZEITEN = [
    ("Montag", "Geschlossen"),
    ("Dienstag", "12:00 – 18:45"),
    ("Mittwoch", "12:00 – 18:45"),
    ("Donnerstag", "12:00 – 18:45"),
    ("Freitag", "12:00 – 18:45"),
    ("Samstag", "12:00 – 18:45"),
    ("Sonntag", "Geschlossen"),
]

# (Name, Beschreibung, Preis, Hinweise)
SPEISEKARTE = {
    "Chibap": [
        ("Sesam Chicken", "", "8,50 €", []),
        ("Yangnyeom Chicken", "", "8,50 €", []),
        ("Soy Garlic Chicken", "", "8,50 €", []),
    ],
    "Corn Dogs": [
        ("Original Hot Corn Dog", "", "6,00 €", []),
        ("Full Cheese Corn Dog", "Mit Gouda", "6,00 €", ["vegetarisch"]),
        ("Half and Half Corn Dog", "Eine Hälfte Corn Dog, eine Hälfte Gouda", "6,00 €", ["vegetarisch"]),
        ("Potato Hot Corn Dog", "Mit Gouda", "6,50 €", []),
        ("Potato Cheese Corn Dog", "Mit Gouda", "6,50 €", ["vegetarisch"]),
        ("Potato Half and Half Corn Dog", "Eine Hälfte Corn Dog, eine Hälfte Gouda", "6,50 €", ["vegetarisch"]),
    ],
    "Hauptspeisen": [
        ("Bibimbap Spiegelei", "Koreanische Reisschale mit Spiegelei, Karotten, Champignons, Sesam, Sesamöl und Saisongemüse. Lauwarm, mit Sauce nach Wahl.", "12,50 €", []),
        ("Bibimbap Hähnchen", "Koreanische Reisschale mit Hähnchenfleisch, Karotten, Champignons, Sesam, Sesamöl und Saisongemüse. Lauwarm, mit Sauce nach Wahl.", "13,50 €", []),
        ("Bibimbap Bulgogi", "Koreanische Reisschale mit Rindhackfleisch, Karotten, Champignons, Sesam, Sesamöl und Saisongemüse. Lauwarm, mit Sauce nach Wahl.", "14,90 €", []),
    ],
    "Salate": [
        ("Großer Salat mit Popcorn Chicken", "Eisbergsalat, Gurken, Karotten, Kimchi, Rettich und Halal Popcorn Chicken", "7,50 €", ["halal"]),
    ],
    "Extras": [
        ("Kimchi", "", "4,50 €", ["scharf"]),
        ("Rettich", "", "4,50 €", ["vegan"]),
        ("Reis", "", "2,50 €", ["vegan"]),
    ],
    "Getränke": [
        ("Coca-Cola", "0,33 l, Einweg", "3,75 €", []),
        ("Coca-Cola Zero Sugar", "0,33 l, Einweg", "3,75 €", []),
        ("Fanta Orange", "0,33 l, Einweg", "3,75 €", []),
        ("Sprite", "0,33 l, Einweg", "3,75 €", []),
    ],
}


# --------------------------------------------------------------------------
# Helfer
# --------------------------------------------------------------------------
def html(block: str) -> None:
    """Rendert HTML ohne Einrückungen und Leerzeilen (sonst macht Markdown Code daraus)."""
    cleaned = "\n".join(line.strip() for line in block.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def logo_data_uri() -> str:
    pfad = Path(__file__).parent / "logo.jpg"
    if not pfad.exists():
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(pfad.read_bytes()).decode()


def jetzt():
    return datetime.now(BERLIN) if BERLIN else datetime.now()


def ist_geoeffnet(t: datetime) -> bool:
    minuten = t.hour * 60 + t.minute
    return 1 <= t.weekday() <= 5 and 12 * 60 <= minuten < 18 * 60 + 45


def menue_zeilen(eintraege) -> str:
    zeilen = []
    for name, beschreibung, preis, hinweise in eintraege:
        tags = "".join(f'<span class="tag">{h}</span>' for h in hinweise)
        zeilen.append(
            f'<div class="item"><div class="item-row">'
            f'<span class="item-name">{name}</span>{tags}'
            f'<span class="item-dots"></span>'
            f'<span class="item-price">{preis}</span></div>'
            + (f'<p class="item-desc">{beschreibung}</p>' if beschreibung else "")
            + "</div>"
        )
    return "".join(zeilen)


# --------------------------------------------------------------------------
# Design: Rot zuerst, dann Gelb, dann Weiß
# --------------------------------------------------------------------------
html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,800;1,800&family=Barlow:wght@400;500;600&display=swap');

:root {
  --rot: #D62F27;
  --rot-tief: #A91E18;
  --gelb: #F2A91F;
  --gelb-hell: #FBE3A8;
  --weiss: #FFFFFF;
  --tinte: #2A1311;
}

/* Streamlit-Rahmen entfernen, Seite randlos machen */
#MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
.stApp { background: var(--weiss); }
.block-container { max-width: 100% !important; padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stMarkdownContainer"] p { margin: 0; }
html { scroll-behavior: smooth; }

.ara, .ara * { box-sizing: border-box; font-family: 'Barlow', sans-serif; }
.ara h1, .ara h2, .ara h3 { font-family: 'Barlow Condensed', sans-serif; margin: 0; letter-spacing: .01em; }
.inner { max-width: 1120px; margin: 0 auto; padding: 0 28px; }

/* 1 · Rot: Hero */
.hero { background: var(--rot); color: var(--weiss); padding: 72px 0 80px; }
.hero .inner { display: grid; grid-template-columns: 1.25fr 1fr; gap: 56px; align-items: center; }
.hero h1 { font-weight: 800; font-style: italic; text-transform: uppercase; font-size: clamp(3rem, 7.2vw, 6rem); line-height: .94; }
.hero p.lead { font-size: 1.2rem; line-height: 1.55; max-width: 34em; margin: 26px 0 34px; color: #FFF3F2; }
.status { display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.4); padding: 8px 16px; border-radius: 999px; font-weight: 600; font-size: .95rem; margin-bottom: 26px; }
.status i { width: 10px; height: 10px; border-radius: 50%; background: var(--gelb); display: inline-block; }
.status.zu i { background: #fff; opacity: .6; }
.btns { display: flex; flex-wrap: wrap; gap: 14px; }
.btn { display: inline-block; padding: 14px 28px; border-radius: 999px; font-weight: 600; font-size: 1.05rem; text-decoration: none !important; }
.btn.gelb { background: var(--gelb); color: var(--tinte) !important; }
.btn.rand { border: 2px solid var(--weiss); color: var(--weiss) !important; }
.btn:focus-visible { outline: 3px solid var(--weiss); outline-offset: 3px; }
.logo-wrap { display: flex; justify-content: center; }
.logo-wrap img { width: min(100%, 400px); aspect-ratio: 1; border-radius: 50%; object-fit: cover; transform: scale(1.01); box-shadow: 0 0 0 10px rgba(255,255,255,.18); }

/* 2 · Gelb: Eckdaten */
.fakten { background: var(--gelb); color: var(--tinte); padding: 52px 0; }
.fakten .inner { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
.fakten h3 { font-weight: 800; font-size: 2rem; color: var(--rot-tief); margin-bottom: 8px; }
.fakten p { font-size: 1.05rem; line-height: 1.55; }

/* 3 · Weiß: Speisekarte */
.karte { background: var(--weiss); color: var(--tinte); padding: 80px 0 24px; }
.karte h2, .zeiten h2 { font-weight: 800; font-style: italic; text-transform: uppercase; font-size: clamp(2.4rem, 5vw, 3.8rem); line-height: 1; color: var(--rot); }
.karte p.intro { font-size: 1.1rem; margin-top: 14px; max-width: 36em; line-height: 1.55; }
[data-testid="stTabs"] { max-width: 1120px; margin: 0 auto; padding: 24px 28px 72px; }
button[data-baseweb="tab"] { font-family: 'Barlow Condensed', sans-serif !important; font-weight: 800; font-size: 1.35rem !important; padding: 10px 18px !important; color: var(--tinte) !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--rot) !important; }
[data-baseweb="tab-highlight"] { background-color: var(--rot) !important; height: 4px !important; }
[data-baseweb="tab-border"] { background-color: var(--gelb-hell) !important; }
.item { padding: 18px 0 6px; max-width: 760px; }
.item-row { display: flex; align-items: baseline; gap: 10px; }
.item-name { font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 1.55rem; color: var(--tinte); }
.item-dots { flex: 1; border-bottom: 2px dotted #E2B54F; transform: translateY(-5px); min-width: 24px; }
.item-price { font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 1.55rem; color: var(--rot-tief); white-space: nowrap; }
.item-desc { color: #5B4340; font-size: 1rem; line-height: 1.5; margin-top: 2px !important; max-width: 36em; }
.tag { background: var(--gelb); color: var(--tinte); font-size: .8rem; font-weight: 600; padding: 2px 10px; border-radius: 999px; }
.hinweis { max-width: 760px; margin-top: 36px; padding: 16px 20px; background: var(--gelb-hell); border-left: 6px solid var(--gelb); font-size: 1rem; line-height: 1.5; color: var(--tinte); }

/* Rot: Öffnungszeiten & Kontakt */
.zeiten { background: var(--rot); color: var(--weiss); padding: 80px 0; }
.zeiten h2 { color: var(--weiss); }
.zeiten .inner { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; }
.zeiten table { width: 100%; border-collapse: collapse; margin-top: 26px; }
.zeiten td { padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,.35); font-size: 1.1rem; }
.zeiten td:last-child { text-align: right; }
.zeiten tr.heute td { font-weight: 600; color: var(--gelb-hell); }
.kontakt p { font-size: 1.15rem; line-height: 1.7; margin-top: 22px; }
.kontakt a { color: var(--weiss); font-weight: 600; text-decoration: underline; text-underline-offset: 4px; }
.kontakt .btns { margin-top: 28px; }

/* Gelb: Fußzeile */
.fuss { background: var(--gelb); color: var(--tinte); padding: 28px 0; font-size: .95rem; }
.fuss .inner { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; }
.fuss a { color: var(--tinte); font-weight: 600; }

@media (max-width: 860px) {
  .hero .inner, .fakten .inner, .zeiten .inner { grid-template-columns: 1fr; gap: 36px; }
  .hero { padding: 48px 0 56px; }
  .logo-wrap { order: -1; }
  .logo-wrap img { width: min(70%, 280px); }
  .karte { padding-top: 56px; }
  .zeiten { padding: 56px 0; }
}
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
</style>
"""
)

# --------------------------------------------------------------------------
# Hero (Rot)
# --------------------------------------------------------------------------
jetzt_ = jetzt()
offen = ist_geoeffnet(jetzt_)
status_text = "Jetzt geöffnet bis 18:45 Uhr" if offen else "Gerade geschlossen. Di bis Sa ab 12:00 Uhr"
status_klasse = "" if offen else "zu"
logo = logo_data_uri()
logo_html = f'<img src="{logo}" alt="Logo ARA by NK Korean Street Foods">' if logo else ""

html(
    f"""
<div class="ara">
<section class="hero">
<div class="inner">
<div>
<div class="status {status_klasse}"><i></i>{status_text}</div>
<h1>Korean Street Food mitten in Regensburg</h1>
<p class="lead">Halal Corn Dogs und Fried Chicken, Bibimbap, frische Salate und vegane Optionen. Schnell gemacht, günstig und nach koreanischer Art gewürzt.</p>
<div class="btns">
<a class="btn gelb" href="#speisekarte">Zur Speisekarte</a>
<a class="btn rand" href="#oeffnungszeiten">Öffnungszeiten &amp; Kontakt</a>
</div>
</div>
<div class="logo-wrap">{logo_html}</div>
</div>
</section>

<section class="fakten">
<div class="inner">
<div><h3>Halal seit 2021</h3><p>Die ersten halal Korean Corn Dogs und das erste halal Fried Chicken in Regensburg.</p></div>
<div><h3>Vegane Optionen</h3><p>Vegetarische Corn Dogs mit Gouda, veganer Rettich und Reis als Beilage.</p></div>
<div><h3>Mitnehmen oder liefern lassen</h3><p>Ein kleiner Imbiss für zwischendurch. Meist zwischen 10 und 20 € pro Person.</p></div>
</div>
</section>

<section class="karte" id="speisekarte">
<div class="inner">
<h2>Speisekarte</h2>
<p class="intro">Von knusprigem Chibap über Corn Dogs bis zur Bibimbap-Reisschale.</p>
</div>
</section>
</div>
"""
)

# --------------------------------------------------------------------------
# Speisekarte (Weiß) mit Tabs
# --------------------------------------------------------------------------
tabs = st.tabs(list(SPEISEKARTE.keys()))
for tab, (kategorie, eintraege) in zip(tabs, SPEISEKARTE.items()):
    with tab:
        html(f'<div class="ara">{menue_zeilen(eintraege)}</div>')
        if kategorie == "Hauptspeisen":
            html('<div class="ara"><div class="hinweis">Alle Bibimbap gibt es mit einer Sauce nach Wahl.</div></div>')

# --------------------------------------------------------------------------
# Öffnungszeiten & Kontakt (Rot) und Fußzeile (Gelb)
# --------------------------------------------------------------------------
heute = jetzt_.weekday()
zeilen_zeiten = "".join(
    f'<tr class="{"heute" if i == heute else ""}"><td>{tag}</td><td>{zeit}</td></tr>'
    for i, (tag, zeit) in enumerate(OEFFNUNGSZEITEN)
)

html(
    f"""
<div class="ara">
<section class="zeiten" id="oeffnungszeiten">
<div class="inner">
<div>
<h2>Öffnungszeiten</h2>
<table>{zeilen_zeiten}</table>
</div>
<div class="kontakt">
<h2>So finden Sie uns</h2>
<p>ARA by NK<br>{ADRESSE}</p>
<p>Telefon: <a href="tel:{TELEFON_LINK}">{TELEFON_ANZEIGE}</a><br>Reservierungen derzeit nur telefonisch.</p>
<p>Instagram: <a href="{INSTAGRAM}" target="_blank" rel="noopener">@nk.kaffee</a></p>
<div class="btns">
<a class="btn gelb" href="tel:{TELEFON_LINK}">Jetzt anrufen</a>
<a class="btn rand" href="{INSTAGRAM}" target="_blank" rel="noopener">Auf Instagram folgen</a>
</div>
</div>
</div>
</section>

<footer class="fuss">
<div class="inner">
<span>© 2026 ARA by NK, Regensburg</span>
<span>Impressum &nbsp;|&nbsp; Datenschutz</span>
</div>
</footer>
</div>
"""
)
