
# PANEL
Dieses Skript ist ein einfaches Panel, das in den Bereich der Objekteigenschaften eingezeichnet wird.

```python
from bpy.types import Panel
```
Um ein benutzerdefiniertes Panel in Blender zu erstellen, musst du die API über import bpy importieren, dann eine Klasse erstellen, die vom Typ bpy.types.Panel erbt und schließlich diese Klasse in den bpy.utils registrieren. Wenn Ihre Klasse richtig konfiguriert ist, wird Ihr benutzerdefiniertes Panel irgendwo im Layout erscheinen.

Notice the ‘CATEGORY_PT_name’ *Panel.bl_idname*, this is a naming convention for panels.

class PANEL_PT_SelectionTools(Panel):
    bl_idname: str = 'PANEL_PT_SelectionTools'
    bl_label: str = 'Selection_Tools'
    bl_space_type: str = 'VIEW_3D'
    bl_region_type: str = 'UI'
    bl_category: str = 'Panel Selection Tools'

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