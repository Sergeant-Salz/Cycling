from abc import abstractmethod, ABC
from multiprocessing.util import abstract_sockets_supported
from pathlib import Path
from typing import Self

import numpy as np

from src.visualization.animation import BikeAnimation
from src.visualization.animation_state import AnimationState


class AbstractSimulationResult(ABC):
    @abstractmethod
    def get_data_array(self) -> np.ndarray:
        pass

    @abstractmethod
    def get_metadata(self) -> dict[str, str]:
        pass

    @abstractmethod
    def set_metadata_field(self, key: str, value: str):
        pass

    @abstractmethod
    def get_timestep(self) -> float:
        """
        Get the timestep used in the simulation in seconds
        :return: The timestep used in the simulation
        """
        pass


class SimulationResult(AbstractSimulationResult, BikeAnimation):
    # store the state variables of the simulation
    # order: phi, delta, phi_dot, delta_dot, T_delta
    # order: roll, steer, roll_rate, steer_rate, steer_torque
    data: np.ndarray
    metadata: dict[str, str] = {}
    timestep: float

    def __init__(self, timestep: float, sample_cnt: int):
        self.timestep = timestep
        self.data = np.zeros((sample_cnt, 5))

    def set_metadata_field(self, key: str, value: str):
        self.metadata[key] = value

    def get_metadata(self) -> dict[str, str]:
        return self.metadata

    def get_data_array(self) -> np.ndarray:
        return self.data

    def get_timestep(self) -> float:
        return self.timestep

    def get_frame_delay_ms(self) -> int:
        return round(self.get_timestep() * 1000)

    def get_duration(self) -> int:
        return self.data.shape[0]

    def get_state_at_frame(self, frame) -> AnimationState:
        dataframe = self.data[frame]
        return AnimationState(dataframe[0], dataframe[1], 0.0)

    def save_to(self, path: Path):
        """
        Save the SimulationResult to a file
        :param path: Path to save the file to
        """
        metadata_fields = {}
        for key, value in self.metadata.items():
            metadata_fields["md_" + key] = value

        np.savez(path, data=self.data, timestep=self.timestep, **metadata_fields)

    @staticmethod
    def load_from(path: Path) -> "SimulationResult":
        """
        Load a SimulationResult from a file
        :param path: Path to the file to load
        :return: A SimulationResult object
        """
        file_contents = np.load(path)
        timestep = file_contents["timestep"]
        data = file_contents["data"]
        metadata = {key[3:]: str(file_contents[key]) for key in file_contents.files if key.startswith("md_")}

        # check dimensions of the data
        if len(data.shape) != 2 or data.shape[1] != 5:
            raise IOError(f"Data array in {path} is not of shape (n, 3)")

        result = SimulationResult(timestep, data.shape[0])
        result.data = data
        result.metadata = metadata
        return result