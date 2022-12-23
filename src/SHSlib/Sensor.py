import typing
from dataclasses import dataclass


@dataclass
class Sensor:
    resolution: int = 10
    Pixel_size_um: int = 20
