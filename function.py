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
import sys
import bpy
from math import pi


# --------------------------- select the edge
obj: Object = context.object;
selectedEdges: List[BMEdge] = list()
bm: BMesh
length: int
if (obj.mode == 'EDIT'):
    bm = from_edit_mesh(obj.data)
    length = len(bm.edges)
    print(bm.edges)
    # for i, v in enumerate(bm.verts):
    # assert(length <=3), "there could be more than 3 Edges selected"
    for i in range(length):
        # print('Nicht selected edges: {}'.format(bm.edges[i]))
        if (bm.edges[i].select):
            print('selected edges: {}'.format(bm.edges[i]))
            selectedEdges.append(bm.edges[i])
else:
    print("Object is not in edit mode.")

# ------------------- def graph

graph: DefaultDict[BMVert, List[BMEdge]] = defaultdict(list);

# -----------------------------


def __getNextEdges(edge: BMEdge) -> List[BMVert]:
    deleteEdges()
    currVertex: BMVert
    vertexIndex: int
    nextEdges: BMElemSeq[BMEdge]
    vertices: List[BMVert] = [vert for vert in edge.verts]
    # print(vertices)
    vertices2 = vertices.copy()
    i: int
    j: int
    for i in range(len(vertices)):
        currVertex = vertices.pop()
        nextEdges = currVertex.link_edges  # <BMElemSeq object at 0x7fd9d5c99780>
        print('number of next edges: {}, number of vertices: {}'.format(len(nextEdges), len(vertices)));
        for j in range(len(nextEdges)):
            print('CURRENT EDGE {}, CURRENT VERTEX:{}, NEXT EDGE: {}, NEXT EDGE INDEX: {}'.format(edge, currVertex, nextEdges[j], nextEdges[j].index));
            if(edge.index == nextEdges[j].index):
                print(nextEdges)
                continue
            addEdges(currVertex, nextEdges[j]);
    return vertices2


def edgeAngle(edge1: BMEdge, edge2: BMEdge) -> float:
    b: BMVert = set(edge1.verts).intersection(edge2.verts).pop()
    a: Vector = edge1.other_vert(b).co - b.co
    c: Vector = edge2.other_vert(b).co - b.co
    return a.angle(c);


def addEdges(key: BMVert, values: List[BMEdge]) -> None:
    graph[key].append(values);


def deleteEdges() -> None:
    graph.clear()

def __searchTheClosestValue(lengthValues: List[float], targetDistanceValue: float = 0.0) -> float:
    return lengthValues[min(range(len(lengthValues)), key=lambda i: abs(lengthValues[i] - targetDistanceValue))]

def __getDistanceBetweenEdges(currEdge: BMEdge, nextEdge: BMEdge) -> float:
    return abs(currEdge - nextEdge);

def edgeAngle(edge1: BMEdge, edge2: BMEdge) -> float:
    b: BMVert = set(edge1.verts).intersection(edge2.verts).pop()
    a: Vector = edge1.other_vert(b).co - b.co
    c: Vector = edge2.other_vert(b).co - b.co
    return a.angle(c);

# ------------------------- distance to target edge
def __estimateTheDistance(currVertex: BMVert, currEdgeLength:float) -> DefaultDict[BMEdge, float]:
    distance:float;
    output:DefaultDict = defaultdict(float)
    for j in range(len(graph[currVertex])):
        nextEdge = graph[currVertex][j];
        distance = __getDistanceBetweenEdges(currEdge=currEdgeLength, nextEdge=nextEdge.calc_length());
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

def __getClosestValue(currVertex:BMVert, currEdge:BMEdge) -> Tuple[BMEdge, float]:

    closestEdge:BMEdge = graph[currVertex][0];#
    closestValue: float = __getDistanceBetweenEdges(currEdge.calc_length(),  closestEdge.calc_length());
    nextLength:float;
    nextEdge:BMEdge;
    for i in range(1, len(graph[currVertex])):
        nextEdge = graph[currVertex][i]
        nextLength = __getDistanceBetweenEdges(currEdge.calc_length(), nextEdge.calc_length());
        if(nextLength < closestValue):
            closestValue = nextLength;
            closestEdge = nextEdge;
    return closestEdge, closestValue
# -------------------------- edges
def __selectNextEdge(EDGE: BMEdge) -> None:
    """
    iterate over the graph excluding the edges that not meet the two criteria
    :param start:
    :return: return nothing
    """
    vertices: List[BMVert] = __getNextEdges(EDGE)
    print('NUMBER OF VERTICES {}'.format(vertices))
    distanceEstimation: float;
    currEdge: BMEdge
    nextEdge: BMEdge
    currVertex: BMVert
    edgeLength: float
    angle: float
    limits: bool;
    i: int = 0;
    while (len(vertices) > 0):
        currEdge = EDGE  # queue.pop(0);
        edgeLength = currEdge.calc_length();
        currVertex = vertices.pop(0)  # vertices[i];
        info('current Edge: {}, current vertices: {}, current vertices index: {}'.format(currEdge, currVertex, currVertex.index))
        distanceEstimation = __searchTheClosestValue(list(__estimateTheDistance(currVertex=currVertex, currEdgeLength=edgeLength).values()));
        closestEdgeLength = __getClosestValue(currVertex, currEdge)
        # angle = (self.__edgeAngle(currEdge, nextEdge)*180)/pi;
        copyGraph: List[BMEdge] = graph[currVertex].copy()
        length: int = len(copyGraph)
        print(len(closestEdgeLength))
        print('function distanceEstimation: {} vs closestEdgeLength: {}'.format(distanceEstimation, closestEdgeLength[1]))
        print('index i: {}, target edge length: {}, closest edge length: {}, distance to the target length: {}'.format(i, edgeLength, closestEdgeLength[0], closestEdgeLength[1]));
        # ---------- this  has to be included in the function getClosestValue ------
        for _ in range(length):
            nextEdge = graph[currVertex].pop(0)
            print('the next edge', nextEdge)
            if (nextEdge == closestEdgeLength[0]):
                graph[currVertex].append(nextEdge)
                print('selected edge length: {}, value of the selected edge length: {}'.format(closestEdgeLength[0], closestEdgeLength[1]));
            else:
                print('delete edge {} from graph -> size of graph {}'.format(nextEdge, len(graph[currVertex])))
        i += 1;
        if (len(graph[currVertex]) > 1):
            info('there is more that one edge, select just one to continue')
    print('the new selected edges'.format(graph))

# --------------run----------------

def __excludeDuplicates() -> List[BMEdge]:
    i:int;
    currIndex:int
    indices:List[BMEdge] = list();
    if (len(selectedEdges)==1):
        return [selectedEdges[0].index]
    elif(len(selectedEdges)<1):
        print('the list ist empty')
    for i in range(len(selectedEdges)):
        indices.append(selectedEdges[i].index) # saves the indices
    return list(set(indices)) # removes the duplicates
# --------- main


start: int = 0;
visited: List[int] = __excludeDuplicates() #[False] * len(self.__selectedEdges)
print(visited)
queue: BMEdge;
currEdge:BMEdge;
while(len(selectedEdges)>0): # endlose Schleife
    currEdge = selectedEdges[start]
    print(currEdge)
    print(start)
    if((len(selectedEdges)>1) and (visited[start] == currEdge.index)):
        start +=1
        continue;
    #select the next edge
    __selectNextEdge(currEdge)
    print('two new edges ware selected and added!');
    # the added edges into the graph muss be also added to the selectedEdges list!!! 
    visited = __excludeDuplicates()
    print(visited)
    if (start == 3):
        print(start, selectedEdges)
    start+=1;

def __activeEdgesEDITMODE( edges:List[BMEdge]) -> None:
    # bm: BMesh = from_edit_mesh(self.__obj.data);
    i:int;
    currEdge:BMEdge;

    for i in range(len(edges)):
        currEdge = edges[i];
        currEdge.select=True;

    bm.select_history.clear()
    bm.select_history.add(currEdge)

    update_edit_mesh(obj.data)


