
# Datenstrukturen in Blender

Die Datenstrukturen in Blender sind für Python über die bmesh-Datenstrukturen zugänglich. Auf der grundlegendsten Ebene sind vier Hauptelementstrukturen zu finden:

- Faces oder Fläche
- Loops (speichert Daten pro Fläche und Vertex, uvs, vcols, etc)**
- Edges oder Kanten
- Vertex oder Knoten

## Vertices
Diese Datenstruktur speichert eine Koordinate und verweist auf eine Kante im Plattenzyklus des Vertex (siehe unten).

## Edge
Edges stellen eine Verbindung zwischen zwei Knoten dar, speichern aber auch eine Verknüpfung zu einer Loop im radialen Zyklus der Edge (siehe unten).

## Loop
Eine Loop definiert die Begrenzungsschleife einer Face. Jede Loop entspricht logischerweise einer Kante, obwohl die Loop lokal auf eine einzelne Fläche beschränkt ist, so dass es normalerweise mehr als eine Loop pro Edge gibt (außer an den Begrenzungskanten der Oberfläche).

### _Loops speichern mehrere praktische Zeiger_:

e - Zeiger auf den Rand der Loop
v - Zeiger auf den Vertex am Anfang der Edge (wobei "Anfang" durch die CCW-Reihenfolge definiert ist)
f - Zeiger auf die mit dieser Loop verbundene Fläche.
Loops speichern Daten pro Face-Vertex (neben anderen Dingen, die später in diesem Dokument beschrieben werden).

## Faces
Die Flächen verweisen auf eine Loop im Schleifenzyklus, welcher die Circular-Linked-List von Loops ist und die Begrenzung der Face definiert.

## Persistente Flaggen
Jedes Element (Vertex/Edge/Loop/Face) in einem Netz hat ein zugehöriges dauerhaftes Bitfeld. Diese Flags speichern Informationen wie die Sichtbarkeit des Elements oder seinen Auswahlstatus.


# Konnektivitäts-Zyklen (Connectivity Cycles)
Die BMesh-Datenstruktur hat die folgenden Merkmale:
- Dauerhafte Adjazenzinformationen
- Lokal modifizierbare Topologie
- Flächen von beliebiger Länge (N-Gons)
- stellt trivialerweise jede nicht-verzweigte Bedingung dar, einschließlich Drahtkanten (wire edges).

Die zweite bis vierte Eigenschaft hängen alle von der ersten ab, und daher ist das System, das diese Möglichkeit bietet, die Grundlage der bmesh-Datenstruktur. Persistente Adjazenzinformationen werden in einem System von doppelt verknüpften zirkulären Listen gespeichert, die die Beziehungen zwischen den topologischen Einheiten aufrechterhalten. Diese Listen sind konzeptionell identisch mit denen anderer Randdarstellungen wie Half-Edge, Radial Edge und Partial Entity, und wie bei diesen anderen Darstellungen ist jede topologische Einheit selbst ein Knoten in den Zyklen, zu denen sie gehört, so dass der Speicherbedarf für die Speicherung von Adjazenzinformationen minimal bleibt.

Die Verbindungen zwischen den Elementen werden durch Schleifen um topologische Einheiten definiert, die als Zyklen bezeichnet werden. Die Basis eines jeden Zyklus ist die Entität, für die der Zyklus Adjazenzabfragen beantworten soll. Ein Zyklus zur Beantwortung der Frage "Welche Kanten teilen sich diesen Knoten?" würde beispielsweise den Knoten selbst als Basis und seine Kanten als Knoten des Zyklus haben. Beachten Sie, dass es nicht erforderlich ist, alle möglichen Adjazenzbeziehungen explizit zu speichern, und dass vollständige Konnektivitätsinformationen schnell abgeleitet werden können, wenn zwei oder mehr Zyklen in Verbindung miteinander verwendet werden.

Die drei explizit in der bmesh-Struktur gespeicherten Zyklen sind der Scheibenzyklus, der radiale Zyklus und der Schleifenzyklus. Nachfolgend werden die Eigenschaften jedes Zyklus und eine Liste von Funktionen für den Umgang mit ihnen aufgeführt. Es ist wichtig zu beachten, dass die mit einem Sternchen (*) gekennzeichneten Funktionen nicht Teil der Mesh Tools API sind und nur vom Modellierungskernel verwendet werden. Außerdem wurden bei der Auflistung von Strukturdefinitionen bestimmte Mitglieder aus Gründen der Übersichtlichkeit weggelassen.

## Der Scheibenzyklus: Ein Kreis von Kanten um einen Knoten
BASE: BM_EDGE_DISK_LINK_GET(BMEdge *, BMVert *)
## Der Schleifenzyklus: Ein Kreis von Flächenkanten um ein Polygon.
BASE: BM_FACE_FIRST_LOOP(BMFace *)
## Der radiale Zyklus: Ein Kreis von Flächen um eine Kante
BASE: BMEdge->loop->radial structure
