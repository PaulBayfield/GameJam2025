import json
import os

from typing import Any, Dict


class Stats:
    """
    Classe pour gérer les statistiques du jeu
    """

    def __init__(self):
        """
        Initialisation de la classe
        """
        if not os.path.exists("stats.json"):
            stats = {
                "kills": 0,
                "deaths": 0,
                "secondsPlayed": 0,
                "gamesPlayed": 0,
            }

            with open("stats.json", "w", encoding="utf-8") as file:
                json.dump(stats, file)

    def update(self, key: str, value: Any) -> None:
        """
        Met à jour les statistiques du jeu

        :param data: Les données à mettre à jour
        :type data: dict
        """
        data = self.load()
        if key in data:
            data[key] += value
        else:
            data[key] = value

        with open("stats.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self) -> Dict[str, Any]:
        """
        Charge les statistiques du jeu

        :return: Les statistiques du jeu
        :rtype: dict
        """
        with open("stats.json", "r", encoding="utf-8") as file:
            return json.load(file)
