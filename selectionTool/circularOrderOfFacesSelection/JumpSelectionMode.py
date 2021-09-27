from bpy.props import StringProperty
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict, Reversible
from queue import PriorityQueue
from abc import ABCMeta, ABC
import bpy

bl_info:Dict[str,str] = {
    "name": "Direct Jump Selection",
    "author": '-',
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": 'Blender',
    "description": 'Enter edit mode and cycle selection type to face/vertex/edge',
    "wiki_url": '',
    "tracker_url": '',
    "category": 'Object'
}


class EditSelectOperator(bpy.types.Operator):
    bl_idname = 'object.edit_face_select'
    bl_label = 'Enter edit mode and set face selection.'

    def execute(self, context):
        if context.object.mode != 'EDIT':
            # if we aren't in edit mode goto edit and set face select
            bpy.ops.object.mode_set(mode='EDIT', toggle=True)
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.select_all(action='DESELECT')
        else:
            # if we are editing cycle through selection modes
            sel_mode = context.tool_settings.mesh_select_mode
            if sel_mode[0]: # vertex
                bpy.ops.mesh.select_mode(type='EDGE')
            elif sel_mode[1]: # edge
                bpy.ops.mesh.select_mode(type='FACE')
            else: # face
                bpy.ops.mesh.select_mode(type='VERT')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(EditSelectOperator)

def unregister():
    bpy.utils.unregister_class(EditSelectOperator)

if __name__ == "__main__":
    register()