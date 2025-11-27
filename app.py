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
        df = pd.read_excel("matvarer.xlsx")
        
        # 1. RENSK OPP I KOLONNENAVN
        df.columns = [str(c).lower().strip() for c in df.columns]

        # 2. IDENTIFISER VIKTIGE KOLONNER
        navn_col = next((c for c in df.columns if "matvare" in c and "id" not in c), None)
        karbo_col = next((c for c in df.columns if "karbo" in c), None)
        gruppe_col = next((c for c in df.columns if "kategori" in c or "gruppe" in c), None)

        if navn_col and karbo_col and gruppe_col:
            df = df[[navn_col, gruppe_col, karbo_col]].copy()
            df.columns = ['Matvare', 'Matvaregruppe', 'Karbo_g']
            df['Matvaregruppe'] = df['Matvaregruppe'].fillna("Diverse")
            df['Karbo_g'] = pd.to_numeric(df['Karbo_g'], errors='coerce').fillna(0)
            return df
        else:
            st.error("Fant ikke kolonner: Matvare, Karbohydrat, Kategori")
            return None

    except FileNotFoundError:
        st.warning("⚠️ Finner ikke 'matvarer.xlsx'.")
        return None
    except Exception as e:
        st.error(f"Feil: {e}")
        return None

df = last_data()

# --- BRUKERGRENSESNITT ---
if df is not None:
    # 1. KATEGORI-FILTER
    unike_kat = sorted([str(k) for k in df['Matvaregruppe'].unique() if k is not None])
    valgt_kat = st.selectbox("Filtrer på kategori (valgfritt):", ["Alle"] + unike_kat)

    if valgt_kat != "Alle":
        df_visning = df[df['Matvaregruppe'] == valgt_kat]
    else:
        df_visning = df

    st.subheader("🔍 Finn matvare")

    # 2. SØKEFELT (Nå med tomt startfelt!)
    matvarer = sorted(df_visning['Matvare'].astype(str).unique())
    
    valgt_mat = st.selectbox(
        "Søk etter matvare:", 
        matvarer, 
        index=None,  # <-- HER ER MAGIEN: Ingen matvare valgt ved start
        placeholder="Skriv for å søke..." 
    )

    # 3. VIS RESULTAT (Kun hvis noe er valgt)
    if valgt_mat:
        rad = df[df['Matvare'] == valgt_mat].iloc[0]
        karbo_100 = rad['Karbo_g']
        kategori_navn = rad['Matvaregruppe']

        # Vis hvilken kategori denne varen faktisk tilhører
        st.info(f"📁 Kategori: {kategori_navn}")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Karbo pr 100g", f"{karbo_100:.1f}")
        with c2:
            mengde = st.number_input("Mengde (g):", value=100, step=10)
        
        tot_mat = (mengde / 100) * karbo_100

        # BBQ
        st.markdown("---")
        with st.expander("🔥 BBQ & Saus"):
            bbq = st.checkbox("Legg til saus/glaze")
            tot_saus = 0
            if bbq:
                g_saus = st.slider("Gram saus:", 0, 150, 20)
                tot_saus = (g_saus/100)*35
                st.caption(f"+ {tot_saus:.1f} g karbo")
        
        # TOTAL
        total = tot_mat + tot_saus
        st.markdown("---")
        st.subheader("Til Pumpa (KH):")
        st.title(f"{total:.1f} g")
        
    else:
        # Hva vises når ingenting er valgt?
        st.markdown("---")
        st.markdown("👈 *Velg en matvare over for å starte beregningen.*")
