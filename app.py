import streamlit as st
import pandas as pd
import requests
import re

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="Hz")

# --- DIN API NØKKEL ---
API_KEY = "9b0hY5ygaH5nvjPVmiFV50YiQAR76xb5jbirGmyK"

# --- INITIALISER HUKOMMELSE ---
if 'kurv' not in st.session_state:
    st.session_state['kurv'] = []

# --- HJELPEFUNKSJONER ---
def finn_antall_i_tekst(beskrivelse):
    if not beskrivelse: return None
    tekst = beskrivelse.lower()
    treff_tall = re.search(r'(\d+)\s*(stk|stykk|pølser|pk)', tekst)
    if treff_tall: return int(treff_tall.group(1))
    tall_ord = {"en": 1, "et": 1, "to": 2, "tre": 3, "fire": 4, "fem": 5, "seks": 6, "sju": 7, "syv": 7, "åtte": 8, "ni": 9, "ti": 10}
    for ord, tall in tall_ord.items():
        if f"{ord} stk" in tekst or f"{ord} pølser" in tekst or f"{ord} i pakken" in tekst:
            return tall
    return None

@st.cache_data(show_spinner=False) 
def sok_kassalapp(sokeord):
    url = "https://kassal.app/api/v1/products"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"search": sokeord, "size": 50}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except: return []

# --- STANDARDVARER (MANUELL LISTE) ---
def hent_standardvarer():
    # Dette er tommelfingerregler. Juster gjerne verdiene!
    return [
        {"navn": "Brødskive (Grov)", "vekt": "40g", "karbo": 16, "icon": "🍞", "info": "En vanlig butikk-skive"},
        {"navn": "Knekkebrød (Wasa)", "vekt": "13g", "karbo": 8, "icon": "🍘", "info": "Husman / Havre"},
        {"navn": "Potet (Medium)", "vekt": "85g", "karbo": 14, "icon": "🥔", "info": "Kokt potet"},
        {"navn": "Eple (Medium)", "vekt": "150g", "karbo": 15, "icon": "🍎", "info": "Granny Smith / Pink Lady"},
        {"navn": "Banan (Medium)", "vekt": "120g", "karbo": 22, "icon": "🍌", "info": "Uten skall"},
        {"navn": "Appelsin", "vekt": "200g", "karbo": 18, "icon": "🍊", "info": "En middels stor"},
        {"navn": "Melk (1 glass)", "vekt": "2 dl", "karbo": 9, "icon": "🥛", "info": "Lettmelk/Helmelk"},
        {"navn": "Yoghurt (Beger)", "vekt": "150g", "karbo": 9, "icon": "🥣", "info": "Naturell/Gresk (uten tilsatt sukker)"},
        {"navn": "Pizza (Grandiosa bit)", "vekt": "1/8 stk", "karbo": 28, "icon": "🍕", "info": "Ett pizzastykke (vanlig størrelse)"},
        {"navn": "Ris (Kokt porsjon)", "vekt": "150g", "karbo": 40, "icon": "🍚", "info": "En middels middagsporsjon"},
        {"navn": "Pasta (Kokt porsjon)", "vekt": "150g", "karbo": 45, "icon": "🍝", "info": "En middels middagsporsjon"},
    ]

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Innstillinger")
    if st.button("🗑️ Tøm kurv"):
        st.session_state['kurv'] = []
        st.rerun()
    
    st.markdown("---")
    st.header("💬 Kontakt")
    st.write("Fant du en feil eller har et ønske?")
    st.link_button("✍️ Send tilbakemelding", "https://forms.gle/xn1RnNAgcr1frzhr8")
    
    st.markdown("---")
    with st.expander("ℹ️ Om dataene"):
        st.markdown("""
        **Kilder:**
        * 🌐 Kassalapp.no (Produktsøk)
        * 🔥 Egne BBQ-beregninger
        
        *Laget for insulinpumper.*
        """)
        
    st.info("Tips: Bruk 'Scan'-knappen på mobiltastaturet ditt i søkefeltet for å scanne strekkoder!")

# --- UI START ---
st.title("🤖 Karbo-Robot")

# --- FANE-SYSTEM ---
tab1, tab2 = st.tabs(["🔍 Søk i butikk", "📏 Tommelfinger-regler"])

# --- FANE 1: BUTIKK-SØK ---
with tab1:
    st.caption("Søk i tusenvis av varer via Kassalapp.no")
    
    col_sok, col_x = st.columns([6, 1])
    with col_sok:
        nett_sok = st.text_input("Søk (navn eller scan strekkode):", key="input_nett_sok", label_visibility="collapsed", placeholder="Søk eller scan EAN...")
    with col_x:
        def slett_sok(): st.session_state.input_nett_sok = ""
        st.button("❌", on_click=slett_sok, help="Tøm søkefeltet")

    if nett_sok:
        resultater = sok_kassalapp(nett_sok)
        
        if not resultater:
            st.warning("Fant ingen varer.")
        else:
            valg_liste = {}
            unike_produkter = set()
            teller = 1
            for p in resultater:
                navn = p['name']
                vendor = p.get('vendor', 'Ukjent')
                signatur = f"{navn}_{vendor}".lower()
                if signatur not in unike_produkter:
                    unike_produkter.add(signatur)
                    visningsnavn = f"{teller}. {navn} ({vendor})"
                    valg_liste[visningsnavn] = p
                    teller += 1

            st.success(f"Fant {len(valg_liste)} unike produkter!")
            valgt_nettvare_navn = st.selectbox("Velg produkt:", list(valg_liste.keys()), index=None)
            
            if valgt_nettvare_navn:
                produkt = valg_liste[valgt_nettvare_navn]
                navn = produkt['name']
                besk
