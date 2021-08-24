from bpy.props import StringProperty

from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict
from collections import defaultdict
from mathutils import Vector
from logging import info, INFO
from stateEdges import StateEdge
from queue import PriorityQueue
from numpy import ndarray, asarray, abs as absolut, array
import sys
import bpy


class SelectionModesManager(Operator):
    bl_idname: str = 'mesh.text';
    bl_label: str = 'show text';
    bl_options: Set[str] = {'REGISTER', 'UNDO'};
    def __init__(self) -> None:
        self.__obj: Object = context.object;
        self.__bm: BMesh;
        self.__selectedEdges: List[BMEdgeSeq] = list();
        #self.__selectedFaces: List[BMElemSeq] = list(); # save the faces
        #self.__extendedNodes: DefaultDict[int, List[BMEdge]] = defaultdict(list);
        self.__priorityQueue:PriorityQueue=PriorityQueue()
        self.__angles: List[float] = list()

    def __getEdges(self) -> List[BMEdgeSeq]:
        return self.__selectedEdges

    def __addStatesToRandList(self, state:StateEdge) -> None:
        self.__priorityQueue.put(state);

    def __deleteAllEdges(self) -> None:
        while not(self.__priorityQueue.empty()):
            try:
                self.__priorityQueue.get(False)
            except Exception:
                continue
            self.__priorityQueue.task_done()

    def calculateFacesAngle(self) -> None:
        pass
    def __randListe(self, state:StateEdge=None)->None:
        assert (state is not None),'state ist NoneType';
        assert(len(state.children)>0),'Children´s List is Empty';
        editedChildren:List[BMEdge]= None;
        children:List[StateEdge] = state.children[:]
        parentChildren:List[StateEdge] = state.parent.children[:] if(state.parent is not None) else None;
        if(parentChildren is not None):
            editedChildren = children + parentChildren;
            for i in range(len(editedChildren)):
                self.__addStatesToRandList(editedChildren[i])
        else:
            for j in range(len(children)):
                self.__addStatesToRandList(children[j])
    def __excludeDuplicates(self) -> List[int]:
        i:int;
        currIndex:int
        indices:List[BMEdge] = list();
        if (len(self.__selectedEdges)==1):
            return list(self.__selectedEdges[0].index)
        elif(len(self.__selectedEdges)<1):
            print('the list ist empty')
        for i in range(len(self.__selectedEdges)):
            indices.append(self.__selectedEdges[i].index) # saves the indices
        return list(set(indices)) # removes the duplicates

    def __constructEdgePath(self) -> StateEdge:
        start: int = 0;
        visited: List[int] = self.__excludeDuplicates() # list of edge indices [False] * len(self.__selectedEdges)
        nextEdge:BMEdge;
        # -------- clear dict EXTENDED NODES
        self.__deleteAllEdges()
        # ------------ declare and define StateEdges
        state:StateEdge = StateEdge(parent=None,action=self.__selectedEdges[0]);
        # ------ create children-edges
        state.createChildrenEdges();
        # ------ save the RAND LIST as a priority queue
        self.__randListe(state)
        while(True): # endlose Schleife
            # ------ look for the next edge and save in SELECTED EDGES
            #nextEdge = state.getScoreOfTheNextEdge();
            nextEdge = self.__priorityQueue.get()
            print('PRIORITY QUEUED EDGE{}, VERTEX{}'.format(nextEdge.action,nextEdge.node))
            assert (nextEdge is not None), 'there is none new selected edge'
            if(nextEdge.action == state.goal):
                visited.append(nextEdge.index);
                state = StateEdge(parent=state, action=nextEdge.action);
                self.__addEdges(start,state);
                print(' the goal EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge.action));
                return state;
            elif(nextEdge.index not in visited):
                start+=1;
                visited.append(nextEdge.index);
                self.__selectedEdges.append(nextEdge.action)
                print('a new EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge.action));
            elif(nextEdge.index in visited):
                continue
            # ------- save the last node, action and children into the class itself
            state = StateEdge(state, nextEdge[0]);
            # ------ create children-edges
            state.createChildrenEdges();
            # -------- save the status in EXTENDED NODES
            self.__randListe(state);
            print('a new OBJECT CLASS STATUS was added into the list of EXTENDED NODES!');
            start+=1;
            if (start == 20):
                while not(self.__priorityQueue.empty()):
                    print(self.__priorityQueue.get().action);
                return state;

    def __activeEdgesEDITMODE(self) -> None:
        #bm: BMesh = from_edit_mesh(self.__obj.data);
        EDGES:StateEdge=self.__constructEdgePath()
        i:int;
        currEdge:BMEdge=None;
        for i in range(len(EDGES)):
            currEdge = EDGES[i];
            currEdge.select=True;
            self.__bm.select_history.clear();
            self.__bm.select_history.add(currEdge);
        update_edit_mesh(self.__obj.data)

    def execute(self, context) -> Set[str]:
        self.__selectedEdges.clear();
        try:
            context.scene.long_string = 'values here:{}'.format(len(self.__selectedEdges))
            self.__activeEdgesEDITMODE()
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
        row_action_1_btn.operator('mesh.text', icon='WORLD_DATA', text='Print Values')

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
    bpy.utils.register_class(SelectionModesManager)
    bpy.utils.register_class(PANEL_PT_SelectionTools)
    bpy.types.Scene.long_string = StringProperty(name='long_string', default='')


def unregister() -> None:
    bpy.utils.unregister_class(SelectionModesManager)
    bpy.utils.unregister_class(PANEL_PT_SelectionTools)
    del bpy.types.Scene.long_string


if __name__ == "__main__":
    register();