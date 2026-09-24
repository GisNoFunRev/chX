# Stage A — Priorisierung der 22 verbliebenen Urban-ABM-Modellfamilien

**Datengrundlage:**
- `european_urban_abm_28_structured_extraction.md`
- `european_urban_abm_11_criteria_gate_screen.md`
- vorhandener Discovery-Corpus zu den 28 Modellfamilien
  
  **Zweck:** Die 22 nach dem ersten Gate-Screen verbliebenen Modellfamilien mit wenigen entscheidenden Kriterien weiter reduzieren.  
  **Wichtig:** In diesem Schritt wurde **keine neue Literaturrecherche** durchgeführt. Unsicherheit wird nicht als Ausschluss gewertet.
- ## Kriterien dieses Schritts
- ### P — Inhaltliche Passung zu Urban Sciences / Lernzielen
  **Priorisierung, kein Hard Gate.**
  
  Relevant sind insbesondere:
- Urban Systems als klarer Gegenstand
- räumliche Modellierung als substanzieller Bestandteil
- sinnvoller Lerngewinn in ABM
  
  Bewertung: **hoch / mittel**
- ### K9 — Grundsätzliche Semester-Machbarkeit
  **Hard Gate.**
  
  Ausschluss nur, wenn die vorhandene Evidenz klar darauf hindeutet, dass selbst eine sinnvolle, wissenschaftlich anschlussfähige Umsetzung den Semesterrahmen durch Modellumfang, Infrastruktur oder Rechenaufwand dominiert.
- ### K8 — Realistische empirische Calibration / Validation
  **Hard Gate; gegenüber der bisherigen Fassung präzisiert.**
  
  Erforderlich ist eine realistische empirische Calibration und eine davon getrennte, möglichst out-of-sample Validation.
  
  Zusätzlich:
- strukturelle Modellschwächen dürfen nicht bloss durch Parameteranpassung kompensiert werden;
- Initialbedingungen und zentrale Prozesse müssen sinnvoll spezifizierbar sein;
- Parameter und Mechanismen sollen inhaltlich interpretierbar bleiben;
- ein guter Fit darf nicht nur in einem engen Kalibrierungsfenster entstehen.
  
  **Wichtig:** Der vorhandene Corpus erlaubt die neue Frage nach Fehlerkompensation / Identifizierbarkeit meist noch nicht abschliessend. Wo dies offen ist, steht 🟡 und nicht ❌.
- ### K7 — ABM-Mehrwert
  **Hard Gate.**
  
  > Ausschluss, wenn die Forschungsfrage mit einem einfacheren statistischen oder räumlichen Modell gleichwertig beantwortet werden könnte.
  
  Fehlende Evidenz für ABM-Mehrwert ist **nicht automatisch ein Ausschluss**. ❌ wird nur vergeben, wenn die vorhandene Modellbeschreibung einen gleichwertigen einfacheren Ansatz hinreichend klar nahelegt.
- ## Bewertungslogik
- ✅ ausreichend gestützt
- 🟡 offen / gezielt zu verifizieren
- ❌ klarer Konflikt
- **weiter** = lohnt gezielte Prüfung im nächsten Schritt
- **Reserve** = kein Hard-Gate-Ausschluss, aber aktuell weniger effizient zu vertiefen
- **ausschliessen** = mindestens ein Hard Gate klar gerissen
  
  ---
- ## Screening
  
  | Modellfamilie | Passung | K9 Semester | K8 Cal./Val. | K7 ABM-Mehrwert | Ergebnis | Kurzbegründung |
  |---|:---:|:---:|:---:|:---:|---|---|
  | **RESMOBcity Leipzig** | hoch | 🟡 | 🟡 | ✅ | **weiter** | Fokussierter räumlicher Residential-Mobility-Kern; keine aktuelle Codebasis, Validations-/Identifizierbarkeitsdetails noch offen. |
  | **Vienna household model** | hoch | 🟡 | 🟡 | 🟡 | **weiter** | Relativ fokussiert; unabhängige Validation und echter Mehrwert gegenüber einfacher Residential-Choice-Modellierung müssen geprüft werden. |
  | **ReMoTe-S** | hoch | ✅ | 🟡 | ✅ | **weiter** | Begrenzter Kern, offene Python/Mesa-Implementation; Validation empirisch, aber kein klassischer temporal OoS-Test. |
  | **COMPASS** | hoch | ✅ | 🟡 | ✅ | **weiter** | Kompakter Behavioural Core + offene Implementation; empirische Schätzung stark, aber Registerdaten/OoS-Validation bleiben kritisch. |
  | **Stockholm residential segregation** | hoch | 🟡 | 🟡 | ✅ | **Reserve** | Wissenschaftlich passend, aber Registerdaten sind der zentrale praktische Engpass; unabhängige Validation nicht belegt. |
  | **Geneva DPSIR / TRACES** | hoch | ✅ | 🟡 | ✅ | **weiter** | Räumlich, interpretierbarer Relocation-Kern, Code/Daten vorhanden; Validation noch nicht sauber als Holdout getrennt. |
  | **Lausanne population–dwellings** | hoch | ❌ | 🟡 | 🟡 | **ausschliessen** | Millionen Agenten, GPU-Architektur und kein bestätigter Code machen eine belastbare Semesterumsetzung derzeit zu gross. |
  | **Aberdeen urban-transition ABM** | hoch | ❌ | 🟡 | ✅ | **ausschliessen** | Mehrschichtiges Gesamtstadtsystem mit Personen, Haushalten, Unternehmen, Industrien und Quartieren; Modellbau würde das Projekt dominieren. |
  | **Vienna-region spatial-agent growth** | hoch | 🟡 | 🟡 | 🟡 | **weiter** | Sehr passende räumliche Urban-Growth-Familie; Legacy-Implementation sowie Mehrwert der Agentenschicht gegenüber CA/spatial model prüfen. |
  | **HUEM Wallonia** | hoch | ✅ | 🟡 | ✅ | **weiter** | Mittlerer Umfang; besonders stark für K7, da ABM explizit gegen Logit/CA-Varianten verglichen wird. Unabhängiger Validationssplit bleibt offen. |
  | **Tallinn CA–Agent** | hoch | ✅ | 🟡 | 🟡 | **weiter** | Umfang grundsätzlich handhabbar; empirischer Holdout und tatsächlicher Zusatznutzen der Agentenschicht gegenüber CA/Markov offen. |
  | **Valladolid domestic-water ABM** | mittel | 🟡 | 🟡 | ✅ | **weiter** | Mehrere gekoppelte Mechanismen, aber transparent und empirisch angebunden; strikte unabhängige Validation noch unklar. |
  | **ENERGY Pro Amsterdam** | mittel | ✅ | 🟡 | ✅ | **weiter** | Gut dokumentiert, offener Code, überschaubarer Household-Adoption-Kern; unabhängige Validation/Identifizierbarkeit noch prüfen. |
  | **Camden Flood Re** | hoch | ❌ | 🟡 | ✅ | **ausschliessen** | Sechs Agenten-/Akteursklassen plus Housing-, Insurance-, Hazard- und Adaptation-System; als Ganzes zu gross für den gewünschten Projektfokus. |
  | **Hamburg pedestrian-flow ABM** | hoch | ✅ | ✅ | 🟡 | **weiter** | Enger Scope und externe reale Beobachtungen für Validation; zentral offen ist, ob ABM gegenüber spatial interaction / flow modelling wirklich nötig ist. |
  | **5aDay Paris** | mittel | 🟡 | 🟡 | ✅ | **Reserve** | Starke Agenten-/Interaktionslogik, aber Millionen Agenten und hohe Rechen-/Datenlast; Downscaling könnte helfen, ist aber noch nicht geprüft. |
  | **MATSim Open Berlin** | hoch | 🟡 | ✅ | ✅ | **weiter** | Sehr gute empirische Prüfung und echte Interaktionen; Framework gross, aber vorhandene 1%-Samples machen einen kleinen Machbarkeitstest sinnvoll. |
  | **eqasim Île-de-France** | hoch | 🟡 | 🟡 | ✅ | **Reserve** | Reproduzierbar, aber umfangreicher Transport-/MATSim-Stack; konkreter semesterfähiger Zuschnitt noch nicht gezeigt. |
  | **mobiTopp** | hoch | 🟡 | 🟡 | ✅ | **Reserve** | Modular und prinzipiell reduzierbar, aber Full-Scale-Modell gross; Validation und sinnvoller kleiner Zuschnitt anwendungsabhängig. |
  | **VirtualBelgium** | hoch | 🟡 | 🟡 | 🟡 | **Reserve** | Sehr grosser Originalmassstab und kein bestätigtes Repo; kleinere Replikation denkbar, aber ABM-Mehrwert und Validation noch nicht ausreichend klar. |
  | **Zurich MATSim transport-planning** | hoch | 🟡 | 🟡 | ✅ | **Reserve** | Urban und agentenbasiert klar passend, aber grosser technischer Stack und kein bestätigtes vollständiges Studienpaket. |
  | **FABILUT / Munich SILO–MATSim** | hoch | ❌ | 🟡 | ✅ | **ausschliessen** | Zwei grosse gekoppelte Microsimulation-Frameworks; Infrastruktur und Gesamtmodellumfang wären voraussichtlich selbst das Hauptprojekt. |
  
  ---
- # Ergebnis
- ## Ausschliessen: 4
  
  1. **Lausanne population–dwellings** — K9
  2. **Aberdeen urban-transition ABM** — K9
  3. **Camden Flood Re** — K9
  4. **FABILUT / Munich SILO–MATSim** — K9
- ## Für gezielte nächste Prüfung: 12
- RESMOBcity Leipzig
- Vienna household model
- ReMoTe-S
- COMPASS
- Geneva DPSIR / TRACES
- Vienna-region spatial-agent growth
- HUEM Wallonia
- Tallinn CA–Agent
- Valladolid domestic-water ABM
- ENERGY Pro Amsterdam
- Hamburg pedestrian-flow ABM
- MATSim Open Berlin
- ## Reserve: 6
- Stockholm residential segregation
- 5aDay Paris
- eqasim Île-de-France
- mobiTopp
- VirtualBelgium
- Zurich MATSim transport-planning
  
  ---
- ## Wichtigste Aussage aus diesem Schritt
  
  **K7 wurde bewusst nicht aggressiv zum Aussortieren verwendet.**  
  Aus dem vorhandenen Corpus lässt sich bei mehreren Modellen noch nicht belastbar zeigen, dass ein einfacheres statistisches/spatiales Modell die gleiche Forschungsfrage gleichwertig beantworten würde. Deshalb bleiben diese Fälle 🟡.
  
  Besonders gezielt auf K7 geprüft werden sollten als Nächstes:
- Vienna household model
- Vienna-region spatial-agent growth
- Tallinn CA–Agent
- Hamburg pedestrian-flow ABM
  
  **HUEM ist dagegen bereits besonders gut für K7 gestützt**, weil die Studie den Hybrid-ABM explizit mit einfacheren Logit-/CA-Varianten vergleicht.
- ## Effizienter nächster Schritt
  
  Nicht alle 12 voll recherchieren. Zuerst nur die offenen Punkte prüfen, die einen Kandidaten tatsächlich noch kippen können:
  
  1. **K7** bei den vier oben genannten Modellen.
  2. **K8**: tatsächlicher Calibration-/Validation-Split + Risiko von Fehlerkompensation / nicht identifizierbaren Parametern.
  3. **K9** nur bei den technisch grösseren Kandidaten, insbesondere Vienna-region, Valladolid und MATSim Open Berlin.
  
  Erst danach sollte die Liste auf wenige Modellfamilien für konkrete RQ-Entwicklung reduziert werden.