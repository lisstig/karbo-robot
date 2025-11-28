import streamlit as st
import pandas as pd
import requests

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

# --- DIN API NØKKEL ---
API_KEY = "x2Y4R0b7NwDZpB19DRlljFlUFQmaT9aMgbzOrN8L"

# --- INITIALISER HUKOMMELSE ---
if 'kurv' not in st.session_state:
    st.session_state['kurv'] = []

# --- FUNKSJON: HENT DATA FRA KASSALAPP ---
def sok_kassalapp(sokeord):
    url = "https://kassal.app/api/v1/products"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # Henter opp til 50 varer
    params = {
        "search": sokeord,
        "size": 50
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except Exception as e:
        st.error(f"Klarte ikke koble til Kassalapp: {e}")
        return []

# --- LASTE LOKALE DATA (EXCEL) ---
@st.cache_data
def last_lokale_data():
    try:
        df = pd.read_excel("matvarer.xlsx")
        df.columns = [str(c).lower().strip() for c in df.columns]
        navn_col = next((c for c in df.columns if "matvare" in c and "id" not in c), None)
        karbo_col = next((c for c in df.columns if "karbo" in c), None)
        gruppe_col = next((c for c in df.columns if "kategori" in c or "gruppe" in c), None)
        vekt_col = next((c for c in df.columns if "vekt" in c), None)

        if navn_col and karbo_col and gruppe_col:
            cols = [navn_col, gruppe_col, karbo_col]
            if vekt_col: cols.append(vekt_col)
            df = df[cols].copy()
            nye_navn = {navn_col: 'Matvare', gruppe_col: 'Matvaregruppe', karbo_col: 'Karbo_g'}
            if vekt_col: nye_navn[vekt_col] = 'Vekt_stk'
            df = df.rename(columns=nye_navn)
            if 'Vekt_stk' not in df.columns: df['Vekt_stk'] = None
            df['Matvaregruppe'] = df['Matvaregruppe'].fillna("Diverse")
            df['Karbo_g'] = pd.to_numeric(df['Karbo_g'], errors='coerce').fillna(0)
            df['Vekt_stk'] = pd.to_numeric(df['Vekt_stk'], errors='coerce')
            return df
        return None
    except:
        return None

df_lokal = last_lokale_data()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Innstillinger")
    if st.button("🗑️ Tøm kurv"):
        st.session_state['kurv'] = []
        st.rerun()
    if st.button("🔄 Oppdater data"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    with st.expander("💬 Kontakt"):
        st.link_button("✍️ Gi tilbakemelding", "https://forms.gle/xn1RnNAgcr1frzhr8")

# --- UI START ---
st.title("🤖 Karbo-Robot")

if st.session_state['kurv']:
    tot_karbo = sum(i['karbo'] for i in st.session_state['kurv'])
    st.info(f"🛒 I kurven: **{len(st.session_state['kurv'])}** varer. Totalt: **{tot_karbo:.1f} g**")

# --- FANER ---
tab1, tab2 = st.tabs(["📂 Mine varer (Excel)", "🌐 Søk på nettet (Ny!)"])

# ==========================
# FANE 1: LOKAL EXCEL
# ==========================
with tab1:
    if df_lokal is not None:
        kats = sorted([str(k) for k in df_lokal['Matvaregruppe'].unique() if k])
        valgt_kat = st.selectbox("Kategori:", ["Alle"] + kats)
        df_vis = df_lokal if valgt_kat == "Alle" else df_lokal[df_lokal['Matvaregruppe'] == valgt_kat]
        
        matvarer = sorted(df_vis['Matvare'].astype(str).unique())
        valgt_mat = st.selectbox("Velg vare:", matvarer, index=None, placeholder="Søk i dine egne varer...")

        if valgt_mat:
            rad = df_lokal[df_lokal['Matvare'] == valgt_mat].iloc[0]
            kb_100 = rad['Karbo_g']
            vekt_stk = rad['Vekt_stk']
            
            st.caption(f"Karbo: {kb_100}g / 100g")
            
            c1, c2 = st.columns(2)
            mengde_txt = ""
            with c1:
                if pd.notna(vekt_stk) and vekt_stk > 0:
                    mode = st.radio("Enhet", ["Gram", f"Stk ({int(vekt_stk)}g)"], horizontal=True)
                    if "Stk" in mode:
                        ant = st.number_input("Antall:", 1.0, step=0.5)
                        gram = ant * vekt_stk
                        mengde_txt = f"{ant} stk"
                    else:
                        gram = st.number_input("Gram:", 100, step=10)
                        mengde_txt = f"{gram} g"
                else:
                    gram = st.number_input("Gram:", 100, step=10)
                    mengde_txt = f"{gram} g"
                    
                    with st.expander("🔢 Har du hele pakken?"):
                        p_vekt = st.number_input("Pakkevekt (g):", min_value=0, value=None, step=1)
                        p_ant = st.number_input("Antall i pakke:", min_value=1, value=1)
                        if p_vekt:
                            stk_v = p_vekt/p_ant
                            st.write(f"1 stk = {stk_v:.0f} g")
                            spist = st.number_input("Spist:", 1.0, step=0.5)
                            gram = spist * stk_v
                            mengde_txt = f"{spist} stk (fra pakke)"

            with c2:
                bbq = st.checkbox("Saus/Glaze?")
                tillegg = 0
                if bbq:
                    g_saus = st.slider("Mengde saus (g):", 0, 150, 20)
                    tillegg = (g_saus/100)*35
                    mengde_txt += f" + saus"
            
            tot = (gram/100)*kb_100 + tillegg
            st.write(f"### = {tot:.1f} g karbo")
            
            if st.button("➕ Legg til", key="add_local"):
                st.session_state['kurv'].append({"navn": valgt_mat, "beskrivelse": mengde_txt, "karbo": tot})
                st.rerun()

# ==========================
# FANE 2: KASSALAPP API
# ==========================
with tab2:
    st.caption("Søker i tusenvis av norske dagligvarer via Kassalapp.no")
    nett_sok = st.text_input("Søk etter noe (f.eks 'Gilde pølse'):")
    
    if nett_sok = st.text_input("Søk etter noe (f.eks 'Gilde pølse'):")
    st.caption("💡 Tips: Får du få treff? Prøv entall (f.eks 'pølse' i stedet for 'pølser') eller færre ord.")
        
        if not resultater:
            st.warning("Fant ingen varer. Prøv et annet ord.")
        else:
            st.success(f"Fant {len(resultater)} produkter!")

            # FIX: Vi lager HELT unike nøkler ved å legge på et tall foran (1. , 2. etc)
            valg_liste = {}
            for i, p in enumerate(resultater):
                navn = p['name']
                vendor = p.get('vendor', '')
                ean = p.get('ean', '')
                
                # Her lager vi "1. Gilde Pølse...", "2. Gilde Pølse..."
                visningsnavn = f"{i+1}. {navn} ({vendor}) {ean}"
                valg_liste[visningsnavn] = p

            valgt_nettvare_navn = st.selectbox("Velg produkt:", list(valg_liste.keys()), index=None)
            
            if valgt_nettvare_navn:
                produkt = valg_liste[valgt_nettvare_navn]
                navn = produkt['name']
                
                # --- KARBO-DETEKTIV ---
                nutr = produkt.get('nutrition', [])
                karbo_api = 0
                found_nutrition = False
                mulige_koder = ['carbohydrates', 'carbohydrate', 'karbohydrater', 'karbohydrat']
                
                for n in nutr:
                    if n.get('code', '').lower() in mulige_koder:
                        karbo_api = n.get('amount', 0)
                        found_nutrition = True
                        break
                
                vekt_api = produkt.get('weight', 0)
                
                # UI VISNING
                c_img, c_info = st.columns([1, 3])
                with c_img:
                    if produkt.get('image'):
                        st.image(produkt['image'], width=100)
                with c_info:
                    st.subheader(navn)
                    
                    if found_nutrition:
                        st.write(f"📊 **Karbo:** {karbo_api}g per 100g")
                    else:
                        st.error("⚠️ Fant ingen karbo-data på dette produktet!")
                    
                    if vekt_api:
                        st.write(f"⚖️ **Vekt registrert:** {vekt_api}g")
                
                # DEBUG DATA
                with st.expander("🛠️ Se rådata (For feilsøking)"):
                    st.write(produkt)

                # KALKULATOR
                st.markdown("---")
                c_kalk1, c_kalk2 = st.columns(2)
                
                mengde_nett = 0
                beskrivelse_nett = ""
                
                with c_kalk1:
                    valg_type = st.radio("Hvordan vil du regne?", ["Gram", "Hele pakken/Stk"], horizontal=True)
                    
                    if valg_type == "Gram":
                        mengde_nett = st.number_input("Antall gram:", 100, step=10, key="nett_gram")
                        beskrivelse_nett = f"{mengde_nett} g"
                    else:
                        st.caption(f"Vi fant vekten: {vekt_api}g. Vet du antallet?")
                        start_vekt = float(vekt_api) if vekt_api else None
                        pk_vekt = st.number_input("Totalvekt (g):", value=start_vekt, step=1.0, key="nett_pk_vekt")
                        pk_ant = st.number_input("Antall i pakke:", min_value=1, value=1, key="nett_pk_ant")
                        
                        if pk_vekt:
                            enhet_vekt = pk_vekt / pk_ant
                            st.write(f"👉 1 stk veier ca **{enhet_vekt:.0f} g**")
                            ant_spist = st.number_input("Antall du spiser:", 1.0, step=0.5, key="nett_spist")
                            mengde_nett = ant_spist * enhet_vekt
                            beskrivelse_nett = f"{ant_spist} stk ({navn})"

                with c_kalk2:
                    bbq_nett = st.checkbox("Saus/Glaze?", key="bbq_nett")
                    tillegg_nett = 0
                    if bbq_nett:
                        g_saus = st.slider("Saus (g):", 0, 150, 20, key="slider_nett")
                        tillegg_nett = (g_saus/100)*35
                        beskrivelse_nett += " + saus"

                tot_nett = (mengde_nett/100)*karbo_api + tillegg_nett
                st.write(f"### = {tot_nett:.1f} g karbo")
                
                if st.button("➕ Legg til i måltid", key="btn_nett"):
                    st.session_state['kurv'].append({"navn": navn, "beskrivelse": beskrivelse_nett, "karbo": tot_nett})
                    st.rerun()

# --- KURV ---
st.markdown("---")
st.header("🍽️ Dagens Måltid")

if st.session_state['kurv']:
    kurv_df = pd.DataFrame(st.session_state['kurv'])
    st.table(kurv_df[['navn', 'beskrivelse', 'karbo']])
    total_sum = sum(item['karbo'] for item in st.session_state['kurv'])
    col_res1, col_res2 = st.columns([2, 1])
    with col_res1:
        st.subheader("Totalt til Pumpa:")
    with col_res2:
        st.title(f"{total_sum:.1f} g")
    if st.button("Angre siste"):
        st.session_state['kurv'].pop()
        st.rerun()
else:
    st.caption("Kurven er tom.")
