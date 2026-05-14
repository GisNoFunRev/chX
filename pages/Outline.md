- **Präsentationsstruktur — System Dynamics Model of Land-Use Change**
- **Ziel: Strukturvalidierung der kausalen Modellannahmen**
- **Dauer: ca. 20 Minuten**
- **Zielpublikum: 2 Dozenten + ca. 12 Masterstudierende, Uni Bern / CDE**
- ---
- Roberto
  background-color:: purple
- Alexis
  background-color:: yellow
- ## Slide 1 — Titel und Framing
  background-color:: purple
  collapsed:: true
	- **Funktion in der Storyline**
		- Die Präsentation wird direkt als konzeptionelle Modellprüfung gerahmt.
		- Wichtig: Nicht als fertige Ergebnispräsentation, sondern als Einladung zu Kritik und Strukturvalidierung.
	- **Inhalt auf der Slide**
		- Titel:
			- **System Dynamics Modelling of Land-Use Change**
		- Untertitel:
			- **A conceptual model for structural validation**
		- Kontext:
			- FHNW project
			- Presentation at University of Bern / CDE
			- Names of presenters
		- Optional kleiner Satz:
			- “We present the model structure to invite feedback on causal mechanisms, assumptions and missing links.”
	- **Nicht auf diese Slide**
		- Noch keine Details zum Modell
		- Keine Resultate
		- Keine grossen Diagramme
		  
		  ---
- ## Slide 2 — Motivation und Ziel der Präsentation
  background-color:: yellow
  collapsed:: true
	- **Funktion in der Storyline**
		- Erklären, warum ihr überhaupt dort seid.
		- Der Fokus wird klar gesetzt: Es geht nicht um Ergebnisvalidierung, sondern um Strukturvalidierung.
	- **Inhalt auf der Slide**
		- Kurze Problemrahmung:
			- Land-use change involves interacting economic, agricultural, urban and policy-related processes.
			- The model uses land-use change as a case to explore system dynamics modelling.
		- Klare Zielaussage:
			- **We do not aim to validate simulation results or exact parameter values.**
			- **We aim to validate the assumed causal structure.**
		- Konkret prüfen wir:
			- Are the causal links plausible?
			- Are relevant mechanisms missing?
			- Are causal directions consistent with literature and expert knowledge?
			- Are feedback loops represented adequately?
	- **Nicht auf diese Slide**
		- Noch keine Vensim-Details
		- Noch keine Stocks/Flows
		- Nicht zu stark behaupten, dass ihr Land-use-Expert:innen seid
		  
		  ---
- ## Slide 3 — Why System Dynamics?
  background-color:: yellow
  collapsed:: true
	- **Funktion in der Storyline**
		- Begründen, warum System Dynamics für diesen Case als Methode sinnvoll ist.
		- System Dynamics wird als Werkzeug zur Strukturierung komplexer Wechselwirkungen vorgestellt.
	- **Inhalt auf der Slide**
		- Ausgangsproblem:
			- Linear cause-effect reasoning is insufficient for land-use dynamics.
			- Individual drivers interact over time.
		- Warum SD?
			- It represents stocks and flows.
			- It makes feedback loops explicit.
			- It allows delays and accumulations to be considered.
			- It helps explore behaviour emerging from structure.
		- Zentrale Aussage:
			- **System Dynamics is used here as a conceptual modelling tool, not primarily as a forecasting tool.**
	- **Visual-Idee**
		- Kleine Gegenüberstellung:
			- Linear model: A → B → C
			- System dynamics: feedback loop diagram
	- **Nicht auf diese Slide**
		- Keine Software-Erklärung von Vensim
		- Keine Gleichungen
		- Keine technische Simulationserklärung
		  
		  ---
- ## Slide 4 — Model Scope and System Boundaries
  background-color:: yellow
  collapsed:: true
	- **Funktion in der Storyline**
		- Früh transparent machen, was das Modell leisten soll und was nicht.
		- Die Grenzen werden nicht als Schwäche versteckt, sondern als bewusste Modellentscheidung gezeigt.
	- **Inhalt auf der Slide**
		- Scope:
			- Spatial scope: EU27 as aggregated macro-system
			- Time horizon: 2026–2050
			- Historical data 2000–2025 used for conceptual calibration / orientation
			- Modelling approach: structural system dynamics model
		- Included:
			- urban land
			- agricultural land
			- land conversion
			- economic pressure / demand mechanisms
			- food pressure / agricultural production proxy
			- policy proxy such as soil protection
		- Excluded:
			- explicit climate dynamics
			- geopolitical shocks
			- global market dynamics
			- explicit actor dynamics
			- normative target definitions
			- explicit backcasting framework
		- Kernaussage:
			- **These boundaries are themselves part of the validation question.**
	- **Nicht auf diese Slide**
		- Keine langen Erklärungen zu jedem ausgeschlossenen Punkt
		- Keine Verteidigung der Grenzen
		- Keine Detailmechanismen
		  
		  ---
- ## Slide 5 — Core Modelling Assumptions
  background-color:: yellow
  collapsed:: true
	- **Funktion in der Storyline**
		- Die wichtigsten Annahmen werden als prüfbare Hypothesen offengelegt.
		- Das Publikum soll verstehen: Diese Punkte sind nicht “gesetzt”, sondern sollen diskutiert werden.
	- **Inhalt auf der Slide**
		- Überschrift:
			- **Core assumptions we would like to validate**
		- Annahmen:
			- Land conversion primarily describes conversion from agricultural land to urban land.
			- Population affects urban land demand exogenously.
			- Urban land and agricultural land are modelled as aggregate land stocks.
			- Reverse conversion from urban to agricultural land is not treated as a dominant trend.
			- Most causal effects are modelled as monotonic directional relationships.
			- EU27 aggregation is considered acceptable for the current conceptual modelling phase.
		- Leitfrage:
			- **Which of these assumptions are problematic or too strong?**
	- **Nicht auf diese Slide**
		- Keine Gleichungen
		- Keine Resultate
		- Keine vollständige Parameterliste
		  
		  ---
- ## Slide 6 — Core Stock-Flow Structure
  background-color:: purple
  collapsed:: true
	- **Funktion in der Storyline**
		- Jetzt wird das Grundmodell eingeführt.
		- Ziel: Publikum soll die mechanische Basis verstehen, bevor Feedback-Loops erklärt werden.
	- **Inhalt auf der Slide**
		- Zentrales Diagramm:
			- Stock 1: **Urban Land**
			- Stock 2: **Agricultural Land**
			- Flow: **Land Conversion Rate**
			- Pfeil: Agricultural Land → Land Conversion Rate → Urban Land
		- Erklärung:
			- Urban Land increases through land conversion.
			- Agricultural Land decreases through the same conversion flow.
			- This ensures land conservation inside the model boundary.
		- Optional:
			- Unit logic:
				- Stocks: km²
				- Flow: km²/year
	- **Visual-Idee**
		- Sehr einfache Stock-Flow-Grafik, nicht das gesamte Vensim-Modell.
		- Rechtecke für Stocks, Ventil/Pfeil für Flow.
	- **Nicht auf diese Slide**
		- Keine 20 Variablen
		- Keine vollständige Vensim-Screenshot-Wand
		- Keine Detailgleichungen ausser optional Units
		  
		  ---
- ## Slide 7 — Key Causal Mechanisms
  background-color:: purple
  collapsed:: true
	- **Funktion in der Storyline**
		- Die wichtigsten Wirkungsbeziehungen werden einzeln als Hypothesen sichtbar gemacht.
		- Diese Slide ist zentral für Strukturvalidierung.
	- **Inhalt auf der Slide**
		- Überschrift:
			- **Key causal mechanisms assumed in the model**
		- Mechanismen als kurze Kausalzeilen:
			- Economic pressure ↑ → Desired urban land ↑ → Land conversion ↑
			- Population ↑ → Urban land demand ↑ → Land conversion ↑
			- Urban density ↑ → Land required per capita ↓ → Land conversion ↓
			- Agricultural land ↓ → Domestic food production capacity ↓ → Food/import pressure ↑
			- Soil protection ↑ → Effective conversion pressure ↓
		- Leitfrage:
			- **Are these transmission channels plausible? Are important channels missing?**
	- **Visual-Idee**
		- Tabelle mit 3 Spalten:
			- Driver
			- Assumed effect
			- Open validation question
		- Oder vereinfachtes Kausaldiagramm.
	- **Nicht auf diese Slide**
		- Keine Feedback-Loops im Detail
		- Keine Simulationsergebnisse
		- Keine grossen Literaturdiskussionen
		  
		  ---
- ## Slide 8 — Feedback Structures
  background-color:: purple
  collapsed:: true
	- **Funktion in der Storyline**
		- Die Modelllogik wird von einzelnen Kausalbeziehungen zu Rückkopplungsstrukturen erweitert.
		- Hier zeigt ihr, dass es nicht nur um einzelne Pfeile geht, sondern um Systemverhalten.
	- **Inhalt auf der Slide**
		- Zwei zentrale Loops zeigen:
		- **Reinforcing Loop: Urban-economic expansion**
			- Urban Land ↑
			- Urban capacity / economic activity ↑
			- Urban demand or economic conversion pressure ↑
			- Land conversion ↑
			- Urban Land ↑
		- **Balancing Loop: Agricultural pressure / policy response**
			- Land conversion ↑
			- Agricultural land ↓
			- Food/import pressure ↑
			- Soil protection / policy response ↑
			- Land conversion pressure ↓
		- Leitfragen:
			- **Are these feedback loops conceptually plausible?**
			- **Are there missing balancing or reinforcing mechanisms?**
			- **Are delays needed between pressure and policy response?**
	- **Visual-Idee**
		- Zwei separate Mini-Loop-Diagramme nebeneinander.
		- Nicht das komplette Modell.
	- **Nicht auf diese Slide**
		- Keine detaillierten mathematischen Funktionen
		- Nicht mehr als 2–3 Loops
		- Keine Resultatkurven
		  
		  ---
- ## Slide 9 — Example Behaviour from the Model
  background-color:: purple
  collapsed:: true
	- **Funktion in der Storyline**
		- Kurze Illustration: Welche Art Dynamik erzeugt die angenommene Struktur?
		- Wichtig: Nicht als “Beweis” präsentieren.
	- **Inhalt auf der Slide**
		- Eine einfache Grafik:
			- Urban Land over time
			- Agricultural Land over time
			- optional: conversion pressure or food/import pressure
		- Kurze Interpretation:
			- The behaviour reflects the assumed feedback structure.
			- Urban land tends to increase under sustained demand.
			- Agricultural land decreases through conversion.
			- Pressure variables may increase or trigger dampening effects depending on assumptions.
		- Klarer Disclaimer:
			- **This is illustrative behaviour, not a validated forecast.**
	- **Nicht auf diese Slide**
		- Keine umfangreiche Szenarienanalyse
		- Keine Parameterdiskussion
		- Keine Aussage “so wird es passieren”
		  
		  ---
- ## Slide 10 — Open Issues and Known Limitations
  background-color:: yellow
  collapsed:: true
	- **Funktion in der Storyline**
		- Zeigen, dass ihr die Grenzen eures Modells bewusst kennt.
		- Diese Slide bereitet die Diskussion vor.
	- **Inhalt auf der Slide**
		- Überschrift:
			- **Open issues identified so far**
		- Punkte:
			- Soil quality is not yet modelled explicitly.
			- Yield is currently too simplified; production should not rely only on wheat.
			- Food system representation may need broader proxies, e.g. crops, legumes, livestock-related land use.
			- Actors are only implicitly represented through aggregate variables such as policy pressure or demand.
			- Backcasting and normative target definitions are outside the current model scope.
			- Some transmission channels may be missing.
			- Nonlinearities, thresholds and delays are not yet systematically validated.
		- Kernaussage:
			- **These are not hidden weaknesses; they are the main points where we seek feedback.**
	- **Nicht auf diese Slide**
		- Keine Lösung für alle offenen Punkte
		- Keine Erweiterung des Modells live erklären
		- Nicht zu defensiv formulieren
		  
		  ---
- ## Slide 11 — Positioning: What Kind of Knowledge Does the Model Produce?
  background-color:: purple
  collapsed:: true
	- **Funktion in der Storyline**
		- Das Modell wird in die Sprache der Sustainability-Transformation-Community übersetzt.
		- Wichtig: Ihr zeigt, dass ihr wisst, was euer Modell kann und was nicht.
	- **Inhalt auf der Slide**
		- Drei Wissensarten:
			- **System knowledge**
				- What dynamics and feedbacks structure land-use change?
				- This is the main contribution of the model.
			- **Target knowledge**
				- What land-use future is desirable?
				- Not addressed in this model.
			- **Transformation knowledge**
				- How can society move toward a desired future?
				- Not directly modelled, but the model may support later discussion of leverage points.
		- Kernaussage:
			- **The model is descriptive and structural, not normative or prescriptive.**
	- **Nicht auf diese Slide**
		- Keine neue Theorie ausführlich erklären
		- Keine Backcasting-Methode ausführen
		- Keine Actor Analysis ausarbeiten
		  
		  ---
- ## Slide 12 — Questions for Discussion
  background-color:: yellow
  collapsed:: true
	- **Funktion in der Storyline**
		- Die Präsentation endet nicht mit “Danke”, sondern mit gezielter Einladung zu Kritik.
		- Diese Slide steuert die anschliessende Diskussion.
	- **Inhalt auf der Slide**
		- Überschrift:
			- **Questions for structural validation**
		- Fragen gruppieren:
		- **System focus**
			- Is the focus on the interaction between agricultural land and urban land appropriate for land-use dynamics?
		- **Mechanisms**
			- Are the identified core mechanisms relevant and correctly represented?
			- Are important structural mechanisms missing?
		- **Causal directions**
			- Are the assumed causal directions consistent with expert knowledge and literature?
		- **Feedback structures**
			- Are the main reinforcing and balancing loops plausible?
			- Are important feedback loops missing?
		- **Dynamics**
			- Are there known nonlinearities or thresholds we should consider?
			- Are relevant delays conceptually misrepresented?
		- **Broader framing**
			- Are there alternative structural explanations or higher-level aspects we should consider?
	- **Nicht auf diese Slide**
		- Keine neuen Inhalte
		- Keine Resultate
		- Nicht zu viele Unterfragen visuell überladen
		  
		  ---
- # Empfohlene Gewichtung in der Präsentation
- Slides 1–3: ca. 5 Minuten
- Slides 4–5: ca. 4 Minuten
- Slides 6–8: ca. 6 Minuten
- Slide 9: ca. 1.5 Minuten
- Slides 10–12: ca. 4 Minuten
- # Gesamtlogik
- Erst klären: Warum präsentieren wir?
- Dann klären: Was ist im Modell drin und was nicht?
- Dann zeigen: Welche Struktur und Mechanismen nehmen wir an?
- Dann illustrieren: Welches Verhalten entsteht daraus?
- Dann öffnen: Was ist unsicher und wo wünschen wir Kritik?