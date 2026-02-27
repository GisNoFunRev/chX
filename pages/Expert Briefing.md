- Briefing **weiter unten**
  background-color:: red
- Reach-out phase strukturvorschlag:
	- Expert Briefing <- Hier sind Wir jetzt
	  background-color:: red
	- Kontaktaufnahme
	- Leitfaden Gespräch
	- Korrektur und Rückkopplung
- ---
- # Framework für unsere Dokumentation
  background-color:: green
- Zweck
	- Strukturvalidierung der angenommenen Kausalmechanismen
	- Offenlegung aller Modellannahmen
	- Trennung zwischen:
		- Konzeptionelles Modell (CLD)-> für unser Experti:innen- Review
		- Formelles Simulationsmodell (Stock-Flow in BPTK) -> Nicht dokumentieren (?)
	- Wir machen (vorerst) ein Systemdynamik- Modell mit VENSIM und nicht eine integrierte Analysemodellierung
- Scope und Systemgrenzen
	- Räumlicher Rahmen
		- EU27 als aggregiertes Gesamtsystem
		- Keine regionale Differenzierung (Phase 1)
		- Keine globale Kopplung (z.B. Importabhängigkeit)
	- Zeitlicher Rahmen
		- Simulationszeitraum: 2026–2050
		- Historische Referenzdaten zur Kalibrierung: 2000–2025
	- Endogen modelliert
		- Land Conversion
		- Agricultural Land
		- Economic Growth
		- Income
		- Land Consumption per Capita
		- Economic Pressure
		- Import Dependence
		- Food Production
		- Agrotechnological Progress
		- Yield per ha
		- Land Requirement
		- Spatial Planning
		- Soil Protection
	- Exogen modelliert
		- Housing Demand
		- Population
	- Anmerkung
		- Urbane Fläche und Landwirschaftliche  Fläche sind nicht als eigene Variablen modelliert, sondern implizit über Land Conversion abgebildet.
		- Bevölkerung ist im CLD bisher als exogene Ursache gekennzeichnet.
	- Nicht Moddeliert
		- Klimadynamiken
- Allgemeine Modellannahmen (sollte klarer forumliert und begründet sein)
	- Aggregation über Länder ist zulässig (keine regionale Heterogenität)
	- weitere Annahmen in den spezifischen Beschreibungen der Kanten des CLD
	-
- ---
- # Struktur der Dokumentation des CLD
  background-color:: blue
- **Dokumentation pro Beziehung im CLD**
  background-color:: blue
- Beschreibung
	- Variable A → Variable B
	- Vorzeichen (+ / -)
- Wirkungslogik
	- Warum wirkt A auf B?
	- Direkte oder indirekte Wirkung?
	- Linear oder nichtlinear?
	- Schwellenwerte bekannt?
- Zeit
	- Sofortwirkung oder Verzögerung?
	- Falls Verzögerung: strukturell oder politisch bedingt?
- Annahmen
- Evidenzbasis **-> Nehmen wir hier (in Gelb) schon was vor, was wir den Expert:innen überlassen sollten?**
  background-color:: yellow
	- Empirisch belegt (Quelle)
	  background-color:: yellow
	- Theoretisch begründet
	  background-color:: yellow
	- Explorative Annahme
	  background-color:: yellow
- Unsicherheitsgrad
  background-color:: yellow
	- Niedrig, Mittel, Hoch
	  background-color:: yellow
- **Dokumentation pro Loop im CLD**
  background-color:: blue
  Jeder Loop wird separat beschrieben.
- Struktur
	- Liste der enthaltenen Variablen und Richtung
	- Loop-Typ (R oder B)
- Interpretation
  background-color:: yellow
	- Welches reale Phänomen repräsentiert dieser Loop?
	  background-color:: yellow
	- Gibt es Literatur, die diesen Mechanismus beschreibt?
	  background-color:: yellow
- Dominanzannahme
  background-color:: yellow
	- Unter welchen Bedingungen dominiert dieser Loop?
	  background-color:: yellow
	- Gibt es bekannte Kipppunkte?
	  background-color:: yellow
- ---
- # Expert Briefing Document  
  background-color:: red
- ## Strukturvalidierung eines systemdynamischen Modells zur Landnutzungsdynamik in den EU27 (2026–2050)
  
  ---
- ## 1. Zielsetzung der Anfrage
  
  Im Rahmen eines systemdynamischen Modellierungsprojekts untersuchen wir die strukturelle Wechselwirkung zwischen Urbanisierungsprozessen und landwirtschaftlicher Flächennutzung in den EU27 im Zeitraum 2026–2050.
  
  Ziel dieser Anfrage ist **nicht** die Validierung von Simulationsergebnissen oder Parametrisierungen, sondern die **Strukturvalidierung der angenommenen kausalen Mechanismen** auf konzeptioneller Ebene (Causal Loop Diagram).
  
  Wir möchten prüfen,
- ob die modellierten Einflussbeziehungen fachlich plausibel sind,
- ob relevante Mechanismen fehlen,
- ob die angenommene Wirkungsrichtung konsistent mit dem Stand der Literatur ist,
- und ob zentrale Rückkopplungsstrukturen adäquat abgebildet sind.
  
  ---
- ## 2. Modellrahmen und Systemgrenzen
  
  Das Modell aggregiert die EU27 als makroskopisches Gesamtsystem. Regionale Differenzierungen werden in dieser Phase nicht modelliert.
  
  Der Simulationszeitraum umfasst 2026–2050. Historische Daten (2000–2025) dienen der konzeptionellen Kalibrierung.
  
  Nicht modelliert werden:
- explizite Klimadynamiken
- geopolitische Schocks
- globale Marktgleichgewichte
- detaillierte sektorale Differenzierungen
  
  Die Modellierung verfolgt einen strukturellen Ansatz im Sinne der System Dynamics (Forrester), mit Fokus auf endogene Rückkopplungen.
  
  ---
- ## 3. Konzeptionelle Kernmechanismen
  
  Auf Basis des Causal Loop Diagrams identifizieren wir vier zentrale strukturelle Dynamiken:
- ### 3.1 Wirtschaftlicher Verstärkungsmechanismus
  
  Wirtschaftliches Wachstum erhöht Einkommen, was den Flächenverbrauch pro Kopf steigert. Dies führt zu erhöhter Landumwandlung und reduziert landwirtschaftliche Fläche. Dieser Mechanismus wirkt selbstverstärkend (Reinforcing Loop), sofern keine starken Gegenmechanismen greifen.
- ### 3.2 Technologischer Kompensationsmechanismus
  
  Agrartechnologischer Fortschritt erhöht den Ertrag pro Hektar, wodurch bei gegebener Produktion weniger Fläche benötigt wird. Dieser Mechanismus wirkt potenziell stabilisierend (Balancing Loop), kann jedoch Flächenverluste nur partiell kompensieren.
- ### 3.3 Raumplanerischer Schutzmechanismus
  
  Institutionelle Eingriffe (Spatial Planning) stärken den Bodenschutz und stabilisieren landwirtschaftliche Fläche. Dieser Mechanismus ist politisch sensitiv und nicht automatisch systemisch dominant.
- ### 3.4 Importdruck-Mechanismus
  
  Sinkende Nahrungsmittelproduktion erhöht Importabhängigkeit. Dies erzeugt wirtschaftlichen Druck, der wiederum Flächennutzungsentscheidungen beeinflussen kann. Dieser Mechanismus stellt eine indirekte Rückkopplung dar.
  
  ---
- ## 4. Zentrale Annahmen
- Aggregation über EU27 ist strukturell zulässig.
- Land Conversion beschreibt primär die Umwandlung landwirtschaftlicher Fläche.
- Bevölkerung wirkt exogen auf Wohnraumnachfrage.
- Beziehungen werden als monoton gerichtet modelliert.
- Rückumwandlungsprozesse werden nicht als dominanter Trend angenommen.
  
  Diese Annahmen sind explizit dokumentiert und offen zur Diskussion.
  
  ---
- ## 5. Konkrete Fragen an die Expert:innen
- 1. Sind die identifizierten Kernmechanismen relevant un korrekt?
- 2.Sind die identifizierten Kernmechanismen vollständig oder fehlen strukturell relevante Einflussfaktoren?
- 3. Sind die angenommenen Wirkungsrichtungen fachlich konsistent?
- 4. Gibt es bekannte Nichtlinearitäten oder Schwellenwerte, die strukturell berücksichtigt werden sollten?
- 5. Sind relevante zeitliche Verzögerungen konzeptionell falsch eingeschätzt?
- 6. Gibt es Literatur, die einzelne Mechanismen explizit stützt oder infrage stellt? (eher streichen - unser Job I guess)
  
  ---
- ## 6. Beilage
- Causal Loop Diagram (CLD)
- Strukturierte Dokumentation der einzelnen Beziehungen
- Loop-Beschreibungen