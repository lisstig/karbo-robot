import streamlit as st
import pandas as pd

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

# --- DATA (Mock database - dette bytter vi ut med API senere) ---
# Struktur: Navn, Karbo per 100g, Standard vekt per stykk (hvis aktuelt)
matvare_data = {
    'Potet (kokt)': {'karbo_100g': 17, 'vekt_stk': 80},
    'Gilde Grillpølse': {'karbo_100g': 4.5, 'vekt_stk': 50},
    'Pølsebrød (Hatting)': {'karbo_100g': 51, 'vekt_stk': 27},
    'Lompe': {'karbo_100g': 38, 'vekt_stk': 25},
    'Røkt Brisket (uten glaze)': {'karbo_100g': 0, 'vekt_stk': None},
    'Coleslaw (hjemmelaget)': {'karbo_100g': 6, 'vekt_stk': None},
    'Pommes Frites': {'karbo_100g': 35, 'vekt_stk': None},
    'Ketchup': {'karbo_100g': 24, 'vekt_stk': 15},
}

# --- TITTEL ---
st.title("🤖 Karbo-Robot")
st.caption("Din assistent for MiniMed 780G")

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
