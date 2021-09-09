#import unittest
from bpy.props import StringProperty
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict, Reversible
from queue import PriorityQueue
from abc import ABCMeta, ABC
import bpy

T:TypeVar = TypeVar('T', BMEdge, Generator)
class EdgesAroundVertex:#(unittest.TestCase):

    def collectSelectedEdge(self)->BMVert:
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
        return selectedEdges[0].verts[0]

    def connectedEdgesFromVertex_CCW(self, vertex:BMVert):
        '''
        Return edges around param vertex in counter-clockwise order
        :param vertex: start vertex
        :return: a list of BMEdge
        '''
        vertex.link_edges.index_update()
        first_edge:BMEdge = vertex.link_edges[0]

        edges_CCW_order:List[BMEdge] = []

        edge:T = first_edge
        while(edge not in edges_CCW_order):
            edges_CCW_order.append(edge)
            try:
                edge = self.__rightEdgeForEdgeRegardToVertex(edge, vertex)
                edge = next(edge);
            except StopIteration as s:
                print('[INFO:]', s)

        return edges_CCW_order
    @staticmethod
    def __rightEdgeForEdgeRegardToVertex(edge:BMEdge, vertex:BMVert)->Generator:
        '''
         Yield the right edge of param edge regard to param vertex
        :param edge: last selected BMEdge
        :param vertex: start Vertex
        :return: a BMEdge
        '''
        right_loop:BMLoop = None
        loops:BMElemSeq = edge.link_loops
        for i in range(len(loops)):
            if (loops[i].vert == vertex):
                right_loop = loops[i]
                yield right_loop.link_loop_prev.edge


if __name__ == '__main__':
    #unittest.main()
    nextEdge: EdgesAroundVertex = EdgesAroundVertex();
    vertex:BMVert=nextEdge.collectSelectedEdge()
    print(nextEdge.connectedEdgesFromVertex_CCW(vertex))
