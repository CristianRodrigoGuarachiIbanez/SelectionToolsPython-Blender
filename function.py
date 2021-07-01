



vertices = __getNextEdges(selectedEdges[0])
print(vertices)
visited: List[bool] = [False] * len(graph)
print(visited)
queue: List[BMEdge] =[selectedEdges[0]]
print(queue)
visited[0] = True;
currEdge: BMEdge
currVertex: BMVert
angle:float
i: int = 0;
while(len(queue)>0):
    currEdge= queue.pop(0)
    vertexIndex = currEdge.index
    #if(
    currVertex = vertices[i]
    print(len(graph[currVertex]))
    for j in range(len(graph[currVertex])): 
        
        #if(visited[i]):
        #    continue
        angle = edgeAngle(currEdge, graph[currVertex][j])
        print('index i: {}, index j {}, angle: {}'.format(i, j, angle))
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

def addEdges( key: BMVert, values: BMElemSeq[BMEdge]) -> None:
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
