from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict
from abc import ABCMeta, ABC
class State(ABC):
    def __init__(self, parent:'StateEdge', action:BMEdge) -> None:
        self.children:List[BMEdge] = [];
        self.parent:'StateEdge'= parent;
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
    def __init__(self, parent:'StateEdge', action:BMEdge) -> None:
        super(StateEdge, self).__init__(parent, action);
        if (parent is not None):
            self.node = action.other_vert(parent.node)#self.__createNodeVertex()
            self.path = parent.path[:];
            self.path.append((action, self.node))
            self.goal: BMEdge = parent.goal;
        else:
            self.node: BMVert = [vert for vert in self.action.verts][0];
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
    def __calcEdgeAngle(self, edge:BMEdge)->float:
        angle:float=0.0
        try:
            angle = edge.calc_face_angle();
        except Exception as e:
            print('[Exception:]', e);
            try:
                angle = edge.calc_face_angle_signed();
            except Exception as e:
                print('[second Exception:]', e)
        return angle
    def calculateTheScore(self, angleScore:bool=False)->None:
        currEdge:float=0.0;
        nextEdge:float=0.0;
        if(angleScore is True):
            self.score = self.__getDistanceBetweenEdges(self.__calcEdgeAngle(self.parent.action), self.__calcEdgeAngle(self.goal))
        else:
            currEdge = self.parent.action.calc_length()
            nextEdge = self.goal.calc_length()
            self.score = self.__getDistanceBetweenEdges(currEdge,nextEdge)
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
    @staticmethod
    def __createNodeVertex(parent,action) -> BMVert:
        assert(parent is not None),'it can not create children because the parent is NoneType';
        vertices: List[BMVert];
        if(parent.node is True):
            return action.other_vert(parent.node);
        else:
            vertices = [vert for vert in action.action.verts]
            return vertices.pop(0) # ------- > ändere das was hier zurückgeliefert wird
    def createChildrenEdges(self, scoreAngle:bool=False) ->None:
        """
        loop over the linked edges, transform all BMEdges into StateEdges Object. Per Defect, it will be calculated the distance-score (length).
        :param scoreAngle: boolean value to specify which score to use
        :return: None
        """
        i:int;
        j:int;
        nextEdges = self.node.link_edges  # recover the linked EDGES
        stateEdge:StateEdge;
        print('number of children edges: {}, parent vertex: {}'.format(len(nextEdges), self.node));
        for j in range(len(nextEdges)):
            print('CURRENT ACTION/EDGE: {}, CURRENT VERTEX/NODE:{}, NEXT EDGE: {}, NEXT EDGE INDEX: {}'.format(self.action, self.node, nextEdges[j],nextEdges[j].index));
            if (self.action.index == nextEdges[j].index):
                continue;
            stateEdge = StateEdge(self, nextEdges[j]);
            if(scoreAngle is True):
                print("[INFO]: angle score will be used!")
                stateEdge.score=self.__getDistanceBetweenEdges(self.__calcEdgeAngle(self.__checkGoalDefinition()), self.__calcEdgeAngle(nextEdges[j]))
            else:
                print("[INFO]: length score will be used!")
                stateEdge.score = self.__getDistanceBetweenEdges(self.__checkGoalDefinition().calc_length(), nextEdges[j].calc_length())
            print('SCORE:', stateEdge.score)
            self.children.append(stateEdge);
        print('number of children edges after: {}'.format(len(self.children)))
