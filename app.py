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
        # Prøver å lese Excel-filen
        df = pd.read_excel("matvarer.xlsx")
        
        # Vi må rydde litt i kolonnenavnene siden Matvaretabellen kan variere
        # Vi ser etter en kolonne som heter noe med "Karbohydrat"
        alle_kolonner = df.columns.tolist()
        karbo_kolonne = next((k for k in alle_kolonner if "Karbohydrat" in k), None)
        
        if karbo_kolonne:
            # Lager en forenklet versjon av tabellen med bare det vi trenger
            df = df[['Matvare', 'Matvaregruppe', karbo_kolonne]].copy()
            df.rename(columns={karbo_kolonne: 'Karbo_g'}, inplace=True)
            return df
        else:
            st.error("Fant ingen kolonne med 'Karbohydrat' i Excel-filen.")
            return None
            
    except FileNotFoundError:
        st.warning("⚠️ Finner ikke 'matvarer.xlsx'. Har du lastet den opp?")
        # Fallback-data (så appen ikke kræsjer før du får lastet opp filen)
        data = {
            'Matvare': ['Test-pølse (mangler fil)', 'Test-brød (mangler fil)'],
            'Matvaregruppe': ['Kjøtt', 'Brødmat'],
            'Karbo_g': [5, 45]
        }
        return pd.DataFrame(data)

df = last_data()

# --- HOVEDKALKULATOR ---
if df is not None:
    st.subheader("🔍 Finn matvare")

    # 1. Velg Kategori (Filter)
    kategorier = sorted(df['Matvaregruppe'].unique())
    valgt_kategori = st.selectbox("Velg kategori:", options=["Alle"] + kategorier)

    # 2. Filtrer listen basert på kategori
    if valgt_kategori != "Alle":
        filtrert_df = df[df['Matvaregruppe'] == valgt_kategori]
    else:
        filtrert_df = df

    # 3. Velg Matvare (Søkbar liste)
    matvarer = sorted(filtrert_df['Matvare'].unique())
    valgt_mat_navn = st.selectbox("Søk etter matvare:", options=matvarer)

    # Hent karbo-tallet
    rad = df[df['Matvare'] == valgt_mat_navn].iloc[0]
    karbo_per_100 = rad['Karbo_g']

    # --- BEREGNING ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Karbo per 100g", f"{karbo_per_100:.1f} g")
    
    with col2:
        mengde = st.number_input("Mengde (gram):", min_value=0, value=100, step=10)
    
    mat_karbo = (mengde / 100) * karbo_per_100

    # --- BBQ-MODUS (Beholdes selvfølgelig!) ---
    st.markdown("---")
    with st.expander("🔥 BBQ & Saus-tillegg"):
        st.write("For oss som røyker maten: Husk glaze og rub!")
        bbq_tillegg = st.checkbox("Legg til saus/glaze?")
        
        tillegg_karbo = 0
        if bbq_tillegg:
            saus_mengde = st.slider("Mengde saus (gram)", 0, 100, 20)
            tillegg_karbo = (saus_mengde / 100) * 35 # Antar 35g karbo i snitt
            st.caption(f"+ {tillegg_karbo:.1f}g karbo fra saus")

    # --- TOTAL ---
    total = mat_karbo + tillegg_karbo
    
    st.markdown("---")
    st.subheader("Til Pumpa:")
    st.title(f"{total:.1f} g")
