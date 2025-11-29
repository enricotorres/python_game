import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.classes import Trainer, Pokemon
from src.scenarios import BattleScene
from src.controllers import BattleController
from src.world_manager import WorldManager

def main():
    print("--- Inicializando Pokémon Python ---")

    ash_team = [
            Pokemon("Bulbasaur", level=100),
            Pokemon("Pikachu", level=100),
            Pokemon("Pidgey", level=5),
            Pokemon("Geodude", level=5),
            Pokemon("Gastly", level=5),
            Pokemon("Squirtle", level=5)
        ]

    gary_team = [
            Pokemon("Charmander", level=100),
            Pokemon("Rattata", level=100),
            Pokemon("Spearow", level=5),
            Pokemon("Onix", level=5),
            Pokemon("Zubat", level=5),
            Pokemon("Mankey", level=5)
        ]

    print("Times criados com sucesso!")

    player = Trainer(name="Ash", xp=0, initial_team=ash_team)
    rival = Trainer(name="Gary", xp=0, initial_team=gary_team)

    game_manager = WorldManager()

    battle_scene = BattleScene(game_manager.window)
    print("Gerenciador e Cena inicializados.")

    controller = BattleController(battle_scene, rival, player)
    controller.run_battle_loop()


if __name__ == "__main__":
    main()
