import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem

from src.visualization.QGraphicsWheelItem import QGraphicsWheelItem
from src.model.bicycle_state import BicycleState


class BirdEyeBikeScene(QGraphicsScene):

    wheel_length = 80
    frame_length = 100
    steering_handle_length = 90

    scene_view_size = frame_length + 2 * wheel_length

    def __init__(self, state: BicycleState = None):
        super().__init__()

        # add some grid lines in light gray
        self.addLine(0, -self.scene_view_size, 0, self.scene_view_size, QPen(Qt.lightGray, 1, Qt.DashLine))
        self.addLine(-self.scene_view_size, 0, self.scene_view_size, 0, QPen(Qt.lightGray, 1, Qt.DashLine))

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

        if state is not None:
            self.update_bike(state)

    def update_bike(self, state: BicycleState):
        # back of the bike is the center
        # front is the center plus the length in the direction of the angle
        bike_front = QPoint(int(self.frame_length * math.cos(state.heading)),
                            int(self.frame_length * math.sin(state.heading)))

        # set the frame rotation
        self.bike_frame.setLine(0, 0, bike_front.x(), bike_front.y())

        # set the back wheel
        self.bike_back_wheel.set_angle(state.heading)

        # the front wheel is centered on the bike front
        # its angle is relative to the bike body angle
        absolute_steering_angle = state.steering_angle + state.heading

        # set the wheel position and rotation
        self.bike_front_wheel.set_center(bike_front.x(), bike_front.y())
        self.bike_front_wheel.set_angle(absolute_steering_angle)

        # set the steering handle position and rotation
        # its direction is orthogonal to the front wheel
        handle_angle = absolute_steering_angle + math.pi / 2
        self.steering_handle.setLine(bike_front.x() - self.steering_handle_length * math.cos(handle_angle) / 2,
                                     bike_front.y() - self.steering_handle_length * math.sin(handle_angle) / 2,
                                     bike_front.x() + self.steering_handle_length * math.cos(handle_angle) / 2,
                                     bike_front.y() + self.steering_handle_length * math.sin(handle_angle) / 2)


class RearViewBikeScene(QGraphicsScene):
    wheel_length = 160
    handle_height = 200
    handle_length = 150

    scene_view_size = 2 * handle_height

    def __init__(self, state: BicycleState = None):
        super().__init__()

        # add a ground plane as a gray rectangle
        self.addRect(-99999, 0, 2*99999, 99999, brush=Qt.gray, pen=Qt.transparent)

        # add the bike parts
        # the front wheel depicted as an ellipse
        self.bike_front_wheel = QGraphicsWheelItem(0, -self.wheel_length / 2, self.wheel_length, 4, angle=math.pi/2)
        wheel_pen = QPen(Qt.red)
        wheel_pen.setWidth(2)
        self.bike_front_wheel.setPen(wheel_pen)
        self.addItem(self.bike_front_wheel)

        # the front wheel fork depicted as a line
        self.bike_fork = QGraphicsLineItem(0, -self.wheel_length / 2, 0, -self.handle_height)
        fork_pen = QPen(Qt.black)
        fork_pen.setWidth(2)
        self.bike_fork.setPen(fork_pen)
        self.addItem(self.bike_fork)

        # the back wheel depicted as an ellipse
        self.bike_back_wheel = QGraphicsWheelItem(0, -self.wheel_length / 2, self.wheel_length, 4, angle=math.pi/2)
        wheel_pen = QPen(Qt.gray)
        wheel_pen.setWidth(2)
        self.bike_back_wheel.setPen(wheel_pen)
        self.addItem(self.bike_back_wheel)

        # the handlebars depicted as a line
        self.bike_handle = QGraphicsLineItem(-self.handle_length / 2, -self.handle_height, self.handle_length / 2, -self.handle_height)
        handle_pen = QPen(Qt.red)
        handle_pen.setWidth(3)
        self.bike_handle.setPen(handle_pen)
        self.addItem(self.bike_handle)

        # set the scene rectangle
        self.setSceneRect(-0.5 * self.scene_view_size, 0.1 * self.scene_view_size, self.scene_view_size,
                          -self.scene_view_size)

        if state is not None:
            self.update_bike(state)

    def update_bike(self, state: BicycleState):
        lean_angle = state.lean_angle

        # based on the lean, compute the center of the wheels
        wheel_center = QPoint(int(self.wheel_length/2 * math.sin(lean_angle)),
                                int(-self.wheel_length/2 * math.cos(lean_angle)))

        # compute the wheel width as a function of the steering angle
        # at 90 degrees, the wheel is at its maximum width and a full circle
        # at 0 degrees, the wheel is at its minimum width and a squished ellipse
        wheel_width = 3 + self.wheel_length * math.sin(state.steering_angle)

        # update the wheels
        self.bike_front_wheel.set(wheel_center.x(), wheel_center.y(), width=wheel_width, angle=(lean_angle + math.pi/2))
        self.bike_back_wheel.set(wheel_center.x(), wheel_center.y(), angle=(lean_angle + math.pi/2))

        # compute the center point of the handlebars
        handle_center = QPoint(int(self.handle_height * math.sin(lean_angle)),
                               int(-self.handle_height * math.cos(lean_angle)))

        # draw the fork
        self.bike_fork.setLine(wheel_center.x(), wheel_center.y(), handle_center.x(), handle_center.y())

        # draw the handlebars
        handlebar_angle = lean_angle
        handlebar_length = self.handle_length * math.cos(state.steering_angle)
        self.bike_handle.setLine(handle_center.x() - handlebar_length * math.cos(handlebar_angle) / 2,
                                handle_center.y() - handlebar_length * math.sin(handlebar_angle) / 2,
                                handle_center.x() + handlebar_length * math.cos(handlebar_angle) / 2,
                                handle_center.y() + handlebar_length * math.sin(handlebar_angle) / 2)
