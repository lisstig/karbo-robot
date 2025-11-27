# 🤖 Karbo-Robot

**Din smarte assistent for karbohydrattelling – tilpasset norske matvarer.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://[LIM INN LINKEN DIN HER])

## 📖 Hva er dette?
Karbo-Robot er en enkel, reklamefri web-app utviklet for å gjøre hverdagen litt enklere for oss med diabetes type 1 (og spesielt for deg med insulinpumpe som MiniMed 780G, Tandem eller Omnipod).

Målet er å fjerne gjettingen fra måltidene. Appen fokuserer på norske merkevarer (Gilde, Hatting, Tine) og lar deg beregne nøyaktig karbohydratinnhold på sekunder.

## ✨ Hvorfor bruke Karbo-Robot?

I motsetning til utenlandske apper eller generelle tabeller, løser denne de "norske" problemene:

* **🌭 "Pølse-matematikk":** Vet nøyaktig hva en Gilde Grillpølse eller et Hatting pølsebrød veier. Du velger antall stk, appen regner gram.
* **🔢 Pakke-kalkulator:** Har du en vare som mangler i listen? Skriv inn totalvekt og antall i pakken, så regner appen ut stykk-vekten for deg der og da.
* **🍽️ Måltidskurv:** Legg til pølser, brød, potetsalat og drikke i samme "kurv" og få én totalsum du kan taste rett inn i pumpa.
* **🔥 BBQ-Modus:** En egen funksjon for oss som er glad i grillmat! Hjelper deg å huske karbohydratene i glaze, rub og saus.

## 🚀 Slik bruker du den
1.  Åpne [appen](https://karbo-robot-scqkaigsbowcy87ijqczdy.streamlit.app/).
2.  **Søk** etter matvaren (f.eks. "Karbonade").
3.  Velg om du vil regne i **Gram** eller **Stk**.
4.  Trykk **"Legg til i måltidet"**.
5.  Se totalen nederst og tast inn i pumpa. 💉

## ℹ️ Datakilder
Vi gjetter ikke på helsa di. Dataene er hentet fra troverdige kilder:
* **Næringsinnhold:** [Matvaretabellen.no](https://www.matvaretabellen.no) (Mattilsynet).
* **Vekt/Mengde:** "Mål og vekt for matvarer" (Mattilsynet/UiO) samt produsentinformasjon fra emballasje.

## ⚠️ Ansvarsfraskrivelse (Disclaimer)
Dette verktøyet er utviklet som et privat hjelpemiddel og deles "som det er" (open source).
* Appen er et supplement til egen kunnskap.
* Sjekk alltid emballasjen på varen hvis du er usikker, da produsenter kan endre innhold.
* Utvikler tar ikke ansvar for eventuelle feilberegninger eller medisinsk dosering.

## 🛠️ For utviklere
Vil du kjøre denne lokalt eller bidra?
Koden er skrevet i Python ved hjelp av [Streamlit](https://karbo-robot-scqkaigsbowcy87ijqczdy.streamlit.app/).

1.  Klone repoet:
    ```bash
    git clone [https://github.com/lisstig/karbo-robot.git](https://github.com/lisstig/karbo-robot.git)
    ```
2.  Installer avhengigheter:
    ```bash
    pip install -r requirements.txt
    ```
3.  Kjør appen:
    ```bash
    streamlit run app.py
    ```

---
*Laget med ❤️ (og litt insulin) av [lisstig](https://github.com/lisstig)*
