- {{renderer :mermaid_69ea47f2-5d6d-4a45-8067-34ee765f8ae8, 3}}
	- ```mermaid
	  flowchart TD
	  
	  UL[Urban Land]
	  UCD[Urban Capacity / Density]
	  NAE[Net Agglomeration Effect]
	  EC[Economic Conditions]
	  DUL[Desired Urban Land]
	  ULG[Urban Land Gap]
	  LCR[Land Conversion Rate]
	  
	  UL --> UCD --> NAE --> EC --> DUL --> ULG --> LCR --> UL
	  
	  UCD --> CLC[Congestion / Land Costs] --> NEP[negative Economic Pressure] --> EC
	  ALL[Agricultural Land Limit] --> LCR
	  ```
-
-
- # Option 1 — Urban economics / Alonso–Muth–Mills + Sprawl
- ## Warum diese Option stark ist
- Das ist die klassische Kernliteratur zu Stadtfläche, Bodenrenten und räumlicher Ausdehnung. In dieser Tradition expandiert Stadtfläche, wenn sich das Gleichgewicht zwischen Einkommen, Transportkosten, Bodenrenten und Alternativwert des Landes verschiebt. Duranton und Puga beschreiben die vom monocentric model inspirierte Literatur ausdrücklich als den zentralen theoretischen Kern der urban land use economics. Brueckner nennt als klassische Treiber von urban sprawl insbesondere steigende Einkommen, Bevölkerungswachstum und sinkende Transportkosten.
  
  Für euren Fall ist das besonders stark, weil diese Theorie direkt landnutzungslogisch ist. Sie fragt nicht zuerst nach abstraktem Makrowachstum, sondern nach der Bedingung, unter der Land an der urbanen Peripherie von landwirtschaftlicher zu urbaner Nutzung wechselt. Genau damit passt sie sehr gut zu eurem Stock-Flow-Setup mit Agricultural Land, Urban Land und einer Conversion Rate.
- ## Vertiefte wissenschaftliche Betrachtung
- Die zentrale Aussage ist: Urbanisierung ist ein räumliches Gleichgewicht, kein blosser Trend. Haushalte und Firmen wählen Standorte, indem sie Wohnen, Wege, Bodenpreise und Nutzungswert gegeneinander abwägen. Je weiter man sich vom Zentrum entfernt, desto geringer sind meist Bodenpreise, aber desto höher die Pendel- oder Transportkosten. Die Stadtgrenze liegt dort, wo der urbane Bodenwert gerade noch mit dem landwirtschaftlichen Alternativwert konkurrieren kann. Wenn Einkommen steigen, wächst typischerweise die Nachfrage nach Wohnfläche; wenn Transport billiger oder schneller wird, werden periphere Lagen attraktiver; wenn der landwirtschaftliche Bodenwert relativ niedrig ist, fällt die Schwelle zur Umnutzung. Das ergibt einen strukturellen Mechanismus, durch den wirtschaftliche Entwicklung in mehr gewünschte Stadtfläche übersetzt wird.
  
  Für euren Loop ist der entscheidende Punkt: Diese Literatur stützt nicht primär die Aussage
  
  `Land Conversion -> Economic Growth`
  
  sondern deutlich eher
  
  `Economic Effects -> Urban Land Demand -> Land Conversion`
  
  Das ist ein wichtiger Unterschied. Die Theorie sagt nicht, dass jede neue Konversion automatisch Wachstum erzeugt. Sie sagt vielmehr, dass ökonomische Bedingungen die Nachfrage nach urbanem Land und damit die räumliche Ausdehnung beeinflussen. Wenn ihr euch wissenschaftlich möglichst robust absichern wollt, ist das wahrscheinlich die beste Umformulierung eures gelben Loops.
- ## Theoretische Kernlogik
- Nicht:
  
  `Land Conversion -> Economic Growth`
  
  sondern eher:
  
  `Economic Effects -> Urban Land Demand -> Land Conversion`
  
  Noch etwas vollständiger:
  
  `Income, Population, Transport, Policy, Agricultural Land Value -> Desired Urban Land -> Land Conversion`
  
  Die ökonomische Kernaussage lautet: Wirtschaftliche Entwicklung erhöht häufig die Zahlungsbereitschaft für urban genutztes Land relativ zum landwirtschaftlichen Alternativwert; dadurch steigt die gewünschte Stadtfläche.
- ## Hauptaussagen
- Stadtfläche ist ein Gleichgewichtsergebnis aus Einkommen, Pendelkosten, Bodenwerten und nicht-urbanem Alternativwert.
- Steigende Einkommen erhöhen typischerweise den Flächenverbrauch pro Haushalt oder pro Kopf.
- Sinkende Transportkosten und bessere Erreichbarkeit fördern periphere Expansion.
- Die wissenschaftlich passendere Zwischengrösse für euer Modell ist `Urban Land Demand` oder `Desired Urban Land`, nicht direkt `Growth`.
- ## Warum das gut in km²/Jahr endet
- Sehr sauber, weil der Wirtschaftsblock nicht direkt als Faktor auf die Conversion Rate wirkt, sondern zuerst auf eine Flächengrösse in km². Die Rate entsteht danach aus einer Flächenlücke pro Zeit. Systemdynamisch ist das meistens robuster als eine direkte Multiplikation der Rate mit abstrakten Faktoren.
- ## Was den positiven Rückpfeil liefern könnte
- Wenn ihr einen Rückpfeil von `Land Conversion` zu ökonomischen Effekten behalten wollt, dann am ehesten schwach als:
  
  `Land Conversion -> Urban Capacity / Development Space -> Economic Effects`
  
  Also: Neue Siedlungs- und Infrastrukturräume können Entwicklung ermöglichen, aber nicht automatisch und nicht unbegrenzt. Die gleiche Literatur betont auch Gegenkräfte wie längere Wege, infrastrukturelle Kosten und ineffiziente Flächennutzung.
- ## Für euch: Urteil
- Das wäre meine Hauptempfehlung.
  
  Sie ist theoretisch etabliert, in der Stadtökonomik Standard und führt am direktesten zu einer Rate in km²/Jahr.
- ## Relevante Papers / Links
-
- Duranton & Puga, *Urban land use*
- Brueckner, *Urban Sprawl: Lessons from Urban Economics*
- ## Kritik und Kritiker
-
- Monocentric models sind oft zu einfach, weil viele reale urbane Systeme polyzentrisch organisiert sind; die monozentrische Struktur ist analytisch stark, aber empirisch nicht immer passend.
- Die Theorie erklärt die Richtung vieler Mechanismen gut, liefert aber nicht automatisch stabile makroregionale Parameter für einen aggregierten EU27-Block. Das ist eher ein Skalierungs- als ein Grundsatzproblem.
- Klassische Sprawl-Logik kann die Rolle von Planung, Regulierung und institutionellen Brüchen unterschätzen, wenn sie zu stark auf Marktgleichgewichte fokussiert wird.
- ## Konkreter Vensim-Block
- **Idee:** Wirtschaftliche Bedingungen erzeugen eine gewünschte urbane Fläche; Konversion entsteht aus der Lücke zur vorhandenen urbanen Fläche.
  
  ```
  Desired Urban Land = Population * Desired Urban Land per Capita
  Desired Urban Land per Capita = Reference Urban Land per Capita * Income Effect * Transport Effect * Policy Effect * Agricultural Land Value Effect
  Urban Land Gap = MAX(0, Desired Urban Land - Urban Land)
  Economic Conversion Demand = Urban Land Gap / Urban Expansion Adjustment Time
  Land Conversion Rate = MIN(Economic Conversion Demand, Agricultural Land / Minimum Conversion Time)
  ```
- ### Einheiten
-
- `Desired Urban Land = km2`
- `Desired Urban Land per Capita = km2/Person`
- `Urban Land Gap = km2`
- `Economic Conversion Demand = km2/Year`
- `Land Conversion Rate = km2/Year`
- ### Typen
- `Desired Urban Land`: Auxiliary
- `Desired Urban Land per Capita`: Auxiliary
- `Urban Land Gap`: Auxiliary
- `Economic Conversion Demand`: Auxiliary
- `Urban Expansion Adjustment Time`: Constant
- `Land Conversion Rate`: Flow
-
- ### Umsetzung
	- [[Umsetzung Urban economics / Alonso–Muth–Mills + Sprawl Dokumentation]]
- ---
- # Option 2 — Agglomeration economies / Economic geography
- ## Warum diese Option stark ist
- Diese Theorie-Familie erklärt, warum wirtschaftliche Aktivität sich räumlich konzentriert und warum Städte Produktivitätsvorteile bieten können. Duranton und Puga unterscheiden drei grosse Mikrofundierungen: sharing, matching und learning. In dichter urbaner Umgebung können Akteure Infrastruktur, spezialisierte Inputs und Märkte besser teilen, passende Partner leichter finden und Wissen schneller austauschen. Gleichzeitig weisen neuere Übersichten und Meta-Analysen darauf hin, dass Agglomerationsvorteile real sind, aber in der Grössenordnung variieren und durch Überlastung, hohe Bodenpreise und Wohnkosten begrenzt werden.
- ## Vertiefte wissenschaftliche Betrachtung
- Für euren Loop ist das die stärkste Theorie, wenn ihr einen positiven ökonomischen Effekt urbaner Konzentration begründen wollt. Die sauberere Aussage wäre aber nicht:
  
  `Land Conversion -> Economic Growth`
  
  sondern eher:
  
  `Land Conversion -> Urban Capacity / Concentration -> Agglomeration Benefits -> Economic Effects`
  
  Das ist viel näher an der Literatur. Agglomerationstheorie sagt nicht, dass jede Flächenumwandlung gut ist. Sie sagt, dass räumliche Konzentration von Aktivität Produktivitätsvorteile erzeugen kann, solange die positiven Externalitäten grösser sind als die negativen. Sobald Stau, Wohnkosten, Bodenpreise und Überlastung steigen, kippt oder flacht der Nettoeffekt ab. Das macht diese Theorie besonders attraktiv für ein SD-Modell, weil sie euch erlaubt, einen nichtlinearen oder sogar humpenförmigen Zusammenhang zu modellieren statt eines simplen Verstärkers.
- ## Theoretische Kernlogik
- Nicht:
  
  `Land Conversion -> Economic Growth`
  
  sondern eher:
  
  `Land Conversion -> Urban Capacity / Density / Accessibility -> Net Agglomeration Benefits -> Economic Effects -> Urban Land Demand -> Land Conversion`
  
  Die Hauptidee ist: Mehr urbane Entwicklungsfläche kann wirtschaftliche Aktivität ermöglichen, aber der eigentliche Effekt läuft über Produktivität, Spezialisierung und Koordination, nicht bloss über die physische Tatsache der Flächenumwandlung.
- ## Hauptaussagen
-
- Städte erzeugen potenziell Produktivitätsvorteile über sharing, matching, learning.
- Agglomerationseffekte sind empirisch breit belegt, aber ihre Grösse ist heterogen und methodisch sensibel.
- Positive Agglomeration wird durch congestion, Wohnkosten und Bodenpreise begrenzt.
- Für euer Modell passt daher eher eine Netto-Grösse wie `Net Urban Economic Attractiveness` oder `Net Agglomeration Effect` als ein direkter `Growth`-Pfeil.
- ## Warum das gut in km²/Jahr endet
- Auch hier sollte der ökonomische Mechanismus nicht direkt in die Rate gehen. Stattdessen erzeugt der Netto-Agglomerationseffekt eine Veränderung in `Desired Urban Land` oder `Additional Urban Land Demand`, die dann in `km2/Year` überführt wird.
- ## Was den positiven Rückpfeil liefern könnte
- Das ist gerade die Stärke dieser Option:
  
  `Land Conversion -> Urban Capacity -> Agglomeration Benefits -> Economic Effects`
  
  Allerdings sollte parallel immer ein negativer Pfad mitlaufen:
  
  `Urban Scale -> Congestion / Land Cost -> negative Economic Effects`
- ## Für euch: Urteil
- Sehr starke Ergänzungs- oder Alternativoption, besonders wenn ihr den positiven Teil des Loops theoretisch begründen wollt, ohne euch auf den zu direkten Satz `mehr Landumwandlung = mehr Wachstum` festzulegen.
- ## Relevante Papers / Links
-
- Duranton & Puga, *Micro-foundations of urban agglomeration economies*
- Donovan et al., *A meta-analysis of agglomeration economies*
- Parr, *Agglomeration Economies: Ambiguities and Confusions*
- ## Kritik und Kritiker
-
- Der Begriff `Agglomeration economies` ist konzeptionell oft unscharf; Parr kritisiert genau diese begrifflichen Unklarheiten.
- Empirische Schätzungen sind stark methodensensibel; Meta-Analysen zeigen teils deutlich kleinere Effekte, wenn bessere Kontrollen genutzt werden.
- Agglomerationsvorteile gelten nicht unbegrenzt; congestion und Bodenkosten können sie teilweise neutralisieren.
- ## Konkreter Vensim-Block
- **Idee:** Urbanisierung verbessert zunächst Agglomerationsbedingungen, aber nur netto nach Abzug von Überlastungskosten.
  
  ```
  Agglomeration Benefit Index = (Urban Population / Reference Urban Population) ^ Agglomeration Elasticity
  Congestion Cost Index = (Urban Land Pressure / Reference Urban Land Pressure) ^ Congestion Elasticity
  Net Urban Economic Attractiveness = Agglomeration Benefit Index / Congestion Cost Index
  Desired Urban Land = Reference Urban Land * Net Urban Economic Attractiveness * Population Effect * Policy Effect
  Urban Land Gap = MAX(0, Desired Urban Land - Urban Land)
  Economic Conversion Demand = Urban Land Gap / Urban Expansion Adjustment Time
  Land Conversion Rate = MIN(Economic Conversion Demand, Agricultural Land / Minimum Conversion Time)
  ```
- ### Einheiten
-
- `Agglomeration Benefit Index = dmnl`
- `Congestion Cost Index = dmnl`
- `Net Urban Economic Attractiveness = dmnl`
- `Desired Urban Land = km2`
- `Economic Conversion Demand = km2/Year`
- ### Typen
-
- alle Indizes: Auxiliary
- Elastizitäten: Constants
- `Land Conversion Rate`: Flow
  
  ---
- # Option 3 — Land-take / urban expansion driver literature
- ## Warum diese Option stark ist
- Diese Literatur ist weniger stark mikrofundiert als Option 1, aber für eure Modellfrage oft am nächsten an der empirischen Praxis. Colsaet et al. werten 193 Studien aus und identifizieren als häufige und robuste Treiber von land take und urban land expansion insbesondere Bevölkerung, GDP und Transportinfrastruktur; ausserdem spielen Politikfaktoren wie Planung, Fragmentierung und Subventionen eine Rolle. Diese Literatur ist damit besonders anschlussfähig an einen EU27-Makroblock, weil sie direkt fragt, welche Treiber Flächeninanspruchnahme empirisch bewegen.
- ## Vertiefte wissenschaftliche Betrachtung
- Für euch ist diese Option stark, weil sie offen mit Multikausalität arbeitet. Sie zwingt euch nicht dazu, einen einzigen dominanten ökonomischen Mechanismus als Theoriezentrum zu nehmen. Stattdessen könnt ihr die Konversion als Ergebnis mehrerer Treiber modellieren:
  
  `Economic Effects + Population + Infrastructure + Policy -> Additional Urban Land Demand -> Land Conversion`
  
  Wissenschaftlich ist das attraktiv, weil Landumwandlung in der empirischen Literatur selten monokausal erklärt wird. Gerade im europäischen Kontext sind Governance, Fragmentierung, Raumplanung und Infrastruktur häufig genauso wichtig wie Einkommen oder GDP. Die Hauptstärke dieser Option ist daher nicht elegante Theorie, sondern gute empirische Anschlussfähigkeit.
- ## Theoretische Kernlogik
- Nicht:
  
  `Land Conversion -> Economic Growth`
  
  sondern eher:
  
  `Economic Effects + Population + Infrastructure + Policy -> Additional Urban Land Demand -> Land Conversion`
  
  Das ist eine driver-based Formulierung. Für ein System-Dynamics-Modell ist das oft nützlich, weil ihr so mehrere bekannte Treiber kombinieren könnt, ohne falsche Scheingenauigkeit vorzutäuschen.
- ## Hauptaussagen
-
- Land take wird häufig von Bevölkerungswachstum, GDP und Verkehrsinfrastruktur mitgetrieben.
- Politische und institutionelle Faktoren können Expansion stark verstärken oder dämpfen.
- Urban expansion ist typischerweise multikausal.
- Für euer Modell passt daher besonders gut eine Zielgrösse wie `Additional Urban Land Demand [km2/yr]`.
- ## Warum das gut in km²/Jahr endet
- Diese Option endet fast direkt dort, wo ihr hinwollt: bei einer zusätzlichen Flächennachfrage in `km2/Year`. Deshalb ist sie operational sehr attraktiv.
- ## Was den positiven Rückpfeil liefern könnte
- Hier würde ich den Rückpfeil eher schwach halten. Die Literatur ist in erster Linie darauf ausgerichtet, Treiber von Expansion zu identifizieren, nicht zu zeigen, dass Konversion selbst wieder stark positive ökonomische Effekte zurückspeist. Wenn ihr einen Rückpfeil wollt, dann eher über `development momentum` oder `infrastructure lock-in`.
- ## Für euch: Urteil
- Sehr gute empirisch-pragmatische Hauptoption, wenn ihr einen EU27-tauglichen Makroblock wollt, der fachlich gut verankert und relativ direkt modellierbar ist.
- ## Relevante Papers / Links
-
- Colsaet et al., *What drives land take and urban land expansion? A systematic review*
- Marquard et al., *Land Consumption and Land Take: Enhancing Conceptual Clarity*
- ## Kritik und Kritiker
- Die Begriffe `land take`, `land consumption` und `sprawl` sind konzeptionell nicht überall deckungsgleich; Marquard et al. verlangen gerade deshalb mehr begriffliche Klarheit im EU-Kontext.
- Die Literatur ist stark kontextabhängig; sie liefert robuste Treiber, aber keine universelle Einheitsfunktion.
- Als Modellbasis ist sie oft gut operationalisierbar, aber weniger stark theoretisch fundiert als Urban Economics. Das ist eher eine Begrenzung als eine Widerlegung.
- ## Konkreter Vensim-Block
- **Idee:** Bekannte Expansionstreiber erzeugen eine zusätzliche Flächennachfrage pro Jahr.
  
  ```
  Economic Land Demand = Reference Economic Land Demand * GDP Effect
  Population Land Demand = Reference Population Land Demand * Population Effect
  Infrastructure Land Demand = Reference Infrastructure Land Demand * Infrastructure Effect
  Policy Land Demand Reduction = Reference Policy Land Demand Reduction * Spatial Planning Effect
  Additional Urban Land Demand = MAX(0, Economic Land Demand + Population Land Demand + Infrastructure Land Demand - Policy Land Demand Reduction)
  Land Conversion Rate = MIN(Additional Urban Land Demand, Agricultural Land / Minimum Conversion Time)
  ```
- ### Einheiten
- alle Demand-Komponenten = `km2/Year`
- `Additional Urban Land Demand = km2/Year`
- `Land Conversion Rate = km2/Year`
- ### Typen
- Demand-Komponenten: Auxiliaries
- Referenzwerte: Constants
- `Land Conversion Rate`: Flow
  
  ---
- # Option 4 — Structural change / sectoral reallocation
- ## Warum diese Option stark ist
- Diese Option ist besonders relevant, wenn ihr die EU27 als makroskopisches Gesamtsystem modelliert. Eckert und Peters entwickeln eine Theorie der spatial structural change, in der Wachstum, sektorale Transformation und räumliche Reallokation gemeinsam bestimmt werden. Neuere Arbeiten zu structural change, land use and urban expansion argumentieren explizit, dass mit wirtschaftlicher Entwicklung Land zwischen Landwirtschaft und urbaner Nutzung umgeschichtet wird und Städte dabei räumlich expandieren können.
- ## Vertiefte wissenschaftliche Betrachtung
- Der Kern dieser Perspektive ist: Urban expansion ist nicht nur ein Effekt steigender Einkommen oder billigerer Mobilität, sondern Ausdruck tieferer struktureller Transformation. Wenn Volkswirtschaften sich von agrarischer Produktion zu Industrie und Dienstleistungen verschieben, wandern nicht nur Arbeit und Kapital, sondern auch Landnutzungen. Im sehr langen Lauf kann dadurch Landwirtschaft relativ an Gewicht verlieren und städtisch geprägte Nutzungen an Fläche gewinnen. Für euren EU27-Block ist das attraktiv, weil es die Konversion von Agricultural Land zu Urban Land als Teil eines grösseren Entwicklungsprozesses interpretiert.
  
  Der Nachteil ist allerdings genauso wichtig: Diese Option ist oft zu indirekt für eine konkrete jährliche Conversion Rate, wenn sie alleine steht. Sie ist hervorragend als Makro-Rahmung, aber weniger präzise als Option 1 oder 3, wenn es um `km2/Year` geht.
- ## Theoretische Kernlogik
- Nicht:
  
  `Land Conversion -> Economic Growth`
  
  sondern eher:
  
  `Structural Change -> Urban Activity Demand -> Urban Land Demand -> Land Conversion`
  
  Oder noch breiter:
  
  `Economic Development -> Sectoral Reallocation -> Land Reallocation -> Urban Expansion`
- ## Hauptaussagen
- Wachstum und sektoraler Wandel sind räumlich gekoppelt; sie verschieben Aktivität zwischen Regionen und Sektoren.
- Diese Reallokation betrifft nicht nur Arbeit, sondern auch Landnutzung.
- Urban expansion kann als Ausdruck langfristiger struktureller Transformation gelesen werden.
- Für euer Modell ist das stark als Makro-Rahmung, aber schwächer als unmittelbare jährliche Flussgleichung.
- ## Warum das gut in km²/Jahr endet — und wo die Grenze liegt
- Es endet gut in `km2/Year`, wenn ihr noch einen zusätzlichen Übersetzungsschritt einbaut, der aus strukturellem Wandel eine konkrete Veränderung von `Urban Activity Demand` oder `Desired Urban Land` macht. Allein ist diese Theorie dafür zu grob.
- ## Was den positiven Rückpfeil liefern könnte
- Wenn ihr einen Rückpfeil wollt, wäre er hier eher systemisch:
  
  `Land Conversion -> More Urban Activity Capacity -> supports Structural Shift`
  
  Aber auch das sollte vorsichtig modelliert werden; die Literatur stellt stärker den langfristigen gemeinsamen Wandel heraus als einen unmittelbaren Verstärker.
- ## Für euch: Urteil
- Sehr gute Makro-Hintergrundoption für das EU27-Modell, aber wahrscheinlich nicht die beste alleinige Struktur für euren Conversion-Flow. Am überzeugendsten ist sie als Rahmung plus Kombination mit Option 1 oder 3.
- ## Relevante Papers / Links
-
- Eckert & Peters, *Spatial Structural Change*
- Coeurdacier et al., *Structural Change, Land Use and Urban Expansion*
- ## Kritik und Kritiker
- Die Perspektive ist für langfristige Erklärung stark, aber für konkrete jährliche Landumwandlungsraten oft zu indirekt.
- Ein Teil der direkteren Land-use-Literatur in dieser Familie ist neu; sie ist vielversprechend, aber noch weniger kanonisch als Alonso-Muth-Mills oder klassische Sprawl-Literatur.
- Für praktische Modellierung braucht ihr fast immer eine zusätzliche Zwischenvariable wie `Urban Activity Demand` oder `Desired Urban Land`. Das ist eher eine Modellanforderung als inhaltliche Kritik.
- ## Konkreter Vensim-Block
- **Idee:** Struktureller Wandel verschiebt Aktivität in Richtung urbaner Sektoren; daraus folgt zusätzlicher urbaner Flächenbedarf.
  
  ```
  Urban Activity Share = Reference Urban Activity Share * Structural Change Effect
  Urban Activity Demand = Urban Activity Share * Population * Urban Space per Activity Unit
  Desired Urban Land = Urban Activity Demand / Urban Activity Density
  Urban Land Gap = MAX(0, Desired Urban Land - Urban Land)
  Economic Conversion Demand = Urban Land Gap / Urban Expansion Adjustment Time
  Land Conversion Rate = MIN(Economic Conversion Demand, Agricultural Land / Minimum Conversion Time)
  ```
- ### Einheiten
- `Urban Activity Share = dmnl`
- `Urban Activity Demand = activity units`
- `Urban Space per Activity Unit = km2/activity unit`
- `Desired Urban Land = km2`
- `Economic Conversion Demand = km2/Year`
- ### Typen
- `Urban Activity Share`: Auxiliary
- `Structural Change Effect`: Auxiliary or Constant
- `Desired Urban Land`: Auxiliary
- `Land Conversion Rate`: Flow
  
  ---
- # Option 1 und Option 2 als gekoppelte Ketten / Loops
- Urban Land
    -> Urban Capacity / Density
      -> Net Agglomeration Effect
        -> Economic Conditions
          -> Desired Urban Land
            -> Urban Land Gap
              -> Land Conversion Rate
                -> Urban Land
- ## Gegenpfade (balancing)
- Urban Capacity / Density
  -> Congestion / Land Costs
    -> negative Economic Pressure
      -> Economic Conditions (−)
  
  Urban Land
  -> Urban Land Gap (−)
    -> Land Conversion Rate (−)
  
  Agricultural Land Limit
  -> Land Conversion Rate (−)
- ---
- (+)
  Urban Land ---------> Urban Capacity / Density
      ^                        |
      |                        v
      |              Net Agglomeration Effect
      |                        |
      |                        v
      |              Economic Conditions
      |                        |
      |                        v
      |              Desired Urban Land
      |                        |
      |                        v
      |                 Urban Land Gap
      |                        |
      |                        v
      +-------- Land Conversion Rate
- ## Balancing loops
- Urban Capacity / Density
    -> Congestion / Land Costs
    -> Economic Conditions (−)
  
  Urban Land
    -> Urban Land Gap (−)
    -> Land Conversion Rate (−)
  
  Agricultural Land Limit
    -> Land Conversion Rate (−)
- ---
- ## Option 1 — Urban land demand / Conversion-Kette
- Option 1 beschreibt primär die **Vorwärtskette von ökonomischen Bedingungen zu Landkonversion**:
  
  ```
  Economic Conditions
  -> Desired Urban Land
  -> Urban Land Gap
  -> Land Conversion Rate
  -> Urban Land
  ```
  
  Inhaltlich:
- Einkommen, Bevölkerung, Erreichbarkeit und Bodenpreise bestimmen die **gewünschte urbane Fläche**
- Die Differenz zwischen gewünschter und vorhandener Fläche erzeugt **Konversionsdruck**
- Daraus folgt **Land Conversion** (Agricultural -> Urban Land)
- ### Rückläufige Richtung (balancing)
- ```
  Urban Land steigt
  -> Urban Land Gap sinkt
  -> Land Conversion Rate sinkt
  ```
  
  Interpretation:
- Je näher `Urban Land` an `Desired Urban Land` liegt, desto schwächer wird die weitere Expansion
- Das ist ein **klassischer balancing mechanism**
  
  ---
- ## Option 2 — Agglomeration / Economic Feedback Loop
- Option 2 beschreibt den **Rückpfeil von Urbanisierung zu ökonomischen Bedingungen**:
  
  ```
  Urban Land / Urban Density / Urban Capacity
  -> Agglomeration Benefits
  -> Economic Effects
  -> Economic Conditions
  ```
  
  Inhaltlich:
- Mehr urbane Dichte/Kapazität erzeugt:
	- sharing
	- matching
	- learning
- Daraus entstehen **Produktivitäts- und Attraktivitätsgewinne**
- ### Rückläufige Richtung (balancing)
  
  ```
  Urban Scale / Density
  -> Congestion / Land Costs / Housing Costs
  -> Net Agglomeration Effect sinkt
  -> Economic Effects sinken
  ```
  
  Interpretation:
- Agglomeration wirkt **nicht unbegrenzt positiv**
- Ab einem Punkt dominieren:
	- Stau
	- hohe Bodenpreise
	- steigende Wohnkosten
	  
	  ---
- ## Schnittstelle der beiden Optionen
  
  Die Verbindung liegt bei:
  
  ```
  Economic Conditions
  ```
- **Option 2 produziert** ökonomische Bedingungen
- **Option 1 konsumiert** diese als Input für Landnachfrage
  
  Zusätzlich indirekt:
  
  ```
  Desired Urban Land
  ```
  
  ---
- ## Gekoppelter Gesamtloop
-
- ## Reinforcing Loop (positiv)
- ```
  Urban Land
  -> Urban Capacity / Density
  -> Net Agglomeration Effect
  -> Economic Conditions
  -> Desired Urban Land
  -> Urban Land Gap
  -> Land Conversion Rate
  -> Urban Land
  ```
  
  Interpretation:
- Mehr Urban Land -> bessere ökonomische Bedingungen
- bessere Bedingungen -> mehr Nachfrage nach Urban Land
- mehr Nachfrage -> mehr Konversion
- → selbstverstärkender Prozess
  
  ---
- ## Balancing Counter-Loop (negativ)
- ```
  Urban Land / Density
  -> Congestion / Land Costs
  -> Net Agglomeration Effect sinkt
  -> Economic Conditions sinken
  -> Desired Urban Land sinkt
  -> Land Conversion Rate sinkt
  ```
  
  Interpretation:
- Wachstum erzeugt **Gegenkräfte**
- Diese bremsen Expansion systemisch