import math

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QFrame

from src.visualization.animation_state import AnimationState

front_wheel_color = QColor(255, 0, 0)
back_wheel_color = QColor(0, 255, 0)
frame_color = Qt.black

def draw_birds_eye_view(canvas: QFrame, animation_state: AnimationState):
    # find the center of the canvas
    center_x = int(canvas.width() / 2)
    center_y = int(canvas.height() / 2)

    # find the length of the bike
    bike_length = int(min(canvas.width(), canvas.height()) * 0.8)

    # back of the bike is the center
    # front is the center plus the length in the direction of the angle
    bike_back = QPoint(center_x, center_y)
    bike_front = QPoint(int(center_x + bike_length * math.cos(animation_state.heading)),
                        int(center_y + bike_length * math.sin(animation_state.heading)))

    # the front wheel is centered on the bike front
    # its angle is relative to the bike body angle
    # it is represented by a very squished ellipse in the direction of the steering angle
    wheel_length = bike_length * 0.2
    absolute_steering_angle = animation_state.steering_angle + animation_state.heading
    wheel_front = QPoint(int(bike_front.x() + wheel_length * math.cos(absolute_steering_angle)),
                         int(bike_front.y() + wheel_length * math.sin(absolute_steering_angle)))
    wheel_back = QPoint(int(bike_front.x() - wheel_length * math.cos(absolute_steering_angle)),
                        int(bike_front.y() - wheel_length * math.sin(absolute_steering_angle)))


    # draw the bike
    painter = QPainter(canvas)
    painter.setPen(QPen(frame_color, 4, Qt.SolidLine))
    painter.drawLine(bike_back, bike_front)
    painter.setPen(QPen(front_wheel_color, 3, Qt.SolidLine))
    painter.drawLine(wheel_back, wheel_front)
    painter.drawEllipse(wheel_front, 5, 5)
    painter.end()


def draw_back_view(canvas: QFrame, animation_state: AnimationState):
    # some dimension values
    ground_height = int(canvas.height() * 0.1)
    bike_height = int(canvas.height() * 0.6)
    wheel_radius = int(canvas.height() * 0.1)

    # find the center of the front wheel
    front_wheel_center = QPoint(int(canvas.width() / 2), ground_height + wheel_radius)

    # width of the front wheel projection is based on the steering angle
    # at 90 degrees, the wheel is fully visible (a circle), while at 0 degrees it is a line
    wheel_width = int(wheel_radius * math.sin(animation_state.steering_angle))

    # find position of the contact point of the rear wheel
    contact_point = QPoint(int(canvas.width() / 2), ground_height)

    # draw the bike from behind
    # draw the front wheel first as an ellipse with wheel_radius height and wheel_width width
    # then draw the frame as a line from the contact point up bike height pixels
    # draw the bike from behind
    painter = QPainter(canvas)

    # draw the front wheel as an ellipse
    painter.setPen(QPen(front_wheel_color, 3, Qt.SolidLine))
    painter.save()
    painter.translate(front_wheel_center)
    painter.rotate(math.degrees(animation_state.lean_angle))
    painter.drawEllipse(-int(wheel_width / 2), -wheel_radius, wheel_width, 2 * wheel_radius)
    painter.restore()

    # draw the frame as a line from the contact point up bike height pixels
    painter.setPen(QPen(frame_color, 4, Qt.SolidLine))
    painter.save()
    painter.translate(contact_point)
    painter.rotate(math.degrees(animation_state.lean_angle))
    painter.drawLine(0, 0, 0, -bike_height)
    painter.restore()

    painter.end()




