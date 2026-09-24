# Schritt 7 — Codebase × Reimplementationsaufwand

**Ausgangspunkt:** 18 nach Schritt 6 verbleibende Modelle  
(12 `weiter` + 6 `Reserve`).
- ## Gate
  
  > **Ausschluss, wenn keine nutzbare offene Codebase verfügbar ist und eine Neuimplementierung aufgrund der Modellkomplexität voraussichtlich einen wesentlichen Teil des Semesters beanspruchen würde.**
  
  Fehlende Codebase allein ist **kein Ausschlusskriterium**.
  
  Bewertung:
- ✅ kein Ausschlussproblem
- 🟡 Reimplementationsrisiko vorhanden, aber noch kein belastbarer Ausschluss
- ❌ Gate gerissen
  
  ---
  
  | Modellfamilie | Codebase | Reimplementationsaufwand | Gate | Ergebnis |
  |---|---|---|:---:|---|
  | RESMOBcity Leipzig | kein öffentliches Repo bestätigt | mittel; räumliche Initialisierung nicht trivial | 🟡 | behalten |
  | Vienna household model | kein öffentliches Repo bestätigt | mittel; relativ fokussierter Behavioural Core | ✅ | behalten |
  | ReMoTe-S | offen, Python/Mesa | niedrig–mittel | ✅ | behalten |
  | COMPASS | offen | mittel; Inference-Pipeline technisch anspruchsvoller | ✅ | behalten |
  | Stockholm residential segregation | kein öffentliches Repo bestätigt | mittel–hoch; konzeptionell aber tractable | 🟡 | behalten |
  | Geneva DPSIR / TRACES | Code + Daten offen | mittel | ✅ | behalten |
  | Vienna-region spatial-agent growth | kein modernes Repo; Legacy-Software | mittel–hoch | 🟡 | behalten |
  | HUEM Wallonia | keine öffentliche Implementation bestätigt | mittel; drei Agententypen + CA/Logit | 🟡 | behalten |
  | Tallinn CA–Agent | kein Repo bestätigt | mittel; Actor-Layer als handhabbar beschrieben | ✅ | behalten |
  | Valladolid domestic-water ABM | kein aktuelles öffentliches Repo bestätigt | mittel–hoch; mehrere gekoppelte Submodelle | 🟡 | behalten |
  | ENERGY Pro Amsterdam | offen, NetLogo + R | mittel | ✅ | behalten |
  | Hamburg pedestrian-flow ABM | kein öffentliches Repo bestätigt | niedrig–mittel; enger Modellkern | ✅ | behalten |
  | 5aDay Paris | frei verfügbarer Modellcode und Analyse-Material | sehr hoher Originalmassstab | ✅ | behalten — Code verhindert Neuimplementierung des Gesamtmodells |
  | MATSim Open Berlin | offene, gepflegte Scenario-Codebase | hoch–sehr hoch | ✅ | behalten |
  | eqasim Île-de-France | offene Codebase | hoch | ✅ | behalten |
  | mobiTopp | offene Codebase | hoch im Full Scale, modular | ✅ | behalten |
  | VirtualBelgium | kein aktuelles öffentliches Repo bestätigt | **sehr hoch**; ca. 10 Mio. Personen / 4.35 Mio. Haushalte im Original | ❌ | **ausschliessen** |
  | Zurich MATSim transport-planning | MATSim offen; exaktes Studienpaket nicht bestätigt | hoch | 🟡 | behalten |
  
  ---
- ## Ergebnis
  
  **Neu ausgeschlossen: 1**
- **VirtualBelgium**  
  Keine aktuelle öffentliche Codebase bestätigt **und** sehr grosser Originalumfang. Eine eigenständige Reimplementation würde damit genau das Risiko erzeugen, das dieses Gate ausschliessen soll.
  
  **Nicht ausgeschlossen, aber mit Reimplementationsrisiko:**
- RESMOBcity Leipzig
- Stockholm residential segregation
- Vienna-region spatial-agent growth
- HUEM Wallonia
- Valladolid domestic-water ABM
- Zurich MATSim transport-planning
  
  Diese Modelle bleiben drin, weil die vorhandene Evidenz **noch nicht ausreicht**, um zu behaupten, dass eine Neuimplementierung zwingend zu gross für das Semester wäre.
- ## Stand nach Schritt 7
- nach Schritt 6: **18**
- neu ausgeschlossen: **1**
- verbleibend: **17**