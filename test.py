#!/usr/bin/env python3
from bpy.types import Panel
from bpy.props import StringProperty

from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh
from bpy import context
from bpy.types import Object, Operator
from bmesh import from_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set
from os.path import dirname, join, expanduser, normpath, realpath
from os import getcwd
import sys
import bpy

class SelectionModesManager(Operator):
    bl_idname: str = 'mesh.text'
    bl_label: str = 'show text'
    bl_options: Set[str] = {'REGISTER', 'UNDO'}
    def __init__(self):
        self.__obj: Object = context.object;
        self.__selectedEdges: List[BMEdgeSeq] = list()

    def getEdges(self) -> List[BMEdgeSeq]:
        return self.__selectedEdges

    def generateVertices(self) -> Generator:
        v1: BMVert
        v2: BMVert
        length: int = len(self.__selectedEdges)
        assert (length > 0), 'there is NONE active vertices';
        for i in range(length):
            v1, v2 = self.__selectedEdges[i].verts
            yield v1, v2;

    def generateEdges(self) -> Generator:
        length: int = len(self.__selectedEdges)
        assert(length > 0), 'there ist none active edges';
        for i in range(length):
            yield self.__selectedEdges[i];

    def __gatherElementSequences(self) -> None:

        bm: BMesh
        length: int
        if (self.__obj.mode == 'EDIT'):
            bm = from_edit_mesh(self.__obj.data)
            length = len(bm.edges)
            # print(length)
            # for i, v in enumerate(bm.verts):
            for i in range(length):
                # print('Nicht selected edges: {}'.format(bm.edges[i]))
                if (bm.edges[i].select):
                    print('selected edges: {}'.format(bm.edges[i]))
                    self.__selectedEdges.append(bm.edges[i])
        else:
            print("Object is not in edit mode.")

    def execute(self, context) -> Set[str]:
        self.__selectedEdges.clear()
        self.__gatherElementSequences()
        try:
            context.scene.long_string = 'values here:{}'.format(len(self.getEdges()))
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, e.args)
            return {'CANCELLED'}

class PANEL_PT_SelectionTools(Panel):
    bl_idname: str = 'PANEL_PT_SelectionTools'
    bl_label: str = 'Selection_Tools'
    bl_space_type: str = 'VIEW_3D'
    bl_region_type: str = 'UI'
    bl_category: str = 'Panel Selection Tools'

    def draw(self, context) -> None:
        row_action_1_btn = self.layout.row()
        row_action_1_btn.operator('mesh.text', icon='WORLD_DATA', text='Print Values')

        # Text area
        row_text = self.layout.row()
        text = context.scene.long_string
        row_text.label(text=text, icon='WORLD_DATA')



bl_info: Dict[str, str] = {
    "name": "Textbox",
    "author": "cristguarachi@gmail.com",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Selection Tools Addon",
    "category": "Development",
}


def register() -> None:
    bpy.utils.register_class(SelectionModesManager)
    bpy.utils.register_class(PANEL_PT_SelectionTools)
    bpy.types.Scene.long_string = StringProperty(name='long_string', default='')


def unregister() -> None:
    bpy.utils.unregister_class(SelectionModesManager)
    bpy.utils.unregister_class(PANEL_PT_SelectionTools)
    del bpy.types.Scene.long_string


if __name__ == "__main__":
    register()