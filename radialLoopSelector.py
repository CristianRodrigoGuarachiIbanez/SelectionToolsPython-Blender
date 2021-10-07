

from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop


class RadialLoopSelector(object):
    _loop:BMLoop;
    def __init__(self, edge:BMEdge=None)->None:
       self._loop = edge.link_loops;
    def leftLoop(self)->BMLoop:
        return self._loop[0]
    def rightLoop(self)->BMLoop:
        return self._loop[1]
    def leftVertex(self)->BMVert:
        return self._loop[0].vert
    def rightVertex(self)->BMVert:
        return self._loop[1].vert
    def leftRadialLoop(self)->BMLoop:
        return self._loop[0].link_loop_radial_next;
    def rightRadialLoop(self)->BMLoop:
        return self._loop[1].link_loop_radial_next


