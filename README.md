# 🤖 Karbo-Robot

**Din smarte assistent for karbohydrattelling – søk direkte i norske dagligvarer.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]https://karbo-robot-scqkaigsbowcy87ijqczdy.streamlit.app/

## 📖 Hva er dette?
Karbo-Robot er en rask web-app utviklet for å gjøre hverdagen enklere for oss med diabetes type 1 (spesielt tilpasset insulinpumper som MiniMed 780G, Tandem eller Omnipod).

I stedet for å gjette, søker denne roboten direkte i databasen til **Kassalapp.no** for å finne karbohydratinnhold på varene du kjøper i butikken.

## ✨ Nøkkelfunksjoner

### 1. 🌐 Smart Produktsøk
Søk på "Gilde Grillpølse" eller "Wasa", og appen henter:
* Næringsinnhold direkte fra butikkhyllene.
* **Tekst-detektiv:** Appen leser produktbeskrivelsen og finner automatisk ut hvor mange pølser/brød det er i pakken (f.eks. "6 stk").

### 2. 🌭 "Pølse-matematikk"
Slutt å regne i hodet. Appen vet at du ikke spiser "120g pølse", men "2 stk".
* Den regner om fra *Totalvekt* og *Antall i pakke* til **karbohydrater per stykk**.

### 3. 🧀 Smarte Tips
* **Påleggs-hjelper:** Legger du til brød eller knekkebrød? Appen gir deg en huskeregel på hvilke pålegg som har karbohydrater (brunost, syltetøy) og hvilke som er "gratis" (ost, skinke).

### 4. 🛒 Måltidskurv
Sett sammen hele middagen:
* Legg til pølser + brød + potetsalat.
* Få **én totalsum** nederst som du taster rett inn i pumpa.

### 5. 🔥 BBQ-Modus
For oss som er glad i grillmat! Egen knapp for å legge til standard BBQ-tillegg (glaze/rub) på kjøtt.

## ℹ️ Datakilder
* **Produktsøk:** [Kassalapp.no](https://kassalapp.no) sitt API.
* **Logikk:** Egne beregninger for stykk-vekt og BBQ-tillegg.

## ⚠️ Ansvarsfraskrivelse
Dette verktøyet er utviklet som et privat hjelpemiddel ("Open Source").
* Appen er et supplement til egen kunnskap.
* **Sjekk alltid emballasjen** hvis du er usikker – produsenter kan endre innhold.
* Utvikler tar ikke ansvar for eventuelle feilberegninger eller medisinsk dosering.

## 🛠️ Teknisk info
Laget med Python og [Streamlit](https://streamlit.io).

---
*Laget for en enklere hverdag med insulinpumpe.*
