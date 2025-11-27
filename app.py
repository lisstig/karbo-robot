import streamlit as st
import pandas as pd

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

st.title("🤖 Karbo-Robot")
st.caption("Din smarte karbo-kalkulator")

# --- KNAPP FOR Å TØMME MINNET ---
if st.sidebar.button("Oppdater data / Nullstill"):
    st.cache_data.clear()
    st.rerun()

# --- LASTE DATA ---
@st.cache_data
def last_data():
    try:
        df = pd.read_excel("matvarer.xlsx")
        
        # RENSK OPP I KOLONNENAVN
        df.columns = [str(c).lower().strip() for c in df.columns]

        # IDENTIFISER KOLONNER
        navn_col = next((c for c in df.columns if "matvare" in c and "id" not in c), None)
        karbo_col = next((c for c in df.columns if "karbo" in c), None)
        gruppe_col = next((c for c in df.columns if "kategori" in c or "gruppe" in c), None)
        # Sjekk etter vekt-kolonne (valgfritt)
        vekt_col = next((c for c in df.columns if "vekt" in c), None)

        if navn_col and karbo_col and gruppe_col:
            cols = [navn_col, gruppe_col, karbo_col]
            if vekt_col: cols.append(vekt_col)
            
            df = df[cols].copy()
            
            nye_navn = {navn_col: 'Matvare', gruppe_col: 'Matvaregruppe', karbo_col: 'Karbo_g'}
            if vekt_col: nye_navn[vekt_col] = 'Vekt_stk'
            
            df = df.rename(columns=nye_navn)
            
            # Lag Vekt_stk hvis den mangler
            if 'Vekt_stk' not in df.columns:
                df['Vekt_stk'] = None
            
            df['Matvaregruppe'] = df['Matvaregruppe'].fillna("Diverse")
            df['Karbo_g'] = pd.to_numeric(df['Karbo_g'], errors='coerce').fillna(0)
            df['Vekt_stk'] = pd.to_numeric(df['Vekt_stk'], errors='coerce')
            
            return df
        else:
            st.error("Mangler kolonner i Excel-arket.")
            return None

    except FileNotFoundError:
        st.warning("⚠️ Finner ikke 'matvarer.xlsx'.")
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
        vekt_stk_db = rad['Vekt_stk'] # Vekt fra Excel (hvis den finnes)
        kategori = rad['Matvaregruppe']

        st.info(f"📁 Kategori: {kategori}")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Karbo pr 100g", f"{karbo_100:.1f}")

        # --- LOGIKK FOR MENGDE ---
        with c2:
            # SCENARIO A: Vi har vekten i Excel allerede
            if pd.notna(vekt_stk_db) and vekt_stk_db > 0:
                enhet = st.radio("Enhet", ["Gram", f"Stk (ca {int(vekt_stk_db)}g)"], horizontal=True)
                if "Stk" in enhet:
                    antall = st.number_input("Antall stk:", value=1.0, step=0.5)
                    mengde_i_gram = antall * vekt_stk_db
                else:
                    mengde_i_gram = st.number_input("Mengde (g):", value=100, step=10)
            
            # SCENARIO B: Vi mangler vekt -> Bruk Pakke-kalkulator
            else:
                # Standard input er gram
                mengde_i_gram = st.number_input("Mengde (g):", value=100, step=10)
                
                # ... men vi tilbyr hjelp!
                st.markdown("---")
                with st.expander("🔢 Har du hele pakken?"):
                    st.caption("Regn ut stykk-vekt her og nå:")
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        pakke_vekt = st.number_input("Totalvekt på pakka (g):", min_value=0, value=0)
                    with col_p2:
                        pakke_antall = st.number_input("Antall i pakka:", min_value=1, value=1)
                    
                    if pakke_vekt > 0:
                        beregnet_vekt = pakke_vekt / pakke_antall
                        st.success(f"1 stk veier ca **{beregnet_vekt:.0f} g**")
                        
                        # Spør hvor mange man spiser
                        antall_spist = st.number_input("Hvor mange spiser du?", min_value=0.5, value=1.0, step=0.5)
                        
                        # Overskriv mengde_i_gram med beregnet verdi
                        mengde_i_gram = antall_spist * beregnet_vekt
                        st.caption(f"Beregner ut fra {mengde_i_gram:.0f} g")

        # --- BEREGNING ---
        tot_mat = (mengde_i_gram / 100) * karbo_100

        # --- BBQ ---
        st.markdown("---")
        with st.expander("🔥 BBQ & Saus"):
            bbq = st.checkbox("Legg til saus/glaze")
            tot_saus = 0
            if bbq:
                g_saus = st.slider("Gram saus:", 0, 150, 20)
                tot_saus = (g_saus/100)*35
                st.caption(f"+ {tot_saus:.1f} g karbo")
        
        # --- TOTAL ---
        total = tot_mat + tot_saus
        st.markdown("---")
        st.subheader("Til Pumpa (KH):")
        st.title(f"{total:.1f} g")
        
        # Vis bekreftelse på hva vi har regnet ut
        if total > 0:
            st.caption(f"Basert på {mengde_i_gram:.0f}g matvare.")
