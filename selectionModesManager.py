#!/usr/bin/env python3
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh
from bpy import context
from bpy.types import Object, Operator
from bmesh import from_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set
from logging import info

#for obj in bpy.data.objects:
#    obj.select_set(False)
#    print(obj)
#    
#    
#ob = bpy.context.scene.objects["object_1"]       # Get the object
##bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
#bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
#ob.select_set(True)                          # Select the cube



##----------------------- select vertices of a mesh --------------------#
#import bpy,bmesh

#ob   = bpy.data.objects['object_1']
#mesh = bmesh.from_edit_mesh(ob.data)
#for v in mesh.verts:
#    v.select = True
#    print(v)

## trigger viewport update
#bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.active


# 
#obj = bpy.context.view_layer.objects.active
# 
#z=0
#mesh = obj.data
#for index in range(6):
#       for vert in mesh.vertices:
#              x = vert.co.x
#              y = vert.co.y
#              bpy.ops.mesh.primitive_uv_sphere_add(radius=.05,location=(x,y,z))
#       z+=.5
#       

#    import bpy
#    import bmesh

#    me = bpy.context.edit_object.data

#    #get bmesh (Object needs to be in Edit mode)
#    bm=bmesh.from_edit_mesh(me)

#    bm.select_history.add(bm.verts[5])

#    #print active vert:
#    print(bm.select_history.active)
    
    

class SelectionModesManager: #(Operator):
    #bl_idname = "view3d.selection"  # idname to display the operator
    #bl_label = "selector"
    #bl_description = "saves the selected edges or vertices in a list"
    def __init__(self):

        self.__obj: Object = context.object;
        self.__selectedEdges: List[BMEdgeSeq] = list()

    def getEdges(self) -> List[BMEdgeSeq]:
        return self.__selectedEdges

    def generateVertices(self) -> Generator:
        v1: BMVert
        v2: BMVert
        length: int = len(self.__selectedEdges)
        assert (length > 0), 'there is NONE active vertices';
        for i in range(length):
            v1, v2 = self.__selectedEdges[i].verts
            yield v1, v2;

    def generateEdges(self) -> Generator:
        length: int = len(self.__selectedEdges)
        assert(length > 0), 'there ist none active edges';
        for i in range(length):
            yield self.__selectedEdges[i];

    def __gatherElementSequences(self) -> None:

        bm: BMesh
        length: int
        if (self.__obj.mode == 'EDIT'):
            bm = from_edit_mesh(self.__obj.data)
            length = len(bm.edges)
            # print(length)
            # for i, v in enumerate(bm.verts):
            for i in range(length):
                # print('Nicht selected edges: {}'.format(bm.edges[i]))
                if (bm.edges[i].select):
                    print('selected edges: {}'.format(bm.edges[i]))
                    self.__selectedEdges.append(bm.edges[i])
        else:
            print("Object is not in edit mode.")

    # def execute(self, context: Any) -> Set[str]:
    #     self.__selectedEdges.clear();
    #     self.__gatherElementSequences();
    #     return {'FINISHED'}
             
def register():
    from bpy.utils import register_class
    #register_class(EdgesSelector)
    pass
    

def unregister():
    from bpy.utils import unregister_class
    #unregister_class(EdgesSelector)
    pass
      
if __name__ == '__main__':
    #register()
    pass
    
