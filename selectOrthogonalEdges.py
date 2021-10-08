"""
https://blender.stackexchange.com/questions/182182/how-to-select-with-python-code-only-vertical-edges-from-cube
"""
from bmesh.types import BMVert, BMEdge, BMesh
from bpy import context
from bpy.types import Object, Panel
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Any, Set
from collections import defaultdict
from mathutils import Vector
from state_edge.stateEdges import StateEdge
from queue import PriorityQueue
import bpy
import bmesh

obj = bpy.context.active_object  # Get selected object

epsilon = 1e-5  # Threshold to account for floating point precision

if obj:
    bpy.ops.object.mode_set(mode='EDIT')  # Go into edit mode
    bpy.ops.mesh.select_mode(type="EDGE")  # Switch to edge select mode

    bm = bmesh.from_edit_mesh(obj.data)  # Create bmesh object for easy mesh evaluation

    for e in bm.edges:  # Check all edges
        first_pos = e.verts[0].co  # Get first vert position of this edge
        other_pos = e.verts[1].co  # Get second vert position of this edge

        # Select or deselect depending of the relative position of both vertices
        e.select_set(abs(first_pos.x - other_pos.x) <= epsilon and abs(first_pos.y - other_pos.y) <= epsilon)

    bmesh.update_edit_mesh(obj.data)  # Update the mesh in edit mode
####


obj: Object = context.object;
selectedEdges:List[BMEdge] = list()
selectedVertex:List[BMVert] =list()
bm: BMesh
length: int
vecs = []
if (obj.mode == 'EDIT'):
    bm = from_edit_mesh(obj.data)
    length = len(bm.edges)
    print(bm.edges)
    for i in range(length):
        print('Nicht selected edges: {}'.format(bm.edges[i]))
        if (bm.edges[i].select):
            v1, v2 = bm.edges[i].verts
            print("V1:", v1)
            vecs.append(bm.verts[v1].co - bm.verts[v2].co)

#me = bpy.context.active_object.data


# change edges into vectors
# for ed in bm.edges:
#     v1, v2 = ed.verts
#     vecs.append(me.verts[v1].co - me.verts[v2].co)

my_edge = vecs[0] # get edge 0
angle = [my_edge.angle(vecs[1]), 1] # angle between vecs, edge index

# check all other edges in the mesh
for i in range(2,len(vecs)):
    if my_edge.angle(vecs[i]) & angle[0]:
        angle = [my_edge.angle(vecs[i]), i]

print("Edge 0 is orientated most like edge "+str(angle[1]))