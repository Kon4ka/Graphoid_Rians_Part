from classes.graph.graph import *


def complete(graph: Graph):
    matrix = graph.getAdjacentMatrix()
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if matrix[x][y] > 0 or x == y:
                matrix[x][y] = 0
            else:
                matrix[x][y] = 1
    adjMatrix = matrix + graph.getAdjacentMatrix()
    print(adjMatrix)
    graph.setEdgesFromAdjacentMatrix(adjMatrix)
