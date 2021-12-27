# View
from PyQt5.QtCore import pyqtSlot
from utils.colorpalletes import *
from utils.windowtext import *
from classes.gui.view import *
import numpy as np
import random
import pandas as pd
import re


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # View settings
        self._view = View(self)
        self._cache = Cache(CACHE_SIZE)
        self._darkTheme = True

        # Window settings
        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.showMaximized()
        self.setWindowTitle(WIN_TITLE)
        self.setFont(QtGui.QFont('Arial', 15))
        self.setStyleSheet(WINDOW_DARK)
        self.setCentralWidget(self._view)

        # Layout management
        self._mainWidget = QtWidgets.QWidget()
        self._mainLayout = QtWidgets.QHBoxLayout()

        # Main layouts
        self._sceneLayout = QtWidgets.QVBoxLayout()
        self._menuLayout = QtWidgets.QVBoxLayout()

        # Menu layout
        self._tableWidget = QtWidgets.QWidget()
        self._tableLayout = QtWidgets.QVBoxLayout()
        self._tableWidget.setLayout(self._tableLayout)
        self._tableWidget.setFixedSize(TABLE_WIDTH, TABLE_HEIGHT)

        self._buttonsWidget = QtWidgets.QWidget()
        self._buttonsLayout = QtWidgets.QVBoxLayout()
        self._buttonsWidget.setLayout(self._buttonsLayout)

        # Add layouts ans widgets
        self._sceneLayout.addWidget(self._view)
        self._menuLayout.addWidget(self._tableWidget)
        self._menuLayout.addWidget(self._buttonsWidget)

        self._mainLayout.addLayout(self._sceneLayout)
        self._mainLayout.addLayout(self._menuLayout)

        self._mainWidget.setLayout(self._mainLayout)
        self.setCentralWidget(self._mainWidget)

        self._initUI()

    # Window initialisation
    def _initUI(self):
        # Menu bar
        self.menuBar = self._createMenuBar()

        # Realtime adjacency matrix
        self._adjacentTable = self._createAdjacentTable()
        self._tableLayout.addWidget(self._adjacentTable)

        # Buttons
        self._createButtons()

    def _createMenuBar(self):
        self.statusBar()
        # Menu initialization
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('&Файл')
        tasksMenu = menuBar.addMenu('&Задачи теории графов')
        settingsMenu = menuBar.addMenu('&Настройки')
        qaMenu = menuBar.addMenu('&?')

        # Load from file
        fileOpenMenu = QtWidgets.QMenu('Загрузить граф...', self)
        fileMenu.addMenu(fileOpenMenu)

        adjMatrixLoadAction = QtWidgets.QAction('&Загрузить матрицу смежности', self)
        adjMatrixLoadAction.triggered.connect(self._loadAdjacentMatrixFromFile)
        fileOpenMenu.addAction(adjMatrixLoadAction)

        incMatrixLoadAction = QtWidgets.QAction('&Загрузить матрицу инцидентности', self)
        incMatrixLoadAction.triggered.connect(self._loadIncidenceMatrixFromFile)
        fileOpenMenu.addAction(incMatrixLoadAction)

        configLoadAction = QtWidgets.QAction('&Загрузить файл конфигурации', self)
        configLoadAction.triggered.connect(self._loadConfigurationFromFile)
        fileOpenMenu.addAction(configLoadAction)

        # Save to file
        fileSaveMenu = QtWidgets.QMenu('Сохранить граф...', self)
        fileMenu.addMenu(fileSaveMenu)

        adjMatrixSaveAction = QtWidgets.QAction('&Сохранить матрицу смежности', self)
        adjMatrixSaveAction.triggered.connect(self._saveAdjacentMatrixToFile)
        fileSaveMenu.addAction(adjMatrixSaveAction)

        incMatrixSaveAction = QtWidgets.QAction('&Сохранить матрицу инцидентности', self)
        incMatrixSaveAction.triggered.connect(self._saveIncidenceMatrixToFile)
        fileSaveMenu.addAction(incMatrixSaveAction)

        configSaveAction = QtWidgets.QAction('&Сохранить файл конфигурации', self)
        configSaveAction.triggered.connect(self._saveConfigurationToFile)
        fileSaveMenu.addAction(configSaveAction)

        imageSaveAction = QtWidgets.QAction('&Сохранить граф в виде изображения', self)
        imageSaveAction.triggered.connect(self._saveToImage)
        fileSaveMenu.addAction(imageSaveAction)

        # Exit from app
        fileExitAction = QtWidgets.QAction('&Выйти из программы', self)
        fileExitAction.triggered.connect(QtWidgets.qApp.quit)
        fileMenu.addAction(fileExitAction)

        # Tasks menu

        algoComp = QtWidgets.QAction('ЛР №9 - Дополнение графа', self)  # Rina
        algoComp.triggered.connect(self._view.viewComp)
        tasksMenu.addAction(algoComp)

        algoBreadth = QtWidgets.QAction('ЛР №2 - Поиск пути в ширину', self)  # Rina
        algoBreadth.triggered.connect(self._view.viewBreadth)
        tasksMenu.addAction(algoBreadth)

        # Settings menu
        settingsChangeTheme = QtWidgets.QAction('&Сменить тему', self)
        settingsChangeTheme.triggered.connect(self._changeTheme)
        settingsMenu.addAction(settingsChangeTheme)

        # QA menu
        qaProgramAction = QtWidgets.QAction('&О программе', self)
        qaProgramAction.triggered.connect(self._instructionDialog)
        qaMenu.addAction(qaProgramAction)

        qaAuthorAction = QtWidgets.QAction('&Об авторе', self)
        qaAuthorAction.triggered.connect(self._authorDialog)
        qaMenu.addAction(qaAuthorAction)

        return menuBar

    @staticmethod
    def _createAdjacentTable():
        _adjacentTable = QtWidgets.QTableWidget()
        _adjacentTable.setGeometry(0, 0, TABLE_WIDTH, TABLE_HEIGHT)
        _adjacentTable.horizontalHeader().setDefaultSectionSize(30)
        _adjacentTable.verticalHeader().setDefaultSectionSize(30)
        _adjacentTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        _adjacentTable.setStyleSheet(TABLE_DARK)
        return _adjacentTable

    def updateAdjacentTable(self):
        vertexList = self._view.getGraph().getVertexList()
        edgeList = self._view.getGraph().getEdgeList()

        columnCount = rowCount = len(vertexList)
        self._adjacentTable.setColumnCount(columnCount)
        self._adjacentTable.setRowCount(rowCount)

        i = 0
        for item in vertexList:
            self._adjacentTable.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(item.getName()))
            self._adjacentTable.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(item.getName()))
            i += 1

        matrix = self._view.getGraph().getAdjacentMatrix()
        for i in range(columnCount):
            for j in range(rowCount):
                self._adjacentTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(matrix[i][j])))

    def _createButtons(self):
        button1 = QtWidgets.QPushButton('Undo', self)
        button1.setFixedHeight(70)
        button1.clicked.connect(self._undoButtonAction)

        button2 = QtWidgets.QPushButton('Redo', self)
        button2.setFixedHeight(70)
        button2.clicked.connect(self._redoButtonAction)

        button3 = QtWidgets.QPushButton('Set defaults', self)
        button3.setFixedHeight(70)
        button3.clicked.connect(self._view.setDefaults)

        self._buttonsLayout.addWidget(button1)
        self._buttonsLayout.addWidget(button2)
        self._buttonsLayout.addWidget(button3)

    # Utils
    def getCache(self):
        return self._cache

    def getTheme(self):
        return self._darkTheme

    # File dialog windows, graph loading/saving
    def _openCSVFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Откройте файл с матрицей", "",
                                                            "Matrix file (*.csv)", options=options)
        return fileName

    def _saveCSVFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Выберите файл для сохранения", "",
                                                            "Matrix file (*.csv);;Image file (*png)", options=options)
        return fileName

    def _messageDialog(self, name: str, message: str):
        inputDialog = QtWidgets.QDialog(self)
        inputDialog.setWindowTitle(name)
        inputDialog.setFont(QtGui.QFont('Arial', 15))

        if self._darkTheme:
            inputDialog.setStyleSheet(WINDOW_DARK)
        else:
            inputDialog.setStyleSheet(WINDOW_BRIGHT)

        form = QtWidgets.QFormLayout(inputDialog)
        form.addRow(QtWidgets.QLabel(message))

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        form.addRow(buttonBox)
        buttonBox.accepted.connect(inputDialog.accept)

        inputDialog.exec_()

    @staticmethod
    def _isCorrectAdjacentMatrix(matrix):
        matrixSize = len(matrix)
        for row in matrix:
            rowSize = len(row)
            if rowSize != matrixSize:
                return False
            for i in range(0, rowSize):
                if row[i] < 0:
                    return False
        return True

    @pyqtSlot()
    def _loadAdjacentMatrixFromFile(self):
        fileName = self._openCSVFileDialog()

        if len(fileName) != 0:
            try:
                adjMatrix = np.array(pd.read_csv(fileName, header=None))
                adjMatrixSize = len(adjMatrix)
                if not self._isCorrectAdjacentMatrix(adjMatrix):
                    raise ValueError

                graph = Graph()
                for i in range(0, adjMatrixSize):
                    cordX = random.randint(0, FIELD_WIDTH - VERTEX_SIZE)
                    cordY = random.randint(0, FIELD_HEIGHT - VERTEX_SIZE)

                    vertex = Vertex(0, 0, str(len(graph.getVertexList()) + 1), VERTEX_COLOR)
                    vertex.setPos(self._view.mapToScene(cordX, cordY))
                    graph.addVertex(vertex)

                vertexList = graph.getVertexList()
                vertexListSize = len(vertexList)

                for i in range(vertexListSize):
                    for j in range(i, vertexListSize):
                        if i == j and adjMatrix[i][j] != 0:
                            edge = Edge(vertexList[i], vertexList[j],
                                        name=str(len(graph.getEdgeList()) + 1),
                                        weight=int(adjMatrix[i][j]))
                            graph.addEdge(edge)
                        else:
                            if adjMatrix[i][j] == adjMatrix[j][i] and adjMatrix[i][j] != 0:
                                edge = Edge(vertexList[i], vertexList[j],
                                            name=str(len(graph.getEdgeList()) + 1),
                                            weight=int(adjMatrix[i][j]),
                                            direction=False)
                                graph.addEdge(edge)

                for i in range(vertexListSize):
                    for j in range(vertexListSize):
                        if i != j and adjMatrix[i][j] != adjMatrix[j][i] and adjMatrix[i][j] != 0:
                            edge = Edge(vertexList[i], vertexList[j],
                                        name=str(len(graph.getEdgeList()) + 1),
                                        weight=int(adjMatrix[i][j]),
                                        direction=True)
                            graph.addEdge(edge)

                if graph.empty():
                    raise ValueError
                else:
                    self._cache.clearAllStates()
                    self._view.addGraph(graph)

            except ValueError:
                self._messageDialog('Ошибка', 'Ошибка в матрице смежности')

    @pyqtSlot()
    def _saveAdjacentMatrixToFile(self):
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            matrix = self._view.getGraph().getAdjacentMatrix()
            pd.DataFrame(matrix).to_csv(fileName, header=False, index=False)

    @staticmethod
    def _isCorrectIncidenceMatrix(matrix):
        rowsCount = len(matrix)
        colsCount = len(matrix[0])

        for row in matrix:
            rowSize = len(row)
            if rowSize != colsCount:
                return False
            for i in range(rowSize):
                if abs(row[i] > 1):
                    return False
        return True

    @pyqtSlot()
    def _loadIncidenceMatrixFromFile(self):
        fileName = self._openCSVFileDialog()

        if len(fileName) != 0:
            try:
                incMatrix = np.array(pd.read_csv(fileName, header=None))
                if not self._isCorrectIncidenceMatrix(incMatrix):
                    raise ValueError

                rows = len(incMatrix)
                cols = len(incMatrix[0])
                graph = Graph()
                for i in range(0, cols):
                    vertexPoints = []
                    for j in range(0, rows):
                        if incMatrix[j][i] != 0:
                            vertexInfo = [str(j + 1), incMatrix[j][i]]
                            vertexPoints.append(vertexInfo)

                    if len(vertexPoints) == 2:
                        if graph.findVertexByName(vertexPoints[0][0]) is None:
                            cordX = random.randint(0, FIELD_WIDTH - VERTEX_SIZE)
                            cordY = random.randint(0, FIELD_HEIGHT - VERTEX_SIZE)

                            startVertex = Vertex(0, 0, str(len(graph.getVertexList()) + 1), VERTEX_COLOR)
                            startVertex.setPos(self._view.mapToScene(cordX, cordY))
                            graph.addVertex(startVertex)
                        else:
                            startVertex = graph.findVertexByName(vertexPoints[0][0])

                        if graph.findVertexByName(vertexPoints[1][0]) is None:
                            cordX = random.randint(VERTEX_SIZE, FIELD_WIDTH - 2 * VERTEX_SIZE)
                            cordY = random.randint(VERTEX_SIZE, FIELD_HEIGHT - 2 * VERTEX_SIZE)

                            endVertex = Vertex(0, 0, str(len(graph.getVertexList()) + 1), VERTEX_COLOR)
                            endVertex.setPos(self._view.mapToScene(cordX, cordY))
                            graph.addVertex(endVertex)
                        else:
                            endVertex = graph.findVertexByName(vertexPoints[1][0])

                        factor = self._view.countEdgeFactor(startVertex, endVertex)
                        if vertexPoints[0][1] == 1 and vertexPoints[1][1] == 1:
                            edge = Edge(startVertex, endVertex,
                                        name=str(len(graph.getEdgeList()) + 1),
                                        factor=factor,
                                        direction=False)
                            graph.addEdge(edge)

                        elif vertexPoints[0][1] == 1 and vertexPoints[1][1] == -1:
                            edge = Edge(startVertex, endVertex,
                                        name=str(len(graph.getEdgeList()) + 1),
                                        factor=factor,
                                        direction=True)
                            graph.addEdge(edge)

                        elif vertexPoints[0][1] == -1 and vertexPoints[1][1] == 1:
                            edge = Edge(endVertex, startVertex,
                                        name=str(len(graph.getEdgeList()) + 1),
                                        factor=factor,
                                        direction=True)
                            graph.addEdge(edge)

                    elif len(vertexPoints) == 1:
                        if vertexPoints[0][1] == 1:
                            if graph.findVertexByName(vertexPoints[0][0]) is None:
                                cordX = random.randint(VERTEX_SIZE, FIELD_WIDTH - 2 * VERTEX_SIZE)
                                cordY = random.randint(VERTEX_SIZE, FIELD_HEIGHT - 2 * VERTEX_SIZE)

                                vertex = Vertex(0, 0, str(len(graph.getVertexList()) + 1), VERTEX_COLOR)
                                vertex.setPos(self._view.mapToScene(cordX, cordY))
                                graph.addVertex(vertex)
                            else:
                                vertex = graph.findVertexByName(vertexPoints[0][0])

                            factor = self._view.countEdgeFactor(vertex, vertex)
                            edge = Edge(vertex, vertex,
                                        name=str(len(graph.getEdgeList()) + 1),
                                        factor=factor)
                            graph.addEdge(edge)

                if graph.empty():
                    raise ValueError
                else:
                    self._cache.clearAllStates()
                    self._view.addGraph(graph)

            except ValueError:
                self._messageDialog('Ошибка', 'Ошибка в матрице инцидентности')

    @pyqtSlot()
    def _saveIncidenceMatrixToFile(self):
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            matrix = self._view.getGraph().getIncidenceMatrix()
            pd.DataFrame(matrix).to_csv(fileName, header=False, index=False)

    @pyqtSlot()
    def _loadConfigurationFromFile(self):
        fileName = self._openCSVFileDialog()

        if len(fileName) != 0:
            stream = open(fileName, 'r')
            try:
                graph = Graph()
                while True:
                    line = stream.readline()
                    if not line:
                        break

                    # Comment
                    pos = line.find('%')
                    if pos != -1:
                        line = line[0:pos]
                        print(line)

                    # Vertex
                    if line.find('Vertex') != -1:
                        vertexRegex = r'(?<=Vertex{)(\d+)\((\d+), ?(\d+)'
                        vertexList = [list(map(int, (v, k, l))) for v, k, l in re.findall(vertexRegex, line)]
                        for item in vertexList:
                            if not graph.findVertexByName(str(item[0])):
                                if 0 <= int(item[1]) <= FIELD_WIDTH - VERTEX_SIZE and \
                                        0 <= int(item[2]) <= FIELD_HEIGHT - VERTEX_SIZE:
                                    vertex = Vertex(0, 0, str(item[0]), VERTEX_COLOR)
                                    vertex.setPos(self._view.mapToScene(int(item[1]), int(item[2])))
                                    graph.addVertex(vertex)

                    # Edge
                    if line.find('Edges') != -1:
                        edgeRegex = r'(?<=Edges{).+?(?=})'
                        digs = list(map(int, re.findall(r'\d+', re.search(edgeRegex, line).group())))
                        edgeList = [digs[i:i + 4] for i in range(0, len(digs), 4)]
                        for item in edgeList:
                            if not graph.findEdgeByName(str(item[0])):
                                startEdge = graph.findVertexByName(str(item[2]))
                                endEdge = graph.findVertexByName(str(item[3]))
                                if startEdge and endEdge:
                                    edge = Edge(startEdge, endEdge, name=str(item[0]), weight=int(item[1]))
                                    graph.addEdge(edge)

                if graph.empty():
                    raise ValueError
                else:
                    self._cache.clearAllStates()
                    self._view.addGraph(graph)

            except ValueError:
                self._messageDialog('Ошибка', 'Ошибка в файле конфигурации')

            stream.close()

    @pyqtSlot()
    def _saveConfigurationToFile(self):
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            vertexList = self._view.getGraph().getVertexList()
            edgeList = self._view.getGraph().getEdgeList()

            stream = open(fileName, 'w')
            for item in vertexList:
                name = item.getName()
                cordX, cordY = item.getPos()
                result = 'Vertex' + '{' + name + '(' + str(cordX) + ',' + str(cordY) + ')' + '}'
                stream.write(result)
                if item != vertexList[-1]:
                    stream.write('\n')

            if len(edgeList) != 0:
                stream.write('\nEdges{')
                for item in edgeList:
                    name = item.getName()
                    weight = item.getWeight()
                    startName = item.getStartVertex().getName()
                    endName = item.getEndVertex().getName()
                    result = str(name) + '(' + str(weight) + ',' + str(startName) + ',' + str(endName) + ')'
                    stream.write(result)
                    if item != edgeList[-1]:
                        stream.write(',')
                stream.write('}')
            stream.close()

    @pyqtSlot()
    def _saveToImage(self):
        fileName = self._saveCSVFileDialog()

        if len(fileName) != 0:
            pixmap = self._view.grab(self._view.sceneRect().toRect())
            pixmap.save(fileName)

    # Button actions
    def _changeTheme(self):
        if self._darkTheme:
            self._darkTheme = False
            self._view.setStyleSheet(FIELD_BRIGHT)
            self.setStyleSheet(WINDOW_BRIGHT)
            self._adjacentTable.setStyleSheet(TABLE_BRIGHT)

        else:
            self._darkTheme = True
            self._view.setStyleSheet(FIELD_DARK)
            self.setStyleSheet(WINDOW_DARK)
            self._adjacentTable.setStyleSheet(TABLE_DARK)

    @pyqtSlot()
    def _undoButtonAction(self):
        cachedGraph = self._cache.getDecreasedState()

        if cachedGraph:
            self._view.addGraph(self._view.copyGraph(cachedGraph))
            self.updateAdjacentTable()

    @pyqtSlot()
    def _redoButtonAction(self):
        cachedGraph = self._cache.getIncreasedState()

        if cachedGraph:
            self._view.addGraph(self._view.copyGraph(cachedGraph))
            self.updateAdjacentTable()

    def _authorDialog(self):
        self._messageDialog('Об авторе', AUTHOR)

    def _instructionDialog(self):
        self._messageDialog('О программе', INSTRUCTION)
