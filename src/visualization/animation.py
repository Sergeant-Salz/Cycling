from abc import ABC, abstractmethod

from src.visualization.animation_state import AnimationState


class BikeAnimation(ABC):

    @abstractmethod
    def get_state_at_frame(self, frame) -> AnimationState:
        pass
