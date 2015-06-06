"""
    Purpose: To verify that Prim's algorithm has more desirable spanning trees
             in terms of its total weight than a Bread-First Search's spanning
             trees total weight, which is not guaranteed to be a minimum
             spanning tree like Prim's algorithm trees are.

"""
#-------------------------------------------------------------------------------

import random
from collections import defaultdict
from heapq import *


def main():
    for n in range(100, 500+1, 100): # n = 100, 200, 300, 400, 500
        sum = 0

        for i in range(1, 10+1):
            graph = randomize_graph(n)
            vertices = [v.id for v in graph.vertices]
            del vertices[0]

            rndVertex = random.randint(1, n)
            vertices[0],vertices[rndVertex-1] = vertices[rndVertex-1],vertices[0]

            BFS_Tree = BFS(graph.vertices[rndVertex], graph.edges)
            Prims_Tree = prims([str(v) for v in vertices], graph.edges)

            ratio = float(get_weight(Prims_Tree)) / get_weight(BFS_Tree)
            sum += ratio

        print "N =", n, "Avg Ratio:", float(sum)/10

# Classes

class Vertex(object):
    def __init__(self, id):
        self.id = id
        self.neighbours = []
        self.mark = "U" # U for 'Unvisited'

    # Used by Graph class. Never needs to be called by itself
    def add_neighbour(self, nbr):
        self.neighbours.append(nbr)

class Graph(object):
    def __init__(self):
        self.num_verts = 0
        self.vertices = []
        self.edges = []

    def add_vertex(self):
        # Creates a vertex given the id of the number of vertices (1, 2, 3...)
        self.vertices.append(Vertex(self.num_verts))
        self.num_verts += 1

    def add_edge(self, x, y, weight): # x, y are vertices, weight is int
        x.add_neighbour(y)
        y.add_neighbour(x)
        self.edges.append((x, y, weight))

    def is_edge(self, x , y): # x, y are vertices
        return y in x.neighbours

    # Displays a each vertex and all of its neighbours
    def show_graph(self):
        print "Vertex\tNeighbours\n"

        for i in range(1, self.num_verts):
            print str(i) + "\t\t",

            for nbr in self.vertices[i].neighbours:
                listNbrs = self.vertices[i].neighbours

                comma = "" if listNbrs.index(nbr) == (len(listNbrs)-1) else ","
                bOpen = "[" if listNbrs.index(nbr) == 0 else ""
                bClose = "]" if listNbrs.index(nbr) == (len(listNbrs)-1) else ""

                print bOpen + str(nbr.id) + comma + bClose,
            print ""
        print ""

    def show_edges(self):
        print "Edges\tWeight"
        for edge in self.edges:
            print "(" + str(edge[0].id) + ", "  + str(edge[1].id) + ")" +"\t"+\
                str(edge[2])
        print ""

def get_weight(spTree):
    return sum([edge[-1] for edge in spTree])

def BFS(v, edges):
    queue = [v]
    spanningTree = []
    v.mark = "V" # V for 'Visited'

    while len(queue) > 0:
        x = queue[0]
        del queue[0]

        for y in x.neighbours:
            if y.mark != "V":
                queue.append(y)
                for n1, n2, c in edges:
                    if (x, y) == (n1, n2):
                        spanningTree.append(((n1, n2), c))
                y.mark = "V"

    return spanningTree

def prims(nodes, edges):
    conn = defaultdict(list)

    for n1, n2, c in edges:
        conn[n1.id].append((c, n1.id, n2.id))
        conn[n2.id].append((c, n2.id, n1.id))

    mst = []
    used = set(nodes[1])
    usable_edges = conn[int(nodes[1])][:]
    heapify(usable_edges)

    while usable_edges:
        cost, n1, n2 = heappop(usable_edges)
        if n2 not in used:
            used.add(n2)
            mst.append(((n1, n2), cost))

            for e in conn[n2]:
                if e[2] not in used:
                    heappush(usable_edges, e)

    # Gets rid of duplicate edges (an edge and its vice-versa)
    # We want to keep track of non-directional edges only
    for e1 in mst:
        for e2 in mst:
            if e1[0][1] == e2[0][0] and e1[0][0] == e2[0][1]:
                del mst[mst.index(e2)]

    return mst

def randomize_graph(numVertices=6):
    n = numVertices
    G = Graph()
    # For all iterations up to n, we will say (n+1). The first vertex is
    # labelled with an id of 0, and the first iteration always starts at 1, so
    # i = 0 is never iterated, and therefore vertex 0 never used, since we
    # start counting at 1. Therefore, for consistency, all iterations are up to
    # n+1.

    [G.add_vertex() for i in range(n+1)]

    for i in range(2, n+1):
        x = random.randint(1, i-1)
        S = []

        for j in range(x):
            y = 0
            while not y in S:
                y = random.randint(1, x)
                if y not in S:
                    S.append(y)

        for s in S:
            w = random.randint(10, 100)
            G.add_edge(G.vertices[s], G.vertices[i], w)

    return G

main()