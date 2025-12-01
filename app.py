import streamlit as st
import pandas as pd
import requests
import re

# --- KONFIGURASJON ---
st.set_page_config(page_title="Karbo-Robot", page_icon="🍖")

# --- DIN API NØKKEL ---
# HUSK: Bytt ut teksten under med din nye nøkkel fra Kassalapp.no!
API_KEY = "x2Y4R0b7NwDZpB19DRlljFlUFQmaT9aMgbzOrN8L"

# --- INITIALISER HUKOMMELSE ---
if 'kurv' not in st.session_state:
    st.session_state['kurv'] = []

# --- DETEKTIV ---
def finn_antall_i_tekst(beskrivelse):
    if not beskrivelse: return None
    tekst = beskrivelse.lower()
    treff_tall = re.search(r'(\d+)\s*(stk|stykk|pølser|pk)', tekst)
    if treff_tall: return int(treff_tall.group(1))
    tall_ord = {"en": 1, "et": 1, "to": 2, "tre": 3, "fire": 4, "fem": 5, "seks": 6, "sju": 7, "syv": 7, "åtte": 8, "ni": 9, "ti": 10}
    for ord, tall in tall_ord.items():
        if f"{ord} stk" in tekst or f"{ord} pølser" in tekst or f"{ord} i pakken" in tekst:
            return tall
    return None

# --- API SØK ---
@st.cache_data(show_spinner=False) 
def sok_kassalapp(sokeord):
    url = "https://kassal.app/api/v1/products"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"search": sokeord, "size": 50}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except: return []

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Innstillinger")
    if st.button("🗑️ Tøm kurv"):
        st.session_state['kurv'] = []
        st.rerun()
    
    st.markdown("---")
    st.header("💬 Kontakt")
    st.write("Fant du en feil eller har et ønske?")
    st.link_button("✍️ Send tilbakemelding", "https://forms.gle/xn1RnNAgcr1frzhr8")
    
    st.markdown("---")
    with st.expander("ℹ️ Om dataene"):
        st.markdown("""
        **Kilder:**
        * 🌐 Kassalapp.no (Produktsøk)
        * 🔥 Egne BBQ-beregninger
        
        *Laget for insulinpumper.*
        """)
        
    st.info("Tips: Nett-søket husker nå hva du fant, så appen jobber raskere!")

# --- UI START ---
st.title("🤖 Karbo-Robot")
st.caption("Søk i tusenvis av norske dagligvarer via Kassalapp.no")

if st.session_state['kurv']:
    tot_karbo = sum(i['karbo'] for i in st.session_state['kurv'])
    st.info(f"🛒 I kurven: **{len(st.session_state['kurv'])}** varer. Totalt: **{tot_karbo:.1f} g**")

# --- SØKEFELT ---
col_sok, col_x = st.columns([6, 1])
with col_sok:
    nett_sok = st.text_input("Søk etter noe (f.eks 'Gilde pølse'):", key="input_nett_sok", label_visibility="collapsed", placeholder="Søk her...")
with col_x:
    def slett_sok(): st.session_state.input_nett_sok = ""
    st.button("❌", on_click=slett_sok, help="Tøm søkefeltet")

st.caption("💡 Tips: Får du få treff? Prøv entall (f.eks 'pølse') og færre ord.")

if nett_sok:
    resultater = sok_kassalapp(nett_sok)
    if not resultater:
        st.warning("Fant ingen varer. Prøv et annet ord.")
    else:
        st.success(f"Fant {len(resultater)} produkter!")
        valg_liste = {}
        for i, p in enumerate(resultater):
            navn = p['name']
            vendor = p.get('vendor', '')
            ean = p.get('ean', str(i))
            visningsnavn = f"{i+1}. {navn} ({vendor}) {ean}"
            valg_liste[visningsnavn] = p

        valgt_nettvare_navn = st.selectbox("Velg produkt:", list(valg_liste.keys()), index=None)
        
        if valgt_nettvare_navn:
            produkt = valg_liste[valgt_nettvare_navn]
            navn = produkt['name']
            beskrivelse = produkt.get('description', '')
            ean_id = produkt.get('ean', 'ukjent')

            nutr = produkt.get('nutrition', [])
            karbo_api = 0
            found_nutrition = False
            mulige_koder = ['carbohydrates', 'carbohydrate', 'karbohydrater', 'karbohydrat']
            for n in nutr:
                if n.get('code', '').lower() in mulige_koder:
                    karbo_api = n.get('amount', 0)
                    found_nutrition = True
                    break
            vekt_api = produkt.get('weight', 0)
            antall_funnet = finn_antall_i_tekst(beskrivelse)
            if not antall_funnet: antall_funnet = finn_antall_i_tekst(navn)

            c_img, c_info = st.columns([1, 3])
            with c_img:
                if produkt.get('image'): st.image(produkt['image'], width=100)
            with c_info:
                st.subheader(navn)
                if found_nutrition: st.write(f"📊 **Karbo:** {karbo_api}g per 100g")
                else: st.error("⚠️ Fant ingen karbo-data!")
                if vekt_api: st.write(f"⚖️ **Vekt:** {vekt_api}g")
                if antall_funnet: st.success(f"🕵️ Fant antall i pakken: **{antall_funnet} stk**")
            
            # --- ENDRET HER: expanded=False ---
            with st.expander("🛠️ Se rådata (Teknisk info)"):
                st.json(produkt, expanded=False)
            
            st.markdown("---")
            
            c_kalk1, c_kalk2 = st.columns(2)
            mengde_nett = 0
            beskrivelse_nett = ""
            
            with c_kalk1:
                valg_type = st.radio("Regnemåte:", ["Gram", "Hele pakken/Stk"], horizontal=True, key=f"radio_{ean_id}")
                
                if valg_type == "Gram":
                    mengde_nett = st.number_input("Antall gram:", min_value=0, value=100, step=10, key=f"gram_{ean_id}")
                    beskrivelse_nett = f"{mengde_nett} g"
                else:
                    start_vekt = float(vekt_api) if vekt_api else 0.0
                    start_antall = int(antall_funnet) if antall_funnet else 1
                    
                    if start_vekt > 0 and start_antall > 1:
                        tekst_expander = "📝 Endre vekt/antall? (Klikk her)"
                        open_expander = False
                    else:
                        tekst_expander = "📝 Fyll inn pakkeinfo (Viktig!)"
                        open_expander = True

                    with st.expander(tekst_expander, expanded=open_expander):
                        pk_vekt = st.number_input("Totalvekt (g):", value=start_vekt, step=1.0, key=f"vekt_{ean_id}")
                        pk_ant = st.number_input("Antall i pakke:", min_value=1, value=start_antall, key=f"ant_{ean_id}")
                    
                    if pk_vekt and pk_ant:
                        enhet_vekt = pk_vekt / pk_ant
                        st.info(f"👉 1 stk veier ca **{enhet_vekt:.0f} g**")
                        
                        if enhet_vekt > 150:
                            st.warning(f"⚠️ {enhet_vekt:.0f}g pr stk? Det var mye! Sjekk 'Antall i pakke'.")
                        
                        ant_spist = st.number_input("Antall du spiser:", 1.0, step=0.5, key=f"spist_{ean_id}")
                        mengde_nett = ant_spist * enhet_vekt
                        beskrivelse_nett = f"{ant_spist} stk ({navn})"

            with c_kalk2:
                bbq_nett = st.checkbox("Saus/Glaze?", key=f"bbq_{ean_id}")
                tillegg_nett = 0
                if bbq_nett:
                    g_saus = st.slider("Saus (g):", 0, 150, 20, key=f"slider_{ean_id}")
                    tillegg_nett = (g_saus/100)*35
                    beskrivelse_nett += " + saus"

            tot_nett = (mengde_nett/100)*karbo_api + tillegg_nett
            st.write(f"### = {tot_nett:.1f} g karbo")
            
            if st.button("➕ Legg til i måltid", key=f"btn_{ean_id}"):
                st.session_state['kurv'].append({"navn": navn, "beskrivelse": beskrivelse_nett, "karbo": tot_nett})
                st.success("Lagt til!")

# --- KURV ---
st.markdown("---")
st.header("🍽️ Dagens Måltid")

if st.session_state['kurv']:
    h1, h2, h3, h4 = st.columns([3, 4, 2, 1])
    h1.caption("Navn")
    h2.caption("Beskrivelse")
    h3.caption("Karbo")
    h4.caption("Slett")

    # Sjekk om vi har brødmat
    har_brødmat = False
    brød_ord = ['brød', 'knekkebrød', 'rundstykke', 'lompe', 'baguett', 'ciabatta', 'polarbrød', 'skive']
    for ting in st.session_state['kurv']:
        if any(b in ting['navn'].lower() for b in brød_ord):
            har_brødmat = True

    if har_brødmat:
        st.info("""
        **🍞 Huskeregel for pålegg:**
        * 🧀 Ost, kjøtt, egg, fisk = **0 karbo**.
        * 🍓 Syltetøy, brunost, prim, sjoko = **Må telles!**
        """)

    for i, item in enumerate(st.session_state['kurv']):
        c1, c2, c3, c4 = st.columns([3, 4, 2, 1])
        with c1: st.write(item['navn'])
        with c2: st.write(item['beskrivelse'])
        with c3: st.write(f"{item['karbo']:.1f}")
        with c4:
            if st.button("❌", key=f"slett_{i}"):
                st.session_state['kurv'].pop(i)
                st.rerun()

    total_sum = sum(item['karbo'] for item in st.session_state['kurv'])
    st.markdown("---")
    col_res1, col_res2 = st.columns([2, 1])
    with col_res1:
        st.subheader("Totalt til Pumpa:")
    with col_res2:
        st.title(f"{total_sum:.1f} g")
    
    if st.button("🗑️ Tøm hele kurven", key="tom_bunn"):
        st.session_state['kurv'] = []
        st.rerun()
else:
    st.caption("Kurven er tom.")
