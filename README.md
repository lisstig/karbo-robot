<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Karbohydratkalkulator og Insulinberegner</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/brython@3.9.5/brython.min.js"></script>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/brython@3.9.5/brython_stdlib.js"></script>
    <style>
        body {
            font-size: 20px;
            padding: 20px;
        }
        input, button {
            font-size: 20px;
            padding: 10px;
            margin: 5px;
        }
        .resultat {
            font-weight: bold;
        }
    </style>
</head>
<body onload="brython()">
    <h2>Karbohydratkalkulator og Insulinberegner</h2>
    <p>Karbohydrater per 100g: <input type="number" id="karbohydrater"></p>
    <p>Vekt (i gram): <input type="number" id="vekt"></p>
    <button id="beregn">Beregn Karbohydrater</button>
    <p id="karbohydrat_resultat" class="resultat"></p>

    <p>Total døgndose insulin (E): <input type="number" id="insulin"></p>
    <button id="beregn_insulin">Beregn Insulin-faktor</button>
    <p id="insulin_resultat" class="resultat"></p>

    <p>Insulin-karbohydratfaktoren forteller deg hvor mange gram karbohydrater én enhet insulin dekker.</p>
    <p>Den beregnes ved å dele 500 på din totale døgndose med insulin.</p>
    <p>Eksempel: Hvis du bruker 50 enheter insulin i døgnet, blir regnestykket 500 / 50 = 10.</p>
    <p>Dette betyr at 1 enhet insulin dekker 10 gram karbohydrater.</p>
    <p id="insulin_advarsel"><b></b></p>

    <button id="nullstill">Nullstill</button>

    <script type="text/python">
from browser import document, alert

def beregn_karbohydrater(ev):
    try:
        karbohydrater = float(document['karbohydrater'].value)
        vekt = float(document['vekt'].value)
        total_karbohydrater = int((karbohydrater / 100) * vekt) # Fjerner desimaler
        document['karbohydrat_resultat'].text = f"Matvaren inneholder totalt {total_karbohydrater} gram karbohydrater."
    except ValueError:
        document['karbohydrat_resultat'].text = "Ugyldig input. Vennligst skriv inn tall."

def beregn_insulin(ev):
    try:
        total_insulin = float(document['insulin'].value)
        if total_insulin == 0:
            document['insulin_resultat'].text = "Døgndosen insulin kan ikke være null."
            return
        insulin_faktor = int(500 / total_insulin) # Fjerner desimaler
        document['insulin_resultat'].text = f"Insulin-karbohydratfaktoren din er {insulin_faktor} gram per enhet insulin."
    except ValueError:
        document['insulin_resultat'].text = "Ugyldig input for døgndose insulin."

def nullstill(ev):
    document['karbohydrater'].value = ""
    document['vekt'].value = ""
    document['karbohydrat_resultat'].text = ""
    document['insulin'].value = ""
    document['insulin_resultat'].text = ""
    document['insulin_advarsel'].text = ""

document['beregn'].bind('click', beregn_karbohydrater)
document['beregn_insulin'].bind('click', beregn_insulin)
document['nullstill'].bind('click', nullstill)
    </script>
</body>
</html>
