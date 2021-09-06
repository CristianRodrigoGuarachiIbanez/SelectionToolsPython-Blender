from bpy.props import StringProperty
from bmesh.types import BMElemSeq, BMEdgeSeq, BMFaceSeq, BMVertSeq
from bmesh.types import BMVert, BMEdge, BMFace, BMesh, BMLoop
from bpy import context
from bpy.types import Object, Operator, Panel, ID
from bmesh import from_edit_mesh, update_edit_mesh
from typing import List, Tuple, Dict, Any, TypeVar, Generator, Callable, Set, DefaultDict, Reversible
from queue import PriorityQueue
from stateEdges import StateEdge
from abc import ABCMeta, ABC
import bpy

class SelectionManager(Operator):
    bl_idname: str = 'selection.manager';
    bl_label: str = 'show searching path';
    bl_options: Set[str] = {'REGISTER', 'UNDO'};
    def __init__(self) -> None:
        self.__obj:Object = context.object;
        self.__bm:BMesh;
        self.__selectedEdges:List[BMEdgeSeq] = list();
        #self.__selectedFaces:List[BMElemSeq] = list(); # save the faces
        self.__priorityQueue:PriorityQueue=PriorityQueue()
        self.__angles:List[float] = list()
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
    def __setSelectedEdges(self)->None:
        length:int;
        if(self.__obj.mode == 'EDIT'):
            self.__bm = from_edit_mesh(self.__obj.data)
            length=len(self.__bm.edges)
            for i in range(length):
                if(self.__bm.edges[i].select):
                    print('selected edges: {}'.format(self.__bm.edges[i]))
                    self.__selectedEdges.append(self.__bm.edges[i])
        else:
            print("Object is not in edit mode.")
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
            return [self.__selectedEdges[0].index]
        elif(len(self.__selectedEdges)<1):
            print('the list ist empty')
        for i in range(len(self.__selectedEdges)):
            indices.append(self.__selectedEdges[i].index) # saves the indices
        return list(set(indices)) # removes the duplicates
    @staticmethod
    def __checkNodeInStatus(action:StateEdge, currState:StateEdge)->bool:
        assert ((currState is not None) and (action is not None)), 'it can not create children because the parent is NoneType';
        vertices: List[BMVert] = [vert for vert in action.action.verts]
        if(currState.node in vertices):
            return True
        else:
            return False  # ------- > ändere das was hier zurückgeliefert wird
    @staticmethod
    def __extractStatesParents(stateValue:StateEdge)->List[BMEdge]:
        parents:List[BMEdge] = list()
        action:StateEdge = stateValue.parent;
        if (action is not None): parents.append(action.action);
        i:int = 0
        while (True):
            if (action.parent is None):
                break
            try:
                action = action.parent
                print('index:{}, action:{}'.format(i, action))
                parents.append(action.action)
            except Exception as e:
                print('[Exception] :', e)
            i += 1
        return parents
    def __constructEdgePath(self) -> List[BMEdge]:
        start: int = 0;
        visited: List[int] = self.__excludeDuplicates() # list of edge indices [False] * len(self.__selectedEdges)
        nextEdge:BMEdge;
        parentNode:bool;
        actions:List[List[BMEdge]]=list();
        # -------- clear dict EXTENDED NODES
        self.__deleteAllEdges()
        # ------------ declare and define StateEdges, first call has none SCORE
        state:StateEdge = StateEdge(parent=None,action=self.__selectedEdges[0]);
        # ------ create children-edges
        state.createChildrenEdges();
        # ------ save the RAND LIST as a priority queue
        self.__randListe(state)
        while(True): # endlose Schleife
            # ------ look for the next edge and save in SELECTED EDGES
            nextEdge = self.__priorityQueue.get()
            print('PRIORITY QUEUED EDGE{}, VERTEX{}'.format(nextEdge.action,nextEdge.node))
            assert (nextEdge is not None), 'there is none new selected edge'
            if(nextEdge.action == state.goal):
                visited.append(nextEdge.action.index);
                state = StateEdge(parent=state, action=nextEdge.action);
                self.__selectedEdges.append(state.action);
                print(' the goal EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge.action));
                while not (self.__priorityQueue.empty()):
                    actions.append(self.__priorityQueue.get().action);
                break;
            elif(nextEdge.action.index not in visited):
                start+=1;
                visited.append(nextEdge.action.index);
                self.__selectedEdges.append(nextEdge.action)
                print('a new EDGE {} was selected and added into SELECTED EDGES!'.format(nextEdge.action));
            elif(nextEdge.action.index in visited):
                continue
            # -------- check if parent node in current edge
            parentNode = self.__checkNodeInStatus(nextEdge,state)
            # ------- save the last node, action and children into the class itself
            if(parentNode is True):
                state = StateEdge(state, nextEdge.action)
                # ------ calculate the score for the current edge
                state.calculateTheScore()
            else:
                # ------ the last state will be saved into the priority queue
                self.__addStatesToRandList(state);
                state = nextEdge
            # ------ create children-edges
            state.createChildrenEdges();
            # -------- save the status in EXTENDED NODES
            self.__randListe(state);
            print('a new OBJECT CLASS STATUS was added into the list of EXTENDED NODES!');
            start+=1;
            if (start == 30):
                actions.append(self.__extractStatesParents(state))
                while not(self.__priorityQueue.empty()):
                    actions.append(self.__extractStatesParents(self.__priorityQueue.get()));
                break;
        return actions
    def __activateEdgesEDITMODE(self,EDGES:List[BMEdge]) -> None:
        #bm: BMesh = from_edit_mesh(self.__obj.data);
        i:int;
        currEdge:BMEdge=None;
        for i in range(len(EDGES)):
            currEdge = EDGES[i];
            currEdge.select=True;
            self.__bm.select_history.clear();
            self.__bm.select_history.add(currEdge);
        update_edit_mesh(self.__obj.data)
    def execute(self, context) -> Set[str]:
        self.__selectedEdges.clear()
        try:
            self.__setSelectedEdges()
            actions = self.__constructEdgePath()
            self.__activateEdgesEDITMODE(actions)
            context.scene.long_string = '[Output Info]:{}'.format(len(actions))
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, e.args)
            return {'CANCELLED'}
