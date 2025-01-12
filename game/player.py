from .dataclasses.player import PlayerData


class Player(PlayerData):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        self.x = 0
        self.y = 0

        self.health = 100
        self.stamina = 100

    def move(self) -> None:
        print(f"{self.name} is moving")

    def attack(self) -> None:
        print(f"{self.name} is attacking")

    def heal(self) -> None:
        print(f"{self.name} is healing")

    def dash(self) -> None:
        print(f"{self.name} is dashing")
