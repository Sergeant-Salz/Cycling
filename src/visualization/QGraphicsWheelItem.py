from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QGraphicsEllipseItem


class QGraphicsWheelItem(QGraphicsEllipseItem):
    length = 10
    height = 3
    center_x = 0
    center_y = 0
    angle = 0

    def __init__(self, center_x, center_y, length, height, angle=0):
        super().__init__(center_x - self.length / 2, center_y - self.height / 2, self.length, self.height)
        self.length = length
        self.height = height
        self.set_center(center_x, center_y)
        self.set_angle(0)

    def set_angle(self, angle):
        self.angle = angle
        self.setRotation(angle)


    def set_center(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.setRect(center_x - self.length / 2, center_y - self.height / 2, self.length, self.height)
        self.setTransformOriginPoint(center_x, center_y)
        self.setRotation(self.angle)