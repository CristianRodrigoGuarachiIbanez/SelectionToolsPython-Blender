
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict, Reversible
from radialLoopSelector import RadialLoopSelector as RLSelector

class FacesSelectionManager(object):
    _lisfOfLoops:List[RLSelector]
    def __init__(self)->None:
        self._listOfLoops = list()
    def getLoops(self)->BMLoop:
        return self._listOfLoops
    def setLoops(self, edge:BMEdge)->None:
        RLM:RLSelector= RLSelector(edge)
        self._listOfLoops.append(RLM.leftLoop())
    def nextLoopFromList(self, index:int)->BMLoop:
        return self._listOfLoops[index].link_loop_next
    def nextLoop(self, previosNextLoop:BMLoop)->BMLoop:
        return previosNextLoop.link_loop_next
    def radialLoop(self, nextLoop:BMLoop)->BMLoop:
        return nextLoop.link_loop_radial_next
    @staticmethod
    def _extractLeftLoops(listOfClassLoops:List[RLSelector])->List[BMLoop]:
        """
        Die Loops, die auf den linken Vertex zeigen, würden aufgerufen
        :param listOfClassLoops: List of RLM Objekt
        :return: a list of Loops mit einem Vertex-Zeiger auf der linken Seite
        """
        return [loop.leftLoop() for loop in listOfClassLoops]
    def recoverNextLoop(self)->None:
        listOfLoops: List[BMLoop] = self._listOfLoops[:]
        nextLoop:BMLoop;
        vertexDir:BMVert;
        radialLoop:BMLoop;
        radialLoop:BMLoop;
        for i in range(len(listOfLoops)):
            nextLoop  = self.nextLoopFromList(i)
            vertexDir = nextLoop.vert
            print("index: {}, loop:{}".format(i, nextLoop))
            while(nextLoop not in self._listOfLoops):
                self._listOfLoops.append(nextLoop)
                radialLoop = self.radialLoop(nextLoop)
                print("RADIAL LOOP:", radialLoop)
                nextLoop = self.nextLoop(radialLoop)
                print("NEXT LOOP:", nextLoop)
                if (i + 1 < len(listOfLoops) and i - 1 >= 0):
                    print("next next loop:", listOfLoops[i+1])
                    if(nextLoop.index == listOfLoops[i+1].index):
                        break

                if not (nextLoop.vert==vertexDir):
                    print("Something went wrong")


