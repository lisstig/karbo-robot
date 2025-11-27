import streamlit as st
import pandas as pd

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

# --- DATA (Mock database - dette bytter vi ut med API senere) ---
# Struktur: Navn, Karbo per 100g, Standard vekt per stykk (hvis aktuelt)
# --- DATA (Utvidet liste for hverdagsmiddager) ---
matvare_data = {
    # --- BASISVARER (Middag) ---
    'Potet (kokt)': {'karbo_100g': 17, 'vekt_stk': 85},
    'Potetmos (hjemmelaget m/melk)': {'karbo_100g': 15, 'vekt_stk': 150}, # En porsjon
    'Pommes Frites (ovnsstekt)': {'karbo_100g': 32, 'vekt_stk': None},
    'Ris, hvit (kokt)': {'karbo_100g': 28, 'vekt_stk': 150}, # En porsjon
    'Pasta/Spaghetti (kokt)': {'karbo_100g': 30, 'vekt_stk': 150}, # En porsjon
    'Søtpotet (bakt)': {'karbo_100g': 20, 'vekt_stk': 150},

    # --- GRØNNSAKER & TILBEHØR ---
    'Gulrot (kokt)': {'karbo_100g': 6.5, 'vekt_stk': 70},
    'Brokkoli/Blomkål': {'karbo_100g': 2, 'vekt_stk': None}, # Veldig lite, men greit å ha
    'Erter (grønne, fryst)': {'karbo_100g': 7, 'vekt_stk': None},
    'Maiskorn (hermetisk)': {'karbo_100g': 16, 'vekt_stk': None},
    'Tyttebærsyltetøy': {'karbo_100g': 40, 'vekt_stk': 20}, # En spiseskje
    'Brun saus (jevnet m/hvetemel)': {'karbo_100g': 6, 'vekt_stk': 50}, # En øse
    'Ketchup': {'karbo_100g': 24, 'vekt_stk': 15},

    # --- BRØD & BAKST ---
    'Brødskive (Grovt/Kneipp)': {'karbo_100g': 40, 'vekt_stk': 40},
    'Knekkebrød (Wasa Husman)': {'karbo_100g': 60, 'vekt_stk': 13},
    'Pølsebrød (Vanlig)': {'karbo_100g': 51, 'vekt_stk': 27},
    'Lompe': {'karbo_100g': 38, 'vekt_stk': 25},
    'Hamburgerbrød (Grovt)': {'karbo_100g': 45, 'vekt_stk': 60},
    'Tortilla (Hvete, medium)': {'karbo_100g': 54, 'vekt_stk': 40},

    # --- KJØTTPRODUKTER (Med karbo) ---
    'Grillpølse (Gilde)': {'karbo_100g': 4.5, 'vekt_stk': 50},
    'Kjøttkaker (Ferdige)': {'karbo_100g': 8, 'vekt_stk': 50},
    'Fiskekaker': {'karbo_100g': 10, 'vekt_stk': 60},
    
    # --- BBQ SPECIALS (Dine favoritter) ---
    'Coleslaw (Ferdigkjøpt)': {'karbo_100g': 10, 'vekt_stk': None},
    'Maiskolbe (kokt)': {'karbo_100g': 18, 'vekt_stk': 200}, # Ca vekt spiselig del
}

# --- TITTEL ---
st.title("🤖 Karbo-Robot")
st.caption("Din smarte karbo-kalkulator")

# --- SIDEBAR: FAVORITTER ---
with st.sidebar:
    st.header("⭐ Mine Favoritter")
    st.write("Her kan du legge hurtigknapper senere.")
    if st.button("Kjapp Frokost (2 brød m/ost)"):
        st.session_state['resultat'] = 30 # Eksempelverdi

# --- HOVEDKALKULATOR ---
st.subheader("🔍 Hva spiser du?")

# 1. Velg matvare
valgt_mat = st.selectbox("Søk etter matvare:", options=list(matvare_data.keys()))

col1, col2 = st.columns(2)

# Hent data for valgt mat
info = matvare_data[valgt_mat]
karbo_per_100 = info['karbo_100g']
standard_vekt = info['vekt_stk']

# 2. Velg mengde (Gram eller Stk)
beregnet_karbo = 0

with col1:
    mode = st.radio("Måleenhet", ["Gram", "Stk/Porsjon"])

with col2:
    if mode == "Gram":
        mengde = st.number_input("Antall gram:", min_value=0, value=100, step=10)
        beregnet_karbo = (mengde / 100) * karbo_per_100
    else:
        if standard_vekt:
            antall = st.number_input(f"Antall stk (ca {standard_vekt}g/stk):", min_value=0.0, value=1.0, step=0.5)
            beregnet_karbo = (antall * standard_vekt / 100) * karbo_per_100
        else:
            st.warning("Ingen stykkvekt registrert for denne varen. Bruk gram.")
            mengde = st.number_input("Antall gram:", min_value=0, value=100)
            beregnet_karbo = (mengde / 100) * karbo_per_100

# --- BBQ-MODUS (Din spesialitet!) ---
st.markdown("---")
st.subheader("🔥 BBQ & Tilbehør")
bbq_tillegg = st.checkbox("Jeg har glaze/rub eller saus på kjøttet")

tillegg_karbo = 0
if bbq_tillegg:
    st.info("Legger til standard BBQ-tillegg (ca 30% sukker i saus)")
    saus_mengde = st.slider("Hvor mye saus/glaze? (gram)", 0, 100, 20)
    # Enkel tommelfingerregel: BBQ saus er ofte ca 30-40g karbo per 100g
    tillegg_karbo = (saus_mengde / 100) * 35 

# --- RESULTAT ---
total_karbo = beregnet_karbo + tillegg_karbo

st.markdown("---")
st.metric(label="Legg inn i pumpa (KH)", value=f"{total_karbo:.1f} g")

if total_karbo > 0:
    st.success(f"Dette består av {beregnet_karbo:.1f}g fra maten og {tillegg_karbo:.1f}g fra saus/glaze.")
