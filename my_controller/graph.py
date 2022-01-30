from collections import defaultdict

class Graph:
    def __init__(self, connections=[]):
        self.__graph = defaultdict(set)
        self.nodes = []
        self.add_connections(connections)

    def add_connections(self, connections):
        for node1, node2 in connections:
            self.add(node1, node2)
    
    def add(self, node1, node2):
        node1Found = False
        node2Found = False
        for node in self.nodes:
            if node.value == node1.value:
                node1Found = True
            elif node.value == node2.value:
                node2Found = True
        if node1Found == False:
            self.nodes.append(node1)
        if node2Found == False:
            self.nodes.append(node2)
        self.__graph[node1.value].add(Edge(node2.value, 0.5))
        self.__graph[node2.value].add(Edge(node1.value, 0.5))
    
    def getGraph(self):
        return self.__graph
    
    def getNode(self, nodeValue):
        found = None
        for node in self.nodes:
            if node.value == nodeValue:
                found = node
        return found
    
    def findPath(self, node1, node2, path=[]):
        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self.__graph:
            return None
        for edge in self.__graph[node1]:
            if edge.node not in path:
                new_path = self.findPath(edge.node, node2, path)
                if new_path:
                    return new_path
        return None

    def setNodeVisited(self, nodeValue):
        for node in self.nodes:
            if node.value == nodeValue:
                node.visited = True

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.__graph))

class Node:
    def __init__(self, value):
        self.value = value
        self.visited = False

    def __repr__(self):
        return '{}({},visited={})'.format(self.__class__.__name__, self.value, self.visited)

    def __str__(self):
        return '{}({},visited={})'.format(self.__class__.__name__, self.value, self.visited)

class Edge:
    def __init__(self, node, weight):
        self.node = node
        self.weight = weight

    def __repr__(self):
        return '{}(to={},weight={})'.format(self.__class__.__name__, str(self.node), self.weight)

    def __str__(self):
        return '{}({},to={},weight={})'.format(self.__class__.__name__, self.node, self.weight)