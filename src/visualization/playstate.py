class PlayState:
    def __init__(self):
        self.frame = 0
        self.playing = True

    def step_forward(self):
        self.frame += 1

    def step_back(self):
        self.frame -= 1