from dataclasses import dataclass


@dataclass
class AnimationState:
    lean_angle: float = 0.0
    steering_angle: float = 0.0
    heading: float = 0.0

    def __init__(self, lean_angle: float, steering_angle: float, heading: float):
        self.lean_angle = lean_angle
        self.steering_angle = steering_angle
        self.heading = heading