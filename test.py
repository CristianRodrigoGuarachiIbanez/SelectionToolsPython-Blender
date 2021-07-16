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
        self.__graph: DefaultDict[BMVert, List[BMEdge]] = defaultdict(list);
        self.__angles: List[float] = list()

    def getEdges(self) -> List[BMEdgeSeq]:
        return self.__selectedEdges

    def addEdges(self, key: BMVert, values: List[BMEdge]) -> None:
        self.__graph[key].append(values);

    def deleteAllEdges(self) -> None:
        self.__graph.clear()

    def calculateFacesAngle(self) -> None:
        pass

    def __gatherElementSequences(self) -> None:
        #bm: BMesh
        length: int;
        if (self.__obj.mode == 'EDIT'):
            self.__bm = from_edit_mesh(self.__obj.data)
            length = len(self.__bm.edges)
            # print(length)
            # for i, v in enumerate(bm.verts):
            assert(length <=3), "there could be more than 3 Edges selected"
            for i in range(length):
                # print('Nicht selected edges: {}'.format(bm.edges[i]))
                if (self.__bm.edges[i].select):
                    print('selected edges: {}'.format(self.__bm.edges[i]))
                    self.__selectedEdges.append(self.__bm.edges[i])
        else:
            print("Object is not in edit mode.")

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
            print('number of next edges: {}, number of vertices: {}'.format(len(nextEdges), len(vertices)));
            for j in range(len(nextEdges)):
                print('CURRENT VERTEX:{}, NEXT EDGE: {}, NEXT EDGE INDEX: {}'.format(currVertex, nextEdges[j], nextEdges[j].index));
                if (edge.index == nextEdges[j].index):
                    continue
                self.addEdges(currVertex, nextEdges[j])
        return output;

    def __selectNextEdge(self, EDGE:BMEdge) -> None:
        """
        iterate over the graph excluding the edges that not meet the two criteria
        :param start:
        :return: return nothing
        """
        vertices: List[BMVert] = self.__getNextEdges(EDGE)
        distanceEstimation:float;
        currEdge: BMEdge
        nextEdge: BMEdge
        currVertex: BMVert
        edgeLength:float
        angle:float
        limits:bool;
        i: int = 0;
        while(len(vertices)>0):
            currEdge= EDGE#queue.pop(0);
            edgeLength = currEdge.calc_length();
            currVertex = vertices.pop(0) #vertices[i];
            info('current Edge: {}, current vertices: {}, current vertices index: {}'.format( currEdge, currVertex, currVertex.index))
            distanceEstimation = self.__searchTheClosestValue(list(self.__estimateTheDistance(currVertex= currVertex,currEdgeLength=edgeLength).values()));
            closestEdgeLength  = self.__getClosestValue(currVertex, currEdge)
            #angle = (self.__edgeAngle(currEdge, nextEdge)*180)/pi;
            copyGraph: List[BMEdge] = self.__graph[currVertex].copy()
            length: int = len(copyGraph)
            #print('function distanceEstimation: {} vs closestEdgeLength: {}'.format(distanceEstimation, closestEdgeLength[1]))
            info('index i: {}, target edge length: {}, closest edge length: {}, distance to the target length: {}'.format(i, edgeLength, closestEdgeLength[0], closestEdgeLength[1]));
            # ---------- this  has to be included in the function getClosestValue ------
            for j in range(length):
                nextEdge = self.__graph[currVertex].pop(0)
                if(nextEdge == closestEdgeLength[0]):
                    self.__graph[currVertex].append(nextEdge)
                    info('selected edge length: {}, value of the selected edge length: {}'.format(closestEdgeLength[0], closestEdgeLength[1]));
                else:
                    print('delete edge {} from graph, size of graph {}'.format(nextEdge, len(self.__graph[currVertex])))
            i += 1;
            if(len(self.__graph[currVertex]) > 1):
                info('there is more that one edge, select just one to continue')

    def __estimateTheDistance(self, currVertex: BMVert, currEdgeLength:float) -> DefaultDict[BMEdge, float]:
        distance:float;
        output:DefaultDict = defaultdict(float)
        for j in range(len(self.__graph[currVertex])):
            nextEdge = self.__graph[currVertex][j];
            distance = self.__getDistanceBetweenEdges(currEdge=currEdgeLength, nextEdge=nextEdge.calc_length());
            output[nextEdge] = distance
            info('index j: {}, current edge length: {}, next edge length: {}, distance between them {}'.format(j, currEdgeLength, nextEdge.calc_length(), distance));
            if (distance > 0):
                info('the current edge is bigger: {}'.format(distance));
                continue;
            elif (distance < 0):
                info('the next distance is bigger: {}'.format(distance))
            else:
                info('the distance is equal to NULL: {}'.format(distance))
        return output

    def __getClosestValue(self, currVertex:BMVert, currEdge:BMEdge) -> Tuple[BMEdge, float]:

        closestEdge:BMEdge = self.__graph[currVertex][0];#
        closestValue: float = self.__getDistanceBetweenEdges(currEdge.calc_length(),  closestEdge.calc_length());
        nextLength:float;
        nextEdge:BMEdge;
        for i in range(1, len(self.__graph[currVertex])):
            nextEdge = self.__graph[currVertex][i]
            nextLength = self.__getDistanceBetweenEdges(currEdge.calc_length(), nextEdge.calc_length());
            if(nextLength < closestValue):
                closestValue = nextLength;
                closestEdge = nextEdge;
        return closestEdge, closestValue

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

    def __constructEdgePath(self) -> List[BMEdge]:

        start: int = 0;
        visited: List[int] = self.__excludeDuplicates() # list of edge indices [False] * len(self.__selectedEdges)
        queue: BMEdge;
        currEdge:BMEdge;
        while(len(self.__selectedEdges)>0): # endlose Schleife
            queue = self.__selectedEdges[start]
            if(visited[start] == queue.index):
                start+=1;
                continue;
            #select the next edge
            self.__selectNextEdge(queue)
            print('two new edges ware selected and added!');
            visited = self.__excludeDuplicates()
            start+=1;
        if(start ==3):
            return self.__selectedEdges

        return self.__selectedEdges

    @staticmethod
    def __searchTheClosestValue(lengthValues: List[float], targetDistanceValue: float = 0.0) -> float:
        return lengthValues[min(range(len(lengthValues)), key=lambda i: abs(lengthValues[i] - targetDistanceValue))]

    @staticmethod
    def __getDistanceBetweenEdges(currEdge: BMEdge, nextEdge: BMEdge) -> float:
        return abs(currEdge - nextEdge);

    @staticmethod
    def edgeAngle(edge1: BMEdge, edge2: BMEdge) -> float:
        b: BMVert = set(edge1.verts).intersection(edge2.verts).pop()
        a: Vector = edge1.other_vert(b).co - b.co
        c: Vector = edge2.other_vert(b).co - b.co
        return a.angle(c);

    def __activeEdgesEDITMODE(self, edges:List[BMEdge]) -> None:
        #bm: BMesh = from_edit_mesh(self.__obj.data);
        i:int;
        currEdge:BMEdge;

        for i in range(len(edges)):
            currEdge = edges[i];
            currEdge.select=True;

        self.__bm.select_history.clear()
        self.__bm.select_history.add(currEdge)

        update_edit_mesh(self.__obj.data)


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