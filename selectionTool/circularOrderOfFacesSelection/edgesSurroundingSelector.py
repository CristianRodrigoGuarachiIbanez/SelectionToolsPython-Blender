#!/usr/bin/env python3.8
from bpy.props import StringProperty
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict, Reversible
import bpy
'''
check https://b3d.interplanety.org/en/learning-loops/
'''
T:TypeVar = TypeVar('T', BMEdge, BMLoop, Generator)
class EdgesSurroundingSelector(Operator):
    bl_idname: str = 'surrounding.selector';
    bl_label: str = 'surrounding faces selector';
    bl_options: Set[str] = {'REGISTER', 'UNDO'};
    bm: BMesh;
    obj:Object;
    selectedVertex:List[BMEdge];
    faces:List[BMFace];
    def __init__(self)->None:
        self.obj: Object = context.object;
        self.selectedVertex:List[BMEdge] = list()
        self.faces:List[BMFace]=None;
    def collectSelectedEdge(self)->List[BMEdge]:
        length:int
        elem:List[BMEdge];
        verticesTemp:BMElemSeq;
        if (self.obj.mode == 'EDIT'):
            self.bm = from_edit_mesh(self.obj.data)
            length = len(self.bm.edges)
            elem = self.bm.edges;
            for i in range(length):
                # print('Nicht selected edges: {}'.format(bm.edges[i]))
                if (elem[i].select):
                    print('selected edges: {}'.format(elem[i]))
                    verticesTemp = elem[i].verts
                    for j in range(len(verticesTemp)):
                        self.selectedVertex.append(verticesTemp[j])
        else:
            print("Object is not in edit mode.")
        return list(set(self.selectedVertex))
    def connectedLoopAroundVertexForPath(self)->Generator:
        vertices:List[BMVert]= self.collectSelectedEdge()
        loops:List[BMLoop] =None;
        faces:List[BMFace] =None;
        # print('Vertices:', vertices)
        for i in range(len(vertices)):
            loops= self.connectedLoopsAroundVertex(vertices[i]);
            faces = self.__loopsToFace(loops)
            for j in range(len(faces)):
                yield faces[j]
    def connectedLoopsAroundVertex(self, vertex:BMVert)->List[BMLoop]:
        '''
        Return Loops around param vertex in counter-clockwise order
        :param vertex: start vertex
        :return: a list of BMEdge
        '''
        #vertex.link_edges.index_update()
        # first_edge:BMEdge = vertex.link_edges[0]
        first_edge:BMLoop= vertex.link_loops[0]
        edges_CCW_order:List[BMLoop] = []

        edge:T = first_edge
        while(edge not in edges_CCW_order):
            edges_CCW_order.append(edge)
            try:
                edge = self.__rightEdgeForEdgeRegardToVertex(edge, vertex)
                edge = next(edge);
                #print(edge)
            except StopIteration as s:
                print('[INFO:]', s)
        return edges_CCW_order
    @staticmethod
    def __rightEdgeForEdgeRegardToVertex(edge:BMLoop, vertex:BMVert)->Generator:
        '''
         Yield the right edge of param edge regard to param vertex
        :param edge: last selected BMEdge
        :param vertex: start Vertex
        :return: a BMEdge
        '''
        right_loop:BMLoop = None
        loops:BMElemSeq = edge.edge.link_loops
        for i in range(len(loops)):
            if (loops[i].vert == vertex):
                right_loop = loops[i]
                #print(right_loop.link_loop_prev)
                yield right_loop.link_loop_prev
    @staticmethod
    def __loopsToFace(loops:List[BMLoop])->List[BMFace]:
        faces:List[BMFace]=list()
        for i in range(len(loops)):
            faces.append(loops[i].face)
        return faces
    def __changeSelectionMode(self)->None:
        sel_mode = context.tool_settings.mesh_select_mode
        if (sel_mode[1] or sel_mode[2]):  # edge or face
            bpy.ops.mesh.select_mode(type='FACE')
        else:  # face
            bpy.ops.mesh.select_mode(type='FACE')
    def activateEdgesEDITMODE(self) -> None:
        # bm: BMesh = from_edit_mesh(self.__obj.data);
        edges=self.connectedLoopAroundVertexForPath()
        currEdge:BMEdge=None;
        i:int=0;
        for edge in edges:
            print('index i:{}, edges:{}'.format(i, edge))
            currEdge = edge;
            currEdge.select = True;
            self.bm.select_history.clear()
            self.bm.select_history.add(currEdge)
            self.__changeSelectionMode()
            i+=1
        update_edit_mesh(self.obj.data);
    def execute(self, context) -> Set[str]:
        actions:List[List[BMEdge]];
        try:
            self.activateEdgesEDITMODE()
            #context.scene.long_string = '[Output Info]:{}'.format(len(self.selectedEdges[0]))
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, e.args)
            return {'CANCELLED'}
class PANEL_PT_SelectionTools(Panel):
    bl_idname: str = 'PANEL_PT_SelectionTools'
    bl_label: str = 'Selection_Tools'
    bl_space_type: str = 'VIEW_3D'
    bl_region_type: str = 'UI'
    bl_category: str = 'Panel Selection Tools'

    def draw(self, context) -> None:
        row_action_1_btn = self.layout.row()
        row_action_1_btn.operator('surrounding.selector', icon='WORLD_DATA', text='Run')

        # Text area
        row_text = self.layout.row()
        text = context.scene.long_string
        row_text.label(text=text, icon='WORLD_DATA')


bl_info: Dict[str, str] = {
    "name": "Textbox",
    "author": "cristguarachi@gmail.com",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Selection Tools Addon",
    "category": "Development",
}

def register() -> None:
    bpy.utils.register_class(EdgesSurroundingSelector)
    bpy.utils.register_class(PANEL_PT_SelectionTools)
    bpy.types.Scene.long_string = StringProperty(name='long_string', default='')


def unregister() -> None:
    bpy.utils.unregister_class(EdgesSurroundingSelector)
    bpy.utils.unregister_class(PANEL_PT_SelectionTools)
    del bpy.types.Scene.long_string


if __name__ == "__main__":
    register();

#if __name__ == '__main__':
    #unittest.main()
    #nextEdge: EdgesAroundVertexSelector = EdgesAroundVertexSelector();
    #vertex:BMVert=nextEdge.collectSelectedEdge()
    #activeEdges:List[BMEdge] =nextEdge.connectedEdgesFromVertex_CCW(vertex)
    #nextEdge.activateEdgesEDITMODE()
