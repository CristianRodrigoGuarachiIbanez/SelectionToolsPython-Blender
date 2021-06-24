#!/usr/bin/env python3
import bpy
from bpy.types import Panel

class PANEL_PT_SelectionTools(Panel):
    bl_idname = 'PANEL_PT_SelectionTools'
    bl_label = 'Selection_Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Panel Selection Tools'

    def draw(self, context):
        row_action_1_btn = self.layout.row()
        row_action_1_btn.operator('mesh.text', icon='WORLD_DATA', text='Print Values')

        # Text area
        row_text = self.layout.row()
        text = context.scene.long_string
        row_text.label(text=text, icon='WORLD_DATA')