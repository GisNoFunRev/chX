# European Urban ABMs — Anwendung der 11 Fit-/Gate-Kriterien

**Datengrundlage:** `european_urban_abm_28_structured_extraction.md`  
**Zweck:** Die 28 zuvor rein deskriptiv erfassten Modellfamilien werden nun erstmals anhand der vereinbarten Projektkriterien geprüft.
- ## Bewertungslogik
- ✅ **erfüllt / durch die aktuelle Extraktion gut gestützt**
- 🟡 **teilweise erfüllt oder noch nicht ausreichend belegt**
- ❌ **klarer Konflikt mit dem Kriterium**
- ↪ **Prozessregel; auf ein bestehendes Modell allein nicht sinnvoll bewertbar**
  
  **Filterregel:** Nur **K3–K9** sind Hard Gates.  
  Ein Modell wird in diesem Schritt nur dann ausgeschlossen, wenn die vorhandene Literaturtabelle bereits einen **klaren ❌-Konflikt** mit mindestens einem dieser Hard Gates zeigt. 🟡 bedeutet: **behalten, aber gezielt verifizieren**.
  
  > K9 (Semester-Machbarkeit), K10 (Übertragbarkeit) und K11 (Forschungsfokus) hängen teilweise von der späteren konkreten Anschluss-RQ ab. Die Bewertung ist deshalb bewusst konservativ.
- ## Die 11 Kriterien
  
  1. **Geografischer Rahmen** — Europa/EU  
  2. **RQ vor Ort** — zuerst RQ/Modellanforderungen, dann Ort  
  3. **Anschluss an bestehende Forschung**  
  4. **Forschungs- und Agentenfundierung**  
  5. **Datenverfügbarkeit und Datenaufwand**  
  6. **Räumliche Repräsentation**  
  7. **ABM-Mehrwert**  
  8. **Empirische Calibration und Validation**  
  9. **Semester-Machbarkeit**  
  10. **Übertragbarkeit**  
  11. **Forschungsfokus** — Mechanismus, Modellvergleich oder Intervention statt möglichst vollständiger Stadtsimulation
  
  ---
- ## A. Housing, Residential Choice, Segregation
  
  | Modell | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | Ergebnis |
  |---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
  | **RESMOBcity** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | **behalten / prüfen** |
  | **Vienna household model** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | **behalten / prüfen** |
  | **HI-LIFE** | ✅ | ↪ | ✅ | 🟡 | 🟡 | ✅ | ✅ | ❌ | 🟡 | ✅ | ✅ | **ausschliessen** |
  | **ReMoTe-S** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | ✅ | 🟡 | ✅ | **behalten / prüfen** |
  | **COMPASS** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | ✅ | **behalten / prüfen** |
  | **Stockholm residential segregation** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | ✅ | **behalten / prüfen** |
  | **Geneva DPSIR / TRACES** | ✅ | ↪ | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ | ✅ | ✅ | **behalten / prüfen** |
  | **Amsterdam tri-sector housing market** | ✅ | ↪ | ✅ | ✅ | 🟡 | ❌ | ✅ | ❌ | ✅ | 🟡 | ✅ | **ausschliessen** |
  | **Lausanne population–dwellings** | ✅ | ↪ | ✅ | 🟡 | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | **behalten / prüfen** |
  | **UK behavioural housing market** | ✅ | ↪ | ✅ | ✅ | 🟡 | ❌ | ✅ | ❌ | 🟡 | 🟡 | ✅ | **ausschliessen** |
- ### Hauptpunkte
- **Geneva** ist in der vorhandenen Tabelle besonders gut durch offene Daten/Code und klare räumliche Struktur gestützt; offen bleibt vor allem die Unabhängigkeit der Validation.
- **COMPASS** und **Stockholm** sind empirisch stark fundiert, aber die praktische Datenverfügbarkeit ist noch nicht geklärt.
- **Amsterdam tri-sector** und **UK behavioural housing market** widersprechen dem räumlichen Gate direkt.
- **HI-LIFE** fällt in der aktuellen Form am Validation-Gate.
  
  ---
- ## B. Urban Growth, Land Use, Development
  
  | Modell | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | Ergebnis |
  |---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
  | **Aberdeen urban-transition ABM** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | **behalten / prüfen** |
  | **Vienna-region spatial-agent growth** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | **behalten / prüfen** |
  | **HUEM Wallonia** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | **behalten / prüfen** |
  | **Nijmegen multi-actor land use** | ✅ | ↪ | ✅ | 🟡 | 🟡 | ✅ | ✅ | ❌ | ✅ | 🟡 | ✅ | **ausschliessen** |
  | **Tallinn CA–Agent model** | ✅ | ↪ | ✅ | 🟡 | 🟡 | ✅ | 🟡 | 🟡 | 🟡 | ✅ | ✅ | **behalten / prüfen** |
  | **Ticino regional economic ABM** | ✅ | ↪ | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | ❌ | 🟡 | 🟡 | 🟡 | **ausschliessen** |
- ### Hauptpunkte
- **HUEM** bleibt besonders interessant, weil der ABM-Mehrwert bereits gegenüber einfacheren Modellen untersucht wird; Calibration/Validation-Trennung und Datenzugang müssen noch geprüft werden.
- **Vienna-region** besitzt historische empirische Prüfung, aber die genaue Unabhängigkeit von Calibration und Validation bleibt offen.
- **Nijmegen** und **Ticino** liefern in der vorhandenen Extraktion keine ausreichende empirische Validation für unser Hard Gate.
  
  ---
- ## C. Urban Environment, Resources, Health & Behaviour
  
  | Modell | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | Ergebnis |
  |---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
  | **Valladolid domestic-water ABM** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | **behalten / prüfen** |
  | **ENERGY Pro Amsterdam** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | ✅ | ✅ | ✅ | **behalten / prüfen** |
  | **Camden Flood Re / housing-market ABM** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | **behalten / prüfen** |
  | **Hamburg pedestrian-flow ABM** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | 🟡 | 🟡 | ✅ | ✅ | ✅ | **behalten / prüfen** |
  | **5aDay Paris** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | ✅ | **behalten / prüfen** |
  | **Urban community-garden ABM** | ✅ | ↪ | ✅ | ✅ | 🟡 | ❌ | ✅ | 🟡 | ✅ | ✅ | ✅ | **ausschliessen** |
- ### Hauptpunkte
- **ENERGY Pro** hat eine günstige Kombination aus dokumentiertem Modell, Code, räumlicher Repräsentation und überschaubarer Anschlussform; unabhängige Validation bleibt zu prüfen.
- **Hamburg pedestrian flow** ist räumlich und empirisch fokussiert; offen ist vor allem, ob ABM gegenüber einer einfacheren räumlichen Bewegungsmodellierung wirklich nötig ist.
- **Community Garden** fällt nicht wegen mangelnder empirischer Qualität aus, sondern weil Raum kein zentraler Bestandteil des Modells ist.
  
  ---
- ## D. Mobility & Integrated Land-Use/Transport
  
  | Modell | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | Ergebnis |
  |---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
  | **MATSim Open Berlin** | ✅ | ↪ | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 | 🟡 | ✅ | 🟡 | **behalten / prüfen** |
  | **eqasim Île-de-France** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | 🟡 | **behalten / prüfen** |
  | **mobiTopp** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | 🟡 | 🟡 | 🟡 | ✅ | 🟡 | **behalten / prüfen** |
  | **VirtualBelgium activity model** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | **behalten / prüfen** |
  | **Zurich MATSim transport-planning** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ | **behalten / prüfen** |
  | **FABILUT / Munich SILO–MATSim** | ✅ | ↪ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | 🟡 | ✅ | 🟡 | **behalten / prüfen** |
- ### Hauptpunkte
- Kein Mobility/LUT-Modell wird auf Basis der bestehenden Tabelle bereits eindeutig ausgeschlossen.
- Der dominante offene Punkt ist hier **K9 Semester-Machbarkeit**: die Frameworks sind technisch und infrastrukturell deutlich grösser als viele Housing-/Land-Use-ABMs.
- **MATSim Open Berlin** hat die klarste offene Daten-/Codebasis; das macht es reproduzierbar, aber nicht automatisch klein genug.
  
  ---
- # Filterergebnis
- ## Klar ausgeschlossen: 6 / 28
  
  | Modell | ausschlaggebendes Hard Gate |
  |---|---|
  | **HI-LIFE** | K8 Calibration / Validation |
  | **Amsterdam tri-sector housing market** | K6 räumliche Repräsentation; K8 Validation |
  | **UK behavioural housing market** | K6 räumliche Repräsentation; K8 Validation |
  | **Nijmegen multi-actor land use** | K8 Calibration / Validation |
  | **Ticino regional economic ABM** | K8 Calibration / Validation |
  | **Urban community-garden ABM** | K6 räumliche Repräsentation |
- ## Vorläufig behalten: 22 / 28
  
  Diese Modelle haben **kein bereits eindeutig gerissenes Hard Gate**, aber fast alle besitzen noch mindestens einen 🟡-Punkt.
  
  Besonders häufig offen sind:
  
  1. **K8 — Calibration / unabhängige Validation**  
   Häufig existiert empirische Kalibrierung oder Validation, aber keine eindeutig getrennte Out-of-Sample-Prüfung.
  
  2. **K5 — Datenzugang**  
   Die Studie nennt verwendete Daten, aber daraus folgt noch nicht automatisch, dass wir dieselben Daten problemlos erhalten können.
  
  3. **K9 — Semester-Machbarkeit**  
   Besonders relevant für grosse Transport-, LUT- und Multi-Layer-Modelle.
- ## Methodische Konsequenz
  
  Der nächste Schritt sollte **nicht nochmals alle 22 Modelle voll analysieren**.  
  Gezielt geprüft werden müssen nur die **gelben Hard-Gate-Felder K4–K9**.
  
  ```text
  28 Modelle
  → 10 Felder deskriptiv
  → 11 Kriterien anwenden
  → 6 klare Ausschlüsse
  → 22 verbleiben
  → nur offene Hard Gates gezielt verifizieren
  → belastbare Shortlist
  → erst danach RQ-Entwicklung
  ```
  
  **Keine eigene Forschungsfrage wurde in diesem Schritt entwickelt.**