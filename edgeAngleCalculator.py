import bpy
from mathutils import Matrix, Vector
from bpy import context
from math import degrees, atan2, pi,cos
from bmesh import from_edit_mesh
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List,Tuple,Generator,Type,TypeVar
# project into XY plane,

E:TypeVar = TypeVar("E",List[BMEdge],List[BMFace])

class EdgeAngleCalculator:
    up:Vector =Vector((0, 0, 1))
    def __init__(self)->None:
        ob = context.object
        me = ob.data
        self.bm = from_edit_mesh(me)
    def getAngleCorners(self,faces:bool=False)->Generator:
        selectedElem:E;
        edges:List[BMEdge];
        angle:float;
        if(faces is True):
            selectedElem = self.__selectedFaces()
            for face in range(len(selectedElem)):
                edges = selectedElem[face].edges[:]
                print("Face", selectedElem[face].index, "Edges:", [e.index for e in edges])
                edges.append(selectedElem[face].edges[0])
                #
                for e1, e2 in zip(edges, edges[1:]):
                    angle = self.__edgeAngle(e1, e2, selectedElem[face].normal)
                    print('Angle:', angle)
                    print("Edge Corner", e1.index, e2.index, "Angle:", degrees(angle))
                    yield e1.index,e2.index,degrees(angle)
        else:
            selectedElem = self.__selectedEdges()
            # selectedElem.append(selectedElem[0])
            # for e1,e2 in zip(selectedElem,selectedElem[1:]):
            #     angle=self.__pureEdgeAngle(e1,e2);
            #     print("Edge Corner", e1.index, e2.index, "Angle:", degrees(angle))
            #     yield e1.index,e2.index,degrees(angle)
            for i in range(len(selectedElem)):
                angle = self.__calcEdgeAngle(selectedElem[i])
                print('Angle:', angle)
                print("Edge Corner", selectedElem[i].index, "Angle:", degrees(angle))
                yield selectedElem[i],degrees(angle)
    def __selectedEdges(self)->List[BMEdge]:
        return [f for f in self.bm.edges if f.select]
    def __pureEdgeAngle(self,e1:BMEdge,e2:BMEdge)->float:
        # check which Vertex is shared from the 2 Edges
        sameEdge:BMEdge = set(e1.verts).intersection(e2.verts).pop()
        # select the another vertex point and calculate the direction vector
        v1:Vector = e1.other_vert(sameEdge).co - sameEdge.co;
        v2:Vector = e2.other_vert(sameEdge).co -sameEdge.co;
        # calculate the scalar product
        dotProduct:float = v1.dot(v2)
        # length of the direction vectors
        lv1:Type[float] = v1.length
        lv2:Type[float] = v2.length
        # set everything in the formel
        x:float=abs(dotProduct)/(lv1 * lv2)
        return cos(x)
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
    def __selectedFaces(self)->List[BMFace]:
        return [f for f in self.bm.faces if f.select]
    def __edgeAngle(self, e1:BMEdge, e2:BMEdge, face_normal:Vector)->float:
        b:BMVert = set(e1.verts).intersection(e2.verts).pop()
        a:Vector = e1.other_vert(b).co - b.co
        c:Vector = e2.other_vert(b).co - b.co
        #M:Vector
        a.negate()
        print(a)
        axis:Vector = a.cross(c).normalized()
        print(axis)
        if(axis.length < 1e-5):
            return pi  # inline vert
        #
        if(axis.dot(face_normal) < 0):
            axis.negate()
        M = axis.rotation_difference(self.up).to_matrix().to_4x4()
        print(M)
        a = (M @ a).xy.normalized()
        c = (M @ c).xy.normalized()
        return pi - atan2(a.cross(c), a.dot(c))
if __name__ == '__main__':
    angle:EdgeAngleCalculator = EdgeAngleCalculator()
    cornerAngle:Generator = angle.getAngleCorners()
    while(True):
        try:
            print(next(cornerAngle))
        except StopIteration:
            break







