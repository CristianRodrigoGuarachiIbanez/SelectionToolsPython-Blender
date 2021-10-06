from bpy.props import StringProperty
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context, data
from bpy.utils import register_class, unregister_class
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, TypeVar, Generator, Callable, Set, DefaultDict, Reversible
import bpy
from os import getcwd, chdir
from os.path import dirname
import sys
# reload(splitext(basename(__file__))[0])
path:str = r"C:\Users\Image Instruments\PycharmProjects/SelectionToolsPython-Blender"
dir: str = dirname(data.filepath)
if(path !=dir):
    chdir(path)
    if not (path in sys.path):
        sys.path.append(path)
    else:
        pass
print(getcwd())
from facesSelectionManager import FacesSelectionManager as FSManager

T:TypeVar = TypeVar('T', BMEdge, BMLoop, Generator)
class EdgesSurroundingSelector(Operator):
    bl_idname: str = 'surrounding.selector';
    bl_label: str = 'surrounding faces selector';
    bl_options: Set[str] = {'REGISTER', 'UNDO'};
    bm: BMesh;
    _EDGEs:List[BMEdge];
    _VERTEx:List[BMVert];
    _FSM:FSManager;
    def __init__(self)->None:
        self.obj: Object = context.object;
        self._EDGEs = list()
        self._VERTEx = list()
        self._FSM = FSManager()
    def __collectSelectedEdge(self)->List[BMVert]:
        vertices:BMElemSeq;
        length: int
        if (self.obj.mode == 'EDIT'):
            self.bm = from_edit_mesh(self.obj.data)
            length = len(self.bm.edges)
            print(self.bm.edges)
            for i in range(length):
                if (self.bm.edges[i].select):
                    print('selected EDGES: {}'.format(self.bm.edges[i]))
                    self._FSM.setLoops(self.bm.edges[i])
                    vertices = self.bm.edges[i].verts
                    for j in range(len(vertices)):
                        self._VERTEx.append(vertices[j])
        else:
            print("Object is not in edit mode.")
        return self._VERTEx
    def linkedLoops(self)->List[BMLoop]:
        # first_edge:BMEdge = vertex.link_edges[0]
        vertices: List[BMElemSeq] = list(self.__collectSelectedEdge())
        print("VERTICES:", vertices)
        first_loop: BMLoop;
        loop: T;
        loopsList: Set[BMLoop] = set()
        for i in range(len(vertices)):
            vertices[i].link_edges.index_update()
            loop = vertices[i].link_loops
            for j in range(len(loop)):
                loopsList.add(loop[j])
        return list(loopsList)
    def linkedLoopsTop(self)->List[BMLoop]:
        self.__collectSelectedEdge()
        self._FSM.recoverNextLoop()
        return self._FSM.getLoops()
    def __loopsToFace(self)->List[BMFace]:
        faces:List[BMFace]=list()
        loops:List[BMLoop] = self.linkedLoopsTop()
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
        i: int;
        faces:List[BMFace] = self.__loopsToFace()
        #faces:List[BMEdge]=[loop.edge for loop in self.linkedLoops()]
        currFace:BMEdge;
        for i in range(len(faces)):
            print('index i:{}, face:{}'.format(i, faces[i]))
            currFace = faces[i];
            currFace.select = True;
            self.bm.select_history.clear()
            self.bm.select_history.add(currFace)
            self.__changeSelectionMode()
        update_edit_mesh(self.obj.data)
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
        row_action_1_btn.operator('surrounding.selector', icon='WORLD_DATA', text='Run Path Search')

        # Text area
        row_text = self.layout.row()
        text = context.scene.long_string
        row_text.label(text=text, icon='WORLD_DATA')

def register() -> None:
    register_class(EdgesSurroundingSelector)
    register_class(PANEL_PT_SelectionTools)
    bpy.types.Scene.long_string = StringProperty(name='long_string', default='')

def unregister() -> None:
    unregister_class(EdgesSurroundingSelector)
    unregister_class(PANEL_PT_SelectionTools)
    del bpy.types.Scene.long_string
if __name__ == "__main__":
    register();