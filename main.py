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
# reload(splitext(basename(__file__))[0])
path:str = "/home/cristian/PycharmProjects/SelectionAlgorithm"
dir: str = dirname(data.filepath)
if(path !=dir):
    chdir(path)
    if not (path in sys.path):
        sys.path.append(path)
    else:
        pass
print(getcwd())
from selectionModeManager import SelectionManager
from panelSelectionTools import PANEL_PT_SelectionTools
from edgesSurroundingSelector import EdgesSurroundingSelector
import edgesSurroundingSelector, panelSelectionTools, selectionModeManager

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
        register_class(SelectionManager)
        register_class(EdgesSurroundingSelector)
        register_class(PANEL_PT_SelectionTools)
    except ValueError or RuntimeError:
        reload(edgesSurroundingSelector)
        reload(selectionModeManager)
        reload(panelSelectionTools)

    Scene.long_string = StringProperty(name='long_string', default='')

def unregister() -> None:
    unregister_class(SelectionManager)
    unregister_class(EdgesSurroundingSelector)
    unregister_class(PANEL_PT_SelectionTools)
    del Scene.long_string

if __name__ == "__main__":
    register();
    #unregister()