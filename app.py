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

# --- SIDEBAR (NY/GJENINNSATT!) ---
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

# --- FANE 1: BUTIKK-SØK (Den gamle koden) ---
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
                # ... (Her henter vi ut data som før)
                navn = produkt['name']
                beskrivelse = produkt.get('description', '')
                ean_id = produkt.get('ean', 'ukjent')
                nutr = produkt.get('nutrition', [])
                karbo_api = 0
                for n in nutr:
                    if n.get('code', '').lower() in ['carbohydrates', 'carbohydrate', 'karbohydrater', 'karbohydrat']:
                        karbo_api = n.get('amount', 0); break
                vekt_api = produkt.get('weight', 0)
                antall_funnet = finn_antall_i_tekst(beskrivelse)
                if not antall_funnet: antall_funnet = finn_antall_i_tekst(navn)

                c_img, c_info = st.columns([1, 3])
                with c_img:
                    if produkt.get('image'): st.image(produkt['image'], width=100)
                with c_info:
                    st.subheader(navn)
                    st.write(f"📊 **Karbo:** {karbo_api}g per 100g")
                
                c_kalk1, c_kalk2 = st.columns(2)
                mengde_nett = 0
                beskrivelse_nett = ""
                with c_kalk1:
                    valg_type = st.radio("Regnemåte:", ["Gram", "Hele pakken/Stk"], horizontal=True, key=f"radio_{ean_id}")
                    if valg_type == "Gram":
                        mengde_nett = st.number_input("Antall gram:", min_value=0, value=100, step=10, key=f"gram_{ean_id}")
                        beskrivelse_nett = f"{mengde_nett} g"
                    else:
                        start_vekt = float(vekt_api) if vekt_api else 0.0
                        start_antall = int(antall_funnet) if antall_funnet else 1
                        with st.expander("📝 Endre vekt/antall?", expanded=(start_vekt==0)):
                            pk_vekt = st.number_input("Totalvekt (g):", value=start_vekt, step=1.0, key=f"vekt_{ean_id}")
                            pk_ant = st.number_input("Antall i pakke:", min_value=1, value=start_antall, key=f"ant_{ean_id}")
                        if pk_vekt and pk_ant:
                            enhet_vekt = pk_vekt / pk_ant
                            st.info(f"👉 1 stk = ca **{enhet_vekt:.0f} g**")
                            ant_spist = st.number_input("Antall du spiser:", 1.0, step=0.5, key=f"spist_{ean_id}")
                            mengde_nett = ant_spist * enhet_vekt
                            beskrivelse_nett = f"{ant_spist} stk ({navn})"
                
                with c_kalk2:
                    tillegg_nett = 0
                    if st.checkbox("Saus/Glaze?", key=f"bbq_{ean_id}"):
                        g_saus = st.slider("Saus (g):", 0, 150, 20, key=f"slider_{ean_id}")
                        tillegg_nett = (g_saus/100)*35
                        beskrivelse_nett += " + saus"

                tot_nett = (mengde_nett/100)*karbo_api + tillegg_nett
                st.write(f"### = {tot_nett:.1f} g karbo")
                if st.button("➕ Legg til i måltid", key=f"btn_{ean_id}"):
                    st.session_state['kurv'].append({"navn": navn, "beskrivelse": beskrivelse_nett, "karbo": tot_nett})
                    st.success("Lagt til!")

# --- FANE 2: TOMMELFINGER-REGLER (Ny!) ---
with tab2:
    st.header("📏 Hva inneholder 1 stk?")
    st.caption("Gjennomsnittsverdier for vanlige matvarer. Kjekt når du ikke orker å veie!")
    
    standardvarer = hent_standardvarer()
    
    # Vi lager et rutenett (grid) med 2 kolonner
    cols = st.columns(2)
    
    for i, vare in enumerate(standardvarer):
        # Annenhver vare i venstre/høyre kolonne
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"## {vare['icon']}")
                st.subheader(vare['navn'])
                st.caption(f"Vekt ca: {vare['vekt']}")
                st.markdown(f"**= {vare['karbo']} g karbo**")
                
                # Legg til-knapp for disse også
                if st.button(f"➕ Legg til", key=f"std_{i}"):
                     st.session_state['kurv'].append({
                         "navn": vare['navn'], 
                         "beskrivelse": f"1 stk/porsjon ({vare['vekt']})", 
                         "karbo": vare['karbo']
                     })
                     st.rerun() # Oppdater siden så kurven viser med en gang

# --- KURV (FELLES FOR BEGGE FANER) ---
st.markdown("---")
st.header("🍽️ Dagens Måltid")

if st.session_state['kurv']:
    # Sjekk brødmat
    har_brødmat = any(x in str(st.session_state['kurv']).lower() for x in ['brød', 'rundstykke', 'knekke'])
    if har_brødmat:
        st.info("🍞 Tips: Ost, skinke og egg er karbofritt. Brunost og syltetøy må telles!")

    for i, item in enumerate(st.session_state['kurv']):
        c1, c2, c3, c4 = st.columns([3, 4, 2, 1])
        with c1: st.write(item['navn'])
        with c2: st.write(item['beskrivelse'])
        with c3: st.write(f"{item['karbo']:.1f}")
        with c4:
            if st.button("❌", key=f"slett_{i}"):
                st.session_state['kurv'].pop(i)
                st.rerun()

    total_sum = sum(item['karbo'] for item in st.session_state['kurv'])
    st.markdown("---")
    c_res1, c_res2 = st.columns([2, 1])
    with c_res1: st.subheader("Totalt til Pumpa:")
    with c_res2: st.title(f"{total_sum:.1f} g")
    
    if st.button("🗑️ Tøm hele kurven", key="tom_bunn"):
        st.session_state['kurv'] = []
        st.rerun()
else:
    st.caption("Kurven er tom.")
