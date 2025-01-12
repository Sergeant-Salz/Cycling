import math

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QGraphicsEllipseItem


class QGraphicsWheelItem(QGraphicsEllipseItem):
    length = 10
    width = 3
    center_x = 0
    center_y = 0
    angle = 0

    def __init__(self, center_x, center_y, length, width, angle=0):
        super().__init__(center_x - self.length / 2, center_y - self.width / 2, self.length, self.width)
        self.length = length
        self.width = width
        self.set_center(center_x, center_y)
        self.set_angle(angle)

    def _redraw(self):
        self.setRect(self.center_x - self.length / 2, self.center_y - self.width / 2, self.length, self.width)
        self.setTransformOriginPoint(self.center_x, self.center_y)
        self.setRotation(math.degrees(self.angle))

    def set_angle(self, angle):
        self.angle = angle
        self._redraw()

    def set_center(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self._redraw()

    def set_width(self, width):
        self.width = width
        self._redraw()

    def set(self, center_x=None, center_y=None, length=None, width=None, angle=None):
        if center_x is not None:
            self.center_x = center_x
        if center_y is not None:
            self.center_y = center_y
        if length is not None:
            self.length = length
        if width is not None:
            self.width = width
        if angle is not None:
            self.angle = angle
        self._redraw()