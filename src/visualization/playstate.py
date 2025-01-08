class PlayState:
    def __init__(self, duration: int):
        self.frame = 0
        self.duration = duration
        self.playing = False

    def step_forward(self):
        self.frame = (self.frame + 1) % self.duration

    def step_back(self):
        self.frame = (self.frame - 1) % self.duration