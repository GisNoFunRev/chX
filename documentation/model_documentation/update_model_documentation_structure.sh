#!/usr/bin/env bash
set -euo pipefail

# Run this from:
# /home/alexis/Projects/FHNW/chX/documentation/model_documentation

python - <<'PY'
from pathlib import Path

# 1) Appendix as a normal final chapter, not inside Quarto appendices block
Path("appendix/A-vensim-gleichungsliste.qmd").write_text("""# Appendix A – vollständige Vensim-Gleichungsliste {.unnumbered}

Dieser Anhang enthält später die vollständige technische Gleichungsliste des finalen Vensim-Modells.

Die Gleichungsliste wird nach Abschluss des Modells aus Vensim exportiert und hier eingefügt.

## Dokumentationsschema

Für jede Variable werden dokumentiert:

- Variablenname
- Typ
- Gleichung
- Einheit
- Initialwert
- Parameterwert
- Quelle oder Begründung
- Rolle im Modell
- Hinweise und Grenzen

## Platzhalter

```text
Die vollständige Vensim-Gleichungsliste wird hier eingefügt.
```
""", encoding="utf-8")

# 2) References remain the formal bibliography page
Path("sections/14-references.qmd").write_text("""# References – Literaturverzeichnis {.unnumbered}

::: {#refs}
:::
""", encoding="utf-8")

# 3) _quarto.yml without a separate appendices block
Path("_quarto.yml").write_text("""project:
  type: book

book:
  title: "Dokumentation des Vensim-Systemdynamikmodells"
  author: "Alexis Boser Makaratzis"
  date: today

  sidebar:
    collapse-level: 2

  chapters:
    - index.qmd
    - sections/01-systemarchitektur.qmd
    - sections/02-dokumentation-struktur-beziehung-cld.qmd
    - sections/03-zweck-und-modellfrage.qmd
    - sections/04-modellgrenze.qmd
    - sections/05-gesamtstruktur.qmd
    - sections/06-theoretical-empirical-basis.qmd
    - sections/06-land-stocks-und-conversion.qmd
    - sections/07-alonso-muth-mills-amm.qmd
    - sections/08-cobb-douglas-untermodell.qmd
    - sections/09-parameter-startwerte-quellen.qmd
    - sections/10-kalibrierung-plausibilitaet.qmd
    - sections/11-simulation-runs-szenarien.qmd
    - sections/12-sensitivitaetsanalyse.qmd
    - sections/13-grenzen-des-modells.qmd
    - appendix/A-vensim-gleichungsliste.qmd
    - sections/14-references.qmd

bibliography: references.bib

format:
  html:
    theme: cosmo
    css: styles.css
    toc: true
    toc-depth: 4
    number-sections: true
    number-depth: 4

  pdf:
    documentclass: scrreprt
    toc: true
    toc-depth: 4
    number-sections: true
    number-depth: 4
""", encoding="utf-8")

print("OK: _quarto.yml, Appendix A und References wurden aktualisiert.")
PY

rm -rf .quarto _book
quarto render
