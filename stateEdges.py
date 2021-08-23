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
    def __lt__(self, other:BMEdge):
        score1: float = self.score
        score2: float = other.score
        if (score1 < score2):
            return True
        return False
    def __le__(self, other:BMEdge):
        score1:float = self.score
        score2:float=other.score
        if(score1<=score2):
            return True
        return False
    def __checkGoalDefinition(self)->BMEdge:
        if (self.parent is None):
            return self.action;
        else:
            if (self.parent.goal is None):
                return self.goal
            else:
                return self.parent.goal
    def getScoreOfTheNextEdge(self) -> Tuple[BMEdge,float]:
        """
                iterate over the list of children excluding the edges that not meet the one/two criteria
                :return: BMEdge
        """
        assert (len(self.children) > 0), "the children's list is empty"
        closestValue:Tuple[StateEdge,float] = self.__getClosestValue(self.children);
        self.children.remove(closestValue[0])
        return closestValue[0].action, closestValue[1]
    @staticmethod
    def __getClosestValue(nextEdges:List['StateEdge']) -> Tuple['StateEdge',float]:
        closestEdge:StateEdge = nextEdges[0];#
        closestValue: float = closestEdge.score;
        nextLength:float;
        nextEdge:BMEdge;
        for i in range(1, len(nextEdges)):
            nextEdge = nextEdges[i]
            nextLength = nextEdge.score
            if(nextLength < closestValue):
                closestValue = nextLength;
                closestEdge = nextEdge;
        return closestEdge, closestValue;
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
        nextEdges = self.node.link_edges  # recover the linked EDGES
        stateEdge: StateEdge;
        print('number of children edges: {}, parent vertex: {}'.format(len(nextEdges), self.node));
        for j in range(len(nextEdges)):
            print('CURRENT ACTION/EDGE: {}, CURRENT VERTEX/NODE:{}, NEXT EDGE: {}, NEXT EDGE INDEX: {}'.format(self.action, self.node, nextEdges[j],nextEdges[j].index));
            if (self.action.index == nextEdges[j].index):
                continue;
            stateEdge = StateEdge(self, nextEdges[j]);
            stateEdge.score = self.__getDistanceBetweenEdges(self.__checkGoalDefinition().calc_length(), nextEdges[j].calc_length())
            print('SCORE:', stateEdge.score)
            self.children.append(stateEdge);
        print('number of children edges after: {}'.format(len(self.children)))
