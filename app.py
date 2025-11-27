import streamlit as st
import pandas as pd

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

# --- INITIALISER HUKOMMELSE (Session State) ---
# Dette gjør at appen husker hva du har lagt i kurven
if 'kurv' not in st.session_state:
    st.session_state['kurv'] = []

# --- TITTEL ---
st.title("🤖 Karbo-Robot")
# Vis en liten oppsummering øverst hvis kurven ikke er tom
if st.session_state['kurv']:
    antall_varer = len(st.session_state['kurv'])
    total_karbo_kurv = sum(item['karbo'] for item in st.session_state['kurv'])
    st.info(f"🛒 Du har **{antall_varer}** ting i kurven. Total: **{total_karbo_kurv:.1f} g**")

# --- KNAPP FOR Å NULLSTILLE ---
with st.sidebar:
    st.header("Innstillinger")
    if st.button("🗑️ Tøm hele kurven"):
        st.session_state['kurv'] = []
        st.rerun()
    
    st.markdown("---")
    if st.button("🔄 Oppdater data fra Excel"):
        st.cache_data.clear()
        st.rerun()

# --- LASTE DATA ---
@st.cache_data
def last_data():
    try:
        df = pd.read_excel("matvarer.xlsx")
        df.columns = [str(c).lower().strip() for c in df.columns]

        # Identifiser kolonner
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

# --- APP UI: VELG MATVARE ---
if df is not None:
    # 1. KATEGORI FILTER
    unike_kat = sorted([str(k) for k in df['Matvaregruppe'].unique() if k is not None])
    valgt_kat = st.selectbox("Velg kategori (valgfritt):", ["Alle"] + unike_kat)

    if valgt_kat != "Alle":
        df_visning = df[df['Matvaregruppe'] == valgt_kat]
    else:
        df_visning = df

    st.subheader("🔍 Finn matvare")

    # 2. SØKEFELT
    matvarer = sorted(df_visning['Matvare'].astype(str).unique())
    valgt_mat = st.selectbox("Søk:", matvarer, index=None, placeholder="Skriv for å søke...")

    # --- HVIS NOE ER VALGT: VIS KALKULATOR ---
    if valgt_mat:
        rad = df[df['Matvare'] == valgt_mat].iloc[0]
        karbo_100 = rad['Karbo_g']
        vekt_stk_db = rad['Vekt_stk']
        kategori = rad['Matvaregruppe']

        st.caption(f"Kategori: {kategori} | Karbo: {karbo_100}g pr 100g")

        # --- MENGDEBEREGNING ---
        c1, c2 = st.columns(2)
        
        # Variabel for å holde styr på hva vi beregner
        beskrivelse_mengde = "" 
        
        with c1:
            # SCENARIO A: Har vekt i Excel
            if pd.notna(vekt_stk_db) and vekt_stk_db > 0:
                enhet = st.radio("Enhet", ["Gram", f"Stk ({int(vekt_stk_db)}g)"], horizontal=True)
                if "Stk" in enhet:
                    antall = st.number_input("Antall stk:", value=1.0, step=0.5)
                    mengde_i_gram = antall * vekt_stk_db
                    beskrivelse_mengde = f"{antall} stk"
                else:
                    mengde_i_gram = st.number_input("Mengde (g):", value=100, step=10)
                    beskrivelse_mengde = f"{mengde_i_gram} g"
            
            # SCENARIO B: Mangler vekt (Pakke-kalkulator)
            else:
                mengde_i_gram = st.number_input("Mengde (g):", value=100, step=10)
                beskrivelse_mengde = f"{mengde_i_gram} g"

                # Pakkehjelp
                with st.expander("🔢 Har du hele pakken?"):
                    pk_vekt = st.number_input("Totalvekt pakke (g):", 0)
                    pk_ant = st.number_input("Antall i pakke:", 1)
                    if pk_vekt > 0:
                        stk_vekt = pk_vekt / pk_ant
                        st.write(f"1 stk = {stk_vekt:.0f} g")
                        ant_spist = st.number_input("Antall spist:", 1.0, step=0.5)
                        mengde_i_gram = ant_spist * stk_vekt
                        beskrivelse_mengde = f"{ant_spist} stk (fra pakke)"

        # --- SAUS / BBQ TILLEGG ---
        with c2:
            st.write("🔥 **BBQ / Saus**")
            bbq_aktiv = st.checkbox("Legg til saus?")
            tillegg_karbo = 0
            if bbq_aktiv:
                g_saus = st.slider("Mengde saus (g):", 0, 150, 20)
                tillegg_karbo = (g_saus/100)*35
                beskrivelse_mengde += f" + {g_saus}g saus"

        # --- BEREGN LINJESUM ---
        mat_karbo = (mengde_i_gram / 100) * karbo_100
        total_linje = mat_karbo + tillegg_karbo
        
        st.markdown(f"### = {total_linje:.1f} g karbo")

        # --- KNAPP: LEGG I KURV ---
        if st.button("➕ Legg til i måltidet", type="primary"):
            # Lagre det vi har funnet ut i en liste
            nytt_element = {
                "navn": valgt_mat,
                "beskrivelse": beskrivelse_mengde,
                "karbo": total_linje
            }
            st.session_state['kurv'].append(nytt_element)
            st.success(f"La til {valgt_mat}!")
            # Vi trenger ikke rerun her, for Streamlit oppdaterer UI automatisk ved neste interaksjon,
            # men for at tabellen under skal oppdatere seg med en gang:
            st.rerun()

    # --- VIS KURVEN (MÅLTIDET) ---
    st.markdown("---")
    st.header("🍽️ Dagens Måltid")

    if st.session_state['kurv']:
        # Lag en fin tabell av kurven
        kurv_df = pd.DataFrame(st.session_state['kurv'])
        
        # Vis tabellen (vi skjuler indeksen for pent utseende)
        st.table(kurv_df[['navn', 'beskrivelse', 'karbo']])
        
        # BEREGN TOTALSUM
        total_sum = sum(item['karbo'] for item in st.session_state['kurv'])
        
        st.markdown("---")
        col_res1, col_res2 = st.columns([2, 1])
        with col_res1:
            st.subheader("Totalt til Pumpa (MiniMed):")
        with col_res2:
            st.title(f"{total_sum:.1f} g")
            
        # Knapp for å angre siste
        if st.button("Angre siste"):
            st.session_state['kurv'].pop()
            st.rerun()
            
    else:
        st.caption("Kurven er tom. Søk og legg til matvarer over.")
