import bpy
from mathutils import Matrix, Vector
from bpy import context
from math import degrees, atan2, pi
from bmesh import from_edit_mesh
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
# project into XY plane,



class EdgeAngleCalculator:
    up:Vector =Vector((0, 0, 1))
    def __init__(self):
        ob = context.object
        me = ob.data
        self.bm = from_edit_mesh(me)

    def edge_angle(self, e1:BMEdge, e2:BMEdge, face_normal:Vector):
        b:BMVert = set(e1.verts).intersection(e2.verts).pop()
        a:Vector = e1.other_vert(b).co - b.co
        c:Vector = e2.other_vert(b).co - b.co
        #M:Vector
        a.negate()
        axis:Vector = a.cross(c).normalized()
        if(axis.length < 1e-5):
            return pi  # inline vert

        if(axis.dot(face_normal) < 0):
            axis.negate()
        M = axis.rotation_difference(self.up).to_matrix().to_4x4()

        a = (M @ a).xy.normalized()
        c = (M @ c).xy.normalized()

        return pi - atan2(a.cross(c), a.dot(c))



import bpy
from mathutils import Matrix, Vector
from bpy import context
from math import degrees, atan2, pi
import bmesh

# project into XY plane,
up = Vector((0, 0, 1))

ob = context.object
me = ob.data
bm = bmesh.from_edit_mesh(me)


def edge_angle(e1, e2, face_normal):
    b = set(e1.verts).intersection(e2.verts).pop()
    a = e1.other_vert(b).co - b.co
    c = e2.other_vert(b).co - b.co
    a.negate()
    axis = a.cross(c).normalized()
    if axis.length < 1e-5:
        return pi  # inline vert

    if axis.dot(face_normal) < 0:
        axis.negate()
    M = axis.rotation_difference(up).to_matrix().to_4x4()

    a = (M @ a).xy.normalized()
    c = (M @ c).xy.normalized()

    return pi - atan2(a.cross(c), a.dot(c))


selected_faces = [f for f in bm.faces if f.select]
for f in selected_faces:
    edges = f.edges[:]
    print("Face", f.index, "Edges:", [e.index for e in edges])
    edges.append(f.edges[0])

    for e1, e2 in zip(edges, edges[1:]):
        angle = edge_angle(e1, e2, f.normal)
        print("Edge Corner", e1.index, e2.index, "Angle:", degrees(angle))