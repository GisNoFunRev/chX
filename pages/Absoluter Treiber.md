## Absoluter Treiber

**Beschreibung**

Ein absoluter Treiber ist eine Variable, die mit ihrem direkten, realen Wert auf eine andere Groesse wirkt. Sie wird also nicht zuerst normiert oder relativiert, sondern geht als absolute Menge in die Modelllogik ein. In einem System-Dynamics-Modell bedeutet das: Die Wirkung haengt unmittelbar von der Groessenordnung der Variable selbst ab.

**Warum er wichtig ist**

Ein absoluter Treiber eignet sich dann, wenn wirklich die absolute Hoehe einer Groesse relevant ist. Wenn zum Beispiel mehr Bevoelkerung direkt mehr Flaechenbedarf erzeugt, dann ist `Population` ein typischer absoluter Treiber. Das Modell sagt dann nicht: "Wie stark ist die Bevoelkerung im Vergleich zu frueher?", sondern: "Wie gross ist sie tatsaechlich?"

**Beispiel**

Wenn ihr schreibt:
- `Agrotechnological Progress = Urban Land * Faktor`
  
  dann wirkt `Urban Land` als absoluter Treiber. Die absolute Zahl der urbanen Flaeche treibt die andere Variable direkt.
  
  **Merksatz**
  
  Ein absoluter Treiber wirkt mit seinem echten, direkten Wert.