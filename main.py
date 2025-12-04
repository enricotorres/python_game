import os
import sys
import logging
from graphics import update

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger("Main")

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.classes import Trainer, Pokemon
from src.scenarios import BattleScene, WorldScene
from src.controllers import BattleController
from src.world_manager import WorldManager


def main():
    logger.info("--- Inicializando Pokémon Python ---")

    ash_team = [
            Pokemon("Bulbasaur", level=1),
            Pokemon("Pikachu", level=100),
            Pokemon("Pidgey", level=5),
            Pokemon("Geodude", level=5),
            Pokemon("Gastly", level=5),
            Pokemon("Squirtle", level=5)
        ]

    gary_team = [
            Pokemon("Charmander", level=1, moves=["Fire Blast"]),
            Pokemon("Bulbasaur", level=1),
            Pokemon("Bulbasaur", level=1),
            Pokemon("Onix", level=5),
            Pokemon("Zubat", level=5),
            Pokemon("Mankey", level=5)
        ]

    logger.info(f"Times criados com sucesso. Player: {len(ash_team)} | Rival: {len(gary_team)}")

    player = Trainer(name="Ash", initial_team=ash_team)
    player.add_item("Potion", quantity=3)
    player.add_item("Revive", quantity=1)

    rival = Trainer(name="Gary", initial_team=gary_team)
    rival.add_item("Super Potion", quantity=2)

    try:
        game_manager = WorldManager()
        game_manager.window.autoflush = False
        world_scene = WorldScene(game_manager.window, player)
        while True:

            world_scene.update()

            if game_manager.window.isClosed():
                break

            update(60)

        logger.info("Gerenciador Gráfico e Cena de Batalha inicializados.")
    except Exception as e:
        logger.critical(f"Falha ao iniciar sistema gráfico: {e}")
        raise e

    #controller = BattleController(battle_scene, rival, player)

    #logger.info("Entrando no loop de batalha")
    #controller.run_battle_loop()

    logger.info("Jogo finalizado normalmente.")


if __name__ == "__main__":
    main()
