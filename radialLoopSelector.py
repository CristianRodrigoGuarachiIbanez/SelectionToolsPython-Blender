
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict, Reversible

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






