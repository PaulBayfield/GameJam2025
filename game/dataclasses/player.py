from dataclasses import dataclass


@dataclass
class PlayerData:
    name: str
    health: int = 100
    health_regen: float = 0.01
    stamina: int = 100
    speed: int = 10
