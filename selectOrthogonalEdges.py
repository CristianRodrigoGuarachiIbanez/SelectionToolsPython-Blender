"""
https://blender.stackexchange.com/questions/182182/how-to-select-with-python-code-only-vertical-edges-from-cube
"""
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