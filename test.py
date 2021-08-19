#!/usr/bin/env python3

from bpy.props import StringProperty

from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict
from collections import defaultdict
from mathutils import Vector
from logging import info, INFO
from state import StateEdge
from math import pi
from numpy import ndarray, asarray, abs as absolut, array
from os.path import dirname, join, expanduser, normpath, realpath
from os import getcwd
import sys
import bpy


class SelectionModesManager(Operator):
    bl_idname: str = 'mesh.text';
    bl_label: str = 'show text';
    bl_options: Set[str] = {'REGISTER', 'UNDO'};
    def __init__(self) -> None:
        self.__obj: Object = context.object;
        self.__bm: BMesh;
        self.__selectedEdges: List[BMEdgeSeq] = list();
        #self.__selectedFaces: List[BMElemSeq] = list(); # save the faces
        self.__extendedNodes: DefaultDict[int, StateEdge] = defaultdict(StateEdge);
        self.__angles: List[float] = list()

    def __getEdges(self) -> List[BMEdgeSeq]:
        return self.__selectedEdges

    def __addEdges(self, key:int, value:BMEdge) -> None:
        self.__extendedNodes[key] = value;

    def __deleteAllEdges(self) -> None:
        self.__extendedNodes.clear()

    def calculateFacesAngle(self) -> None:
        pass

    def __excludeDuplicates(self) -> List[int]:
        i:int;
        currIndex:int
        indices:List[BMEdge] = list();
        if (len(self.__selectedEdges)==1):
            return list(self.__selectedEdges[0].index)
        elif(len(self.__selectedEdges)<1):
            print('the list ist empty')
        for i in range(len(self.__selectedEdges)):
            indices.append(self.__selectedEdges[i].index) # saves the indices
        return list(set(indices)) # removes the duplicates

    def __constructEdgePath(self) -> Tuple[DefaultDict, List[BMEdge]]:

        start: int = 0;
        visited: List[int] = self.__excludeDuplicates() # list of edge indices [False] * len(self.__selectedEdges)
        nextEdge:BMEdge;
        # -------- clear dict EXTENDED NODES
        self.__deleteAllEdges()
        # ------------ declare and define StateEdges
        searchingPath:StateEdge = StateEdge(parent=None,action=self.__selectedEdges[0], goal=self.__selectedEdges[0]);
        # ------ create children-edges
        searchingPath.createChildrenEdges();
        # ------ save the status in EXTENDED NODES
        self.__addEdges(0,searchingPath)
        while(True): # endlose Schleife
            # ------ look for the next edge and save in SELECTED EDGES
            nextEdge = searchingPath.getScoreOfTheNextEdge();
            if(nextEdge is not None):
                if(nextEdge == searchingPath.goal):
                    visited.append(nextEdge.index);
                    searchingPath = StateEdge(parent=searchingPath, action=nextEdge);
                    self.__addEdges(start,searchingPath);
                    print(' the goal EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge));
                    return self.__extendedNodes, self.__selectedEdges;
                elif(nextEdge.index not in visited):
                    visited.append(nextEdge.index);
                    self.__selectedEdges.append(nextEdge)
                    print('a new EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge));
                elif(nextEdge.index in visited):
                    start+=1;
                    continue
            else:
                print('NEXT EDGE is None');
                break
            # ------- save the last node, action and children into the class itself
            searchingPath = StateEdge(searchingPath, nextEdge);
            # ------ create children-edges
            searchingPath.createChildrenEdges();
            # -------- save the status in EXTENDED NODES
            self.__addEdges(start, searchingPath);
            print('a new OBJECT CLASS STATUS was added into the list of EXTENDED NODES!');
            start+=1;
            if (start == 3):
                return self.__extendedNodes, self.__selectedEdges

    def __activeEdgesEDITMODE(self) -> None:
        #bm: BMesh = from_edit_mesh(self.__obj.data);
        EDGES:List[BMEdge]=self.__selectedEdges
        i:int;
        currEdge:BMEdge=None;
        for i in range(len(EDGES)):
            currEdge = EDGES[i];
            currEdge.select=True;
        self.__bm.select_history.clear()
        self.__bm.select_history.add(currEdge)
        update_edit_mesh(self.__obj.data)

    def execute(self, context) -> Set[str]:
        self.__selectedEdges.clear();
        try:
            context.scene.long_string = 'values here:{}'.format(len(self.__selectedEdges))
            self.__activeEdgesEDITMODE()
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