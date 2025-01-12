from dataclasses import dataclass

import numpy as np


@dataclass
class BicycleState:
    lean_angle: float = 0.0
    steering_angle: float = 0.0
    lean_rate: float = 0.0
    steering_rate: float = 0.0
    steer_torque: float = 0.0
    heading: float = 0.0

    def __init__(self,
                 lean_angle: float,
                 steering_angle: float,
                 lean_rate: float,
                 steering_rate: float,
                 steer_torque: float,
                 heading: float):
        self.lean_angle = lean_angle
        self.steering_angle = steering_angle
        self.lean_rate = lean_rate
        self.steering_rate = steering_rate
        self.steer_torque = steer_torque
        self.heading = heading

    def get_q(self) -> np.array:
        return np.array([self.lean_angle, self.steering_angle])

    def get_q_dot(self) -> np.array:
        return np.array([self.lean_rate, self.steering_rate])

    def get_f(self) -> np.array:
        return np.array([0.0, self.steer_torque])

    def get_roll(self) -> float:
        return self.lean_angle

    def get_steering_angle(self) -> float:
        return self.steering_angle

    def get_roll_rate(self) -> float:
        return self.lean_rate

    def get_steering_rate(self) -> float:
        return self.steering_rate

    def get_steer_torque(self) -> float:
        return self.steer_torque

    def get_heading(self) -> float:
        return self.heading
