bl_info = {
    "name": "Multiple operator example",
    "author": "Robert Guetzkow",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > My own addon",
    "description": "Example with multiple operators",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}

from bpy.types import Object
from bmesh.types import BMesh, BMEdge, BMVert, BMFace
import bpy
from  bmesh import from_edit_mesh
from typing import List, Tuple, Dict, Any, Generator

class SelectionModesManager:
    def __init__(self) -> None:
        self.__obj: Object = bpy.context.object
        self.__selectedEdges: List[] = list();
    def generateSelectedEdges() -> Generator:
        length: int = len(self.__selectedEdges)
        for i in range(length):
            yield self.__selectedEdges[i];
        
    def __EdgeRetriever(self) -> None:
        bm:BMesh
        length: int
        if (obj.mode == 'EDIT'):
            bm=from_edit_mesh(obj.data)
            length = len(bm.edges)
            #print(length)
            #for i, v in enumerate(bm.verts):
            for i in range(length):
                #print('Nicht selected edges: {}'.format(bm.edges[i]))
                if(bm.edges[i].select):
                    print('selected edges: {}'.format(bm.edges[i]))
                    self.__selectEdges.append(bm.edges[i])
         else:
             print("Object is not in edit mode.")
     def exceute(self, context) -> None:
         self.__selectedEdges.clear()
         self.__EdgeRetriever();
         gen: Generator = 
          
edges: List[BMEdge] = list()               
obj:Object =bpy.context.object
bm:BMesh

length: int
if (obj.mode == 'EDIT'):
    bm=from_edit_mesh(obj.data)
    #length = len(bm.verts)
    length = len(bm.edges)
    #for i, v in enumerate(bm.verts):
    for i in range(length):
        #print(bm.verts[i])
        print(bm.edges[i])
        if(bm.edges[i].select):
            print(bm.edges[i])
            edges.append(bm.edges[i])
else:
    print("Object is not in edit mode.")
    
print(edges)

import bmesh
from bpy import context as C

m = C.active_object.data
bm = bmesh.from_edit_mesh(m)

indices = [0,1]
edges: BMEdge = bm.edges
length: int = len(bm.edges)
for i in range(length):
    print(edges[i])
    #if edges[i].verts[0].index in indices and edges[i].verts[1].index in indices:
    if(edges[i].index in indices):
        edges[i].select = True
        break