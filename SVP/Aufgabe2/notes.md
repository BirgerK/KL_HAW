# Gefundene Fehler
Die Zeilennummerierung bezieht sich auf die Original-Datei. In der korrigierten Form sind die Zeilen etwas verschoben.
## Syntaktische Fehler
* Zeile: 31-32  
  Entdeckt durch Syntax-Kontrolle von FDR3  
  Macht sich bemerkbar, indem FDR3 die Datei nicht einlesen kann  
  Behoben durch die Definition des Datentyps
* Zeile: 77  
  Entdeckt durch Syntax-Kontrolle von FDR3  
  Macht sich bemerkbar, indem FDR3 die Datei nicht einlesen kann  
  Behoben durch Übergeben von Argumenten an die Prozesse `READ_INDEX` und `WRITE_INDEX`
* Zeile: 170
  Entdeckt durch Syntax-Kontrolle von FDR3  
  Macht sich bemerkbar, indem FDR3 die Datei nicht einlesen kann  
  Behoben durch ersetzen von `;` durch `->`
* Zeile: 145
  Entdeckt durch Syntax-Kontrolle von FDR3  
  Macht sich bemerkbar, indem FDR3 die Datei nicht einlesen kann  
  Behoben durch ersetzen von `=` durch `==`
* Zeile: 173
  Entdeckt durch Syntax-Kontrolle von FDR3  
  Macht sich bemerkbar, indem FDR3 die Datei nicht einlesen kann  
  Behoben durch ersetzen von `;` durch `->`
* Zeile: 194  
  Entdeckt durch Syntax-Kontrolle von FDR3  
  Macht sich bemerkbar, indem FDR3 die Datei nicht einlesen kann  
  Vervollständigen mit `|`. Erklärung: Schreibt man `M = { rd_ri,rd_wi,wr_ri,wr_wi }`, dann enthält `M`, die Mengen `möglicher Wertebereich von rd_ri`, `möglicher Wertebereich von rd_wi`, `möglicher Wertebereich von wr_ri`und `möglicher Wertebereich von wr_wi`. Ergänzt man die geschweiften Klammern mit `|`, dann enthält `M` nicht die Mengen, sondern die konkreten Werte von `rd_ri`, `rd_wi`, `wr_ri`und `wr_wi`.

## Semantische Fehler
* Zeile: 55  
  Entdeckt durch Fehlschlagen von Test Nr.2  
  Behoben durch Entfernen des Elements `process_rd` aus dem Prozess `READ_ABS`.
* Zeile: 77-79  
  Entdeckt durch Fehlschlagen von Test Nr.1  
  Behoben durch das geschickte Einbinden des Prozesses `CBUF` im Prozess in `SYS_CON`.
* Zeile: 98-100  
  Entdeckt durch "Überlegen wie die Prozesse funktionieren sollen"  
  Der Fehler macht sich bemerkbar, indem Tests fehlschlagen  
  Behoben durch Ersetzen von `WRITE_INDEX` durch `READ_INDEX` und teilweises Ersetzen von `i` durch `x`.
* Zeile: 147  
  Entdeckt durch Lesen der Prozess-Spezifikation - steht über dem Prozess als Kommentar geschrieben. Dort fällt auf, dass der `if`- und `else`-Funktionsblock miteinander getauscht werden müssen.  
  Behoben durch Austauschen der `if`- und `else`-Funktionsblöcke.
* Zeile: 168  
  Entdeckt durch Lesen der Prozess-Spezifikation - steht über dem Prozess als Kommentar geschrieben. Dort fällt auf, dass der zu vergleichende Term nicht mit der If-Bedingung übereinstimmt.  
  Behoben durch inkrementieren von `y` bevor Modulo mit `max+1`
