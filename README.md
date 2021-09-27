# Selection Tools for Blender with Python
**this project was developed to implement a A* Search Algorithm as a extension of the selection tools in blender. The selection algorithm was written in pure python with the version 3.9.2 and was tested in blender 2.9.3.
The core of this algorithm is the implementation of a pure pythonic data structure to handle the gathered blender specific data structures like Vertices, Loops, Edges or Faces. This data structure represents the current status to be expanded in a A* Algorithm and provides a handy way to compare expanded states and order them in a priority queue.  
![ selection manager ](selection_manager_test.mp4)
## Installation 
- the first step to running the set of algorithms is installing or updating Python on the local computer. There are a multitude of installation methods: you can download official Python distributions from [Python.org](https://www.python.org/), install from a package manager, and even install specialized distributions for scientific computing, Internet of Things, and embedded systems. A very comprehensive Tutorial to install python could be found [here](https://realpython.com/installing-python/).

- the blender installation could be done following the instruction on the [documentation](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html)**
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

## How to use it 
**see the file _documentation.txt_ above**
