# 🤖 Karbo-Robot

**Din smarte assistent for karbohydrattelling – nå med produktsøk i sanntid!**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://[LIM INN LINKEN TIL APPEN DIN HER])

## 📖 Hva er dette?
Karbo-Robot er en web-app utviklet for å gjøre hverdagen enklere for oss med diabetes type 1 (spesielt tilpasset insulinpumper som MiniMed 780G, Tandem eller Omnipod).

Appen løser problemet med å "gjette" karbohydrater ved å kombinere dine egne favoritter med et **direkte søk i norske dagligvarer**.

## ✨ Nøkkelfunksjoner

### 1. 🌐 Smart Produktsøk (Nyhet!)
Koblet direkte mot **Kassalapp API**. Søk på "Gilde Grillpølse" eller "Hatting", og appen henter:
* Næringsinnhold direkte fra butikkhyllene.
* Totalvekt på pakken.
* **Tekst-detektiv:** Appen leser produktbeskrivelsen og finner automatisk ut hvor mange pølser/brød det er i pakken (f.eks. "6 stk").

### 2. 🌭 "Pølse-matematikk"
Slutt å regne i hodet. Appen vet at du ikke spiser "100g pølse", men "2 pølser".
* Den regner om fra *Totalvekt* og *Antall i pakke* til **karbohydrater per stykk**.

### 3. 🔥 BBQ-Modus
For oss som er glad i røyking av kjøtt og grilling!
* Kjøtt har 0 karbo, men glaze og rub har sukker.
* Egen knapp for å legge til standard BBQ-tillegg (saus/glaze) slik at insulindosen blir riktig.

### 4. 🛒 Måltidskurv
Sett sammen hele middagen:
* Legg til 2 pølser + 2 brød + potetsalat.
* Få **én totalsum** nederst som du taster rett inn i pumpa.
* Slett-knapp hvis du angrer.

### 5. 📂 Mine Spesialiteter (Excel)
En egen fane for dine unike matvarer som ikke finnes i butikken (hjemmelaget mat, spesielle oppskrifter).

## ℹ️ Datakilder
Vi baserer oss på troverdige kilder:
* **Internett-søk:** [Kassalapp.no](https://kassalapp.no) (Norske dagligvarer).
* **Grunndata:** [Matvaretabellen.no](https://www.matvaretabellen.no) (Mattilsynet).
* **Logikk:** Egne beregninger for stykk-vekt og BBQ.

## ⚠️ Ansvarsfraskrivelse
Dette verktøyet er utviklet som et privat hjelpemiddel ("Open Source").
* Appen er et supplement til egen kunnskap.
* Sjekk alltid emballasjen hvis du er usikker – produsenter kan endre innhold.
* Utvikler tar ikke ansvar for eventuelle feilberegninger eller medisinsk dosering.

## 🛠️ Teknisk info
Laget med Python og [Streamlit](https://streamlit.io).
Bruker `pandas` for databehandling, `requests` for API-kall og `regex` for tekstanalyse.

---
*Laget for en enklere hverdag med MiniMed 780G.*
