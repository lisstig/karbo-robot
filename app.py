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
        # Les filen
        df = pd.read_excel("matvarer.xlsx")
        
        # 1. RENSK OPP I KOLONNENAVN (Gjør alt til små bokstaver)
        df.columns = [str(c).lower().strip() for c in df.columns]

        # 2. IDENTIFISER VIKTIGE KOLONNER
        # Nå ser vi etter 'kategori' også!
        navn_col = next((c for c in df.columns if "matvare" in c and "id" not in c), None)
        karbo_col = next((c for c in df.columns if "karbo" in c), None)
        
        # Sjekker om vi finner en kolonne som heter "kategori" eller "gruppe"
        gruppe_col = next((c for c in df.columns if "kategori" in c or "gruppe" in c), None)

        if navn_col and karbo_col and gruppe_col:
            
            # 3. VELG UT DATA
            # Nå trenger vi ikke masse logikk, vi bare henter kolonnene
            df = df[[navn_col, gruppe_col, karbo_col]].copy()
            
            # 4. STANDARDISERING
            df.columns = ['Matvare', 'Matvaregruppe', 'Karbo_g']
            
            # Rydd opp i kategorinavnene (noen ganger henger det med tomme celler)
            df['Matvaregruppe'] = df['Matvaregruppe'].fillna("Diverse")
            
            # Sikre at Karbo er tall
            df['Karbo_g'] = pd.to_numeric(df['Karbo_g'], errors='coerce').fillna(0)
            
            return df
        else:
            # Feilmelding hvis den ikke finner den nye kolonnen din
            st.error(f"Fant ikke alle kolonner. Jeg ser etter 'Matvare', 'Karbohydrat' og 'Kategori'. Fant disse: {df.columns.tolist()}")
            return None

    except FileNotFoundError:
        st.warning("⚠️ Finner ikke 'matvarer.xlsx'. Husk å laste opp den nye filen til GitHub!")
        return None
    except Exception as e:
        st.error(f"Noe gikk galt: {e}")
        return None

df = last_data()

# --- BRUKERGRENSESNITT ---
if df is not None:
    # 1. KATEGORI-VELGER
    # Hent unike kategorier og sorter dem alfabetisk
    unike_kat = sorted([str(k) for k in df['Matvaregruppe'].unique() if k is not None])
    
    valgt_kat = st.selectbox("Velg kategori:", ["Alle"] + unike_kat)

    # Filtrer tabellen basert på valg
    if valgt_kat != "Alle":
        df_visning = df[df['Matvaregruppe'] == valgt_kat]
    else:
        df_visning = df

    st.subheader("🔍 Finn matvare")

    # 2. SØKEFELT
    matvarer = sorted(df_visning['Matvare'].astype(str).unique())
    valgt_mat = st.selectbox("Søk:", matvarer)

    if valgt_mat:
        # Hent tallene
        rad = df[df['Matvare'] == valgt_mat].iloc[0]
        karbo_100 = rad['Karbo_g']

        # 3. VISNING OG KALKULATOR
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Karbo pr 100g", f"{karbo_100:.1f}")
        with c2:
            mengde = st.number_input("Mengde (g):", value=100, step=10)
        
        tot_mat = (mengde / 100) * karbo_100

        # 4. BBQ-SEKSJON
        st.markdown("---")
        with st.expander("🔥 BBQ & Saus"):
            bbq = st.checkbox("Legg til saus/glaze")
            tot_saus = 0
            if bbq:
                g_saus = st.slider("Gram saus:", 0, 150, 20)
                tot_saus = (g_saus/100)*35
                st.caption(f"+ {tot_saus:.1f} g karbo")
        
        # 5. TOTAL
        total = tot_mat + tot_saus
        st.markdown("---")
        st.subheader("Til Pumpa (KH):")
        st.title(f"{total:.1f} g")
