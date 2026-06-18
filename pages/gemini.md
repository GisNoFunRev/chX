# Die zeitliche Dimension des Alonso-Muth-Mills (AMM) Modells: Einordnung und Literaturrecherche

Das klassische Alonso-Muth-Mills-Modell (AMM) ist von Natur aus ein statisches Gleichgewichtsmodell. Es beschreibt einen Zustand, in dem sich alle Akteure (Haushalte, Entwickler, Grundbesitzer) perfekt und ohne Transaktionskosten an exogene Parameter angepasst haben.

Die von Ihnen identifizierten drei zeitlichen Phänomene beschreiben die wesentlichen Friktionen und Dynamiken realer urbaner Räume. Im Folgenden werden diese drei Dimensionen systematisch eingeordnet und anschließend im Rahmen einer Literaturrecherche analysiert, wie die Wissenschaft diese zeitlichen Komponenten modelliert hat.
- ## Teil 1: Systematische Einordnung Ihrer drei Beobachtungen
  
  Die drei von Ihnen genannten Dynamiken lassen sich hervorragend als unterschiedliche **Zeitskalen (Time Scales)** und **Marktmechanismen** innerhalb eines dynamischen stadtökonomischen Systems einordnen. Sie repräsentieren das Zusammenspiel von kurzfristigen Preissignalen, mittelfristigen Nachfrageverschiebungen und extrem langfristigen strukturellen Anpassungen.
  
  ```
  [ SCHNELL ]  ------------->  [ MITTELFRISTIG ]  ------------->  [ SEHR LANGSAM ]
       Preisdynamik                  Populationsdynamik                 Inertia / Trägheit
  (Sofortiges Clearing)             (Demografischer Wandel)           (Physischer Umbau der Stadt)
  ```
- ### 1. Preisdynamik (Die kurzfristige Anpassung / Fast-Moving Variable)
- **Einordnung:** Die Preis- und Mietdynamik ist das am schnellsten reagierende Element im System. Während Gebäude Jahrzehnte stehen, können sich Mieten und Bodenpreise bei Nachfrageschocks (z. B. plötzlicher Zuzug, Zinsänderungen) innerhalb von Monaten oder gar Wochen anpassen.
- **Wirkungsweise im AMM-Kontext:** Wenn sich die Rahmenbedingungen ändern, reagiert zuerst der Preisgradient (die Bid-Rent-Kurve). Er verschiebt oder steilt sich auf, um den Markt kurzfristig zu räumen (Market Clearing), noch bevor auch nur ein einziges neues Gebäude gebaut oder abgerissen werden kann.
- ### 2. Populationsdynamik (Die mittelfristige Anpassung / Medium-Term Variable)
- **Einordnung:** Demografische Entwicklungen, Zu- und Abwanderung (Migration) sowie Verschiebungen in den Haushaltsstrukturen (z. B. Trend zu Single-Haushalten) vollziehen sich mittelfristig (Monate bis Jahre).
- **Wirkungsweise im AMM-Kontext:** Die Population $N$ ist im klassischen AMM-Modell entweder fixiert (geschlossene Stadt) oder vollkommen elastisch durch Migration reguliert (offene Stadt, in der das Nutzenniveau an das Umland gekoppelt ist). Reale Populationsdynamiken erzeugen kontinuierliche Verschiebungen der Nachfragekurve, auf die das System reagieren muss. Sie bestimmen die Gesamtgröße der Stadt und den Druck auf den Wohnungsmarkt.
- ### 3. Trägheit & Transition: Ist- vs. Soll-Zustand (Die langfristige Anpassung / Slow-Moving Variable)
- **Einordnung:** Dies ist die fundamentale physikalische Friktion der Stadt. Gebäude sind extrem langlebige Güter ("durable housing capital"). Einmal gegossener Beton kann nicht ohne enorme Kosten (Sunk Costs) umgeformt werden.
- **Wirkungsweise im AMM-Kontext:** Das klassische AMM-Modell ist ein "Putty-Putty"-Modell (Kapital ist wie Knete: jederzeit formbar). Die Realität ist jedoch ein "Putty-Clay"-System (Kapital ist anfangs formbar, erstarrt dann aber wie Ton zu festen Gebäuden). Der Ist-Zustand hinkt dem Soll-Zustand (dem theoretischen Gleichgewicht) oft um Jahrzehnte hinterher. Dies führt zu historischen "Schichten" (Vintages) in der Stadtstruktur: Dichten und Gebäudetypen im Stadtzentrum spiegeln oft das Gleichgewicht des 19. oder frühen 20. Jahrhunderts wider, nicht das von heute.
- ## Teil 2: Literaturrecherche – Wie geht die Wissenschaft mit diesen Dynamiken um?
  
  Die theoretische und quantitative Stadtökonomie hat verschiedene Modellklassen entwickelt, um die statische Natur des AMM-Modells aufzubrechen. Im Folgenden wird dokumentiert, wie die Literatur Ihre drei Beobachtungen mathematisch und algorithmisch gelöst hat.
- ### 1. Die Modellierung von Langlebigkeit und Trägheit ("Durable Capital" & "Vintages")
  
  Die Pionierarbeit zur Einführung von Trägheit in das AMM-Modell begann in den 1970er und 1980er Jahren. Die Kernfrage war: Wie wächst eine Stadt, wenn einmal gebaute Strukturen nicht mehr verändert werden können?
- **Harrison & Kain (1974) – "Cumulative Urban Growth":**
  
  In ihrer bahnbrechenden Arbeit zeigten sie, dass die Dichte einer Stadt ein historisches Akkumulationsprodukt ist. Sie argumentierten, dass die Dichte in jedem Bezirk zum Zeitpunkt des Baus fixiert wird und sich danach kaum noch verändert. Die heutige Stadtstruktur ist demnach das "fossile" Abbild einer Serie historischer Gleichgewichte.
- **Brueckner (1980) – "A Vintage Model of Residential Growth" (Journal of Urban Economics):**
  
  Jan Brueckner formalisierte dieses Konzept mathematisch. Er entwickelte ein Modell, in dem Gebäude eine unendliche Lebensdauer haben, es sei denn, sie werden aktiv abgerissen. Er zeigte, dass das Städtewachstum am Stadtrand (Urban Fringe) stattfindet, während das Zentrum in seiner historischen Dichte "eingefroren" bleibt.
- **Wheaton (1982) – "Urban Spatial Growth with Durable Structure" (American Economic Review):**
  
  William Wheaton führte das "Putty-Clay"-Modell in die Stadtökonomie ein. Er bewies mathematisch, dass in einer wachsenden Stadt mit langlebigen Gebäuden die Bodenpreise im Zentrum stetig steigen, ohne dass sofort eine Verdichtung stattfindet. Eine Neubebauung (Redevelopment) findet erst statt, wenn der Bodenwert unter einer neuen, dichteren Nutzung die Kosten für den Abriss des alten Gebäudes plus dessen entgangenen Restwert übersteigt.
- **Capozza & Helsley (1989) – "The Fundamentals of Land Prices and Urban Growth":**
  
  Dieses Papier integrierte die Unsicherheit in die zeitliche Dimension. Sie wendeten die **Realoptions-Theorie** auf die Stadtentwicklung an. Da die Bebauung unumkehrbar ist (Irreversibilität), haben Entwickler einen Anreiz, mit der Bebauung zu warten (Option to Wait), selbst wenn das statische AMM-Modell bereits eine Bebauung vorschreiben würde. Dies erklärt, warum der Ist-Zustand systematisch hinter dem Soll-Zustand zurückbleibt.
- ### 2. Die Modellierung von Preis- und Populationsdynamiken
  
  Wenn Populationen und Einkommen schwanken, verändern sich auch die Mieten. Die Wissenschaft musste Wege finden, diese Schocks über die Zeit hinweg zu simulieren.
- **Braid (1988) – "The Trajectory of Land Prices in a Developing City":**
  
  Braid untersuchte den genauen zeitlichen Pfad von Bodenpreisen und Mieten, wenn die Bevölkerung kontinuierlich wächst. Er zeigte, dass Erwartungshaltungen über zukünftiges Populationswachstum bereits in den heutigen Bodenpreisen eingepreist sind, was zu Spekulationsgaps führt.
- **Anas (1982) – "Residential Location Markets and Urban Transportation":**
  
  Alex Anas entwickelte eines der ersten dynamischen, quantitativen Modelle (das sogenannte METROPOLIS-Framework). Er kombinierte das AMM-Modell mit diskreten Entscheidungsmodellen (Discrete Choice) für Haushalte. Hier reagieren die Akteure nicht instantan, sondern verzögert auf Preis- und Populationsänderungen. Seine Simulationen zeigten, dass Preisschocks im Wohnungsmarkt zyklische Wellenbewegungen auslösen können, da die Angebotsseite (Bauwirtschaft) zeitlich verzögert reagiert (Schweinezyklus im Wohnungsbau).
- ### 3. Moderne Ansätze: Quantitative Spatial Models (QSM) & Agentenbasierte Modelle (ABM)
  
  In den letzten 15 Jahren hat sich die Forschung von rein analytischen Gleichungen wegbewegt hin zu computergestützten, dynamischen Modellen, die direkt auf realen Geodaten kalibriert werden.
- **Ahlfeldt, Redding, Sturm & Wolf (2015) – "The Economics of Density: Evidence from the Berlin Wall" (Econometrica):**
  
  Obwohl dieses Modell strukturell auf einem statischen Gleichgewicht basiert, nutzen die Autoren den extremen historischen Schock der Berliner Mauer (Teilung und Wiedervereinigung), um die dynamischen Anpassungspfade von Bodenpreisen und Beschäftigung über die Zeit zu schätzen. Sie zeigen, wie sich die Stadtstruktur über Jahrzehnte hinweg langsam entlang der neuen "Soll-Pfade" reorganisiert.
- **Desmet & Rossi-Hansberg (2014) – "Spatial Development" (American Economic Review):**
  
  Diese Autoren entwickelten eines der führenden makro-räumlichen dynamischen Modelle. Sie modellieren kontinuierliche Zeitpfade, in denen sich Technologie, Transportkosten und Populationen über die Zeit verändern. Haushalte migrieren jedes Jahr neu, um ihren Nutzen zu maximieren, während Firmen in Technologie investieren. Dieses Modell löst die Statik des AMM-Modells vollständig auf, indem es endogenes Wachstum und räumliche Dynamik verknüpft.
- **ALMA & agentenbasierte Stadtmodelle (z. B. Filatova et al., 2009):**
  
  Agentenbasierte Modelle (ABMs) brechen radikal mit dem Diktat des perfekten Gleichgewichts. Agenten (Käufer, Verkäufer) agieren mit begrenzter Information (bounded rationality) und suchen aktiv nach Wohnungen. Die **Preisdynamik** entsteht hier emergent durch Verhandlungen (Bid-Ask-Spreads). Die **Trägheit** wird dadurch abgebildet, dass Transaktionen Zeit kosten und Verträge bindend sind. Der Ist-Zustand fluktuiert ständig um ein dynamisches Soll-Gleichgewicht herum, erreicht es aber fast nie ganz.
- ## Fazit für Ihre Modellierung
  
  Wenn Sie städtische Dynamiken in **Python** oder **Vensim** modellieren wollen, spiegeln Ihre drei Punkte exakt die Programmierlogik wider:
- **Vensim (System Dynamics):** Eignet sich hervorragend für die Verzögerungsschleifen (Delays) zwischen dem Soll-Zustand (Signal) und dem Ist-Zustand (Baufertigstellung). Die Preisdynamik wird über Feedback-Loops (Angebot-Nachfrage-Preis-Spirale) gesteuert.
- **Python (z.B. NEDUM-2D oder eigene Simulationen):** Hier können Sie "Putty-Clay"-Kapital explizit codieren. Ein einmal bebautes Rasterpixel (Grid-Zelle) behält seine Dichte für eine definierte Anzahl von Simulationsschritten (z. B. Lebensdauer von 50 Jahren), während sich die Mieten in jedem Zeitschritt über einen Marktbereinigungsalgorithmus (z. B. Gradient Descent) rasant an die aktuelle Populationsgröße anpassen.