from queue import Queue
from classes.graph.graph import *


class Cache:
    def __init__(self, size):
        self._size = size
        self._pos = -1
        self._cacheQueue = Queue(maxsize=self._size)

    def updateCache(self, graph: Graph):
        if self._cacheQueue.qsize() < self._size:
            self._cacheQueue.put(graph)
            self._pos += 1
        else:
            self._cacheQueue.get()
            self._cacheQueue.put(graph)

    def clearAllStates(self):
        self._pos = -1
        self._cacheQueue.queue.clear()

    def getIncreasedState(self):
        graph = None
        if self._pos < self._cacheQueue.qsize() - 1:
            self._pos += 1
            graph = self._cacheQueue.queue[self._pos]
        return graph

    def getDecreasedState(self):
        graph = None
        if self._pos > 0:
            self._pos -= 1
            graph = self._cacheQueue.queue[self._pos]
        return graph
