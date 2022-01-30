from asyncio.windows_events import NULL
import sys
from tkinter import *
from entryState import EntryState
from graph import Graph, Node
from queue import Queue
from time import sleep


class MazeMap:

    def __init__(self, width, height):
        self.__matrix = [[0 for i in range(10)] for j in range(10)]
        self.__root = Tk()
        self.__width = width
        self.__height = height
        self.__root.geometry(str(round(self.__root.winfo_screenwidth(
        ) / 2)) + "x" + str(self.__root.winfo_screenheight()) + "+" + str(round(self.__root.winfo_screenwidth(
        ) / 2)) + "+0")
        self.__root.resizable(False, False)
        self.__canvas = Canvas(self.__root, height=height,
                               width=width, bg="white")
        self.__startNodeId = None
        self.__targetNodeId = None
        self.startCallback = None

    def __setTileColors(self, allBlack=False):
        for i in range(len(self.__matrix)):
            for j in range(len(self.__matrix[i])):
                color = '#000fff'  # obstacle color
                value = self.entryValue(self.__matrix[i][j])
                key = self.entryKey(self.__matrix[i][j])
                if allBlack == True:
                    color = "#000000"
                    if value == EntryState.OBSTACLE:
                        color = '#000fff'
                    elif value == EntryState.TARGET:
                        color = '#eb3434'
                    elif value == EntryState.START:
                        color = '#34eb4f'
                else:
                    if value == EntryState.VISITED_ONCE:
                        color = "#000000"
                    elif value == EntryState.VISITED_TWICE:
                        color = '#b8b8b8'
                    elif value == EntryState.START:
                        color = '#34eb4f'
                    elif value == EntryState.TARGET:
                        color = '#eb3434'
                    elif value == EntryState.POSSIBLE_PATH:
                        color = '#e042f5'
                self.__canvas.itemconfigure(key, fill=color)

    def visualize(self):
        try:
            self.__canvas.pack()
            self.__setTileColors()
            self.__root.mainloop()
        except:
            print("oho")

    def getMatrix(self):
        return self.__matrix

    def getKey(self, position):
        return self.entryKey(self.__matrix[position[0]][position[1]])

    def getDirectionRelativeToCurrentPosition(self, currentPosition, key, direction):
        pos = self.__matrix[currentPosition[0]][currentPosition[1]]
        posLeft = self.__matrix[currentPosition[0]][currentPosition[1] - 1]
        posRight = self.__matrix[currentPosition[0]][currentPosition[1] + 1]
        posTop = self.__matrix[currentPosition[0] - 1][currentPosition[1]]
        posBottom = self.__matrix[currentPosition[0] + 1][currentPosition[1]]
        if self.entryKey(posLeft) == key:
            newDirection = "west"
            if direction == "west":
                return [newDirection, "straight"]
            if direction == "east":
                return [newDirection, "around"]
            if direction == "north":
                return [newDirection, "left"]
            if direction == "south":
                return [newDirection, "right"]
        if self.entryKey(posRight) == key:
            newDirection = "east"
            if direction == "west":
                return [newDirection, "around"]
            if direction == "east":
                return [newDirection, "straight"]
            if direction == "north":
                return [newDirection, "right"]
            if direction == "south":
                return [newDirection, "left"]
        if self.entryKey(posTop) == key:
            newDirection = "north"
            if direction == "west":
                return [newDirection, "right"]
            if direction == "east":
                return [newDirection, "left"]
            if direction == "north":
                return [newDirection, "straight"]
            if direction == "south":
                return [newDirection, "around"]
        if self.entryKey(posBottom) == key:
            newDirection = "south"
            if direction == "west":
                return [newDirection, "right"]
            if direction == "east":
                return [newDirection, "left"]
            if direction == "north":
                return [newDirection, "around"]
            if direction == "south":
                return [newDirection, "straight"]
        if self.entryKey(pos) == key:
            if direction == "west":
                newDirection = "east"
                return [newDirection, "around"]
            if direction == "east":
                newDirection = "west"
                return [newDirection, "around"]
            if direction == "north":
                newDirection = "south"
                return [newDirection, "around"]
            if direction == "south":
                newDirection = "north"
                return [newDirection, "around"]

    def getSurroundingPositionTypes(self, direction, position):
        # the direction parameter matters here because we need to define where to turn relative to the robot.
        posLeft = None
        posRight = None
        posFront = None
        posTwoFront = None
        if direction == "north":
            try:
                posLeft = self.entryValue(
                    self.__matrix[position[0]][position[1] - 1])
                posRight = self.entryValue(
                    self.__matrix[position[0]][position[1] + 1])
                posFront = self.entryValue(
                    self.__matrix[position[0] - 1][position[1]])
                posTwoFront = self.entryValue(
                    self.__matrix[position[0] - 2][position[1]])
                return [posLeft, posRight, posFront, posTwoFront]
            except IndexError:
                return [posLeft, posRight, posFront, posTwoFront]
        elif direction == "south":
            try:
                posLeft = self.entryValue(
                    self.__matrix[position[0]][position[1] + 1])
                posRight = self.entryValue(
                    self.__matrix[position[0]][position[1] - 1])
                posFront = self.entryValue(
                    self.__matrix[position[0] + 1][position[1]])
                posTwoFront = self.entryValue(
                    self.__matrix[position[0] + 2][position[1]])
                return [posLeft, posRight, posFront, posTwoFront]
            except IndexError:
                return [posLeft, posRight, posFront, posTwoFront]
        elif direction == "west":
            try:
                posLeft = self.entryValue(
                    self.__matrix[position[0] + 1][position[1]])
                posRight = self.entryValue(
                    self.__matrix[position[0] - 1][position[1]])
                posFront = self.entryValue(
                    self.__matrix[position[0]][position[1] - 1])
                posTwoFront = self.entryValue(
                    self.__matrix[position[0]][position[1] - 1])
                return [posLeft, posRight, posFront, posTwoFront]
            except IndexError:
                return [posLeft, posRight, posFront, posTwoFront]
        elif direction == "east":
            try:
                posLeft = self.entryValue(
                    self.__matrix[position[0] - 1][position[1]])
                posRight = self.entryValue(
                    self.__matrix[position[0] + 1][position[1]])
                posFront = self.entryValue(
                    self.__matrix[position[0]][position[1] + 1])
                posTwoFront = self.entryValue(
                    self.__matrix[position[0]][position[1] + 2])
                return [posLeft, posRight, posFront, posTwoFront]
            except IndexError:
                return [posLeft, posRight, posFront, posTwoFront]

    def getTargetPathDirections(self, targetPosition, currentPosition, visualizeFinalPath=False):
        self.__startNodeId = self.entryKey(
            self.__matrix[currentPosition[0]][currentPosition[1]])
        self.__targetNodeId = self.entryKey(
            self.__matrix[targetPosition[0]][targetPosition[1]])
        graph = self.getGraphFromMatrix()
        path = self.bfs(graph)
        if visualizeFinalPath == True:
            self.visualizePath(path)
        return path

    def addGoalSection(self, position):
        self.__matrix[position[0]
                      ][position[1]][self.entryKey(self.__matrix[position[0]
                                                                 ][position[1]])] = EntryState.TARGET
    # This is a mess, I KNOW....

    def addMazePathSection(self, direction, currentPosition, potentialJunctions):
        newPosition = NULL
        junctionAdded = NULL
        if direction == "north":
            row = currentPosition[0] - 1
            col = currentPosition[1]
            newPosition = [row, col]
        elif direction == "south":
            row = currentPosition[0] + 1
            col = currentPosition[1]
            newPosition = [row, col]
        elif direction == "west":
            row = currentPosition[0]
            col = currentPosition[1] - 1
            newPosition = [row, col]
        elif direction == "east":
            row = currentPosition[0]
            col = currentPosition[1] + 1
            newPosition = [row, col]

        if currentPosition == [0, 0]:
            self.__matrix[currentPosition[0]
                          ][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0]
                                                                            ][currentPosition[1]])] = EntryState.START
        elif self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1]]) == EntryState.VISITED_ONCE or self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1]]) == EntryState.VISITED_TWICE:
            self.__matrix[currentPosition[0]][currentPosition[1]][self.entryKey(
                self.__matrix[currentPosition[0]][currentPosition[1]])] = EntryState.VISITED_TWICE
        else:
            self.__matrix[currentPosition[0]][currentPosition[1]
                                              ][self.entryKey(self.__matrix[currentPosition[0]][currentPosition[1]
                                                                                                ])] = EntryState.VISITED_ONCE

        if direction == "north":
            if potentialJunctions[0] == True and self.entryValue(self.__matrix[currentPosition[0] - 1][currentPosition[1]]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0] -
                              1][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0] -
                                                                                 1][currentPosition[1]])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0] -
                                 1, currentPosition[1]]
            if potentialJunctions[1] == True and self.entryValue(self.__matrix[currentPosition[0] + 1][currentPosition[1]]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0] +
                              1][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0] +
                                                                                 1][currentPosition[1]])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0] +
                                 1, currentPosition[1]]
            if potentialJunctions[2] == True and self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1] - 1]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0]
                              ][currentPosition[1] - 1][self.entryKey(self.__matrix[currentPosition[0]
                                                                                    ][currentPosition[1] - 1])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0], currentPosition[1] - 1]
            if potentialJunctions[3] == True and self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1] + 1]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0]
                              ][currentPosition[1] + 1][self.entryKey(self.__matrix[currentPosition[0]
                                                                                    ][currentPosition[1] + 1])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0], currentPosition[1] + 1]
        elif direction == "south":
            if potentialJunctions[0] == True and self.entryValue(self.__matrix[currentPosition[0] + 1][currentPosition[1]]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0] +
                              1][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0] +
                                                                                 1][currentPosition[1]])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0] +
                                 1, currentPosition[1]]
            if potentialJunctions[1] == True and self.entryValue(self.__matrix[currentPosition[0] - 1][currentPosition[1]]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0] -
                              1][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0] -
                                                                                 1][currentPosition[1]])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0] -
                                 1, currentPosition[1]]
            if potentialJunctions[2] == True and self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1] + 1]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0]
                              ][currentPosition[1] + 1][self.entryKey(self.__matrix[currentPosition[0]
                                                                                    ][currentPosition[1] + 1])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0], currentPosition[1] + 1]
            if potentialJunctions[3] == True and self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1] - 1]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0]
                              ][currentPosition[1] - 1][self.entryKey(self.__matrix[currentPosition[0]
                                                                                    ][currentPosition[1] - 1])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0], currentPosition[1] - 1]
        elif direction == "west":
            if potentialJunctions[0] == True and self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1] - 1]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0]
                              ][currentPosition[1] - 1][self.entryKey(self.__matrix[currentPosition[0]
                                                                                    ][currentPosition[1] - 1])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0], currentPosition[1] - 1]
            if potentialJunctions[1] == True and self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1] + 1]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0]
                              ][currentPosition[1] + 1][self.entryKey(self.__matrix[currentPosition[0]
                                                                                    ][currentPosition[1] + 1])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0], currentPosition[1] + 1]
            if potentialJunctions[2] == True and self.entryValue(self.__matrix[currentPosition[0] + 1][currentPosition[1]]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0] + 1
                              ][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0] + 1
                                                                                ][currentPosition[1]])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0] + 1, currentPosition[1]]
            if potentialJunctions[3] == True and self.entryValue(self.__matrix[currentPosition[0] - 1][currentPosition[1]]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0] - 1
                              ][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0] - 1
                                                                                ][currentPosition[1]])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0] - 1, currentPosition[1]]
        elif direction == "east":
            if potentialJunctions[0] == True and self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1] + 1]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0]
                              ][currentPosition[1] + 1] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0], currentPosition[1] + 1]
            if potentialJunctions[1] == True and self.entryValue(self.__matrix[currentPosition[0]][currentPosition[1] - 1]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0]
                              ][currentPosition[1] - 1][self.entryKey(self.__matrix[currentPosition[0]
                                                                                    ][currentPosition[1] - 1])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0], currentPosition[1] - 1]
            if potentialJunctions[2] == True and self.entryValue(self.__matrix[currentPosition[0] - 1][currentPosition[1]]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0] - 1
                              ][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0] - 1
                                                                                ][currentPosition[1]])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0] - 1, currentPosition[1]]
            if potentialJunctions[3] == True and self.entryValue(self.__matrix[currentPosition[0] + 1][currentPosition[1]]) == EntryState.OBSTACLE:
                self.__matrix[currentPosition[0] + 1
                              ][currentPosition[1]][self.entryKey(self.__matrix[currentPosition[0] + 1
                                                                                ][currentPosition[1]])] = EntryState.POSSIBLE_PATH
                junctionAdded = [currentPosition[0] + 1, currentPosition[1]]

        return [newPosition, currentPosition, self.__matrix[newPosition[0]][newPosition[1]], junctionAdded]

    def entryValue(self, entry):
        return next(iter(entry.values()))

    def entryKey(self, entry):
        return next(iter(entry.keys()))

    def visualizePath(self, path):
        try:
            self.__canvas.pack()
            self.__setTileColors(allBlack=True)
            for node in path:
                self.__canvas.itemconfigure(node, fill="#1aff00")
            self.__root.mainloop()
        except:
            print("error")

    def bfs(self, graphObject):
        queue = Queue()
        graph = graphObject.getGraph()
        currentPath = {}
        graphObject.setNodeVisited(self.__startNodeId)
        # self.__canvas.itemconfigure(self.__startNodeId, fill="#77917c")
        queue.enqueue(self.__startNodeId)

        def backtrace(parent, start, end):
            path = [end]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return path

        while queue.isEmpty() == False:
            v = queue.dequeue()
            # self.__canvas.itemconfigure(v, fill="#5f5f5f")
            if v == self.__targetNodeId:
                return backtrace(currentPath, self.__startNodeId, v)
            for edge in graph[v]:
                if graphObject.getNode(edge.node).visited == False:
                    graphObject.setNodeVisited(edge.node)
                    currentPath[edge.node] = v
                    # self.__canvas.itemconfigure(edge.node, fill="#bdb720")
                    queue.enqueue(edge.node)
            # sleep(0.01)
            # self.__root.update()

    def getGraphFromMatrix(self):
        connections = []
        # we need to convert current matrix to a graph.
        for i in range(len(self.__matrix)):
            # last row is special case: it has no successor.
            if i == len(self.__matrix) - 1:
                for j in range(len(self.__matrix[i])):
                    if j < len(self.__matrix[i]) - 1:
                        # there should be an edge between this and next entry on the same row.
                        if self.entryValue(self.__matrix[i][j]) != EntryState.OBSTACLE and self.entryValue(self.__matrix[i][j + 1]) != EntryState.OBSTACLE:
                            connections.append((Node(self.entryKey(self.__matrix[i][j])), Node(
                                self.entryKey(self.__matrix[i][j + 1]))))
            # default case: row has successor.
            else:
                for j in range(len(self.__matrix[i])):
                    if j == len(self.__matrix[i]) - 1:
                        # there should be an edge between this and the entry on the next row.
                        if self.entryValue(self.__matrix[i][j]) != EntryState.OBSTACLE and self.entryValue(self.__matrix[i + 1][j]) != EntryState.OBSTACLE:
                            connections.append((Node(self.entryKey(self.__matrix[i][j])), Node(
                                self.entryKey(self.__matrix[i + 1][j]))))
                    else:
                        # there should be an edge between this and next entry on the same row.
                        if self.entryValue(self.__matrix[i][j]) != EntryState.OBSTACLE and self.entryValue(self.__matrix[i][j + 1]) != EntryState.OBSTACLE:
                            connections.append((Node(self.entryKey(self.__matrix[i][j])), Node(
                                self.entryKey(self.__matrix[i][j + 1]))))
                        # there should be an edge between this and the entry on the next row.
                        if self.entryValue(self.__matrix[i][j]) != EntryState.OBSTACLE and self.entryValue(self.__matrix[i + 1][j]) != EntryState.OBSTACLE:
                            connections.append((Node(self.entryKey(self.__matrix[i][j])), Node(
                                self.entryKey(self.__matrix[i + 1][j]))))
        graph = Graph(connections)
        return graph
        #optimalPath = self.bfs(graph)
        # self.visualizePath(optimalPath)

    def setup(self, m_size=[10, 10]):  # m_size : size of matrix [Rows x Columns]
        try:
            if m_size[0] < 4 or m_size[1] < 4:
                raise ValueError("Grid can't be smaller than 4x4!")
            self.__matrix = [[EntryState.OBSTACLE for i in range(
                m_size[0])] for j in range(m_size[1])]
            w = self.__canvas.winfo_width()
            h = self.__canvas.winfo_height()
            self.__canvas.delete("grid_line")
            v_lines = len(self.__matrix[0])  # number of vertical lines
            h_lines = len(self.__matrix)  # number of horizontal lines
            rect_width = self.__width / v_lines
            rect_height = self.__height / h_lines
            y_pos = 0

            for i in range(len(self.__matrix)):
                x_pos = 0  # keep track of where we're at currently
                for j in range(len(self.__matrix[i])):
                    color = '#000fff'  # obstacle color
                    rect_id = self.__canvas.create_rectangle(
                        x_pos, y_pos, x_pos + rect_width, y_pos + rect_height, fill=color, outline='#fff')
                    self.__matrix[i][j] = {rect_id: EntryState.OBSTACLE}
                    x_pos += rect_width
                y_pos += rect_height

        except ValueError as e:
            sys.exit(1)
