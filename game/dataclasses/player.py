from dataclasses import dataclass


@dataclass
class PlayerData:
    name: str
    health: int = 100
    stamina: int = 100
