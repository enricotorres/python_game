import logging
import sys
from pathlib import Path


from src.battle.scene import BattleScene
from src.lib.graphics import update
from src import Trainer, Pokemon, SceneManager, WorldScene, PokecenterScene

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger("Main")

def main():
    logger.info("--- Inicializando Pokémon Python ---")

    ash_team = [
        Pokemon("Bulbasaur", level=1),
        Pokemon("Pikachu", level=100),
        Pokemon("Pidgey", level=5),
        Pokemon("Geodude", level=5),
        Pokemon("Gastly", level=5),
        Pokemon("Squirtle", level=5),
    ]

    gary_team = [
        Pokemon("Charmander", level=1, moves=["Fire Blast"]),
        Pokemon("Bulbasaur", level=1),
        Pokemon("Bulbasaur", level=1),
        Pokemon("Onix", level=5),
        Pokemon("Zubat", level=5),
        Pokemon("Mankey", level=5),
    ]

    logger.info(f"Times criados com sucesso. Player: {len(ash_team)} | Rival: {len(gary_team)}")

    player = Trainer(name="Ash", initial_team=ash_team)
    player.add_item("Potion", quantity=3)
    player.add_item("Revive", quantity=1)

    rival = Trainer(name="Gary", initial_team=gary_team)
    rival.add_item("Super Potion", quantity=2)

    try:
        game_manager = SceneManager(player=player)
        game_manager.change_scene(WorldScene, player=player)

        while True:
            game_manager.current_scene.update()
            if game_manager.window.isClosed():
                break
            update(60)

        logger.info("Gerenciador Gráfico e Cena de Mundo inicializados.")
    except Exception as e:
        logger.critical(f"Falha ao iniciar sistema gráfico: {e}")
        raise

    logger.info("Jogo finalizado normalmente.")


if __name__ == "__main__":
    main()
