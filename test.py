#!/usr/bin/env python3
from bpy.types import Panel
from bpy.props import StringProperty

from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator
from bmesh import from_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict
from collections import defaultdict
from mathutils import Vector
from logging import info, INFO
from math import pi
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
        self.__selectedEdges: List[BMEdgeSeq] = list();
        #self.__selectedFaces: List[BMElemSeq] = list(); # save the faces
        self.__graph: DefaultDict[BMVert, List[BMEdge]] = defaultdict(list);
        self.__angles: List[float] = list()

    def getEdges(self) -> List[BMEdgeSeq]:
        return self.__selectedEdges

    def addEdges(self, key: BMVert, values: List[BMEdge]) -> None:
        self.__graph[key].append(values);

    def deleteEdges(self) -> None:
        self.__graph.clear()


    def generateVertices(self) -> Generator:
        v1: BMVert
        v2: BMVert
        length: int = len(self.__selectedEdges)
        assert (length > 0), 'there is NONE active vertices';
        for i in range(length):
            v1, v2 = self.__selectedEdges[i].verts
            yield v1, v2;
    def calculateFacesAngle(self) -> None:
        pass
    @staticmethod
    def edgeAngle(edge1: BMEdge, edge2: BMEdge) -> float:
        b:BMVert = set(edge1.verts).intersection(edge2.verts).pop()
        a:Vector = edge1.other_vert(b).co - b.co
        c:Vector = edge2.other_vert(b).co - b.co
        return a.angle(c);

    def __getNextEdges(self, edge: BMEdge) -> List[BMVert]:
        self.deleteEdges()
        currVertex: BMVert
        vertexIndex: int
        nextEdges: BMElemSeq[BMEdge]
        vertices: List[BMVert] = [vert for vert in edge.verts]
        output: List[BMVert] = vertices.copy()
        i: int
        j: int
        for i in range(len(vertices)):
            currVertex = vertices.pop()
            nextEdges = currVertex.link_edges # <BMElemSeq object at 0x7fd9d5c99780>
            print('next edges length: {}'.format(len(nextEdges)));
            for j in range(len(nextEdges)):
                print('current vertex: {}, next edge: {}, next edge index: {}'.format(currVertex, nextEdges[j], nextEdges[j].index));
                self.addEdges(currVertex, nextEdges[j])
        return output;

    def __selectNextEdge(self, start: int) -> None:
        """
        iterate over the graph excluding the edges that not meet the two criteria
        :param start:
        :return: return a
        """
        vertices: List[BMVert] = self.__getNextEdges(self.__selectedEdges[start])
        limitS:float = 5.2
        limitIn1:float = 5.0
        limitIn2:float = 5.0
        limitI:Tuple[float, bool]
        currEdge: BMEdge
        nextEdge: BMEdge
        currVertex: BMVert
        edgeLength:float
        angle:float
        limits:bool;
        i: int = 0;
        while(len(vertices)>0):
            currEdge= self.__selectedEdges[start]#queue.pop(0);
            edgeLength = currEdge.calc_length();
            currVertex = vertices.pop(0) #vertices[i];
            info('current Edge: {}, current vertices: {}, current vertices index: {}'.format( currEdge, currVertex, currVertex.index))
            limitI = (limitIn1,True) if((i + 1) % 2 == 0) else (limitIn2,False)
            for j in range(len(self.__graph[currVertex])):
                nextEdge = self.__graph[currVertex][j]; # self.__graph[currVertex].pop(0)
                angle = (self.__edgeAngle(currEdge, nextEdge)*180)/pi;
                limits = limitI[0]<angle<limitS
                info('index i: {}, index j: {}, edge index: {}, angle value: {}'.format(i, j, nextEdge.index, angle));
                if(limits and (edgeLength == nextEdge.calc_length())):
                    pass
                    info('current edge length: {}, next edge length: {}'.format(edgeLength, nextEdge.calc_length()));
                else:
                    self.__graph[currVertex].remove(nextEdge);
            i += 1;
            if(len(self.__graph[currVertex]) > 1):
                vertices.append(currVertex);
                limitI[0] += 0.1 ;
                limitIn1 = limitI[0] if(limitI[1]) else limitIn1;
                limitIn2 = limitI[0] if(limitI[1] is False) else limitIn2
            elif(len(self.__graph[currVertex])==1):
                self.__selectedEdges.append(nextEdge)
            else:
                #len is 0
                pass

    def __gatherElementSequences(self) -> None:

        bm: BMesh
        length: int
        if (self.__obj.mode == 'EDIT'):
            bm = from_edit_mesh(self.__obj.data)
            length = len(bm.edges)
            # print(length)
            # for i, v in enumerate(bm.verts):
            assert(length <=3), "there could be more than 3 Edges selected"
            for i in range(length):
                # print('Nicht selected edges: {}'.format(bm.edges[i]))
                if (bm.edges[i].select):
                    print('selected edges: {}'.format(bm.edges[i]))
                    self.__selectedEdges.append(bm.edges[i])
        else:
            print("Object is not in edit mode.")

    def __collectSurroundingEdges(self) -> None:
        edges: List[BMEdgeSeq] = self.getEdges()
        length: int = len(edges)
        assert(length>=0), 'the length of the BMEdges List is empty';
        for i in range(length):
            self.__selectedFaces.append(self.__selectedEdges[i].link_faces);

    def __constructEdgePath(self) -> List[BMEdge]:

        start: int;
        visited: List[bool] = [False] * len(self.__graph)
        queue: BMEdge; # =[self.__selectedEdges[0]]
        visited[0] = True;
        i:int =0;
        while(len(self.__selectedEdges)>0):
            queue = self.__selectedEdges.pop(0)
            #select the next edge
            self.__selectNextEdge(i)
            print('two new edges ware selected!')



    def execute(self, context) -> Set[str]:
        self.__selectedEdges.clear();
        self.__gatherElementSequences();
        self.__collectSurroundingEdges();
        try:
            context.scene.long_string = 'values here:{}'.format(len(self.__selectedFaces))
            #context.scene.long_string = 'value 2 here: {}'.format(self.getEdges()[0].calc_length())
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