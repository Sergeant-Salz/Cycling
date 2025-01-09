import numpy as np

from src.model.bicycle_state import BicycleState
from src.model.simulation_parameters import SimulationParameters
from src.model.simulation_result import SimulationResult


def check_abortion_criteria(state: BicycleState):
    """
    Abort is the bicycle has fallen over or the steering angle is larger than 90 degrees
    :param state:
    :return: True, if the simulation should be aborted
    """
    return abs(state.get_roll()) > np.pi / 2 or abs(state.get_steering_angle()) > np.pi / 2


class Simulation:

    parameters: SimulationParameters
    result: SimulationResult
    result_populated: bool = False

    def __init__(self, parameters: SimulationParameters):
        self.parameters = parameters
        self.result = SimulationResult(parameters.timestep, parameters.stepcount)

    def run(self):
        # populate the result with initial state
        # order: roll, steer, roll_rate, steer_rate, steer_torque
        self.result.data[0] = [self.parameters.initial_state.get_roll(),
                               self.parameters.initial_state.get_steering_angle(),
                               self.parameters.initial_state.get_roll_rate(),
                               self.parameters.initial_state.get_steering_rate(),
                               self.parameters.controller.calculate_control(self.parameters.initial_state).steer_torque]

        # compute the inverse of mass matrix M because we will need it for every timestep
        M_inv = np.linalg.inv(self.parameters.bicycle_model.M)
        # store some parameters for easier access
        v = self.parameters.bicycle_velocity
        g = 9.81
        C1 = self.parameters.bicycle_model.C1
        K0 = self.parameters.bicycle_model.K0
        K2 = self.parameters.bicycle_model.K2

        # for every timestep
        for step in range(1, self.parameters.stepcount):
            # calculate the second derivative of the previous state
            prev_q = self.result.data[step - 1][0:2]
            prev_q_dot = self.result.data[step - 1][2:4]
            prev_f = np.array([0.0, self.result.data[step - 1][4]])
            # equation 5.3 rearranged for q_ddot
            prev_q_ddot = prev_f - M_inv @ ((v * C1) @ prev_q_dot + (g * K0 + v ** 2 * K2) @ prev_q)

            # calculate the next state based on the previous state and second derivative
            # use a simple first-order approximation for the integral
            q_dot = prev_q_dot + self.parameters.timestep * prev_q_ddot
            q = prev_q + self.parameters.timestep * prev_q_dot
            curr_state = BicycleState(q[0], q[1], q_dot[0], q_dot[1])
            steering_torque = self.parameters.controller.calculate_control(curr_state).steer_torque
            # store the new state
            self.result.data[step] = [q[0], q[1], q_dot[0], q_dot[1], steering_torque]
            # check, if the simulation should be aborted
            if check_abortion_criteria(curr_state):
                # fill all remaining rows with the last state
                for i in range(step + 1, self.parameters.stepcount):
                    self.result.data[i] = self.result.data[step]
                break

        # populate other fields of the result
        self.result.metadata = self.parameters.get_description()
        self.result.timestep = self.parameters.timestep
        self.result_populated = True

    def get_result(self) -> SimulationResult:
        if not self.result_populated:
            raise ValueError("Simulation has not been run yet")
        return self.result

