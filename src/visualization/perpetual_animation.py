import math

from src.visualization.animation import BikeAnimation
from src.visualization.animation_state import AnimationState


class PerpetualAnimation(BikeAnimation):
    # how many radians the bike turns per frame
    turning_rate = 2 * math.pi / (5 * 60)
    # how often the steering changes per frame (sine wave period)
    steering_rate = 2 * math.pi / 60
    max_steering_ange = math.pi / 6

    def __init__(self):
        super().__init__()

    def get_state_at_frame(self, frame) -> AnimationState:
        # calculate the turning angle at the given frame
        turn = self.turning_rate * frame
        # calculate the steering angle at the given frame
        steer = self.max_steering_ange * math.cos(self.steering_rate * frame)
        return AnimationState(steer, steer, turn)

    def get_frame_delay_ms(self) -> int:
        return 33

    def get_duration(self) -> int:
        return max(round(2 * math.pi / self.steering_rate), round(2 * math.pi / self.turning_rate))

    def get_metadata(self) -> dict[str, str]:
        return {
            'name': 'Perpetual Animation',
            'description': 'A simple looping animation of arbitrary values',
            'framerate': str(round(1000 / self.get_frame_delay_ms())),
            'duration': str(self.get_duration())
        }