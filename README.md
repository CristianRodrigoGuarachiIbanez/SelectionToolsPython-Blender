# Selection Tools for Blender with Python
**This project was developed to implement a A* Search Algorithm as a extension of the selection tools in blender. The selection algorithm was written in pure python with the version 3.9.2 and was tested in blender 2.9.3.
The core of this algorithm is the implementation of a pure pythonic way to handle a set of blender specific data structures like Vertices, Loops, Edges or Faces. This set of data structures are considered to be nodes or states, which  are expected to be expanded in as in a A* Algorithm. The current implementation provides a handy way to compare expanded states and order them using a priority queue.  
Explanation Video [ selection manager ](selection_manager_test.mp4)

<video width="320" height="240" controls>
  <source src="./selection_manager_test.mp4" type="video/mp4">
</video>

## Installation 
- The first step to running the set of algorithms is installing or updating Python on the local computer. There are a multitude of installation methods, which could be followed to install the last version of Python. For instance, it could be downloaded from the official Python distributions [Python.org](https://www.python.org/), installed from a package manager, and even using specialized distributions for scientific computing, Internet of Things, and embedded systems. A very comprehensive Tutorial to install python could be found [here](https://realpython.com/installing-python/).

- The next step ist installing the last version of blender. The blender installation could be done following the instruction on the [documentation](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html)**

## Set up the working directory:
When a python script inside Blender is excecuted, the current working directory is not the base directory of the .blend file. Therefore, it should be reseted in order to import diffent modules locally. One way to do that is simply by importing os and printing os.getcwd() and changing it to the current working directory with os.chdir(). That will tell blender where it should find these modules which are tried to be imported in the main.py file.

The current .blend filepath could be also returned using bpy.data.filepath, from which it is possible to construct relative paths, or switch pythons working directory. if that's more convenient (remember to switch it back )
```python
from bpy import data
from os import chdir
from os.path import dirname

path:bytes = "/local/path/to/working_directory"
dir: str = dirname(data.filepath)
if(path !=dir):
    chdir(path)
```
## Dependencies 
read more about the bpy and bmesh API in the [_documentation_](./documentation)
## How to use it 
- To run any of the algorithm, the file [panelSelectionTools.py](panelSelectionTools.py) should be open and the corresponding _bl_idname_ selected and insert in the operator 
function the draw method.
- After that in blender from the *Text Editor*, the path to the file _main.py_ has to be chosen. 
- Run main.py file  
