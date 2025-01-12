import numpy as np

from model.bicycle_state import BicycleState
from model.simulation_parameters import SimulationParameters
from model.simulation_result import SimulationResult


class Simulation:

    parameters: SimulationParameters
    result: SimulationResult
    result_populated: bool = False

    def __init__(self, parameters: SimulationParameters):
        self.parameters = parameters
        self.result = SimulationResult(parameters.timestep, parameters.stepcount)

    def run(self):
        # populate the result with initial state
        initial_steer_tourque = self.parameters.controller.calculate_control(
            self.parameters.initial_state.get_roll(),
            self.parameters.initial_state.get_steering_angle(),
            self.parameters.initial_state.get_roll_rate(),
            self.parameters.initial_state.get_steering_rate()).steer_torque
        self.result.set_state_at(0,
                                 self.parameters.initial_state.get_roll(),
                                 self.parameters.initial_state.get_steering_angle(),
                                 self.parameters.initial_state.get_roll_rate(),
                                 self.parameters.initial_state.get_steering_rate(),
                                 initial_steer_tourque,
                                 self.parameters.initial_state.get_heading())

        # compute the inverse of mass matrix M because we will need it for every timestep
        M_inv = np.linalg.inv(self.parameters.bicycle_model.M)
        # store some parameters for easier access
        v = self.parameters.bicycle_velocity
        g = self.parameters.bicycle_model.get_parameter('g')
        bike_lambda = self.parameters.bicycle_model.get_parameter('lambda')
        wheelbase = self.parameters.bicycle_model.get_parameter('w')
        trail = self.parameters.bicycle_model.get_parameter('c')
        C1 = self.parameters.bicycle_model.C1
        K0 = self.parameters.bicycle_model.K0
        K2 = self.parameters.bicycle_model.K2

        # for every timestep
        for step in range(1, self.parameters.stepcount):
            # calculate the second derivative of the previous state
            prev_state = self.result.get_state_at_frame(step - 1)
            prev_q = prev_state.get_q()
            prev_q_dot = prev_state.get_q_dot()
            prev_f = prev_state.get_f()
            # equation 5.3 rearranged for q_ddot
            prev_q_ddot = prev_f - M_inv @ ((v * C1) @ prev_q_dot + (g * K0 + v ** 2 * K2) @ prev_q)

            # calculate the next state based on the previous state and second derivative
            # use a simple first-order approximation for the integral
            q = prev_q + self.parameters.timestep * prev_q_dot
            q_dot = prev_q_dot + self.parameters.timestep * prev_q_ddot
            # get the controller input for the current state
            steering_torque = self.parameters.controller.calculate_control(q[0], q[1], q_dot[0], q_dot[1]).steer_torque

            # calculate the heading angle psi
            # based on equation (B6) from Appendix B
            psi_dot = trail / wheelbase * q_dot[1] + v * np.cos(bike_lambda) / wheelbase * q[1]
            psi = prev_state.heading + self.parameters.timestep * psi_dot

            # store the new state
            self.result.set_state_at(step, q[0], q[1], q_dot[0], q_dot[1], steering_torque, psi)
            # check, if the simulation should be aborted
            # if the bicycle has fallen over or the steering angle is larger than 90 degrees
            if abs(q[0]) > np.pi / 2 or abs(q[1]) > np.pi / 2:
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

