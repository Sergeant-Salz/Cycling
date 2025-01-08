from src.model.simulation_parameters import SimulationParameters
from src.model.simulation_result import SimulationResult


class Simulation:

    parameters: SimulationParameters
    result: SimulationResult
    result_populated: bool = False

    def __init__(self, parameters: SimulationParameters):
        self.parameters = parameters
        self.result = SimulationResult(parameters.timestep, parameters.stepcount)

    def run(self):
        # dummy code for now which will fill the result with zeros
        self.result.data[0] = [self.parameters.initial_state.get_roll(),
                               self.parameters.initial_state.get_steering_angle(),
                               self.parameters.initial_state.get_roll_rate(),
                               self.parameters.initial_state.get_steering_rate(),
                               0]
        for step in range(1, self.parameters.stepcount):
            self.result.data[step] = [0, 0, 0, 0, 0]

        # populate other fields of the result
        self.result.metadata = self.parameters.get_description()
        self.result.timestep = self.parameters.timestep
        self.result_populated = True

    def get_result(self) -> SimulationResult:
        if not self.result_populated:
            raise ValueError("Simulation has not been run yet")
        return self.result

