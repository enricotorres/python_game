import logging

from src.lib.graphics import update
from src import Trainer, Pokemon, SceneManager
from src.world.scenes import PokecenterScene, WorldScene

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger("Main")

def main():
    logger.info("--- Inicializando Pokémon Python ---")

    ash_team = [
        Pokemon("Pikachu", level=50, moves=["Thunderbolt", "Quick Attack", "Iron Tail", "Thunder Wave"]),
        Pokemon("Bulbasaur", level=50, moves=["Solar Beam", "Sludge Bomb", "Leech Seed", "Razor Leaf"]),
        Pokemon("Charmander", level=50, moves=["Flamethrower", "Slash", "Dragon Rage", "Fire Spin"]),
        Pokemon("Squirtle", level=50, moves=["Hydro Pump", "Ice Beam", "Surf", "Bite"]),
        Pokemon("Pidgey", level=50, moves=["Aerial Ace", "Steel Wing", "Wing Attack", "Quick Attack"]),
        Pokemon("Mankey", level=50, moves=["Brick Break", "Karate Chop", "Submission", "Seismic Toss"])
    ]

    gary_team = [
        Pokemon("Onix", level=50, moves=["Iron Tail", "Earthquake", "Rock Slide", "Double Edge"]),
        Pokemon("Geodude", level=50, moves=["Earthquake", "Rock Throw", "Self Destruct", "Double Edge"]),
        Pokemon("Gastly", level=50, moves=["Shadow Ball", "Hypnosis", "Dream Eater", "Confuse Ray"]),
        Pokemon("Zubat", level=50, moves=["Sludge Bomb", "Aerial Ace", "Confuse Ray", "Bite"]),
        Pokemon("Charmander", level=50, moves=["Fire Blast", "Dragon Claw", "Brick Break", "Smokescreen"]),
        Pokemon("Squirtle", level=50, moves=["Hydro Cannon", "Ice Beam", "Water Pulse", "Skull Bash"])
    ]

    logger.info(f"Times criados com sucesso. Player: {len(ash_team)} | Rival: {len(gary_team)}")

    player = Trainer(name="Ash", initial_team=ash_team)
    player.add_item("Potion", quantity=3)
    player.add_item("Revive", quantity=1)

    rival = Trainer(name="Gary", initial_team=gary_team)
    rival.add_item("Super Potion", quantity=2)

    try:
        game_manager = SceneManager(player=player)
        game_manager.change_scene(PokecenterScene)
        world_scene = game_manager.current_scene
        world_scene.add_npc(rival, x=1550, y=1360)

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
