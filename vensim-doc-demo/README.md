# Vensim Variablensuche fuer Quarto

Dieser POC enthaelt nur die statische HTML-Suchfunktion fuer die automatische Vensim-Modelldokumentation.

## Inhalt

```text
assets/
  model_search_data.js      # vorberechnete Variablendaten und SVG-Grafiken
  variable_search.css       # Styling der Suche
  variable_search.js        # Such- und Anzeige-Logik
data/
  DiamondDuckTheClean.mdl
libs/
models/
scripts/
  build_search_assets.py    # Suchdaten bei Modellaenderungen neu generieren
index.qmd
_quarto.yml
requirements.txt
```

## Funktionen

- Suche nur nach Variablennamen
- Auswahl einer Fokusvariable
- Filter nach Variablentyp und View
- Grafik als erster Block
- Einheiten und Typ
- Dokumentation aus Vensim-Kommentaren
- Gleichung aus der `.mdl`-Datei
- verbundene Variablen getrennt nach Input und Output
- View-Zuordnung
- technische Steuergrössen wie `INITIAL TIME`, `FINAL TIME`, `TIME STEP` und `SAVEPER` werden in der Suche ausgeblendet

## Rendern

```bash
pip install -r requirements.txt
brew install graphviz
quarto render
```

Auf Ubuntu/Debian:

```bash
sudo apt-get install graphviz
```

## Suchdaten neu erzeugen

Wenn das Vensim-Modell angepasst wurde:

```bash
python scripts/build_search_assets.py
quarto render
```
