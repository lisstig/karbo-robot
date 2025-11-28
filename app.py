import streamlit as st
import pandas as pd
import requests

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

# --- DIN API NØKKEL ---
# HUSK: Bytt ut teksten under med din nye nøkkel fra Kassalapp.no!
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
                    g_saus = st.slider("Mengde saus (g):",
