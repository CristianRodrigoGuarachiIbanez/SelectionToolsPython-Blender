#  BMesh-Modul (bmesh)
Dieses Modul ermöglicht den Zugriff auf Blenders bmesh-Datenstrukturen.

## Einführung
Hierbei handelt es sich um API, welche den Zugriff auf die Blender-interne Mesh-Editing-API ermöglicht. Diese enthält Geometriekonnektivitätsdaten und Zugriff auf Editieroperationen wie Split, Separate, Collapse und Dissolve.
Die dargestellten Features sind eng an die C-API angelehnt und geben Python Zugriff auf die Funktionen, die von Blenders eigenen Mesh-Editing-Tools verwendet werden.


## Eigenständiges Modul
Das BMesh-Modul ist so geschrieben, dass es eigenständig ist, mit Ausnahme von mathutils, das für Vertexpositionen und Normalen verwendet wird. Die einzige andere Ausnahme ist die Konvertierung von Mesh-Daten in und aus bpy.types.Mesh.

## Mesh-Zugriff
Es gibt zwei Möglichkeiten, auf BMesh-Daten zuzugreifen: 

- Durch die Erstellung eines neuen BMesh, wobei ein Mesh aus bpy.types.BlendData.meshes konvertiert werden muss oder 
- es wird auf das aktuelle Mesh in Edit Mode zugegriffen. Siehe: _bmesh.types.BMesh.from_mesh_ bzw. _bmesh.from_edit_mesh_.

Bei der expliziten Konvertierung von Mesh-Daten werden die Daten mit Hilfe von Python bearbeitet, d. h. das Mesh existiert nur, solange Python einen Verweis darauf hält. Das Skript ist dafür verantwortlich, es nach der Bearbeitung wieder in einen Mesh-Datenblock zu verwandeln.

Zu beachten ist, dass im Gegensatz zu bpy ein BMesh nicht notwendigerweise den Daten in der aktuell geöffneten Blend-Datei entspricht. Ein BMesh kann erstellt, bearbeitet und wieder freigegeben werden, ohne dass der Benutzer es jemals sieht oder Zugriff darauf hat. Im Gegensatz zum Edit-Mode kann das BMesh-Modul mehrere BMesh-Instanzen gleichzeitig verwenden.

Achtung! wenn Sie mit mehreren BMesh-Instanzen arbeiten, da die Mesh-Daten sehr viel Speicherplatz benötigen können. 
Das Mesh, welches durch das Python-Skript aktiv ist, freigegeben wird, wenn das Skript keine Referenzen darauf hält. Eine gute Praxis ist hierbei bmesh.types.BMesh.free aufzurufen, was alle Mesh-Daten sofort entfernt und den weiteren Zugriff verhindert.

#### Example Script
```python
#  In diesem Beispiel wird davon ausgegangen, dass ein Netzobjekt ausgewählt ist

import bpy
import bmesh

# Abrufen des aktiven Netzes
me = bpy.context.object.data

# Eine BMesh-Darstellung erhalten
bm = bmesh.new()   # ein leeres BMesh erstellen
bm.from_mesh(me)   # aus einer Masche ausfüllen

# das bmesh zurück in das Netz verweisen
bm.to_mesh(me)
bm.free()  # frei und verhindern weiteren Zugriff

```
## Zugriff auf CustomData
BMesh bietet eine einheitliche Methode für den Zugriff auf Netzattribute wie UVs, Vertices-Farben, Formschlüssel, Kantenfalten usw. 
Dies funktioniert dadurch, dass eine Layer-Eigenschaft auf BMesh-Datensequenzen implementiert wurde, um auf die benutzerdefinierten Datenlayer zuzugreifen, die dann für den Zugriff auf die tatsächlichen Daten auf jedem Vert, jeder Edge, faces oder Loop verwendet werden können.

Hier sind einige Beispiele:
```python
uv_lay = bm.loops.layers.uv.active

for face in bm.faces:
    for loop in face.loops:
        uv = loop[uv_lay].uv
        print("Loop UV: %f, %f" % uv[:])
        vert = loop.vert
        print("Loop Vert: (%f,%f,%f)" % vert.co[:])
```