



vertices = __getNextEdges(selectedEdges[0])
print(vertices)
visited: List[bool] = [False] * len(graph)
print(visited)
queue: List[BMEdge] =[selectedEdges[0]]
print(queue)
currEdge: BMEdge
nextEdge: BMEdge
currVertex: BMVert
edgeLength:float
angle:float
i: int = 0;
while(len(queue)>0):
    currEdge= queue.pop(0);
    edgeLength = currEdge.calc_length();
    currVertex = vertices[i];
    print('current Edge: {}, edge length: {}, current vertices: {}'.format(currEdge, edgeLength, currVertex))
    if (visited[i] is True):
        print('index i:{}, edge: {}'.format(i, self.__graph[currVertex][i]));
        continue;
    print(len(graph[currVertex]))
    for j in range(len(graph[currVertex])): 
        nextEdge = self.__graph[currVertex][i];
        angle = self.__edgeAngle(currEdge, nextEdge);
        print('index i: {}, index j: {}, angle value: {}'.format(i, j, angle));
        if(edgeLength == nextEdge.calc_length()):
            print('current edge length: {}, next edge length: {}'.format(edgeLength, nextEdge.calc_length()));
    visited[i] = True;
    i+=1


def __getNextEdges(edge: BMEdge) -> None:
    currVertex: BMVert
    vertexIndex: int
    nextEdges: BMElemSeq[BMEdge]
    vertices: List[BMVert] = [vert for vert in edge.verts]
    print(vertices)
    vertices2 = vertices.copy()	
    for i in range(len(vertices)):
        currVertex = vertices.pop()
        nextEdges = currVertex.link_edges # <BMElemSeq object at 0x7fd9d5c99780>
        for i in range(len(nextEdges)):
            addEdges(currVertex, nextEdges[i])
    return vertices2


def edgeAngle(edge1: BMEdge, edge2: BMEdge) -> float:
    b:BMVert = set(edge1.verts).intersection(edge2.verts).pop()
    a:Vector = edge1.other_vert(b).co - b.co
    c:Vector = edge2.other_vert(b).co - b.co
    return a.angle(c);

def addEdges( key: BMVert, values: List[BMEdge]) -> None:
        graph[key].append(values);


obj: Object = context.object;
selectedEdges: List[BMEdge] = list()
bm: BMesh
length: int
if (obj.mode == 'EDIT'):
    bm = from_edit_mesh(obj.data)
    length = len(bm.edges)
    print(bm.edges)
    # for i, v in enumerate(bm.verts):
    #assert(length <=3), "there could be more than 3 Edges selected"
    for i in range(length):
        # print('Nicht selected edges: {}'.format(bm.edges[i]))
        if (bm.edges[i].select):
            print('selected edges: {}'.format(bm.edges[i]))
            selectedEdges.append(bm.edges[i])
else:
    print("Object is not in edit mode.")
