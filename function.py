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
from queue import PriorityQueue


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

extendedNodes:PriorityQueue=PriorityQueue()

# -----------------------------



def edgeAngle(edge1: BMEdge, edge2: BMEdge) -> float:
    b: BMVert = set(edge1.verts).intersection(edge2.verts).pop()
    a: Vector = edge1.other_vert(b).co - b.co
    c: Vector = edge2.other_vert(b).co - b.co
    return a.angle(c);


def addEdges(values:StateEdge) -> None:
    extendedNodes.put(values)


def __deleteAllEdges() -> None:
    while not (extendedNodes.empty()):
        try:
            extendedNodes.get(False)
        except Exception:
            continue
        extendedNodes.task_done()

def __searchTheClosestValue(lengthValues: List[float], targetDistanceValue: float = 0.0) -> float:
    return lengthValues[min(range(len(lengthValues)), key=lambda i: abs(lengthValues[i] - targetDistanceValue))]

def __getDistanceBetweenEdges(currEdge: BMEdge, nextEdge: BMEdge) -> float:
    return abs(currEdge - nextEdge);

def __randListe( state: StateEdge = None) -> None:
    assert (len(state.children) > 0), 'Children´s List is Empty'
    editedChildren: List[BMEdge] = None;
    children: List[StateEdge] = state.children[:]
    parentChildren: List[StateEdge] = state.children[:]
    if (parentChildren is not None):
        editedChildren = children + parentChildren;
        for i in range(len(editedChildren)):
            addEdges(editedChildren[i])
    else:
        for j in range(len(children)):
            addEdges(children[j])
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
__deleteAllEdges()
nextEdge:StateEdge;
searchingPath: StateEdge = StateEdge(parent=None, action=selectedEdges[0]);
# ------ create children-edges
searchingPath.createChildrenEdges();
# ------ save the status in EXTENDED NODES
__randListe(searchingPath);
while(True): # endlose Schleife
    #nextEdge = searchingPath.getScoreOfTheNextEdge();
    nextEdge = extendedNodes.get()
    #print('CUSTOMED NEXT EDGE {} vs  PRIORITY QUEUED EDGE{}'.format(nextEdge, nextEdge2[1].action))
    print('NEXT EDGE {}'.format(nextEdge))
    assert(nextEdge is not None), 'there is none edge!'
    if (nextEdge.action == searchingPath.goal):
        visited.append(nextEdge.action.index);
        selectedEdges.append(nextEdge.action)
        searchingPath = StateEdge(parent=searchingPath, action=nextEdge.action);
        __randListe(searchingPath);
        print(' the goal EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge));
        print(extendedNodes, selectedEdges);
        break
    elif (nextEdge.action.index not in visited):
        visited.append(nextEdge.action.index);
        selectedEdges.append(nextEdge.action)
        print('a new EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge));
    elif (nextEdge.action.index in visited):
        start += 1;
        print('Jumping the code')
        continue
    # ------- save the last node, action and children into the class itself
    searchingPath = StateEdge(searchingPath, nextEdge.action);
    # ------ create children-edges
    searchingPath.createChildrenEdges();
    # -------- save the status in EXTENDED NODES
    __randListe(searchingPath);
    print('a new OBJECT CLASS STATUS was added into the list of EXTENDED NODES!');
    start += 1;
    if (start == 20):
        print(selectedEdges);
        while not (extendedNodes.empty()):
            print(extendedNodes.get())
        break

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


