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
        return BicycleControl(0.0, - self.gain * roll_rate)

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
