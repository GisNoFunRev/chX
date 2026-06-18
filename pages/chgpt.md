- Ja. Deine 3 Beobachtungen sind genau die richtigen Kategorien. Ich würde sie so einordnen:
- ## 1. Deine drei Zeit-Ebenen im AMM-Kontext
- ### A.  **Exogene Treiber verändern sich über Zeit**
  
  Das sind Dinge wie:
- Population
- Einkommen
- Transportkosten
- Agricultural rent
- Housing demand
  
  Im klassischen AMM werden diese Grössen **als gegeben** behandelt. Wenn sie sich ändern, berechnet man ein **neues Gleichgewicht**. Das nennt man eher **comparative statics** als echte Dynamik.
  
  Beispiel:
  
  > 
  
  Einkommen steigt → neues Gleichgewicht mit grösserer Stadtfläche.
  
  Das Modell erklärt aber nicht selbst, **warum** Einkommen steigt.
  
  ---
- ### B.  **Preise / Renten passen sich im Gleichgewicht an**
  
  Im AMM sind Bodenrenten und Dichten Teil der Gleichgewichtslösung.
  
  Also:
  
  > 
  
  Bei gegebenem Einkommen, Transportkosten und Population ergibt sich ein Rentenprofil über Distanz.
  
  Aber im klassischen Modell passiert diese Anpassung **instantan**. Es wird nicht simuliert, wie Preise langsam reagieren.
  
  Das ist wichtig: **Preisstruktur ja, Preisdynamik nein.**
  
  ---
- ### C.  **Ist-Zustand ≠ Gleichgewichtszustand**
  
  Das ist der für euer Vensim-Modell wichtigste Punkt.
  
  AMM gibt euch eher:
  
  > 
  
  Welche Stadtgrösse wäre im Gleichgewicht?
  
  Euer SD-Modell kann dann sagen:
  
  > 
  
  Die tatsächliche Stadtfläche nähert sich diesem Gleichgewicht nur langsam an.
  
  Das ist eure eigene dynamische Erweiterung:
  
  ```
  Equilibrium Urban Land - Actual Urban Land
  → Urban Land Gap
  → Land Conversion Rate
  ```
  
  Das ist nicht reines AMM, aber es ist eine plausible **dynamic adjustment interpretation**.
  
  ---
- # 2. Wie die Literatur mit dieser Zeitfrage umgeht
- ## 2.1 Klassisches AMM: statisches Gleichgewicht
  
  Die Standardliteratur beschreibt AMM bzw. das monocentric city model als **statisches räumliches Gleichgewichtsmodell**. Es kombiniert Transportkosten, Bodenrenten, Bevölkerung und Landnutzung in einer Gleichgewichtsstruktur. Die Reserve Bank of Australia sagt explizit, dass das Modell statisch ist und nicht den Prozess urbaner Veränderung, langlebige Housing Stocks, Gentrifizierung oder Finanzierungsdynamiken modelliert. ([Reserve Bank of Australia](https://www.rba.gov.au/publications/rdp/2011/2011-03/alonso-muth-mills-model.html?utm_source=chatgpt.com))
  
  Das heisst:
  
  > 
  
  Klassisches AMM beantwortet nicht: Wie verändert sich die Stadt von Jahr zu Jahr?
  Es beantwortet: Wie sähe die Gleichgewichtsstruktur bei gegebenen Parametern aus?
  
  Duranton und Puga ordnen Alonso, Mills und Muth ebenfalls als Ursprung des modernen **monocentric city model** ein, also als formales Grundmodell für Transport, Landnutzung und Bevölkerung in einer Stadt. ([matthewturner.org](https://matthewturner.org/ec2410/readings/Duranton_Puga_Handbook_2015.pdf?utm_source=chatgpt.com))
  
  ---
- ## 2.2 Comparative statics: Veränderung der Inputs, neues Gleichgewicht
  
  Die erste Art, Zeit indirekt zu behandeln, ist:
  
  > 
  
  Man verändert einen Parameter und schaut, wie sich das Gleichgewicht verändert.
  
  Also zum Beispiel:
- Population steigt
- Einkommen steigt
- Transportkosten sinken
- Agricultural rent sinkt
  
  Dann wird ein neues Gleichgewicht berechnet.
  
  Empirische Tests des Standard Urban Model zeigen genau diese Logik: Städte breiten sich tendenziell stärker aus, wenn sie reicher, bevölkerungsreicher und Transport oder Farmland günstiger sind. ([arXiv](https://arxiv.org/abs/2111.02112?utm_source=chatgpt.com))
  
  Das passt sehr gut zu deiner Beobachtung A:
  
  > 
  
  Population und Einkommen ändern sich über Zeit, AMM liefert jeweils den dazu passenden Gleichgewichtszustand.
  
  Aber: Das ist noch keine echte dynamische Simulation.
  
  ---
- ## 2.3 Dynamische Erweiterung 1: sequence of short-run equilibria
  
  Ein wichtiger wissenschaftlicher Umgang mit dem Problem ist: Man modelliert Stadtentwicklung als **Abfolge kurzfristiger Gleichgewichte**.
  
  Anas entwickelt 1978 ein dynamisches Modell des urban residential market und zeigt, dass Städte unter bestimmten Annahmen durch eine **sequence of short-run equilibria** wachsen. Dabei werden rekursive Gleichungen genutzt, um Effekte von Wachstum auf Renten, Dichten und Wohlfahrt zu analysieren. ([SUNY University at Buffalo](https://researchconnect.buffalo.edu/en/publications/dynamics-of-urban-residential-growth/?utm_source=chatgpt.com))
  
  Das ist für euch sehr relevant, weil es genau die Brücke ist:
  
  ```
  AMM-artiges Gleichgewicht pro Zeitschritt
  +
  rekursive Aktualisierung über Zeit
  ```
  
  Das ist wissenschaftlich viel näher an Vensim als die reine statische AMM-Version.
  
  ---
- ## 2.4 Dynamische Erweiterung 2: durable housing / langlebige gebaute Struktur
  
  Die zweite grosse Erweiterung ist: Gebäude und Stadtstruktur sind **dauerhaft**.
  
  Das ist zentral, weil eine Stadt nicht jedes Jahr vollständig neu gebaut wird. Der gebaute Bestand ist träge.
  
  Wheaton entwickelte ein Modell von **urban spatial development with durable but replaceable capital**. Die Literaturbeschreibung sagt, dass die Urban Spatial Development Theorie bis dahin primär eine statische Gleichgewichtstheorie war, und Wheaton genau diese Richtung dynamisierte. ([Semantic Scholar](https://www.semanticscholar.org/paper/Urban-spatial-development-with-durable-but-capital-Wheaton/a4dd87179e9e3ac68992f431cd00a89738623702?utm_source=chatgpt.com))
  
  Brueckner entwickelte ebenfalls ein **vintage model of urban growth**, also ein Modell, in dem ältere Wohnungsbestände und Wachstum über Zeit eine Rolle spielen. ([IDEAS/RePEc](https://ideas.repec.org/a/eee/juecon/v8y1980i3p389-402.html?utm_source=chatgpt.com))
  
  Glaeser und Gyourko zeigen später für urban decline, dass langlebiger Wohnungsbestand erklärt, warum Schrumpfung nicht einfach das Spiegelbild von Wachstum ist. Städte können schneller wachsen als schrumpfen, und negative Schocks senken eher Preise als sofort Bevölkerung oder Gebäudezahl. ([joeornstein.github.io](https://joeornstein.github.io/pols-4641/readings/Glaeser%2C%20Gyourko%20-%202005%20-%20Urban%20Decline%20and%20Durable%20Housing.pdf?utm_source=chatgpt.com))
  
  Das passt zu deiner Beobachtung C:
  
  > 
  
  Der Gleichgewichtszustand kann sich ändern, aber der Ist-Zustand folgt langsam, weil gebaute Fläche träge ist.
  
  ---
- ## 2.5 Dynamische Erweiterung 3: Landpreise und Entwicklungserwartungen
  
  Eine weitere Literaturströmung sagt: Landpreise enthalten Erwartungen über zukünftige Entwicklung.
  
  Capozza und Helsley zeigen in **The fundamentals of land prices and urban growth**, dass der Preis urbanen Landes aus mehreren Bestandteilen bestehen kann, darunter agricultural land rent, conversion cost, accessibility value und erwartetes urban growth premium. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/009411908990003X?utm_source=chatgpt.com))
  
  Das ist wichtig, weil es deine Preis-Dynamik-Beobachtung präzisiert:
  
  > 
  
  Preise sind nicht nur aktueller Gleichgewichtsausdruck. Sie können auch Erwartungen über zukünftige Umwandlung und Wachstum enthalten.
  
  Das geht klar über einfaches AMM hinaus, ist aber eine etablierte dynamische Erweiterung der Urban-Land-Use-Literatur.
  
  ---
- ## 2.6 Dynamische Erweiterung 4: räumliche Landnutzungsdynamik statt reines Gleichgewicht
  
  Irwin argumentiert, dass Land-Use-Change-Modelle dynamischer werden müssen und mehrere Formen räumlicher Heterogenität berücksichtigen sollten. Sie unterscheidet explizit zwischen räumlicher Heterogenität und **spatial dynamics**, also Übergangsprozessen von räumlichen Mustern über Zeit. ([Federal Reserve Bank of New York](https://www.newyorkfed.org/medialibrary/media/research/conference/2009/jrs/Irwin.pdf?utm_source=chatgpt.com))
  
  Das ist für euer Projekt wichtig, weil ihr Land Conversion über 2026 bis 2050 modelliert. Ihr seid also nicht nur an einem statischen Stadtbild interessiert, sondern an einem Übergangsprozess.
  
  Die wissenschaftliche Konsequenz ist:
  
  > 
  
  Reines AMM ist als Zielgleichgewicht nützlich, aber für Land-Use-Change braucht man zusätzliche Dynamik.
  
  ---
- ## 2.7 Alternative technische Umsetzung: Agent-Based Dynamics
  
  Ein anderer Umgang mit der Zeitfrage ist, AMM nicht als Gleichungssystem, sondern als Agent-Based-Prozess zu bauen.
  
  Lemoy et al. zeigen ein Agent-Based Model, dessen Dynamik zu einem Standard-AMM-Gleichgewicht führen kann. Agenten bewegen sich, bieten für Land und erreichen am Ende Renten-, Dichte- und Landnutzungsgleichgewichte. ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0198971516302952?utm_source=chatgpt.com))
  
  Das ist interessant, weil es zeigt:
  
  > 
  
  Man kann AMM dynamisieren, indem man explizit modelliert, wie Akteure sich bewegen und bieten.
  
  Für Vensim ist das aber weniger direkt geeignet, weil Vensim keine natürliche ABM-Umgebung ist.
  
  ---
- # 3. Gesamtordnung der Wissenschaft
  
  Die Literatur scheint ungefähr so mit der Zeitfrage umzugehen:
  
  | Ansatz | Was wird gemacht? | Nähe zu eurem Vensim-Modell |
  | ---- | ---- | ---- |
  | Klassisches AMM | statisches räumliches Gleichgewicht | theoretische Basis |
  | Comparative statics | Inputs ändern, neues Gleichgewicht | gut für Szenarien |
  | Sequence of short-run equilibria | pro Periode Gleichgewicht, dann Update | sehr relevant |
  | Durable housing / vintage models | gebaute Struktur passt sich langsam an | sehr relevant |
  | Land price expectations | Preise enthalten Zukunftserwartungen | relevant, aber komplex |
  | ABM-Dynamik | Agenten bewegen sich zum Gleichgewicht | theoretisch interessant, aber nicht Vensim-nah |
  | Spatial land-use dynamics | räumliche Übergänge über Zeit | relevant, aber datenintensiv |
  
  ---
- # 4. Was bedeutet das für euer Modell?
  
  Deine 3 Beobachtungen lassen sich wissenschaftlich sauber so einordnen:
- ## Beobachtung 1: Population, Einkommen, Transport ändern sich
  
  Das entspricht:
  
  > 
  
  Moving equilibrium / comparative statics over time
  
  Also: Jedes Jahr ändern sich Parameter, und daraus ergibt sich ein neuer AMM-Gleichgewichtswert.
  
  ---
- ## Beobachtung 2: Preise / Renten ändern sich
  
  Im reinen AMM sind Renten Ergebnis des Gleichgewichts. In dynamischen Erweiterungen können Preise aber träge sein oder Erwartungen enthalten. Besonders Capozza und Helsley sind hier relevant, weil Landpreise in Bestandteile zerlegt werden, darunter agricultural land value, conversion cost, accessibility und expected growth. ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/009411908990003X?utm_source=chatgpt.com))
  
  ---
- ## Beobachtung 3: Ist-Zustand weicht vom Ought-/Equilibrium-Zustand ab
  
  Das ist genau die Brücke zu Vensim.
  
  Wissenschaftlich passt das zu:
- Anas: sequence of short-run equilibria
- Wheaton und Brueckner: durable housing / gradual urban growth
- Irwin: dynamic land-use change over time
  
  Damit könnt ihr sagen:
  
  > 
  
  We use AMM to compute a long-run equilibrium urban land demand, while the SD model represents gradual adjustment of actual urban land toward that equilibrium.
  
  Wichtig: Das ist **nicht reines AMM**, sondern eine **AMM-inspired dynamic adjustment model**.
  
  ---
- # 5. Mein Urteil
  
  Deine drei Kategorien sind gut. Ich würde sie nur sprachlich leicht schärfen:
- **Parameter dynamics**
  Population, income, transport costs, agricultural rent change over time.
- **Equilibrium recalculation**
  Given those parameters, AMM defines a new spatial equilibrium.
- **Adjustment dynamics**
  Actual built land does not instantly equal equilibrium land, because housing and infrastructure are durable and development takes time.
  
  Das ist die saubere Ordnung.
  
  Der entscheidende Satz für eure Doku wäre:
  
  > 
  
  The Alonso-Muth-Mills model is used as a static spatial equilibrium framework. In the system-dynamics model, changing exogenous drivers shift the AMM-implied equilibrium urban land demand over time, while actual urban land adjusts only gradually due to the durability of built structures and land conversion delays.
  
  Das ist wissenschaftlich gut anschlussfähig und vermeidet die falsche Behauptung, AMM selbst sei ein dynamisches SD-Modell.