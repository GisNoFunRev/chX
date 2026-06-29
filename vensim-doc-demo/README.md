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
- fachliche Zusatzdokumentation aus `docs/variable_documentation.csv`: Zweck, Modelllogik, Annahme, Quelle, Kalibrierung und Interpretation
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

Wenn nur die CSV-Dokumentation angepasst wurde:

```bash
python scripts/build_search_assets.py
quarto render
```

Das Script verwendet vorhandene SVG-Grafiken wieder und ist deshalb schnell.

Wenn sich die Modellstruktur geändert hat und alle Dependency-Grafiken neu erzeugt werden sollen:

```bash
python scripts/build_search_assets.py --regenerate-graphs
quarto render
```

## Variablen-Dokumentation als CSV erzeugen

Aus dem Projektroot:

```bash
python scripts/export_variable_documentation_template.py
```

Das erzeugt oder aktualisiert:

```text
docs/variable_documentation.csv
```

Die technischen Spalten werden automatisch aus dem Vensim-Modell gefüllt. Bereits manuell ausgefüllte Felder wie `purpose`, `logic`, `assumption`, `source`, `calibration`, `interpretation` und `status` bleiben bei erneutem Export erhalten.

Wichtige manuelle Felder:

```text
priority,purpose,logic,assumption,source,calibration,interpretation,status
```

Optional:

```bash
python scripts/export_variable_documentation_template.py --include-controls
python scripts/export_variable_documentation_template.py --model data/AnderesModell.mdl
python scripts/export_variable_documentation_template.py --output docs/meine_doku.csv
```
