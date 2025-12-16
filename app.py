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

# --- INITIALISER STANDARDVARER (FRA DIN FIL) ---
if 'standardvarer' not in st.session_state:
    st.session_state['standardvarer'] = [
        # --- BRØD & KNEKKEBRØD 🍞 ---
        {"navn": "Grovbrød", "vekt": "1 skive (35g)", "karbo": 15, "icon": "🍞"},
        {"navn": "Loff", "vekt": "1 skive (30g)", "karbo": 15, "icon": "🍞"},
        {"navn": "Pumpernikkel", "vekt": "1 skive (65g)", "karbo": 25, "icon": "🍞"},
        {"navn": "Lavkarbo-brød", "vekt": "1 skive (40g)", "karbo": 5, "icon": "🍞"},
        {"navn": "Knekkebrød", "vekt": "1 stk (15g)", "karbo": 10, "icon": "🍘"},
        {"navn": "FiberPlus / Ryvita", "vekt": "1 stk (9g)", "karbo": 5, "icon": "🍘"},
        {"navn": "Rundstykke", "vekt": "1 stk (60g)", "karbo": 30, "icon": "🥯"},
        {"navn": "Polarbrød", "vekt": "1 stk (40g)", "karbo": 15, "icon": "🫓"},
        {"navn": "Pitabrød", "vekt": "1 stk (80g)", "karbo": 35, "icon": "🫓"},
        {"navn": "Hamburgerbrød", "vekt": "1 stk (60g)", "karbo": 30, "icon": "🍔"},
        {"navn": "Pølsebrød (lite)", "vekt": "1 stk (30g)", "karbo": 15, "icon": "🌭"},
        {"navn": "Pølsebrød (stort)", "vekt": "1 stk (50g)", "karbo": 25, "icon": "🌭"},
        {"navn": "Lompe / Lefse", "vekt": "1 stk (30g)", "karbo": 10, "icon": "🌮"},
        {"navn": "Tortilla (liten)", "vekt": "1 stk (40g)", "karbo": 20, "icon": "🌯"},
        {"navn": "Tortilla (stor)", "vekt": "1 stk (60g)", "karbo": 30, "icon": "🌯"},
        {"navn": "Tacoskjell", "vekt": "1 stk (10g)", "karbo": 5, "icon": "🌮"},
        {"navn": "Foccacia", "vekt": "1 stk (130g)", "karbo": 58, "icon": "🍞"},
        {"navn": "Croissant", "vekt": "1 stk (90g)", "karbo": 34, "icon": "🥐"},
        {"navn": "Naan / Chapati", "vekt": "1 stk (40g)", "karbo": 20, "icon": "🫓"},

        # --- FROKOST & GRØT 🥣 ---
        {"navn": "Havregryn", "vekt": "1 dl (40g)", "karbo": 25, "icon": "🌾"},
        {"navn": "Havregrøt (ferdig)", "vekt": "1 porsjon (350g)", "karbo": 25, "icon": "🥣"},
        {"navn": "Cornflakes", "vekt": "1 dl (15g)", "karbo": 10, "icon": "🥣"},
        {"navn": "Cheerios", "vekt": "1 porsjon (30g)", "karbo": 20, "icon": "🥣"},
        {"navn": "Granola / Müsli", "vekt": "1 dl (50g)", "karbo": 30, "icon": "🥣"},
        {"navn": "Weetabix", "vekt": "1 stk (20g)", "karbo": 10, "icon": "🌾"},

        # --- PÅLEGG & TILBEHØR 🍯 ---
        {"navn": "Syltetøy", "vekt": "1 ts (10g)", "karbo": 5, "icon": "🍓"},
        {"navn": "Brunost", "vekt": "1 skive (15g)", "karbo": 5, "icon": "🧀"},
        {"navn": "Sjokoladepålegg", "vekt": "1 ts (10g)", "karbo": 5, "icon": "🍫"},
        {"navn": "Honning", "vekt": "1 ts (10g)", "karbo": 5, "icon": "🍯"},
        {"navn": "Prim", "vekt": "1 ts (10g)", "karbo": 5, "icon": "🧀"},

        # --- YOGHURT & MEIERI 🥛 ---
        {"navn": "Melk", "vekt": "1 glass (2dl)", "karbo": 10, "icon": "🥛"},
        {"navn": "Skolemelk / Kakao", "vekt": "1 kartong", "karbo": 15, "icon": "🧃"},
        {"navn": "Biola", "vekt": "1 glass (2dl)", "karbo": 20, "icon": "🥛"},
        {"navn": "Yoghurt (Naturell)", "vekt": "1 dl", "karbo": 5, "icon": "🥣"},
        {"navn": "Yoghurt (Frukt)", "vekt": "1 beger", "karbo": 20, "icon": "🍓"},
        {"navn": "Go'morgen", "vekt": "1 beger", "karbo": 30, "icon": "🥣"},
        {"navn": "Skyr / Kesam", "vekt": "1 beger", "karbo": 10, "icon": "🥣"},

        # --- MIDDAG & FASTFOOD 🍕 ---
        {"navn": "Grandiosa Pizza", "vekt": "1 porsjon", "karbo": 30, "icon": "🍕"},
        {"navn": "Pasta (kokt)", "vekt": "1 porsjon (ca 150g)", "karbo": 45, "icon": "🍝"},
        {"navn": "Ris (kokt)", "vekt": "1 porsjon (ca 150g)", "karbo": 40, "icon": "🍚"},
        {"navn": "Potet (kokt)", "vekt": "1 stk (70g)", "karbo": 10, "icon": "🥔"},
        {"navn": "Potetmos (pose)", "vekt": "1 pose", "karbo": 70, "icon": "🥔"},
        {"navn": "Pølse (Wiener/Grill)", "vekt": "1 stk", "karbo": 4, "icon": "🌭"},
        {"navn": "Hamburger", "vekt": "1 stk", "karbo": 35, "icon": "🍔"},
        {"navn": "Pommes Frites", "vekt": "1 porsjon", "karbo": 40, "icon": "🍟"},
        {"navn": "Kebab", "vekt": "1 stk", "karbo": 60, "icon": "🥙"},
        {"navn": "Sushi", "vekt": "1 bit", "karbo": 6, "icon": "🍣"},
        {"navn": "Suppe (Rett i koppen)", "vekt": "1 pose", "karbo": 12, "icon": "🍜"},
        {"navn": "Saus (Brun/Hvit)", "vekt": "1 dl", "karbo": 5, "icon": "🥣"},

        # --- FRUKT & GRØNT 🍎 ---
        {"navn": "Eple / Pære", "vekt": "1 stk", "karbo": 15, "icon": "🍎"},
        {"navn": "Banan", "vekt": "1 stk", "karbo": 22, "icon": "🍌"},
        {"navn": "Appelsin", "vekt": "1 stk", "karbo": 18, "icon": "🍊"},
        {"navn": "Druer (neve)", "vekt": "1 neve", "karbo": 15, "icon": "🍇"},
        {"navn": "Mais (boks)", "vekt": "1 liten boks", "karbo": 25, "icon": "🌽"},

        # --- KAKER & SNACKS 🍪 ---
        {"navn": "Muffins", "vekt": "1 stk", "karbo": 35, "icon": "🧁"},
        {"navn": "Bolle", "vekt": "1 stk", "karbo": 30, "icon": "🥯"},
        {"navn": "Wienerbrød", "vekt": "1 stk", "karbo": 25, "icon": "🥨"},
        {"navn": "Vaffel", "vekt": "1 plate", "karbo": 25, "icon": "🧇"},
        {"navn": "Pannekake", "vekt": "1 stk", "karbo": 18, "icon": "🥞"},
        {"navn": "Sjokoladekake", "vekt": "1 stykke", "karbo": 25, "icon": "🍰"},
        {"navn": "Is (Pinup/Krone)", "vekt": "1 stk", "karbo": 25, "icon": "🍦"},
        {"navn": "Potetgull", "vekt": "1 porsjon (50g)", "karbo": 25, "icon": "🍿"},
        {"navn": "Sjokolade", "vekt": "1 stripe/bar", "karbo": 20, "icon": "🍫"},
        
        # --- DRIKKE 🥤 ---
        {"navn": "Brus / Juice", "vekt": "1 glass (2dl)", "karbo": 20, "icon": "🥤"},
        {"navn": "Energidrikk", "vekt": "1 boks (5dl)", "karbo": 55, "icon": "⚡"},
        {"navn": "Iskaffe", "vekt": "1 kartong", "karbo": 25, "icon": "☕"},
    ]

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

# --- CALLBACK FOR Å LAGRE REGLER ---
def lagre_ny_regel():
    navn = st.session_state.input_navn
    vekt = st.session_state.input_vekt
    karbo = st.session_state.input_karbo
    icon = st.session_state.input_icon

    if navn:
        ny_regel = {"navn": navn, "vekt": vekt, "karbo": karbo, "icon": icon}
        st.session_state['standardvarer'].append(ny_regel)
        
        st.session_state.input_navn = ""
        st.session_state.input_vekt = ""
        st.session_state.input_karbo = 0.0
        st.session_state.input_icon = "🍽️"

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
    if st.button("🔄 Nullstill regler"):
        # Denne nullstiller til den hardkodede listen ved omstart
        if 'standardvarer' in st.session_state:
            del st.session_state['standardvarer']
        st.rerun()
        
    st.markdown("---")
    st.header("💬 Kontakt")
    st.write("Fant du en feil eller har et ønske?")
    st.link_button("✍️ Send tilbakemelding", "https://forms.gle/xn1RnNAgcr1frzhr8")
    
    with st.expander("ℹ️ Om dataene"):
        st.markdown("""
        **Kilder:**
        * 🌐 Kassalapp.no (Produktsøk)
        * 🔥 Egne BBQ-beregninger
        """)
        
    st.info("Tips: Bruk 'Scan'-knappen på mobiltastaturet ditt i søkefeltet for å scanne strekkoder!")

# --- UI START ---
st.title("🤖 Karbo-Robot")

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
                ean_id = produkt.get('ean', 'ukjent')
                beskrivelse = produkt.get('description', '')
                
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

# --- FANE 2: TOMMELFINGER-REGLER ---
with tab2:
    st.header("📏 Hva inneholder 1 stk?", anchor=False)
    
    with st.expander("➕ Legg til ny tommelfinger-regel"):
        c1, c2 = st.columns(2)
        c1.text_input("Navn (f.eks. Bolle)", placeholder="Navn på matvare", key="input_navn")
        c2.text_input("Emoji (f.eks. 🥐)", value="🍽️", key="input_icon")
        
        c3, c4 = st.columns(2)
        c3.text_input("Vekt-tekst (f.eks. 60g)", placeholder="Ca. vekt", key="input_vekt")
        c4.number_input("Karbo per stk (gram)", min_value=0.0, step=1.0, key="input_karbo")
        st.button("Lagre ny regel", on_click=lagre_ny_regel)

    st.markdown("---")

    # --- VISNING AV REGLER (GRID) ---
    cols = st.columns(2)
    
    for i, vare in enumerate(st.session_state['standardvarer']):
        with cols[i % 2]:
            with st.container(border=True):
                st.header(vare['icon'], anchor=False)
                st.subheader(vare['navn'], anchor=False)
                
                std_vekt = vare['vekt']
                std_karbo = vare['karbo']
                
                st.caption(f"Standard: {std_vekt}")
                st.markdown(f"**= {std_karbo} g karbo**")
                
                # --- MINIKALKULATOR ---
                with st.expander("🧮 Endre mengde?"):
                    faktor = st.number_input("Antall / Porsjoner:", min_value=0.1, value=1.0, step=0.5, key=f"calc_{i}")
                    ny_karbo = std_karbo * faktor
                    
                    st.write(f"{faktor} x {std_karbo}g = **{ny_karbo:.1f} g**")
                    
                    if st.button("Legg til dette", key=f"add_calc_{i}"):
                         st.session_state['kurv'].append({
                             "navn": vare['navn'], 
                             "beskrivelse": f"{faktor} stk/porsj ({std_vekt})", 
                             "karbo": ny_karbo
                         })
                         st.rerun()

                # --- HURTIGKNAPPER ---
                c_add, c_del = st.columns([4, 1])
                with c_add:
                    if st.button("1 stk", key=f"add_{i}", use_container_width=True):
                         st.session_state['kurv'].append({
                             "navn": vare['navn'], 
                             "beskrivelse": f"1 stk/porsj ({std_vekt})", 
                             "karbo": std_karbo
                         })
                         st.rerun()
                with c_del:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state['standardvarer'].pop(i)
                        st.rerun()

# --- KURV (FELLES) ---
st.markdown("---")
st.header("🍽️ Dagens Måltid", anchor=False)

if st.session_state['kurv']:
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
    with c_res1: st.subheader("Totalt til Pumpa:", anchor=False)
    with c_res2: st.title(f"{total_sum:.1f} g", anchor=False)
    
    if st.button("🗑️ Tøm hele kurven", key="tom_bunn"):
        st.session_state['kurv'] = []
        st.rerun()
else:
    st.caption("Kurven er tom.")
