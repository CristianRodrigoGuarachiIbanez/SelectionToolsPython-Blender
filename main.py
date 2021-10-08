#!/usr/bin/env python3
from importlib import reload
from bpy.props import StringProperty
from bpy import data
from bpy.utils import register_class, unregister_class
from typing import List, Dict
from os.path import dirname, basename, splitext
from os import chdir,getcwd
from bpy.types import Scene
import sys

path:str = r"C:\Users\Image Instruments\PycharmProjects/SelectionToolsPython-Blender"
dir: str = dirname(data.filepath)
if(path !=dir):
    chdir(path)
    if not (path in sys.path):
        sys.path.append(path)
    else:
        pass
print(getcwd())
from selectionManager.faceAnglePathSelectionManager import FacesAnglePathSelectionManager
from selectionManager.lengthEdgePathSelectionManager import LengthEdgePathSelectionManager
from panelSelectionTools import PANEL_PT_SelectionTools
from loopSelector.leftLoopsSelector import LeftLoopsSelector
from loopSelector.rightLoopsSelector import RightLoopsSelector
from loopSelector import leftLoopsSelector, rightLoopsSelector
from selectionManager import faceAnglePathSelectionManager, lengthEdgePathSelectionManager
import panelSelectionTools


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
    try:
        register_class(FacesAnglePathSelectionManager)
        register_class(LengthEdgePathSelectionManager)
        register_class(LeftLoopsSelector)
        register_class(RightLoopsSelector)
        register_class(PANEL_PT_SelectionTools)
    except ValueError or RuntimeError:
        reload(leftLoopsSelector)
        reload(faceAnglePathSelectionManager)
        reload(panelSelectionTools)

    Scene.long_string = StringProperty(name='long_string', default='')

def unregister() -> None:
    unregister_class(FacesAnglePathSelectionManager)
    unregister_class(LengthEdgePathSelectionManager)
    unregister_class(RightLoopsSelector)
    unregister_class(LeftLoopsSelector)
    unregister_class(PANEL_PT_SelectionTools)
    del Scene.long_string

if __name__ == "__main__":
    register();
    #unregister()