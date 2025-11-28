import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.classes import Trainer, Pokemon, Move
from src.scenarios import BattleScene
from src.controllers import BattleController

def main():

    move_tackle = Move(name="Tackle", type="Normal", power=40, accuracy=100, max_pp=35)
    move_scratch = Move(name="Scratch", type="Normal", power=40, accuracy=100, max_pp=35)

    player_pkmn = Pokemon(
        name="Bulbasaur", primary_type="Grass", level=5, xp=0, pokedex_id=1,
        base_hp=45, atk=49, defense=49, speed=45, moves=[move_tackle]
    )

    trainer_pkmn = Pokemon(
        name="Charmander", primary_type="Fire", level=5, xp=0, pokedex_id=4,
        base_hp=39, atk=52, defense=43, speed=65, moves=[move_scratch]
    )

    player = Trainer(name="ash", xp=0, initial_team=[player_pkmn])
    trainer = Trainer(name="gary", xp=0, initial_team=[trainer_pkmn])

    battle_scene = BattleScene()

    controller = BattleController(battle_scene, trainer, player)

    controller.run_battle_loop()

if __name__ == "__main__":
    main()
