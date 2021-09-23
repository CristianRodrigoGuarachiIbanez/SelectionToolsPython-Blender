
# Data Structures in Blender

**The data structures in Blender are accessible for python in the bmesh data structures. There could be found, at the most basic level, four main element structures:**
**- Faces**

**- Loops (stores per-face-vertex data, uvs, vcols, etc)**

**- Edges**

**- Verts**

##Vertices
**Vertices store a coordinate and link to an edge in the disk cycle of the vertex (covered below).**

##Edges
**Edges represent a connection between two vertices, but also store a link to a loop in the radial cycle of the edge (covered below).**

##Loops
**Loops define the boundary loop of a face. Each loop logically corresponds to an edge, though the loop is local to a single face so there will usually be more than one loop per edge (except at boundary edges of the surface).**

###_Loops store several handy pointers_:

**e - pointer to the loop's edge
v - pointer to the vertex at the start of the edge (where "start" is defined by CCW order)
f - pointer to the face associated with this loop.
Loops store per-face-vertex data (amongst other things outlined later in this document).**

##Faces
**Faces link to a loop in the loop cycle, the circular linked list of loops defining the boundary of the face.**


The mesh data is accessed in object mode and intended for compact storage, for more flexible mesh editing from python see
