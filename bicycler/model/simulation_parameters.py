import math

from model.bicycle_controller import BicycleController, NoControlController
from model.bicycle_model import BicycleModel
from model.bicycle_state import BicycleState


class SimulationParameters:
    bicycle_model: BicycleModel
    initial_state: BicycleState
    controller: BicycleController
    timestep: float
    stepcount: int

    def __init__(self,
                 initial_state: BicycleState,
                 bicycle_model: BicycleModel = BicycleModel(),
                 bicycle_velocity: float = 4.0,
                 controller: BicycleController = NoControlController(),
                 timestep: float = 0.01,
                 stepcount: int = 500):
        self.bicycle_model = bicycle_model
        self.initial_state = initial_state
        self.bicycle_velocity = bicycle_velocity
        self.controller = controller
        self.timestep = timestep
        self.stepcount = stepcount

    def get_description(self) -> dict[str, str]:
        description = {'bicycle_model': "default" if self.bicycle_model.is_default() else "custom",
                       'initial_state': (f"roll: {round(math.degrees(self.initial_state.get_roll()), 3)}°, "
                                         f"steer: {round(math.degrees(self.initial_state.get_steering_angle()), 3)}°"),
                       'bicycle_velocity': f"{self.bicycle_velocity} m/s",
                       'controller': self.controller.get_name(),
                       'timestep': f"{round(self.timestep * 1000, 3)}ms",
                       'stepcount': str(self.stepcount)}

        # add non-default parameters to description if they exist
        if not self.bicycle_model.is_default():
            description['bicycle_model'] = description['bicycle_model'] + f" ({', '.join([k + ':' + str(v) for k, v in self.bicycle_model.get_non_default_values().items()])})"


        # add controller parameters to description if they exist
        controller_params = self.controller.get_parameters()
        if len(controller_params):
            description['controller'] = description['controller'] + f" ({', '.join([k + ':' + v for k, v in controller_params.items()])})"

        return description