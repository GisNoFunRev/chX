-
- type:: analysis
  theorie:: Alonso-Muth-Mills + Urban Sprawl
  quelle:: Brueckner (2001), Urban Sprawl: Lessons from Urban Economics
-
- ## Berechnung mit aktuellen Werten
	- Werte: Ag = 2, Policy = 1,5, Transport = 1,9, Income = 2 × Urban Land Index
	- Bei Urban Land Index = 1 (Startzustand) ist Income Effect = 2
	- Gesamtmultiplikator: `2 (Ag) × 1,5 (Policy) × 1,9 (Transport) × 2 (Income) = 11,4`
	- Desired Urban Land (= faktisch pro Kopf) = `11,4 × 30 m² = 342 m²/Kopf` schon im Startzustand
	- **Kernerkenntnis:** 342 m²/Kopf ist als gewünschte Pro-Kopf-Stadtfläche realistisch, aber die Referenz von 30 m²/Kopf ist ein extrem dichter Floor (dichter als praktisch jede reale Stadt). Die vier Effekte tragen die gesamte Last, von diesem unrealistisch dichten Floor auf ein realistisches Niveau zu heben — hier passt die Magnitude einzelner Effekte nicht zur Empirie.
-
- ## Theoretische Grundlage
	- **Quelle:** Brueckner, J. K. (2001), *Urban Sprawl: Lessons from Urban Economics*, Brookings-Wharton Papers on Urban Affairs, S. 65–97.
	- **Link:** [lessons.pdf (UC Irvine, frei zugänglich)](https://sites.socsci.uci.edu/~jkbrueck/course%20readings/lessons.pdf)
	- **S. 69, Gleichung (3):** komparativ-statisch x̄ = g[n⁺, y⁺, t⁻, ra⁻] → gibt die Vorzeichen aller vier Treiber vor: Fläche steigt mit Bevölkerung und Einkommen, **fällt** mit Pendelkosten und Agrarrente.
	- **S. 70 (nach Gl. 4):** Bevölkerungselastizität = 1,1; Einkommen = 1,5; Agrarrente = −0,23; Pendelkosten-Effekt **statistisch nicht signifikant**.
-
- ## TODOs
	- TODO Agricultural Land Value Effect: von 2 auf ≈ 0,9–1,1 anpassen + Vorzeichen prüfen [höchste Priorität]
	  collapsed:: true
		- Mit ε ≈ −0,23 impliziert ein Multiplikator von 2 einen ~95-%-Einbruch der Agrarrente (`2^(1/−0,23) ≈ 0,05`).
		- Eine Halbierung des Agrarwerts gäbe nur `0,5^−0,23 ≈ 1,17`. Der Multiplikator kann sich strukturell kaum von 1 entfernen.
		- Richtung falsch herum: höhere Agrarrente soll die Stadt *schrumpfen*. Wert > 1 nur korrekt, wenn Eingangssignal *niedriger* Agrarwert ist → dokumentieren.
		- **Beleg:** S. 69 (Gl. 3, Vorzeichen), S. 70 (Elastizität −0,23 + Mechanismus „produktives Agrarland ist umwandlungsresistenter").
	- TODO Transport Effect: von 1,9 auf ≈ 1,0–1,2 senken, als Hochunsicherheits-Hebel deklarieren
	  collapsed:: true
		- Ausgerechnet der empirisch insignifikante Kanal trägt den zweitgrößten Hebel. 1,9 ist nicht verteidigbar.
		- Eng um 1 halten, als Szenariovariable mit breitem Unsicherheitsband behandeln.
		- Vorzeichen: x̄ steigt, wenn t *fällt* → Effekt > 1 repräsentiert *sinkende* Pendelkosten.
		- **Beleg:** S. 70 („not statistically significant"), S. 69–70 (Mechanismus t↓ → x̄↑).
	- TODO Income Effect: Struktur überdenken (= die Runaway-Maschine)
	  collapsed:: true
		- Aktuell: `Income Effect = 2 × Urban Land Index`
		- *Magnitude:* Koeffizient 2 übersteigt die Einkommenselastizität 1,5. Income allein verdoppelt am Referenzpunkt die Pro-Kopf-Fläche.
		- *Struktur (gravierender):* Koppelt „Income" an Urban Land selbst, nicht an einen Einkommenstreiber. Die 1,5-Elastizität misst Einkommen → Fläche, nicht Fläche → Fläche. Ergebnis: unverankerter, linearer, ungesättigter Self-Reinforcing-Kern → exponentielles Wachstum. Deshalb muss der Balancing Loop „zu stark" sein.
		- **Empfehlung:** entweder an echten Einkommens-/BIP-Treiber mit Exponent ≈ 1,5 koppeln, oder (falls Urban-Land-Index als Agglomerations-Proxy gemeint) Sättigungsfunktion statt linearer `2 ×` einbauen und Gain Richtung 1,5 senken.
		- **Beleg:** S. 70 (Einkommenselastizität 1,5), S. 69 (Einkommensmechanismus).
	- TODO Policy Effect (1,5): behalten, aber als normativ dokumentieren + Richtung klären
	  collapsed:: true
		- Keine Standard-Elastizität → legitimer Szenario-Hebel.
		- Die meisten realen Politiken (UGB, Greenbelt) restringieren, wirken also < 1.
		- Numerisches Beispiel S. 82–84: UGB halbiert Stadtradius von 30,8 auf 15 Meilen.
		- Policy Effect > 1 repräsentiert explizit wachstums*fördernde* Politik (großzügiges Zoning, niedrige Impact Fees) → benennen.
		- **Beleg:** S. 82–84 (UGB-Simulation), S. 87 (Farm-Subventionen erhöhen Agrarrente → restringieren).
	- TODO Variablen umbenennen (interne Konsistenz)
	  collapsed:: true
		- Mathematik macht „Desired Urban Land" zur Pro-Kopf-Größe und „Desired Urban Land per Capita" (= × Population) zur Gesamtfläche → Namen gegenüber Einheiten vertauscht.
		- Conversion-Formel ist dadurch zwar dimensional korrekt (Gesamt − Gesamt), aber irreführend benannt → tauschen.
	- TODO Balancing Loop nicht überdrehen, sondern Reinforcing-Gain senken
	  collapsed:: true
		- „Balancing Loop ist zu stark" ist Symptom, nicht Ursache.
		- Brueckner S. 89: Marktversagen ist „of secondary importance compared with the powerful, fundamental forces" — korrigierende Kräfte sind in der Realität moderat, nicht draconisch.
		- Riesiger Balancing Loop = Hinweis, dass Reinforcing-Gain (TODO Income) zu hoch ist. Erst Income lösen, dann Balancing Loop neu kalibrieren.
		- **Beleg:** S. 89 (Conclusion).
-
- ## Effekt der Korrekturen
	- Nach Ag + Transport fällt der konstante Teil von 5,7 auf ≈ `1,5 (Policy) × 1,1 (Ag) × 1,1 (Transport) ≈ 1,8`.
	- Kombiniert mit gesättigtem Income-Term liegt der Kompound-Multiplikator dann verteidigbar statt bei 11,4.
	- Reinforcing Loop bleibt Haupttreiber (Annahme 2), läuft aber nicht ungebremst; Balancing Loop wird kalibrierbar.
-
- ## Offene Frage
	- Ist `Reference Land per Capita = 30 m²/Kopf` ein bewusst gesetzter Dichte-Floor oder ein empirischer Startwert? Davon hängt ab, ob der hohe Restmultiplikator nötig ist oder ob stattdessen die Referenz angehoben werden sollte.