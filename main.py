#!/usr/bin/env python3

from bpy.props import StringProperty
from bpy import data
from typing import List, Dict
from os.path import dirname
from os import chdir
import bpy
import sys

path:str = "/home/cristian/PycharmProjects/SelectionAlgorithm"
dir: str = dirname(data.filepath)
if(path !=dir):
    if not (path in sys.path):
        sys.path.append(path)
        chdir(path)
    else:
        pass

from selectionModeManager import SelectionManager
from panelSelectionTools import PANEL_PT_SelectionTools

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
    bpy.utils.register_class(SelectionManager)
    bpy.utils.register_class(PANEL_PT_SelectionTools)
    bpy.types.Scene.long_string = StringProperty(name='long_string', default='')


def unregister() -> None:
    bpy.utils.unregister_class(SelectionManager)
    bpy.utils.unregister_class(PANEL_PT_SelectionTools)
    del bpy.types.Scene.long_string


if __name__ == "__main__":
    register();