import math


class PlayState:
    target_framerate = 60

    def __init__(self, duration: int, timestep: float):
        self.frame = 0
        self.duration = duration
        self.timestep = timestep
        # get an approximate frame rate of 30 fps
        self.steps_per_frame = max(math.floor(1000 / self.target_framerate / self.timestep), 1)
        self.playing = False

    def step_forward(self):
        self.frame = (self.frame + 1) % self.duration

    def step_back(self):
        self.frame = (self.frame - 1) % self.duration

    def next_frame(self):
        self.frame = (self.frame + self.steps_per_frame) % self.duration

    def get_animation_delay_ms(self):
        return round(self.timestep * self.steps_per_frame)