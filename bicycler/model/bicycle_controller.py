import math
from abc import abstractmethod, ABC
from dataclasses import dataclass

import numpy as np


@dataclass
class BicycleControl:
    roll_torque: float
    steer_torque: float

    def get_roll_torque(self):
        return self.roll_torque

    def get_steer_torque(self):
        return self.steer_torque



class BicycleController(ABC):
    @abstractmethod
    def calculate_control(self, roll: float, steer: float, roll_rate: float, steer_rate: float) -> BicycleControl:
        pass

    @abstractmethod
    def get_parameters(self) -> dict[str, str]:
        pass

    def get_name(self) -> str:
        return self.__class__.__name__

class NoControlController(BicycleController):
    """
    Controller which applies no control input.
    """
    def calculate_control(self, roll: float, steer: float, roll_rate: float, steer_rate: float) -> BicycleControl:
        return BicycleControl(0.0, 0.0)

    def get_parameters(self) -> dict[str, str]:
        return {}


class RollRateFeedbackController(BicycleController):
    """
    Controller which applies a steer torque proportional to the negative roll angular rate
    """
    def __init__(self, gain: float):
        self.gain = gain

    def calculate_control(self, roll: float, steer: float, roll_rate: float, steer_rate: float) -> BicycleControl:
        return BicycleControl(0.0, self.gain * roll_rate)

    def get_parameters(self) -> dict[str, str]:
        return {'gain': str(self.gain)}


class RollFeedbackController(BicycleController):
    """
    Controller which applies a steer torque proportional to the negative roll angle
    """
    def __init__(self, gain: float):
        self.gain = gain

    def calculate_control(self, roll: float, steer: float, roll_rate: float, steer_rate: float) -> BicycleControl:
        return BicycleControl(0.0, self.gain * roll)

    def get_parameters(self) -> dict[str, str]:
        return {'gain': str(self.gain)}


class RollPIDController(BicycleController):
    """
    PID control for roll angle
    """
    target_roll = 0.0
    integral_window_size: int
    integral_window: np.ndarray
    integral_window_idx = 0

    def __init__(self, kp: float, ki: float, kd: float, window_size = 10):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_window_size = window_size
        self.integral_window = np.zeros(window_size)

    def calculate_control(self, roll: float, steer: float, roll_rate: float, steer_rate: float) -> BicycleControl:
        error = self.target_roll - roll
        derivative = roll_rate
        self.integral_window[self.integral_window_idx] = error
        self.integral_window_idx = (self.integral_window_idx + 1) % self.integral_window_size
        integral = np.sum(self.integral_window)
        print(f"error: {error}, integral: {integral}, derivative: {derivative} -> control: {self.kp * error - self.ki * integral + self.kd * derivative}")
        return BicycleControl(0.0, self.kp * error - self.ki * integral + self.kd * derivative)

    def get_parameters(self) -> dict[str, str]:
        return {'kp': str(self.kp), 'ki': str(self.ki), 'kd': str(self.kd)}

class RollPDController(BicycleController):
    """
    PD control for roll angle
    """
    target_roll = 0.0

    def __init__(self, kp: float, kd: float):
        self.kp = kp
        self.kd = kd
        self.integral = 0.0

    def calculate_control(self, roll: float, steer: float, roll_rate: float, steer_rate: float) -> BicycleControl:
        error = self.target_roll - roll
        derivative = roll_rate
        print(f"error: {error}, derivative: {derivative} -> control: {self.kp * error + self.kd * derivative}")
        return BicycleControl(0.0, self.kp * error + self.kd * derivative)

    def get_parameters(self) -> dict[str, str]:
        return {'kp': str(self.kp), 'kd': str(self.kd)}