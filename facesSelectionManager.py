
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict, Reversible
from radialLoopSelector import RadialLoopSelector as RLSelector
from logging import basicConfig, info, INFO
basicConfig(filename='loops.log',level=INFO)
class FacesSelectionManager(object):
    _lisfOfLoops:List[RLSelector]
    def __init__(self)->None:
        self._reset()
    def _reset(self)->None:
        self._listOfLoops = list()
    def getLoops(self)->BMLoop:
        return self._listOfLoops
    def setLoops(self, edge:BMEdge, left:bool=True)->None:
        RLM:RLSelector= RLSelector(edge)
        if(left is False):
            self._listOfLoops.append(RLM.rightLoop())
            info('length: {}, ITEMS: {}'.format(len(self._listOfLoops), RLM.rightLoop()))
        else:
            self._listOfLoops.append(RLM.leftLoop())
    def nextLoopFromList(self, index:int)->BMLoop:
        return self._listOfLoops[index].link_loop_next
    @staticmethod
    def nextLoop( previosNextLoop:BMLoop)->BMLoop:
        return previosNextLoop.link_loop_next
    @staticmethod
    def radialLoop( nextLoop:BMLoop)->BMLoop:
        return nextLoop.link_loop_radial_next
    @staticmethod
    def nextLoopRightPrev(previousNextLoop:BMLoop)->BMLoop:
        return previousNextLoop.link_loop_prev
    @staticmethod
    def _extractLeftLoops(listOfClassLoops:List[RLSelector])->List[BMLoop]:
        """
        Die Loops, die auf den linken Vertex zeigen, würden aufgerufen
        :param listOfClassLoops: List of RLM Objekt
        :return: a list of Loops mit einem Vertex-Zeiger auf der linken Seite
        """
        return [loop.leftLoop() for loop in listOfClassLoops]
    def recoverNextLoopRight(self)->None:
        listOfLoops: List[BMLoop] = self._listOfLoops[:]
        info("LIST OF LOOPS{}:".format(len(listOfLoops)))
        nextLoop:BMLoop;
        vertexDir:BMVert;
        radialLoop:BMLoop;
        radialLoop:BMLoop;
        for i in range(len(listOfLoops)):
            vertexDir = listOfLoops[i].vert
            nextLoop  = self.nextLoopFromList(i)
            nextLoop = self.nextLoop(nextLoop)
            info("index: {}, right loop:{}".format(i, nextLoop))
            while(nextLoop not in self._listOfLoops):
                self._listOfLoops.append(nextLoop)
                radialLoop = self.radialLoop(nextLoop)
                #print("RADIAL LOOP RIGHT:", radialLoop)
                assert (radialLoop.vert == vertexDir), "Something went wrong";
                nextLoop = self.nextLoopRightPrev(radialLoop)
                #print("NEXT LOOP RIGHT:", nextLoop)
                if (i + 1 < len(listOfLoops) and i - 1 >= 0):
                   #print("next next loop right:", listOfLoops[i+1])
                    if(nextLoop.index == listOfLoops[i+1].index):
                        break

    def recoverNextLoop(self)->None:
        listOfLoops: List[BMLoop] = self._listOfLoops[:]
        info("LIST OF LOOPS{}:".format(len(listOfLoops)))
        nextLoop: BMLoop;
        vertexDir: BMVert;
        radialLoop: BMLoop;
        radialLoop: BMLoop;
        for i in range(len(listOfLoops)):
            nextLoop = self.nextLoopFromList(i)
            vertexDir = nextLoop.vert
            info("index: {}, loop:{}".format(i, nextLoop))
            while (nextLoop not in self._listOfLoops):
                self._listOfLoops.append(nextLoop)
                radialLoop = self.radialLoop(nextLoop)
                print("RADIAL LOOP:", radialLoop)
                nextLoop = self.nextLoop(radialLoop)
                print("NEXT LOOP:", nextLoop)
                assert (nextLoop.vert == vertexDir), "Something went wrong";
                if (i + 1 < len(listOfLoops) and i - 1 >= 0):
                    print("next next loop:", listOfLoops[i + 1])
                    if (nextLoop.index == listOfLoops[i + 1].index):
                        break


