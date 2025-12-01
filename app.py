import streamlit as st
import pandas as pd
import requests
import re

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

# --- DIN API NØKKEL ---
# HUSK: Bytt ut teksten under med din nye nøkkel fra Kassalapp.no!
API_KEY = "LIM_INN_DEN_NYE_NØKKELEN_DIN_HER"

# --- INITIALISER HUKOMMELSE ---
if 'kurv' not in st.session_state:
    st.session_state['kurv'] = []

# --- DETEKTIV ---
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

# --- API SØK ---
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
st.caption("Søk i tusenvis av norske dagligvarer via Kassalapp.no")

if st.session_state['kurv']:
    tot_karbo = sum(i['karbo'] for i in st.session_state['kurv'])
    st.info(f"🛒 I kurven: **{len(st.session_state['kurv'])}** varer. Totalt: **{tot_karbo:.1f} g**")

# --- SØKEFELT ---
col_sok, col_x = st.columns([6, 1])
with col_sok:
    nett_sok = st.text_input("Søk (navn eller scan strekkode):", key="input_nett_sok", label_visibility="collapsed", placeholder="Søk eller scan EAN...")
with col_x:
    def slett_sok(): st.session_state.input_nett_sok = ""
    st.button("❌", on_click=slett_sok, help="Tøm søkefeltet")

st.caption("💡 Tips: Får du få treff? Prøv entall (f.eks 'pølse') og færre ord.")

if nett_sok:
    resultater = sok_kassalapp(nett_sok)
    
    # --- NYTT: SORTERING PÅ DATO ---
    # Vi sorterer slik at de nyligst oppdaterte varene kommer først
    resultater.sort(key=lambda x: x.get('updated_at', ''), reverse=True)

    if not resultater:
        st.warning("Fant ingen varer. Prøv et annet ord eller sjekk strekkoden.")
    else:
        st.success(f"Fant {len(resultater)} produkter!")
        
        valg_liste = {}
        for i, p in enumerate(resultater):
            navn = p['name']
            
            # Hent butikknavn
            butikk_obj = p.get('store')
            if butikk_obj:
                butikk = butikk_obj.get('name', 'Ukjent')
            else:
                butikk = "Ukjent butikk"
            
            # Hent pris
            pris = p.get('current_price')
            pris_tekst = f"{pris} kr" if pris else "Ingen pris"
            
            visningsnavn = f"{i+1}. {navn} ({butikk}) - {pris_tekst}"
            valg_liste[visningsnavn] = p

        valgt_
