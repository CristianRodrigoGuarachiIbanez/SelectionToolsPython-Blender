#!/usr/bin/env python3

from bpy.props import StringProperty
import bpy
from bpy.types import Operator

class MESH_TxtPrinter(Operator):
    bl_idname = 'mesh.text'
    bl_label = 'show text'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        try:
            context.scene.long_string = 'values here:'
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, e.args)
            return {'CANCELLED'}

