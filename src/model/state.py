from dataclasses import dataclass


@dataclass
class BicycleState:
    """
    BicycleState class.
    - the value of phi describes lean/roll of the frame
    - the value of delta describes the steering angle
    - the value of omega describes the rate of change of the lean
    - the value of beta describes the rate of change of the steering angle
    """

    def __init__(self):
        self.phi = 0.0
        self.delta = 0.0
        self.omega = 0.0
        self.beta = 0.0


    def get_roll(self):
        return self.phi

    def get_steering_angle(self):
        return self.delta

    def get_roll_rate(self):
        return self.omega

    def get_steering_rate(self):
        return self.beta