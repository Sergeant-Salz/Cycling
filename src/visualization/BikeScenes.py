import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem

from src.visualization.animation_state import AnimationState


class BirdEyeBikeScene(QGraphicsScene):

    wheel_length = 80
    frame_length = 170

    scene_view_size = frame_length + wheel_length

    def __init__(self):
        super().__init__()

        # add some grid lines in light gray
        self.addLine(0, -self.scene_view_size, 0, self.scene_view_size, QPen(Qt.lightGray))
        self.addLine(-self.scene_view_size, 0, self.scene_view_size, 0, QPen(Qt.lightGray))

        # add the two bike parts
        self.bike_frame = QGraphicsLineItem(0, 0, self.frame_length, 0)
        frame_pen = QPen(Qt.black)
        frame_pen.setWidth(5)
        self.bike_frame.setPen(frame_pen)
        self.addItem(self.bike_frame)

        self.bike_front_wheel = QGraphicsLineItem(self.frame_length - self.wheel_length / 2, 0,
                                                  self.frame_length + self.wheel_length / 2, 0)
        wheel_pen = QPen(Qt.red)
        wheel_pen.setWidth(3)
        self.bike_front_wheel.setPen(wheel_pen)
        self.addItem(self.bike_front_wheel)

        # set the scene rectangle
        self.setSceneRect(-0.5 * self.scene_view_size, -0.5 * self.scene_view_size, self.scene_view_size, self.scene_view_size)

    def update_bike(self, state: AnimationState):
        # back of the bike is the center
        # front is the center plus the length in the direction of the angle
        bike_front = QPoint(int(self.frame_length * math.cos(state.heading)),
                            int(self.frame_length * math.sin(state.heading)))

        # set the frame rotation
        self.bike_frame.setLine(0, 0, bike_front.x(), bike_front.y())

        # the front wheel is centered on the bike front
        # its angle is relative to the bike body angle
        absolute_steering_angle = state.steering_angle + state.heading
        wheel_direction = QPoint(int(self.wheel_length * math.cos(absolute_steering_angle)),
                                 int(self.wheel_length * math.sin(absolute_steering_angle)))

        # set the wheel position and rotation
        self.bike_front_wheel.setLine(bike_front.x() - wheel_direction.x() / 2, bike_front.y() - wheel_direction.y() / 2,
                                      bike_front.x() + wheel_direction.x() / 2, bike_front.y() + wheel_direction.y() / 2)
