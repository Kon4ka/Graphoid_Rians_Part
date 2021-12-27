from classes.graph.vertex import *
from math import sqrt, sin, cos, acos, pi, radians, degrees


class Edge(QtWidgets.QGraphicsLineItem):

    def __init__(self, startVertex, endVertex, name='1', weight=1, color=QtCore.Qt.white, direction=False, factor=0, parent=None):
        super().__init__(parent)

        # Edge variables
        self._startVertex = startVertex
        self._endVertex = endVertex
        self._name = name
        self._weight = weight
        self._color = color
        self._curveFactor = factor
        self._isDirection = direction
        self._serviceValue = ""

        if self._weight == 1:
            self._isWeight = False
        else:
            self._isWeight = True

    def toggleDirection(self):
        self._isDirection = not self._isDirection

    def isDirected(self):
        return self._isDirection

    def setWeight(self, weight):
        self._weight = weight
        self._isWeight = True

    def getWeight(self):
        return self._weight

    def getStartVertex(self):
        return self._startVertex

    def getEndVertex(self):
        return self._endVertex

    def getName(self):
        return self._name

    def getFactor(self):
        return self._curveFactor

    def getColor(self):
        return self._color

    def setColor(self, color: str):
        self._color = color

    def boundingRect(self):
        start_x, start_y = self._startVertex.pos().x(), self._startVertex.pos().y()
        end_x, end_y = self._endVertex.pos().x(), self._endVertex.pos().y()

        a = end_x - start_x
        b = start_y - end_y
        c = sqrt(a ** 2 + b ** 2)
        angle = 0

        if end_y < start_y and c != 0:
            angle = acos(a / c)
        elif end_y >= start_y and c != 0:
            angle = 2 * pi - acos(a / c)

        start_x += VERTEX_SIZE / 2 * cos(angle)
        start_y -= VERTEX_SIZE / 2 * sin(angle)
        end_x -= VERTEX_SIZE / 2 * cos(angle)
        end_y += VERTEX_SIZE / 2 * sin(angle)

        start = QtCore.QPointF(start_x, start_y)
        end = QtCore.QPointF(end_x, end_y)

        p1 = start + self._startVertex.rect().center()
        p3 = end + self._endVertex.rect().center()

        bounds = p3 - p1
        size = QtCore.QSizeF(bounds.x(), bounds.y())
        return QtCore.QRectF(p1, size)

    def paint(self, painter, option, widget=None):
        # Calculate start and end positions
        start_x, start_y = self._startVertex.pos().x(), self._startVertex.pos().y()
        end_x, end_y = self._endVertex.pos().x(), self._endVertex.pos().y()

        a = end_x - start_x
        b = start_y - end_y
        c = sqrt(a ** 2 + b ** 2)
        angle = 0

        if end_y < start_y and c != 0:
            angle = acos(a / c)
        elif end_y >= start_y and c != 0:
            angle = 2 * pi - acos(a / c)

        offset = 1.1
        start_x += VERTEX_SIZE * offset / 2 * cos(angle)
        start_y -= VERTEX_SIZE * offset / 2 * sin(angle)
        end_x -= VERTEX_SIZE * offset / 2 * cos(angle)
        end_y += VERTEX_SIZE * offset / 2 * sin(angle)

        pointStart = QtCore.QPointF(start_x, start_y) + self._startVertex.rect().center()
        pointEnd = QtCore.QPointF(end_x, end_y) + self._endVertex.rect().center()

        # Calculate bezier curves for loop
        if self._startVertex == self._endVertex:

            pointStartX = self._startVertex.x() + VERTEX_SIZE * 0.5 - 5
            pointStartY = self._startVertex.y()
            pointStart = QtCore.QPointF(pointStartX, pointStartY)

            pointEndX = self._startVertex.x()
            pointEndY = self._startVertex.y() + VERTEX_SIZE * 0.5 - 5
            pointEnd = QtCore.QPointF(pointEndX, pointEndY)

            point1X = pointStart.x() - VERTEX_SIZE * 0.5
            point1Y = pointStart.y() - VERTEX_SIZE * 2

            point2X = pointEnd.x() - VERTEX_SIZE * 2
            point2Y = pointEnd.y() - VERTEX_SIZE * 0.5

            myPath = QtGui.QPainterPath(pointStart)
            myPath.cubicTo(QtCore.QPointF(point1X, point1Y), QtCore.QPointF(point2X, point2Y), pointEnd)

            pen = QtGui.QPen()
            pen.setColor(self._color)
            pen.setWidth(VERGE_WIDTH)
            painter.setPen(pen)
            painter.drawPath(myPath)

            pen.setColor(QtGui.QColor(VERTEX_COLOR))
            pen.setWidth(10)
            painter.setPen(pen)
            painter.setFont(QtGui.QFont('Arial', 14))

            # Update factor for text and arrow drawing
            painter.drawText(pointEnd.x() - VERTEX_SIZE, pointStart.y() - VERTEX_SIZE, self._name)

            # Edge direction
            if self._isDirection:
                endPoint = QtCore.QPointF(pointEndX, pointEndY)
                dx, dy = pointStart.x() - endPoint.x(), pointStart.y() - endPoint.y()
                length = sqrt(dx ** 2 + dy ** 2) / 1.2

                normX, normY = dx / length, dy / length
                perpX, perpY = normY, -normX

                leftX = endPoint.x() - VERTEX_SIZE / 5 + 5
                leftY = endPoint.y() - VERTEX_SIZE / 5 - 1
                rightX = endPoint.x() - VERTEX_SIZE / 5
                rightY = endPoint.y() + VERTEX_SIZE / 5 - 4

                point2 = QtCore.QPointF(leftX, leftY)
                point3 = QtCore.QPointF(rightX, rightY)

                newPen = QtGui.QPen()
                newPen.setColor(self._color)
                newPen.setWidth(ARROW_SIZE)
                painter.setPen(newPen)
                painter.drawPolygon(point2, point3, endPoint)

            # Edge weight display
            if self._isWeight:
                newPen = QtGui.QPen()
                newPen.setColor(QtGui.QColor(VERTEX_COLOR))
                painter.setPen(newPen)
                painter.setFont(QtGui.QFont('Arial', 14))
                painter.drawText(pointEnd.x() - VERTEX_SIZE, pointStart.y() - VERTEX_SIZE,
                                 self._name + ': ' + str(self._weight))

        # Calculate bezier curve loop default edge
        else:
            point3X = ((pointEnd.x() + pointStart.x()) / 2)
            point3Y = ((pointEnd.y() + pointStart.y()) / 2)
            factor = VERTEX_SIZE * self._curveFactor
            angle2 = radians(90) + angle

            myPath = QtGui.QPainterPath(pointStart)
            myPath.cubicTo(QtCore.QPointF(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2)),
                           QtCore.QPointF(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2)),
                           pointEnd)

            pen = QtGui.QPen()
            pen.setColor(self._color)
            pen.setWidth(VERGE_WIDTH)
            painter.setPen(pen)
            painter.drawPath(myPath)

            # Update factor for text and arrow drawing
            pen.setColor(QtGui.QColor(VERTEX_COLOR))
            painter.setPen(pen)
            painter.setFont(QtGui.QFont('Arial', 14))

            factor *= 3 / 4
            textOffset = VERTEX_SIZE / 4
            painter.drawText(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2) - textOffset, self._name)

            # Edge direction
            if self._isDirection:
                endPoint = QtCore.QPointF(point3X + factor * cos(-angle2),  point3Y + factor * sin(-angle2))

                leftX = endPoint.x() + VERTEX_SIZE / 4 * cos(angle + pi / 2 + pi / 4)
                leftY = endPoint.y() - VERTEX_SIZE / 4 * sin(angle + radians(90 + 45))
                rightX = endPoint.x() + VERTEX_SIZE / 4 * cos(angle + radians(90 + 90 + 45))
                rightY = endPoint.y() - VERTEX_SIZE / 4 * sin(angle + radians(90 + 90 + 45))

                point2 = QtCore.QPointF(leftX, leftY)
                point3 = QtCore.QPointF(rightX, rightY)

                newPen = QtGui.QPen()
                newPen.setColor(self._color)
                newPen.setWidth(ARROW_SIZE)
                painter.setPen(newPen)
                painter.drawPolygon(point2, endPoint, point3)

            # Edge weight display
            if self._isWeight:
                newPen = QtGui.QPen()
                newPen.setColor(QtGui.QColor(VERTEX_COLOR))
                painter.setPen(newPen)
                painter.setFont(QtGui.QFont('Arial', 14))
                textOffset = VERTEX_SIZE / 4
                painter.drawText(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2) - textOffset,
                                 self._name + ': ' + str(self._weight))
