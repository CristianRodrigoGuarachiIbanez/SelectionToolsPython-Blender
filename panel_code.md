
# PANEL
Dieses Skript ist ein einfaches Panel, das in den Bereich der Objekteigenschaften eingezeichnet wird.

```python
from bpy.types import Panel
```
Um ein benutzerdefiniertes Panel in Blender zu erstellen, musst du die API über import bpy importieren, dann eine Klasse erstellen, die vom Typ bpy.types.Panel erbt und schließlich diese Klasse in den bpy.utils registrieren. Wenn Ihre Klasse richtig konfiguriert ist, wird Ihr benutzerdefiniertes Panel irgendwo im Layout erscheinen.

Die 4 Haupteigenschaften einer Blender Panel Klasse sind:

- bl_idname: die eindeutige ID des Panels. Diese muss einer bestimmten Syntaxkonvention folgen, die mit einigen großgeschriebenen Informationen über den Typ der Klasse (hier: ein Panel, PT) und seine Position im Layout (in diesem Fall wird es in der 3D-Ansicht angezeigt, VIEW_3D) beginnt
- bl_label: dies ist der eigentliche Anzeigename des Panels in der Benutzeroberfläche. Es handel sich hierbei um das Label, das dem Benutzer gezeigt werden will.
- bl_space_type: legt fest, in welchem Teil des Layouts das Panel erscheinen soll: in der 3D-Ansicht, im Bild-Editor, im Kurven-Editor, im Eigenschaften-Panel, usw.; eine Liste der gültigen Werte finden Sie hier!
- bl_region_type: legt fest, in welchem Teil der Benutzeroberfläche das Panel erscheint (Topbar, Sidebar...); hier finden Sie eine Liste aller gültigen Werte.

Alle diese Einstellungen werden als Klassenvariablen definiert, im Körper der Klasse, aber außerhalb jeder Funktion:
```python
class PANEL_PT_SelectionTools(Panel):
    bl_idname: str = 'PANEL_PT_SelectionTools'
    bl_label: str = 'Selection_Tools'
    bl_space_type: str = 'VIEW_3D'
    bl_region_type: str = 'UI'
    bl_category: str = 'Panel Selection Tools'
```


    def draw(self, context) -> None:
        row_action_1_btn = self.layout.row()
        row_action_1_btn.operator('lengthscore.selectionmanager', icon='WORLD_DATA', text='Select Edge Length Path')

        row_action_btn = self.layout.row();
        row_action_btn.operator('anglescore.selectionmanager', icon='WORLD_DATA', text='Select Faces Angle Path')

        # Text area
        row_text = self.layout.row()
        text = context.scene.long_string
        row_text.label(text=text, icon='WORLD_DATA')

        # -------- second button
        row_action_2_btn = self.layout.row()
        row_action_2_btn.operator('leftloops.selector', text='Top Faces Selection')
        # --------- third button
        row_action_3_btn = self.layout.row()
        row_action_3_btn.operator('rightloops.selector', text='Bottom Faces Selection')

        row_text1 = self.layout.row()
        text1 = context.scene.long_string
        row_text1.label(text=text1, icon='WORLD_DATA')