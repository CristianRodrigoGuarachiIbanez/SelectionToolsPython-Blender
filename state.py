
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict
from copy import deepcopy
from abc import ABCMeta, ABC

class State(ABC):
    def __init__(self, parent:'State', action:BMEdge) -> None:
        self.children:List[BMEdge] = [];
        self.parent:'State'= parent;
        self.action: BMEdge = action;
        # ----- define later
        self.node: BMVert = None;
        self.score:float = 0.0; # value of compering the current action/edge with the next action/edge
        self.path: List[Tuple[BMEdge, BMVert]] = list();
        self.goal:BMEdge=None
        # -----  Children's Length
        self.__len:int=len(self.children);
    def __len__(self) -> int:
        return self.__len
    def getScoreOfTheNextEdge(self)->BMEdge:
        pass
    def createNodeVertex(self)-> BMVert:
        pass
    def createChildrenEdges(self)->None:
        pass

class StateEdge(State):
    def __init__(self, parent:State, action:BMEdge) -> None:
        super(StateEdge, self).__init__(parent, action);
        if (parent):
            self.node: BMVert = self.__createNodeVertex()
            self.path = parent.path[:];
            self.path.append((action, self.node))
            self.goal: BMEdge = deepcopy(parent.goal);
        else:
            self.node: BMVert = [vert for vert in self.action.verts][0]
            self.path = [(action, self.node)]
            self.goal: BMEdge = action;
    def getScoreOfTheNextEdge(self) -> BMEdge:
        """
                iterate over the list of children excluding the edges that not meet the one/two criteria
                :return: BMEdge
        """
        currEdge: BMEdge;
        if(self.parent is None):
            currEdge = self.action;
        else:
            if(self.parent.goal is None):
                currEdge = self.goal
            else:
                currEdge = self.parent.goal
        closestEdgeLength: Tuple[BMEdge, float] = self.__getClosestValue(self.children, currEdge);
        self.score = closestEdgeLength[1]
        length: int = len(self.children)
        # ---------- this  has to be included in the function getClosestValue ------
        nextEdge: BMEdge
        for j in range(length):
            nextEdge = self.children.pop(0)
            if (nextEdge == closestEdgeLength[0]):
                return nextEdge
            else:
                print('delete edge {} and size of the children edges {}'.format(nextEdge, len(self.children)));
    def __getClosestValue(self, nextEdges:List[BMEdge], currEdge:BMEdge) -> Tuple[BMEdge, float]:
        assert(len(nextEdges)>0), "the children's list is empty"
        closestEdge:BMEdge = nextEdges[0];#
        closestValue: float = self.__getDistanceBetweenEdges(currEdge.calc_length(),  closestEdge.calc_length());
        nextLength:float;
        nextEdge:BMEdge;
        for i in range(1, len(nextEdges)):
            nextEdge = nextEdges[i]
            nextLength = self.__getDistanceBetweenEdges(currEdge.calc_length(), nextEdge.calc_length());
            if(nextLength < closestValue):
                closestValue = nextLength;
                closestEdge = nextEdge;
        return closestEdge, closestValue
    @staticmethod
    def __getDistanceBetweenEdges(currEdge: float, nextEdge:float) -> float:
        return abs(currEdge - nextEdge);
    def __createNodeVertex(self) -> BMVert:
        vertices: List[BMVert];
        if(self.parent.node is None):
            vertices = [vert for vert in self.action.verts]
            return vertices.pop(0);
        else:
            return self.action.other_vert(self.parent.node);
    def createChildrenEdges(self) ->None:
        i:int;
        j:int;
        nextEdges = self.node.link_edges  #
        print('number of children edges: {}, parent vertex: {}'.format(len(nextEdges), self.node));
        for j in range(len(nextEdges)):
            print('CURRENT ACTION/EDGE: {}, CURRENT VERTEX/NODE:{}, NEXT EDGE: {}, NEXT EDGE INDEX: {}'.format(self.action, self.node, nextEdges[j],nextEdges[j].index));
            if (self.action.index == nextEdges[j].index):
                continue
            self.children.append(nextEdges[j])


