import streamlit as st
import pandas as pd

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

st.title("🤖 Karbo-Robot")
st.caption("Din smarte karbo-kalkulator")

# --- LASTE DATA ---
@st.cache_data
def last_data():
    try:
        # Les Excel-filen
        df = pd.read_excel("matvarer.xlsx")
        
        # 1. STANDARIDISERING AV KOLONNER
        # Gjør overskriftene om til små bokstaver og fjern mellomrom
        df.columns = [str(c).lower().strip() for c in df.columns]

        # Finn nøkkel-kolonnene
        # Vi ser etter 'karbohydrat' (kan hete 'karbohydrat (g)')
        karbo_col = next((c for c in df.columns if "karbo" in c), None)
        # Vi ser etter 'matvare' 
        navn_col = next((c for c in df.columns if "matvare" in c and "id" not in c), None)
        # Vi ser etter ID (for å skille overskrifter fra mat)
        id_col = next((c for c in df.columns if "id" in c), None)

        if karbo_col and navn_col:
            
            # 2. HÅNDTER KATEGORIER (Den smarte delen!)
            # Hvis filen har kategorier som overskrifter i radene (som "Meieriprodukter")
            # sjekker vi om ID-kolonnen mangler data på de radene.
            
            if id_col:
                # Lag en ny kolonne for Kategori
                df['kategori'] = None
                
                # Hvis ID mangler, er det en overskrift -> Bruk navnet som kategori
                mask_overskrift = df[id_col].isna()
                df.loc[mask_overskrift, 'kategori'] = df.loc[mask_overskrift, navn_col]
                
                # "Fyll nedover": Alle matvarer under "Meieriprodukter" får den kategorien
                df['kategori'] = df['kategori'].ffill()
                
                # Fjern selve overskrifts-radene (vi trenger ikke "Meieriprodukter" som et matvalg)
                df = df[~mask_overskrift].copy()
            else:
                # Hvis ingen ID finnes, legg alt i én haug
                df['kategori'] = "Alle varer"

            # 3. RENSHIET OG FORMATERING
            # Gi kolonnene standard navn
            df = df.rename(columns={navn_col: 'Matvare', karbo_col: 'Karbo_g', 'kategori': 'Matvaregruppe'})
            
            # Behold kun det vi trenger
            df = df[['Matvare', 'Matvaregruppe', 'Karbo_g']]
            
            # Sikre at karbo er tall (0 hvis tomt)
            df['Karbo_g'] = pd.to_numeric(df['Karbo_g'], errors='coerce').fillna(0)
            
            return df
        else:
            st.error(f"Fant ikke 'Matvare' og 'Karbohydrat'. Fant disse: {df.columns.tolist()}")
            return None

    except FileNotFoundError:
        st.warning("⚠️ Finner ikke 'matvarer.xlsx'. Last opp filen til GitHub.")
        return None
    except Exception as e:
        st.error(f"Noe gikk galt: {e}")
        return None

df = last_data()

# --- APP UI ---
if df is not None:
    # 1. KATEGORI-VELGER
    unike_kategorier = sorted(df['Matvaregruppe'].astype(str).unique())
    valgt_kategori = st.selectbox("Velg kategori:", ["Alle"] + unike_kategorier)

    if valgt_kategori != "Alle":
        df_visning = df[df['Matvaregruppe'] == valgt_kategori]
    else:
        df_visning = df

    st.subheader("🔍 Finn matvare")

    # 2. SØKEFELT
    matvarer = sorted(df_visning['Matvare'].astype(str).unique())
    valgt_mat = st.selectbox("Søk:", matvarer)

    if valgt_mat:
        # Hent data for valgt vare
        rad = df[df['Matvare'] == valgt_mat].iloc[0]
        karbo_100 = rad['Karbo_g']

        # 3. KALKULATOR
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Karbo pr 100g", f"{karbo_100:.1f}")
        with c2:
            mengde = st.number_input("Mengde (g):", value=100, step=10)
        
        tot_mat = (mengde / 100) * karbo_100

        # 4. BBQ-MODUS
        st.markdown("---")
        with st.expander("🔥 BBQ & Saus"):
            bbq_aktiv = st.checkbox("Legg til glaze/saus")
            tot_saus = 0
            if bbq_aktiv:
                g_saus = st.slider("Gram saus:", 0, 150, 20)
                tot_saus = (g_saus / 100) * 35 # Antar 35g kh/100g
                st.caption(f"+ {tot_saus:.1f} g karbo fra saus")
        
        # 5. RESULTAT TIL PUMPA
        total = tot_mat + tot_saus
        st.markdown("---")
        st.subheader("Til Pumpa (KH):")
        st.title(f"{total:.1f} g")
