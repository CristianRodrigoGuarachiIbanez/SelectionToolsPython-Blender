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
from stateEdges import StateEdge
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

extendedNodes:DefaultDict[BMVert, StateEdge] = defaultdict(StateEdge);

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


def addEdges(key: BMVert, values:StateEdge) -> None:
    extendedNodes[key]=values;

def deleteEdges() -> None:
    extendedNodes.clear()

def __searchTheClosestValue(lengthValues: List[float], targetDistanceValue: float = 0.0) -> float:
    return lengthValues[min(range(len(lengthValues)), key=lambda i: abs(lengthValues[i] - targetDistanceValue))]

def __getDistanceBetweenEdges(currEdge: BMEdge, nextEdge: BMEdge) -> float:
    return abs(currEdge - nextEdge);


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
deleteEdges()
searchingPath: StateEdge = StateEdge(parent=None, action=selectedEdges[0]);
# ------ create children-edges
searchingPath.createChildrenEdges();
# ------ save the status in EXTENDED NODES
addEdges(0, searchingPath);
while(len(selectedEdges)>0): # endlose Schleife
    nextEdge = searchingPath.getScoreOfTheNextEdge();
    assert(nextEdge is not None), 'there is none edge!'
    if (nextEdge == searchingPath.goal):
        visited.append(nextEdge.index);
        searchingPath = StateEdge(parent=searchingPath, action=nextEdge);
        addEdges(start, searchingPath);
        print(' the goal EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge));
        print(extendedNodes, selectedEdges);
    elif (nextEdge.index not in visited):
        visited.append(nextEdge.index);
        selectedEdges.append(nextEdge)
        print('a new EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge));
    elif (nextEdge.index in visited):
        start += 1;
        print('Jumping the code')
        continue
    # ------- save the last node, action and children into the class itself
    searchingPath = StateEdge(searchingPath, nextEdge);
    # ------ create children-edges
    searchingPath.createChildrenEdges();
    # -------- save the status in EXTENDED NODES
    addEdges(start, searchingPath);
    print('a new OBJECT CLASS STATUS was added into the list of EXTENDED NODES!');
    start += 1;
    if (start == 20):
        print(extendedNodes, selectedEdges);

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


