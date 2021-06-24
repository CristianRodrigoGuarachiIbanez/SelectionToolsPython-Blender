#!/usr/bin/env python3
# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class
from bpy.types import Scene
from bpy import data
from typing import List, Dict
from os.path import dirname
import bpy
import sys

dir: str = dirname(data.filepath)
if not (dir in sys.path):
    sys.path.append(dir)
else:
    pass

from viewPrinter import MESH_TxtPrinter
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
    bpy.utils.register_class(MESH_TxtPrinter)
    bpy.utils.register_class(PANEL_PT_SelectionTools)
    bpy.types.Scene.long_string = StringProperty(name='long_string', default='')


def unregister()-> None:
    bpy.utils.unregister_class(MESH_TxtPrinter)
    bpy.utils.unregister_class(PANEL_PT_SelectionTools)
    del bpy.types.Scene.long_string


if __name__ == "__main__":
    register()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
