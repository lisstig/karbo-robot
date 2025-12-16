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

# --- INITIALISER STANDARDVARER (MED KATEGORIER) ---
if 'standardvarer' not in st.session_state:
    st.session_state['standardvarer'] = [
        # --- BRØD & KNEKKEBRØD ---
        {"kategori": "Brød & Bakst", "navn": "Grovbrød", "vekt": "1 skive (35g)", "karbo": 15, "icon": "🍞"},
        {"kategori": "Brød & Bakst", "navn": "Loff", "vekt": "1 skive (30g)", "karbo": 15, "icon": "🍞"},
        {"kategori": "Brød & Bakst", "navn": "Knekkebrød", "vekt": "1 stk (15g)", "karbo": 10, "icon": "🍘"},
        {"kategori": "Brød & Bakst", "navn": "Rundstykke", "vekt": "1 stk (60g)", "karbo": 30, "icon": "🥯"},
        {"kategori": "Brød & Bakst", "navn": "Polarbrød", "vekt": "1 stk (40g)", "karbo": 15, "icon": "🫓"},
        {"kategori": "Brød & Bakst", "navn": "Pølsebrød", "vekt": "1 stk (30g)", "karbo": 15, "icon": "🌭"},
        {"kategori": "Brød & Bakst", "navn": "Hamburgerbrød", "vekt": "1 stk (60g)", "karbo": 30, "icon": "🍔"},
        {"kategori": "Brød & Bakst", "navn": "Lompe", "vekt": "1 stk (30g)", "karbo": 10, "icon": "🌮"},
        {"kategori": "Brød & Bakst", "navn": "Tortilla (stor)", "vekt": "1 stk (60g)", "karbo": 30, "icon": "🌯"},

        # --- FROKOST & GRØT ---
        {"kategori": "Frokost & Grøt", "navn": "Havregryn", "vekt": "1 dl (40g)", "karbo": 25, "icon": "🌾"},
        {"kategori": "Frokost & Grøt", "navn": "Havregrøt (ferdig)", "vekt": "1 porsjon", "karbo": 25, "icon": "🥣"},
        {"kategori": "Frokost & Grøt", "navn": "Cornflakes", "vekt": "1 dl (15g)", "karbo": 10, "icon": "🥣"},
        {"kategori": "Frokost & Grøt", "navn": "Müsli / Granola", "vekt": "1 dl (50g)", "karbo": 30, "icon": "🥣"},

        # --- PÅLEGG ---
        {"kategori": "Pålegg", "navn": "Syltetøy", "vekt": "1 ts", "karbo": 5, "icon": "🍓"},
        {"kategori": "Pålegg", "navn": "Brunost", "vekt": "1 skive", "karbo": 5, "icon": "🧀"},
        {"kategori": "Pålegg", "navn": "Sjokopålegg", "vekt": "1 ts", "karbo": 5, "icon": "🍫"},
        {"kategori": "Pålegg", "navn": "Honning", "vekt": "1 ts", "karbo": 5, "icon": "🍯"},

        # --- MEIERI & YOGHURT ---
        {"kategori": "Meieri & Yoghurt", "navn": "Melk", "vekt": "1 glass (2dl)", "karbo": 10, "icon": "🥛"},
        {"kategori": "Meieri & Yoghurt", "navn": "Sjokomelk", "vekt": "1 kartong", "karbo": 15, "icon": "🧃"},
        {"kategori": "Meieri & Yoghurt", "navn": "Yoghurt (Naturell)", "vekt": "1 dl", "karbo": 5, "icon": "🥣"},
        {"kategori": "Meieri & Yoghurt", "navn": "Yoghurt (Frukt)", "vekt": "1 beger", "karbo": 20, "icon": "🍓"},
        {"kategori": "Meieri & Yoghurt", "navn": "Go'morgen", "vekt": "1 beger", "karbo": 30, "icon": "🥣"},

        # --- MIDDAG ---
        {"kategori": "Middag", "navn": "Grandiosa", "vekt": "1 porsjon", "karbo": 30, "icon": "🍕"},
        {"kategori": "Middag", "navn": "Pasta (kokt)", "vekt": "1 porsjon", "karbo": 45, "icon": "🍝"},
        {"kategori": "Middag", "navn": "Ris (kokt)", "vekt": "1 porsjon", "karbo": 40, "icon": "🍚"},
        {"kategori": "Middag", "navn": "Potet (kokt)", "vekt": "1 stk (70g)", "karbo": 10, "icon": "🥔"},
        {"kategori": "Middag", "navn": "Pølse i brød", "vekt": "1 stk", "karbo": 20, "icon": "🌭"},
        {"kategori": "Middag", "navn": "Hamburger", "vekt": "1 stk", "karbo": 35, "icon": "🍔"},
        {"kategori": "Middag", "navn": "Pommes Frites", "vekt": "1 porsjon", "karbo": 40, "icon": "🍟"},
        {"kategori": "Middag", "navn": "Kebab", "vekt": "1 stk", "karbo": 60, "icon": "🥙"},
        {"kategori": "Middag", "navn": "Sushi", "vekt": "1 bit", "karbo": 6, "icon": "🍣"},
        {"kategori": "Middag", "navn": "Suppe (Pose)", "vekt": "1 porsjon", "karbo": 15, "icon": "🍜"},

        # --- FRUKT & GRØNT ---
        {"kategori": "Frukt & Grønt", "navn": "Eple / Pære", "vekt": "1 stk", "karbo": 15, "icon": "🍎"},
        {"kategori": "Frukt & Grønt", "navn": "Banan", "vekt": "1 stk", "karbo": 22, "icon": "🍌"},
        {"kategori": "Frukt & Grønt", "navn": "Appelsin", "vekt": "1 stk", "karbo": 18, "icon": "🍊"},
        {"kategori": "Frukt & Grønt", "navn": "Druer", "vekt": "1 neve", "karbo": 15, "icon": "🍇"},
        {"kategori": "Frukt & Grønt", "navn": "Mais", "vekt": "1 liten boks", "karbo": 25, "icon": "🌽"},

        # --- KAKER & SNACKS ---
        {"kategori": "Kaker & Snacks", "navn": "Muffins", "vekt": "1 stk", "karbo": 35, "icon": "🧁"},
        {"kategori": "Kaker & Snacks", "navn": "Bolle", "vekt": "1 stk", "karbo": 30, "icon": "🥯"},
        {"kategori": "Kaker & Snacks", "navn": "Wienerbrød", "vekt": "1 stk", "karbo": 25, "icon": "🥨"},
        {"kategori": "Kaker & Snacks", "navn": "Vaffel", "vekt": "1 plate", "karbo": 25, "icon": "🧇"},
        {"kategori": "Kaker & Snacks", "navn": "Pannekake", "vekt": "1 stk", "karbo": 18, "icon": "🥞"},
        {"kategori": "Kaker & Snacks", "navn": "Sjokoladekake", "vekt": "1 stykke", "karbo": 25, "icon": "🍰"},
        {"kategori": "Kaker & Snacks", "navn": "Is (Pinup)", "vekt": "1 stk", "karbo": 25, "icon": "🍦"},
        {"kategori": "Kaker & Snacks", "navn": "Potetgull", "vekt": "1 porsjon", "karbo": 25, "icon": "🍿"},
        {"kategori": "Kaker & Snacks", "navn": "Sjokolade", "vekt": "1 bar", "karbo": 20, "icon": "🍫"},
        
        # --- DRIKKE ---
        {"kategori": "Drikke", "navn": "Brus / Juice", "vekt": "1 glass (2dl)", "karbo": 20, "icon": "🥤"},
        {"kategori": "Drikke", "navn": "Energidrikk", "vekt": "1 boks", "karbo": 55, "icon": "⚡"},
        {"kategori": "Drikke", "navn": "Iskaffe", "vekt": "1 kartong", "karbo": 25, "icon": "☕"},
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
    kategori = st.session_state.input_kategori # Nytt felt!

    if navn:
        ny_regel = {
            "kategori": kategori,
            "navn": navn, 
            "vekt": vekt, 
            "karbo": karbo, 
            "icon": icon
        }
        st.session_state['standardvarer'].append(ny_regel)
        
        # Tøm feltene
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
        * 📁 Karbo-tabell for diabetikere
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

    # --- HENT ALLE UNIKE KATEGORIER ---
    alle_varer = st.session_state['standardvarer']
    unike_kategorier = sorted(list(set([v.get('kategori', 'Annet') for v in alle_varer])))
    unike_kategorier.insert(0, "Alle") # Legg til "Alle" valget øverst
    
    # --- KATEGORI-VELGER ---
    valgt_kategori = st.selectbox("📂 Velg kategori:", unike_kategorier)

    # --- FILTRER LISTEN ---
    if valgt_kategori == "Alle":
        vis_varer = alle_varer
    else:
        vis_varer = [v for v in alle_varer if v.get('kategori') == valgt_kategori]

    st.markdown("---")
    
    # --- SKJEMA FOR Å LEGGE TIL NY VARE ---
    with st.expander("➕ Legg til ny tommelfinger-regel"):
        c1, c2 = st.columns(2)
        c1.text_input("Navn (f.eks. Bolle)", placeholder="Navn på matvare", key="input_navn")
        c2.text_input("Emoji (f.eks. 🥐)", value="🍽️", key="input_icon")
        
        c3, c4 = st.columns(2)
        c3.text_input("Vekt-tekst (f.eks. 60g)", placeholder="Ca. vekt", key="input_vekt")
        c4.number_input("Karbo per stk (gram)", min_value=0.0, step=1.0, key="input_karbo")
        
        # Velg hvilken kategori den nye tingen skal ha
        st.selectbox("Kategori", unike_kategorier[1:], key="input_kategori") # Hopper over "Alle"
        
        st.button("Lagre ny regel", on_click=lagre_ny_regel)

    # --- VISNING AV REGLER (GRID) ---
    cols = st.columns(2)
    
    if not vis_varer:
        st.info("Ingen varer i denne kategorien ennå.")
    
    for i, vare in enumerate(vis_varer):
        with cols[i % 2]:
            with st.container(border=True):
                st.header(vare['icon'], anchor=False)
                st.subheader(vare['navn'], anchor=False)
                st.caption(f"{vare.get('kategori', 'Annet')}") # Viser kategorien
                
                std_vekt = vare['vekt']
                std_karbo = vare['karbo']
                
                st.markdown(f"**Vekt:** {std_vekt}")
                st.markdown(f"**= {std_karbo} g karbo**")
                
                # --- MINIKALKULATOR ---
                with st.expander("🧮 Endre mengde?"):
                    faktor = st.number_input("Antall / Porsjoner:", min_value=0.1, value=1.0, step=0.5, key=f"calc_{i}_{vare['navn']}")
                    ny_karbo = std_karbo * faktor
                    
                    st.write(f"{faktor} x {std_karbo}g = **{ny_karbo:.1f} g**")
                    
                    if st.button("Legg til dette", key=f"add_calc_{i}_{vare['navn']}"):
                         st.session_state['kurv'].append({
                             "navn": vare['navn'], 
                             "beskrivelse": f"{faktor} stk/porsj ({std_vekt})", 
                             "karbo": ny_karbo
                         })
                         st.rerun()

                # --- HURTIGKNAPPER ---
                c_add, c_del = st.columns([4, 1])
                with c_add:
                    if st.button("1 stk", key=f"add_{i}_{vare['navn']}", use_container_width=True):
                         st.session_state['kurv'].append({
                             "navn": vare['navn'], 
                             "beskrivelse": f"1 stk/porsj ({std_vekt})", 
                             "karbo": std_karbo
                         })
                         st.rerun()
                with c_del:
                    # Vi må finne indeksen i hovedlisten for å slette riktig (siden vi filtrerer)
                    if st.button("🗑️", key=f"del_{i}_{vare['navn']}"):
                        st.session_state['standardvarer'].remove(vare)
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
