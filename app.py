import streamlit as st
import pandas as pd
import numpy as np

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
        # Les filen
        df = pd.read_excel("matvarer.xlsx")
        
        # 1. RENSK OPP I KOLONNENAVN
        df.columns = [str(c).lower().strip() for c in df.columns]

        # 2. IDENTIFISER VIKTIGE KOLONNER
        navn_col = next((c for c in df.columns if "matvare" in c and "id" not in c and "gruppe" not in c), None)
        karbo_col = next((c for c in df.columns if "karbo" in c), None)
        id_col = next((c for c in df.columns if "id" in c), None) # Matvare ID

        if navn_col and karbo_col:
            
            # 3. FIX KATEGORIER
            if id_col:
                df['kategori'] = None
                
                # --- FORBEDRET LOGIKK FOR Å FINNE OVERSKRIFTER ---
                # Vi tvinger ID til å være numerisk. Alt som ikke er tall (tekst, tomme felt, mellomrom) blir NaN
                id_numeric = pd.to_numeric(df[id_col], errors='coerce')
                
                # Hvis ID mangler (er NaN), antar vi det er en Kategori-overskrift
                mask_kategori = id_numeric.isna()
                
                # Kopier navnet over til kategori-kolonnen
                df.loc[mask_kategori, 'kategori'] = df.loc[mask_kategori, navn_col]
                
                # Fyll nedover (Adzukibønner arver kategorien over seg)
                df['kategori'] = df['kategori'].ffill()
                
                # Fjern radene som bare er overskrifter
                df = df[~mask_kategori].copy()
                
                # Hvis kategorier fortsatt er tomme (f.eks hvis første rad var data), sett en standard
                df['kategori'] = df['kategori'].fillna("Diverse")
            else:
                df['kategori'] = "Alle varer"

            # 4. FERDIGSTILLING
            df = df.rename(columns={navn_col: 'Matvare', karbo_col: 'Karbo_g', 'kategori': 'Matvaregruppe'})
            df = df[['Matvare', 'Matvaregruppe', 'Karbo_g']]
            
            # Sikre at Karbo er tall
            df['Karbo_g'] = pd.to_numeric(df['Karbo_g'], errors='coerce').fillna(0)
            
            return df
        else:
            st.error(f"Fant ikke riktige kolonner. Fant disse: {df.columns.tolist()}")
            return None

    except FileNotFoundError:
        st.warning("⚠️ Finner ikke 'matvarer.xlsx'.")
        return None
    except Exception as e:
        st.error(f"Noe gikk galt: {e}")
        return None

df = last_data()

# --- BRUKERGRENSESNITT ---
if df is not None:
    # Kategori-filter
    unike_kat = sorted([str(k) for k in df['Matvaregruppe'].unique() if k is not None])
    
    # UI Layout
    valgt_kat = st.selectbox("Velg kategori:", ["Alle"] + unike_kat)

    if valgt_kat != "Alle":
        df_visning = df[df['Matvaregruppe'] == valgt_kat]
    else:
        df_visning = df

    st.subheader("🔍 Finn matvare")

    # Søkefelt
    matvarer = sorted(df_visning['Matvare'].astype(str).unique())
    valgt_mat = st.selectbox("Søk:", matvarer)

    if valgt_mat:
        rad = df[df['Matvare'] == valgt_mat].iloc[0]
        karbo_100 = rad['Karbo_g']

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Karbo pr 100g", f"{karbo_100:.1f}")
        with c2:
            mengde = st.number_input("Mengde (g):", value=100, step=10)
        
        tot_mat = (mengde / 100) * karbo_100

        # BBQ-seksjon
        st.markdown("---")
        with st.expander("🔥 BBQ & Saus"):
            bbq = st.checkbox("Legg til saus/glaze")
            tot_saus = 0
            if bbq:
                g_saus = st.slider("Gram saus:", 0, 150, 20)
                tot_saus = (g_saus/100)*35
                st.caption(f"+ {tot_saus:.1f} g karbo")
        
        # Totalsum
        total = tot_mat + tot_saus
        st.markdown("---")
        st.subheader("Til Pumpa (KH):")
        st.title(f"{total:.1f} g")

    # --- DEBUG VERKTØY (Kun synlig nederst) ---
    st.markdown("---")
    with st.expander("🛠️ Se rådata (For feilsøking)"):
        st.write("Her er de 10 første radene appen ser:")
        st.dataframe(df.head(10))
        st.write(f"Antall kategorier funnet: {len(unike_kat)}")
        st.write(unike_kat)
