"""
ARA by NK – Prototyp der Restaurant-Website (nur Darstellung)
Start: streamlit run app.py
Das Logo (logo.jpg) liegt im selben Ordner wie diese Datei.
Sprache: Deutsch ist Standard, oben rechts kann auf English umgeschaltet werden.
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
# Feste Daten
# --------------------------------------------------------------------------
ADRESSE = "Weiße-Lilien-Straße 6, 93047 Regensburg"
TELEFON_ANZEIGE = "0941 20916513"
TELEFON_LINK = "+4994120916513"
INSTAGRAM = "https://www.instagram.com/nk.kaffee"

# --------------------------------------------------------------------------
# Texte (Deutsch = Standard)
# --------------------------------------------------------------------------
T = {
    "de": {
        "status_offen": "Jetzt geöffnet bis 18:45 Uhr",
        "status_zu": "Gerade geschlossen. Di bis Sa ab 12:00 Uhr",
        "h1": "Korean Street Food mitten in Regensburg",
        "lead": "Halal Corn Dogs und Fried Chicken, Bibimbap, frische Salate und vegane Optionen. Schnell gemacht, günstig und nach koreanischer Art gewürzt.",
        "btn_karte": "Zur Speisekarte",
        "btn_zeiten": "Öffnungszeiten &amp; Kontakt",
        "f1_t": "Halal seit 2021",
        "f1_p": "Die ersten halal Korean Corn Dogs und das erste halal Fried Chicken in Regensburg.",
        "f2_t": "Vegane Optionen",
        "f2_p": "Vegetarische Corn Dogs mit Gouda, veganer Rettich und Reis als Beilage.",
        "f3_t": "Mitnehmen oder liefern lassen",
        "f3_p": "Ein kleiner Imbiss für zwischendurch. Meist zwischen 10 und 20 € pro Person.",
        "karte_h": "Speisekarte",
        "karte_intro": "Von knusprigem Chibap über Corn Dogs bis zur Bibimbap-Reisschale.",
        "hinweis_bibimbap": "Alle Bibimbap gibt es mit einer Sauce nach Wahl.",
        "zeiten_h": "Öffnungszeiten",
        "finden_h": "So finden Sie uns",
        "telefon": "Telefon",
        "reservierung": "Reservierungen derzeit nur telefonisch.",
        "btn_anrufen": "Jetzt anrufen",
        "btn_insta": "Auf Instagram folgen",
        "impressum": "Impressum &nbsp;|&nbsp; Datenschutz",
        "zu": "Geschlossen",
        "tage": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
        "tags": {"veg": "vegetarisch", "vegan": "vegan", "halal": "halal", "scharf": "scharf"},
        "kategorien": {
            "chibap": "Chibap", "corndogs": "Corn Dogs", "haupt": "Hauptspeisen",
            "salate": "Salate", "extras": "Extras", "drinks": "Getränke",
        },
    },
    "en": {
        "status_offen": "Open now until 6:45 pm",
        "status_zu": "Closed right now. Tue to Sat from 12:00 noon",
        "h1": "Korean street food in the heart of Regensburg",
        "lead": "Halal corn dogs and fried chicken, bibimbap, fresh salads and vegan options. Quick, affordable and seasoned the Korean way.",
        "btn_karte": "View the menu",
        "btn_zeiten": "Opening hours &amp; contact",
        "f1_t": "Halal since 2021",
        "f1_p": "The first halal Korean corn dogs and the first halal fried chicken in Regensburg.",
        "f2_t": "Vegan options",
        "f2_p": "Vegetarian corn dogs with Gouda, plus vegan radish and rice as sides.",
        "f3_t": "Take away or delivery",
        "f3_p": "A small snack shop for in between. Usually €10 to €20 per person.",
        "karte_h": "Menu",
        "karte_intro": "From crispy chibap and corn dogs to bibimbap rice bowls.",
        "hinweis_bibimbap": "Every bibimbap comes with the sauce of your choice.",
        "zeiten_h": "Opening hours",
        "finden_h": "Find us",
        "telefon": "Phone",
        "reservierung": "Reservations by phone only for now.",
        "btn_anrufen": "Call now",
        "btn_insta": "Follow on Instagram",
        "impressum": "Legal notice &nbsp;|&nbsp; Privacy policy",
        "zu": "Closed",
        "tage": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "tags": {"veg": "vegetarian", "vegan": "vegan", "halal": "halal", "scharf": "spicy"},
        "kategorien": {
            "chibap": "Chibap", "corndogs": "Corn Dogs", "haupt": "Main dishes",
            "salate": "Salads", "extras": "Sides", "drinks": "Drinks",
        },
    },
}

# Speisekarte: (Name, Beschreibung DE, Beschreibung EN, Preis, Hinweise)
BIBI_DE = "Koreanische Reisschale mit {z}, Karotten, Champignons, Sesam, Sesamöl und Saisongemüse. Lauwarm, mit Sauce nach Wahl."
BIBI_EN = "Korean rice bowl with {z}, carrots, mushrooms, sesame, sesame oil and seasonal vegetables. Served lukewarm, with the sauce of your choice."

SPEISEKARTE = {
    "chibap": [
        ("Sesam Chicken", "", "", 8.50, []),
        ("Yangnyeom Chicken", "", "", 8.50, []),
        ("Soy Garlic Chicken", "", "", 8.50, []),
    ],
    "corndogs": [
        ("Original Hot Corn Dog", "", "", 6.00, []),
        ("Full Cheese Corn Dog", "Mit Gouda", "With Gouda", 6.00, ["veg"]),
        ("Half and Half Corn Dog", "Eine Hälfte Corn Dog, eine Hälfte Gouda", "One half corn dog, one half Gouda", 6.00, ["veg"]),
        ("Potato Hot Corn Dog", "Mit Gouda", "With Gouda", 6.50, []),
        ("Potato Cheese Corn Dog", "Mit Gouda", "With Gouda", 6.50, ["veg"]),
        ("Potato Half and Half Corn Dog", "Eine Hälfte Corn Dog, eine Hälfte Gouda", "One half corn dog, one half Gouda", 6.50, ["veg"]),
    ],
    "haupt": [
        ("Bibimbap Spiegelei", BIBI_DE.format(z="Spiegelei"), BIBI_EN.format(z="fried egg"), 12.50, []),
        ("Bibimbap Hähnchen", BIBI_DE.format(z="Hähnchenfleisch"), BIBI_EN.format(z="chicken"), 13.50, []),
        ("Bibimbap Bulgogi", BIBI_DE.format(z="Rindhackfleisch"), BIBI_EN.format(z="minced beef"), 14.90, []),
    ],
    "salate": [
        (
            "Großer Salat mit Popcorn Chicken",
            "Eisbergsalat, Gurken, Karotten, Kimchi, Rettich und Halal Popcorn Chicken",
            "Iceberg lettuce, cucumber, carrots, kimchi, radish and halal popcorn chicken",
            7.50, ["halal"],
        ),
    ],
    "extras": [
        ("Kimchi", "", "", 4.50, ["scharf"]),
        ("Rettich", "", "", 4.50, ["vegan"]),
        ("Reis", "", "", 2.50, ["vegan"]),
    ],
    "drinks": [
        ("Coca-Cola", "0,33 l, Einweg", "0.33 l, single-use", 3.75, []),
        ("Coca-Cola Zero Sugar", "0,33 l, Einweg", "0.33 l, single-use", 3.75, []),
        ("Fanta Orange", "0,33 l, Einweg", "0.33 l, single-use", 3.75, []),
        ("Sprite", "0,33 l, Einweg", "0.33 l, single-use", 3.75, []),
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


def preis(wert: float, lang: str) -> str:
    text = f"{wert:.2f}"
    return text.replace(".", ",") + " €" if lang == "de" else "€" + text


def menue_zeilen(eintraege, lang: str) -> str:
    tx = T[lang]
    zeilen = []
    for name, desc_de, desc_en, wert, hinweise in eintraege:
        beschreibung = desc_de if lang == "de" else desc_en
        tags = "".join(f'<span class="tag">{tx["tags"][h]}</span>' for h in hinweise)
        zeilen.append(
            f'<div class="item"><div class="item-row">'
            f'<span class="item-name">{name}</span>{tags}'
            f'<span class="item-dots"></span>'
            f'<span class="item-price">{preis(wert, lang)}</span></div>'
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

/* Sprachumschalter (rote Leiste ganz oben) */
.st-key-langbar { background: var(--rot); padding: 16px max(28px, calc((100% - 1064px) / 2)) 0; }
.st-key-langbar [data-testid="stWidgetLabel"] { display: none; }
.st-key-langbar [role="radiogroup"] { justify-content: flex-end; gap: 8px; }
.st-key-langbar label[data-baseweb="radio"] { border: 2px solid #fff; border-radius: 999px; padding: 2px 16px; margin: 0; cursor: pointer; }
.st-key-langbar label[data-baseweb="radio"] > div:first-child { display: none; }
.st-key-langbar label[data-baseweb="radio"] p { color: #fff; font-weight: 600; font-family: 'Barlow', sans-serif; }
.st-key-langbar label[data-baseweb="radio"]:has(input:checked) { background: var(--gelb); border-color: var(--gelb); }
.st-key-langbar label[data-baseweb="radio"]:has(input:checked) p { color: var(--tinte); }

.ara, .ara * { box-sizing: border-box; font-family: 'Barlow', sans-serif; }
.ara h1, .ara h2, .ara h3 { font-family: 'Barlow Condensed', sans-serif; margin: 0; letter-spacing: .01em; }
.inner { max-width: 1120px; margin: 0 auto; padding: 0 28px; }

/* 1 · Rot: Hero */
.hero { background: var(--rot); color: var(--weiss); padding: 40px 0 80px; }
.hero .inner { display: grid; grid-template-columns: 1.25fr 1fr; gap: 56px; align-items: center; }
.hero h1 { font-weight: 800; font-style: italic; text-transform: uppercase; font-size: clamp(2.4rem, 5.6vw, 4.6rem); line-height: .98; text-wrap: balance; }
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
.kontakt a.btn { text-decoration: none; }
.kontakt a.btn.gelb { color: var(--tinte); }
.kontakt .btns { margin-top: 28px; }

/* Gelb: Fußzeile */
.fuss { background: var(--gelb); color: var(--tinte); padding: 28px 0; font-size: .95rem; }
.fuss .inner { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; }

@media (max-width: 860px) {
  .hero .inner, .fakten .inner, .zeiten .inner { grid-template-columns: 1fr; gap: 36px; }
  .hero { padding: 32px 0 56px; }
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
# Sprachumschalter: Deutsch ist der Standard
# --------------------------------------------------------------------------
with st.container(key="langbar"):
    auswahl = st.radio(
        "Sprache / Language",
        ["Deutsch", "English"],
        index=0,
        horizontal=True,
        key="sprache",
    )
lang = "de" if auswahl == "Deutsch" else "en"
tx = T[lang]

# --------------------------------------------------------------------------
# Hero (Rot), Eckdaten (Gelb), Kopf der Speisekarte (Weiß)
# --------------------------------------------------------------------------
jetzt_ = jetzt()
offen = ist_geoeffnet(jetzt_)
status_text = tx["status_offen"] if offen else tx["status_zu"]
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
<h1>{tx["h1"]}</h1>
<p class="lead">{tx["lead"]}</p>
<div class="btns">
<a class="btn gelb" href="#speisekarte">{tx["btn_karte"]}</a>
<a class="btn rand" href="#oeffnungszeiten">{tx["btn_zeiten"]}</a>
</div>
</div>
<div class="logo-wrap">{logo_html}</div>
</div>
</section>

<section class="fakten">
<div class="inner">
<div><h3>{tx["f1_t"]}</h3><p>{tx["f1_p"]}</p></div>
<div><h3>{tx["f2_t"]}</h3><p>{tx["f2_p"]}</p></div>
<div><h3>{tx["f3_t"]}</h3><p>{tx["f3_p"]}</p></div>
</div>
</section>

<section class="karte" id="speisekarte">
<div class="inner">
<h2>{tx["karte_h"]}</h2>
<p class="intro">{tx["karte_intro"]}</p>
</div>
</section>
</div>
"""
)

# --------------------------------------------------------------------------
# Speisekarte (Weiß) mit Tabs
# --------------------------------------------------------------------------
tabs = st.tabs([tx["kategorien"][k] for k in SPEISEKARTE])
for tab, (kategorie, eintraege) in zip(tabs, SPEISEKARTE.items()):
    with tab:
        html(f'<div class="ara">{menue_zeilen(eintraege, lang)}</div>')
        if kategorie == "haupt":
            html(f'<div class="ara"><div class="hinweis">{tx["hinweis_bibimbap"]}</div></div>')

# --------------------------------------------------------------------------
# Öffnungszeiten & Kontakt (Rot) und Fußzeile (Gelb)
# --------------------------------------------------------------------------
heute = jetzt_.weekday()
zeiten = [tx["zu"], "12:00 – 18:45", "12:00 – 18:45", "12:00 – 18:45", "12:00 – 18:45", "12:00 – 18:45", tx["zu"]]
zeilen_zeiten = "".join(
    f'<tr class="{"heute" if i == heute else ""}"><td>{tag}</td><td>{zeit}</td></tr>'
    for i, (tag, zeit) in enumerate(zip(tx["tage"], zeiten))
)

html(
    f"""
<div class="ara">
<section class="zeiten" id="oeffnungszeiten">
<div class="inner">
<div>
<h2>{tx["zeiten_h"]}</h2>
<table>{zeilen_zeiten}</table>
</div>
<div class="kontakt">
<h2>{tx["finden_h"]}</h2>
<p>ARA by NK<br>{ADRESSE}</p>
<p>{tx["telefon"]}: <a href="tel:{TELEFON_LINK}">{TELEFON_ANZEIGE}</a><br>{tx["reservierung"]}</p>
<p>Instagram: <a href="{INSTAGRAM}" target="_blank" rel="noopener">@nk.kaffee</a></p>
<div class="btns">
<a class="btn gelb" href="tel:{TELEFON_LINK}">{tx["btn_anrufen"]}</a>
<a class="btn rand" href="{INSTAGRAM}" target="_blank" rel="noopener">{tx["btn_insta"]}</a>
</div>
</div>
</div>
</section>

<footer class="fuss">
<div class="inner">
<span>© 2026 ARA by NK, Regensburg</span>
<span>{tx["impressum"]}</span>
</div>
</footer>
</div>
"""
)
