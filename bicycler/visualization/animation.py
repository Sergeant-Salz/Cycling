from abc import ABC, abstractmethod

from model.bicycle_state import BicycleState


class BikeAnimation(ABC):

    @abstractmethod
    def get_state_at_frame(self, frame) -> BicycleState:
        pass

    @abstractmethod
    def get_frame_delay_ms(self) -> int:
        pass

    @abstractmethod
    def get_duration(self) -> int:
        """
        Get the duration of the animation in frames
        :return: The number of frames in the animation
        """
        pass

    @abstractmethod
    def get_metadata(self) -> dict[str, str]:
        pass