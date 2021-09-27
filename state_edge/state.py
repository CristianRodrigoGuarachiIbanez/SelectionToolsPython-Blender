from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict
from .stateEdges import StateEdge
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


