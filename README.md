# 🤖 Karbo-Robot

**Din smarte assistent for karbohydrattelling – søk direkte i norske dagligvarer.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://[LIM INN LINKEN TIL APPEN DIN HER])

## 📖 Hva er dette?
Karbo-Robot er en rask og enkel web-app utviklet for å gjøre hverdagen enklere for oss med diabetes type 1 (spesielt tilpasset insulinpumper som MiniMed 780G, Tandem eller Omnipod).

I stedet for å gjette eller slå opp i tabeller, søker denne roboten direkte i databasen til **Kassalapp.no** for å finne næringsinnhold på varene du kjøper i butikken.

## ✨ Nøkkelfunksjoner

### 1. 🌐 Smart Produktsøk
Søk på "Gilde Grillpølse" eller "Hatting", og appen henter:
* Næringsinnhold (karbohydrater per 100g).
* Bilde av produktet så du vet du har valgt riktig.
* **Tekst-detektiv:** Appen leser produktbeskrivelsen og prøver automatisk å finne ut hvor mange pølser/brød det er i pakken (f.eks. "6 stk").

### 2. 🌭 "Pølse-matematikk"
Slutt å regne i hodet. Appen vet at du ikke spiser "120g pølse", men "2 stk".
* Den regner om fra *Totalvekt* og *Antall i pakke* til **karbohydrater per stykk**.
* Du kan enkelt justere vekten eller antallet hvis roboten gjetter feil.

### 3. 🛒 Måltidskurv
Sett sammen hele middagen:
* Legg til 2 pølser + 2 brød + potetsalat.
* Få **én totalsum** nederst som du taster rett inn i pumpa.
* Slett-knapp (❌) hvis du angrer.

### 4. 🔥 BBQ-Modus
En egen funksjon for oss som er glad i grillmat!
* Kjøtt har 0 karbo, men glaze og rub har sukker.
* Egen knapp for å legge til standard BBQ-tillegg (saus/glaze) slik at insulindosen blir riktig.

## ℹ️ Datakilder
* **Produktsøk & Næringsinnhold:** [Kassalapp.no](https://kassalapp.no) sitt API.
* **Logikk:** Egne beregninger for stykk-vekt og BBQ-tillegg.

## ⚠️ Ansvarsfraskrivelse
Dette verktøyet er utviklet som et privat hjelpemiddel ("Open Source").
* Appen er et supplement til egen kunnskap.
* **Sjekk alltid emballasjen** hvis du er usikker – produsenter kan endre innhold, og databasen kan ha feil.
* Utvikler tar ikke ansvar for eventuelle feilberegninger eller medisinsk dosering.

## 🛠️ Teknisk info
Laget med Python og [Streamlit](https://streamlit.io).

---
*Laget for en enklere hverdag med insulinpumpe.*
