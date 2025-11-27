import streamlit as st
import pandas as pd

# --- KONFIGURASJON & SØKEORD ---
# Her legger vi inn nøkkelord i tittelen så Google lettere finner den
st.set_page_config(
    page_title="Karbo-Robot: Norsk Karbokalkulator for Diabetes Type 1", 
    page_icon="🍖",
    layout="centered"
)

# --- INITIALISER HUKOMMELSE ---
if 'kurv' not in st.session_state:
    st.session_state['kurv'] = []

# --- TITTEL ---
st.title("🤖 Karbo-Robot")

if st.session_state['kurv']:
    antall_varer = len(st.session_state['kurv'])
    total_karbo_kurv = sum(item['karbo'] for item in st.session_state['kurv'])
    st.info(f"🛒 Du har **{antall_varer}** ting i kurven. Total: **{total_karbo_kurv:.1f} g**")

# --- SIDEBAR (Meny & Hjelp) ---
with st.sidebar:
    st.header("Innstillinger")
    
    if st.button("🗑️ Tøm hele kurven"):
        st.session_state['kurv'] = []
        st.rerun()
    
    if st.button("🔄 Oppdater data"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    
    # --- NYTT: BRUKSANVISNING ---
    with st.expander("❓ Slik bruker du appen"):
        st.markdown("""
        1. **Søk** etter matvare (f.eks "Pølse").
        2. Velg **antall** eller **gram**.
        3. Mangler du vekt? Bruk **Pakke-kalkulatoren** som dukker opp.
        4. Trykk **"Legg til i måltidet"**.
        5. Gjenta for alle matvarer (f.eks brød, drikke).
        6. Se **totalsummen** nederst og legg inn i pumpa.
        """)

    # --- OM DATAENE ---
    with st.expander("ℹ️ Om dataene"):
        st.markdown("""
        **Kilder:**
        * 🥗 **Næringsinnhold:** [Matvaretabellen.no](https://www.matvaretabellen.no).
        * ⚖️ **Vekt:** Produsentinfo (Gilde, Hatting, etc.).
        * 🔥 **BBQ:** Egne beregninger.
        
        *Laget for MiniMed 780G.*
        """)

# --- LASTE DATA ---
@st.cache_data
def last_data():
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
        else:
            st.error("Mangler kolonner i Excel.")
            return None
    except Exception as e:
        st.error(f"Feil: {e}")
        return None

df = last_data()

# --- APP UI ---
if df is not None:
    # 1. KATEGORI
    unike_kat = sorted([str(k) for k in df['Matvaregruppe'].unique() if k is not None])
    valgt_kat = st.selectbox("Velg kategori (valgfritt):", ["Alle"] + unike_kat)

    if valgt_kat != "Alle":
        df_visning = df[df['Matvaregruppe'] == valgt_kat]
    else:
        df_visning = df

    st.subheader("🔍 Finn matvare")

    # 2. SØK
    matvarer = sorted(df_visning['Matvare'].astype(str).unique())
    valgt_mat = st.selectbox("Søk:", matvarer, index=None, placeholder="Skriv for å søke...")

    if valgt_mat:
        rad = df[df['Matvare'] == valgt_mat].iloc[0]
        karbo_100 = rad['Karbo_g']
        vekt_stk_db = rad['Vekt_stk']
        kategori = rad['Matvaregruppe']

        st.caption(f"Kategori: {kategori} | Karbo: {karbo_100}g pr 100g")

        c1, c2 = st.columns(2)
        beskrivelse_mengde = "" 
        
        with c1:
            # SCENARIO A: Har vekt i Excel
            if pd.notna(vekt_stk_db) and vekt_stk_db > 0:
                enhet = st.radio("Enhet", ["Gram", f"Stk ({int(vekt_stk_db)}g)"], horizontal=True)
                if "Stk" in enhet:
                    antall = st.number_input("Antall stk:", value=1.0, step=1.0)
                    mengde_i_gram = antall * vekt_stk_db
                    beskrivelse_mengde = f"{antall} stk"
                else:
                    mengde_i_gram = st.number_input("Mengde (g):", value=100, step=10)
                    beskrivelse_mengde = f"{mengde_i_gram} g"
            
            # SCENARIO B: Mangler vekt (Pakke-kalkulator)
            else:
                mengde_i_gram = st.number_input("Mengde (g):", value=100, step=10)
                beskrivelse_mengde = f"{mengde_i_gram} g"

                with st.expander("🔢 Har du hele pakken?"):
                    pk_vekt = st.number_input("Totalvekt pakke (g):", min_value=0, value=None, step=1, placeholder="F.eks 600")
                    pk_ant = st.number_input("Antall i pakke:", min_value=1, value=1, step=1)
                    
                    if pk_vekt and pk_ant:
                        stk_vekt = pk_vekt / pk_ant
                        st.success(f"1 stk veier ca **{stk_vekt:.0f} g**")
                        
                        ant_spist = st.number_input("Antall spist:", value=1.0, step=1.0)
                        
                        mengde_i_gram = ant_spist * stk_vekt
                        beskrivelse_mengde = f"{ant_spist} stk (fra pakke)"
        
        with c2:
            st.write("🔥 **BBQ / Saus**")
            bbq_aktiv = st.checkbox("Legg til saus?")
            tillegg_karbo = 0
            if bbq_aktiv:
                g_saus = st.slider("Mengde saus (g):", 0, 150, 20)
                tillegg_karbo = (g_saus/100)*35
                beskrivelse_mengde += f" + {g_saus}g saus"

        mat_karbo = (mengde_i_gram / 100) * karbo_100
        total_linje = mat_karbo + tillegg_karbo
        
        st.markdown(f"### = {total_linje:.1f} g karbo")

        if st.button("➕ Legg til i måltidet", type="primary"):
            nytt_element = {
                "navn": valgt_mat,
                "beskrivelse": beskrivelse_mengde,
                "karbo": total_linje
            }
            st.session_state['kurv'].append(nytt_element)
            st.success(f"La til {valgt_mat}!")
            st.rerun()

    st.markdown("---")
    st.header("🍽️ Dagens Måltid")

    if st.session_state['kurv']:
        kurv_df = pd.DataFrame(st.session_state['kurv'])
        st.table(kurv_df[['navn', 'beskrivelse', 'karbo']])
        
        total_sum = sum(item['karbo'] for item in st.session_state['kurv'])
        
        st.markdown("---")
        col_res1, col_res2 = st.columns([2, 1])
        with col_res1:
            st.subheader("Totalt til Pumpa (MiniMed):")
        with col_res2:
            st.title(f"{total_sum:.1f} g")
            
        if st.button("Angre siste"):
            st.session_state['kurv'].pop()
            st.rerun()
            
    else:
        st.caption("Kurven er tom. Søk og legg til matvarer over.")
