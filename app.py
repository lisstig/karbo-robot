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
