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
        print('next edges length: {}, vertices length: {}'.format(len(nextEdges), len(vertices)));
        for j in range(len(nextEdges)):
            print('current vertex: {}, next edge: {}, next edge index: {}'.format(currVertex, nextEdges[j],
                                                                                  nextEdges[j].index));
            addEdges(currVertex, nextEdges[j])
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



# -------------------------- edges
def __selectNextEdge(EDGE: BMEdge) -> None:
    """
    iterate over the graph excluding the edges that not meet the two criteria
    :param start:
    :return: return a
    """
    vertices: List[BMVert] = __getNextEdges(EDGE)
    limitS: float = 5.2
    limitIn1: float = 5.0
    limitIn2: float = 5.0
    limitI: Tuple[float, bool]
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
        info('current Edge: {}, current vertices: {}, current vertices index: {}'.format(currEdge, currVertex,
                                                                                         currVertex.index))
        limitI = (limitIn1, True) if ((i + 1) % 2 == 0) else (limitIn2, False)
        for j in range(len(graph[currVertex])):
            nextEdge = graph[currVertex][j];  # self.__graph[currVertex].pop(0)
            angle = (edgeAngle(currEdge, nextEdge) * 180) / pi;
            limits = limitI[0] < angle < limitS
            info('index i: {}, index j: {}, edge index: {}, angle value: {}'.format(i, j, nextEdge.index, angle));
            if (limits and (edgeLength == nextEdge.calc_length())):
                pass
                info('current edge length: {}, next edge length: {}'.format(edgeLength, nextEdge.calc_length()));
            else:
                graph[currVertex].remove(nextEdge);
        i += 1;
        if (len(graph[currVertex]) > 1):
            vertices.append(currVertex);
            limitI[0] += 0.1;
            limitIn1 = limitI[0] if (limitI[1]) else limitIn1;
            limitIn2 = limitI[0] if (limitI[1] is False) else limitIn2
        elif (len(graph[currVertex]) == 1):
            selectedEdges.append(nextEdge)
        else:
            # len is 0
            pass

# --------------run----------------

def __excludeDuplicates() -> List[BMEdge]:
    i:int;
    currIndex:int
    indices:List[BMEdge] = list();
    if (len(selectedEdges)==1):
        return list(selectedEdges[0].index)
    elif(len(selectedEdges)<1):
        print('the list ist empty')
    for i in range(len(selectedEdges)):
        indices.append(selectedEdges[i].index) # saves the indices
    return list(set(indices)) # removes the duplicates
# --------- main


start: int = 0;
visited: List[int] = __excludeDuplicates() #[False] * len(self.__selectedEdges)
queue: BMEdge;
currEdge:BMEdge;
while(len(selectedEdges)>0): # endlose Schleife
    queue = selectedEdges[start]
    if(visited[start] == queue.index):
        start+=1;
        continue;
    #select the next edge
    __selectNextEdge(queue)
    print('two new edges ware selected and added!');
    visited = __excludeDuplicates()
    start+=1;

def __activeEdgesEDITMODE( edges:List[BMEdge]) -> None:
    #bm: BMesh = from_edit_mesh(self.__obj.data);
    i:int;
    currEdge:BMEdge;

    for i in range(len(edges)):
        currEdge = edges[i];
        currEdge.select=True;

    bm.select_history.clear()
    bm.select_history.add(currEdge)

    update_edit_mesh(obj.data)


