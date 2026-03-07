# 🤖 Karbo-Robot

**Din digitale assistent for karbohydrattelling og insulinberegning.**

Karbo-Robot er utviklet for å gjøre hverdagen enklere for diabetikere og insulinpumpe-brukere. Appen kombinerer et søk i tusenvis av norske dagligvarer med en omfattende database over "tommelfinger-regler" for matvarer uten strekkode.

🔗 **[Klikk her for å åpne appen](https://karbo-robot-scqkaigsbowcy87ijqczdy.streamlit.app)** (Bytt ut med din lenke hvis den er annerledes)

## ✨ Hovedfunksjoner

### 1. 📏 Tommelfinger-regler (Hjertet i appen)
En stor, innebygd database med over 100 vanlige matvarer som ofte spises, men som er vanskelige å skanne (f.eks. en brødskive, en porsjon ris, frukt eller bakst).
* **Kategorisert:** Sortert i grupper som *Middag*, *Brød & Bakst*, *Snacks*, *Drikke* osv.
* **Minikalkulator:** Endre mengde direkte på kortet (f.eks. endre fra "1 glass" til "1.5 glass") og få karbohydratene regnet ut automatisk.
* **Legg til egne:** Du kan opprette midlertidige matvarer i listen hvis du mangler noe.

### 2. 🔍 Butikksøk (Via Kassalapp.no)
Søk i tusenvis av norske dagligvarer for å finne nøyaktig næringsinnhold.
* **Strekkodesøk:** Bruk mobilen til å skanne EAN-koden direkte i søkefeltet.
* **Smart filtrering:** Appen rydder automatisk bort duplikater (f.eks. samme pølse fra 3 forskjellige butikker) for en renere liste.
* **Detaljert info:** Ser karbohydrater per 100g, vekt på varen, og utregning per porsjon.

### 3. 🍽️ Måltidsbygger
Alt du velger (både fra butikksøk og tommelfinger-regler) havner i en felles **"Dagens Måltid"**-kurv nederst.
* Full oversikt over alt du skal spise.
* **Total sum:** Viser nøyaktig hvor mange gram karbohydrater du skal plotte inn i insulinpumpen.

---

## 🛠️ Teknisk info
Appen er bygget med **Python** og **Streamlit**.

* **API:** Bruker [Kassalapp.no](https://kassalapp.no) sitt API for sanntidsdata om dagligvarer.
* **Database:** Inneholder en hardkodet, strukturert database basert på offisielle karbohydrat-lister og erfaringsbaserte data.

## ⚠️ Ansvarsfraskrivelse
*Dette verktøyet er ment som en hjelp i hverdagen. Dobbeltsjekk alltid verdiene mot emballasje eller egne erfaringer ved dosering av insulin.*

---
*Laget med ❤️ for en enklere diabetes-hverdag.*
