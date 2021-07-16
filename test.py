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
from os.path import dirname, join, expanduser, normpath, realpath
from os import getcwd
from statistics import mean
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

    def __selectNextEdge(self, EDGE: BMEdge) -> None:
        """
        iterate over the graph excluding the edges that not meet the two criteria
        :param start:
        :return: return a
        """
        vertices: List[BMVert] = self.__getNextEdges(EDGE);
        difference:float = 0.09
        currEdge: BMEdge
        nextEdge: BMEdge
        currVertex: BMVert
        optim_value:float = 0.01;
        edgeLength:float
        angle:float
        limits:bool;
        i: int = 0;
        while(len(vertices)>0):
            currEdge= EDGE #queue.pop(0);
            edgeLength = currEdge.calc_length();
            currVertex = vertices.pop(0) #vertices[i];
            info('current Edge: {}, current vertices: {}, current vertices index: {}'.format( currEdge, currVertex, currVertex.index))
             #(limitIn1,True) if((i + 1) % 2 == 0) else (limitIn2,False)
            self.__removeEdgesFromGraph(edgeLength, currVertex, difference, optim_value);
            i += 1;

            if(len(self.__graph[currVertex]) > 1):
                vertices.append(currVertex);
                difference -= 0.01;
                while(difference >0):
                    self.__removeEdgesFromGraph(edgeLength, currVertex, difference, optim_value)
                    difference -= 0.01;
            elif(len(self.__graph[currVertex])==1):
                self.__selectedEdges.append(nextEdge);
            else:
                #len is 0
                pass
    def __removeEdgesFromGraph(self, edgeLength:float, currVertex:BMVert, difference:float, optim_value:float) -> None:
        limitS: Tuple[float, float, bool];
        limitIn: Tuple[float, float, bool];
        limitSup1: float
        limitInf1: float;
        limitInf1, limitSup1 = self.__createLimits(edgeLength, difference)
        for j in range(len(self.__graph[currVertex])):
            nextEdge = self.__graph[currVertex][j];  # self.__graph[currVertex].pop(0)
            # angle = (self.__edgeAngle(currEdge, nextEdge)*180)/pi;
            limitS = self.__compareUpperLimits(limitSup1, edgeLength, nextEdge.calc_length(), optim_value);   # limitI[0]<angle<limitS
            limitIn = self.__compareLowerLimits(limitInf1, edgeLength, nextEdge.calc_length(), optim_value);
            info('index j: {}, edge length upper limit: {}, edge length lower limit: {}'.format(j, limitS, limitIn));
            if ((limitIn[2] is True) and (limitS[2] is True)):
                info('current edge length: {}, next edge length: {}'.format(edgeLength, nextEdge.calc_length()));
                continue;
            elif ((limitIn[1] is True) and (limitS[1] is False)):
                
                self.__graph[currVertex].remove(nextEdge);
            elif ((limitIn[1] is False) and (limitS[1] is True)):
                self.__graph[currVertex].remove(nextEdge);
            else:
                self.__graph[currVertex].remove(nextEdge);

    def __compareLowerLimits(self, lowerLimit:float, trueValue:float, newValue:float, opt_value:float, trial:int=10) -> Tuple[float, float, bool]:
        lowerLimits: List[float] = list();
        lowerLimitMean:float;
        distance:float;
        i:int =0;

        while((lowerLimit < trueValue) and (lowerLimit < newValue)): # as long as the lower limit is smaller
            lowerLimit = self.__increaseLowerLimit(lowerLimit, opt_value);
            lowerLimits.append(lowerLimit);
            if(trial==i):
                break;
            i+=1;

        if(lowerLimit < newValue):
            #calculate the distance between lower limit and value
            distance = newValue - lowerLimit;
            return lowerLimit, distance, True;
        elif(lowerLimit==newValue):
            distance = newValue - lowerLimit;
            return lowerLimit, distance, True;
        else:
            distance = lowerLimit - newValue;
            return lowerLimit, distance, False;

    def __compareUpperLimits(self, upperLimit:float, trueValue:float, newValue:float,  opt_value:float, trial:int=10) -> Tuple[float, float, bool]:
        upperLimits: List[float] = list();
        lowerLimitMean: float;
        distance:float;
        i: int = 0;

        while ((upperLimit > trueValue) and (upperLimit > newValue)): # as long as the upper limit is bigger
            upperLimit = self.__dicreaseUpperLimit(upperLimit, opt_value);
            upperLimits.append(upperLimit);
            if (trial == i):
                break;
            i += 1;
        if (upperLimit > newValue):
            # calculate the distance between upper limit and value
            distance = upperLimit -newValue;
            return upperLimit, distance, True;
        elif (upperLimit == newValue):
            distance = upperLimit - newValue;
            return upperLimit, distance, True;
        else:
            distance = newValue - upperLimit;
            return upperLimit, distance, False;

    @staticmethod
    def __createLimits(valueLength:float, diff:float) -> Tuple[float,float]:
        assert(valueLength > 0), ' the length of the edge is zero';
        if (diff is None):
            diff = 0.0;
        lowerLimit:float = valueLength - diff;
        upperLimit:float = valueLength + diff
        return lowerLimit, upperLimit;

    @staticmethod
    def __increaseLowerLimit(lowerLimit:float, opt_value:float)-> float:
        return lowerLimit + opt_value;

    @staticmethod
    def __dicreaseUpperLimit(upperLimit:float, opt_value:float) -> float:
        return upperLimit - opt_value;

    def __excludeDuplicates(self) -> List[BMEdge]:
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
        visited: List[int] = self.__excludeDuplicates() #[False] * len(self.__selectedEdges)
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

        return self.__selectedEdges

    def __activeEdgesEDITMODE(self, edges:List[BMEdge]) -> None:
        #bm: BMesh = from_edit_mesh(self.__obj.data);
        i:int;
        currEdge:BMEdge = None;

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