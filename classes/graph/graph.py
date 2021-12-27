# Model

from classes.graph.edge import *
from classes.graph.vertex import *
import numpy as np


class Graph:
    def __init__(self, directed=False, weighted=False):
        self._vertexList = list()
        self._edgeList = list()
        self._isDirectedGraph = directed
        self._isWeightedGraph = weighted

    # Vertex methods
    def addVertex(self, vertex: Vertex):
        if vertex is not None:
            self._vertexList.append(vertex)

    def removeVertex(self, vertex: Vertex):
        if vertex is not None:
            for item in reversed(self._edgeList):
                if item.getStartVertex() == vertex or item.getEndVertex() == vertex:
                    self._edgeList.remove(item)

            for item in self._vertexList:
                item.removeAdjacentVertex(vertex)

            self._vertexList.remove(vertex)

    def findVertexByName(self, name: str):
        for item in self._vertexList:
            if item.getName() == name:
                return item

    # Edge methods
    def addEdge(self, edge: Edge):
        if edge is not None:
            startVertex = edge.getStartVertex()
            endVertex = edge.getEndVertex()

            self._edgeList.append(edge)
            startVertex.addAdjacentVertex(endVertex, edge)
            endVertex.addAdjacentVertex(startVertex, edge)

    def removeEdge(self, edge: Edge):
        if edge is not None:
            startVertex = edge.getStartVertex()
            endVertex = edge.getEndVertex()

            if startVertex == endVertex:
                startVertex.setLoop(value=False)

            self._edgeList.remove(edge)
            startVertex.removeAdjacentVertex(endVertex)
            endVertex.removeAdjacentVertex(startVertex)

    def findEdgeByName(self, name: str):
        for edge in self._edgeList:
            if edge.getName() == name:
                return edge

    def toggleEdgeDirection(self, edge: Edge):
        if edge in self._edgeList:
            edge.toggleDirection()
        self._isDirectedGraph = False
        for item in self._edgeList:
            if item.isDirected():
                self._isDirectedGraph = True

    def setEdgeWeight(self, edge: Edge, weight: int):
        if edge in self._edgeList:
            edge.setWeight(weight)

    def setDirected(self, value: bool):
        self._isDirectedGraph = value

    def setWeighted(self, value: bool):
        self._isWeightedGraph = value

    def findEdgeByVertexes(self, start: int, end: int):
        for edge in self._edgeList:
            if edge.getStartVertex() == start and edge.getEndVertex() == end:
                return edge

    # Utils
    def getVertexList(self):
        return self._vertexList

    def getEdgeList(self):
        return self._edgeList

    def isDirected(self):
        return self._isDirectedGraph

    def isWeighted(self):
        return self._isWeightedGraph

    def clear(self):
        self._edgeList.clear()
        self._vertexList.clear()

        self._isDirectedGraph = False
        self._isWeightedGraph = False

    def empty(self):
        return len(self._vertexList) == 0 and len(self._edgeList) == 0

    def setEdgesFromAdjacentMatrix(self, adjMatrix):  # Rina
        self._edgeList.clear()
        vertexList = self.getVertexList()
        vertexListSize = len(vertexList)

        for i in range(vertexListSize):
            for j in range(i, vertexListSize):
                if i == j and adjMatrix[i][j] != 0:
                    edge = Edge(vertexList[i], vertexList[j],
                                name=str(len(self.getEdgeList()) + 1),
                                weight=int(adjMatrix[i][j]))
                    self.addEdge(edge)
                else:
                    if adjMatrix[i][j] == adjMatrix[j][i] and adjMatrix[i][j] != 0:
                        edge = Edge(vertexList[i], vertexList[j],
                                    name=str(len(self.getEdgeList()) + 1),
                                    weight=int(adjMatrix[i][j]),
                                    direction=False)
                        self.addEdge(edge)

        for i in range(vertexListSize):
            for j in range(vertexListSize):
                if i != j and adjMatrix[i][j] != adjMatrix[j][i] and adjMatrix[i][j] != 0:
                    edge = Edge(vertexList[i], vertexList[j],
                                name=str(len(self.getEdgeList()) + 1),
                                weight=int(adjMatrix[i][j]),
                                direction=True)
                    self.addEdge(edge)

    def getAdjacentMatrix(self):
        m = len(self._vertexList)
        matrix = np.array([[0] * m] * m)
        for edge in self._edgeList:
            start = self._vertexList.index(edge.getStartVertex())
            end = self._vertexList.index(edge.getEndVertex())
            matrix[start][end] = edge.getWeight()
            if not edge.isDirected():
                matrix[end][start] = edge.getWeight()
        return matrix

    def getIncidenceMatrix(self):
        n = len(self._edgeList)
        m = len(self._vertexList)
        matrix = np.array([[0] * n] * m)
        i = 0
        for edge in self._edgeList:
            start = self._vertexList.index(edge.getStartVertex())
            end = self._vertexList.index(edge.getEndVertex())
            matrix[start][i] = 1
            if edge.isDirected():
                matrix[end][i] = -1
            else:
                matrix[end][i] = 1
            i += 1
        return matrix
