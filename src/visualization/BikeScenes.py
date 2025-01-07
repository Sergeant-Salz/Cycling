import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem

from src.visualization.QGraphicsWheelItem import QGraphicsWheelItem
from src.visualization.animation_state import AnimationState


class BirdEyeBikeScene(QGraphicsScene):

    wheel_length = 80
    frame_length = 100
    steering_handle_length = 90

    scene_view_size = frame_length + 2 * wheel_length

    def __init__(self):
        super().__init__()

        # add some grid lines in light gray
        self.addLine(0, -self.scene_view_size, 0, self.scene_view_size, QPen(Qt.lightGray))
        self.addLine(-self.scene_view_size, 0, self.scene_view_size, 0, QPen(Qt.lightGray))

        # add the bike parts
        # the front wheel depicted as a squished ellipse
        self.bike_front_wheel = QGraphicsWheelItem(self.frame_length, 0, self.wheel_length, 6)
        wheel_pen = QPen(Qt.red)
        wheel_pen.setWidth(2)
        self.bike_front_wheel.setPen(wheel_pen)
        self.addItem(self.bike_front_wheel)

        # the back wheel depicted as a squished ellipse
        self.bike_back_wheel = QGraphicsWheelItem(0, 0, self.wheel_length, 6)
        wheel_pen = QPen(Qt.gray)
        wheel_pen.setWidth(2)
        self.bike_back_wheel.setPen(wheel_pen)
        self.addItem(self.bike_back_wheel)

        # the frame depicted as a line
        self.bike_frame = QGraphicsLineItem(0, 0, self.frame_length, 0)
        frame_pen = QPen(Qt.black)
        frame_pen.setWidth(3)
        self.bike_frame.setPen(frame_pen)
        self.addItem(self.bike_frame)

        # the steering handle as a line
        self.steering_handle = QGraphicsLineItem(self.frame_length, self.steering_handle_length / 2, self.frame_length, -self.steering_handle_length / 2)
        steering_pen = QPen(Qt.red)
        steering_pen.setWidth(3)
        self.steering_handle.setPen(steering_pen)
        self.addItem(self.steering_handle)

        # set the scene rectangle
        self.setSceneRect(-0.5 * self.scene_view_size, -0.5 * self.scene_view_size, self.scene_view_size, self.scene_view_size)

    def update_bike(self, state: AnimationState):
        # back of the bike is the center
        # front is the center plus the length in the direction of the angle
        bike_front = QPoint(int(self.frame_length * math.cos(state.heading)),
                            int(self.frame_length * math.sin(state.heading)))

        # set the frame rotation
        self.bike_frame.setLine(0, 0, bike_front.x(), bike_front.y())

        # set the back wheel
        self.bike_back_wheel.set_angle(math.degrees(state.heading))

        # the front wheel is centered on the bike front
        # its angle is relative to the bike body angle
        absolute_steering_angle = state.steering_angle + state.heading

        # set the wheel position and rotation
        self.bike_front_wheel.set_center(bike_front.x(), bike_front.y())
        self.bike_front_wheel.set_angle(math.degrees(absolute_steering_angle))

        # set the steering handle position and rotation
        # its direction is orthogonal to the front wheel
        handle_angle = absolute_steering_angle + math.pi / 2
        self.steering_handle.setLine(bike_front.x() - self.steering_handle_length * math.cos(handle_angle) / 2,
                                     bike_front.y() - self.steering_handle_length * math.sin(handle_angle) / 2,
                                     bike_front.x() + self.steering_handle_length * math.cos(handle_angle) / 2,
                                     bike_front.y() + self.steering_handle_length * math.sin(handle_angle) / 2)
