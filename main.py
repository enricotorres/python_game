import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.classes import Trainer, Pokemon, Move
from src.scenarios import BattleScene
from src.controllers import BattleController

def main():
    move_tackle = Move(name="Tackle", type="Normal", power=40, accuracy=100, max_pp=35)
    move_scratch = Move(name="Scratch", type="Normal", power=40, accuracy=100, max_pp=35)
    move_growl = Move(name="Growl", type="Normal", power=0, accuracy=100, max_pp=40)
    move_leer = Move(name="Leer", type="Normal", power=0, accuracy=100, max_pp=30)

    # Ataques Específicos
    move_vine_whip = Move(name="Vine Whip", type="Grass", power=45, accuracy=100, max_pp=25)
    move_ember = Move(name="Ember", type="Fire", power=40, accuracy=100, max_pp=25)
    move_water_gun = Move(name="Water Gun", type="Water", power=40, accuracy=100, max_pp=25)
    move_thunder_shock = Move(name="Thunder Shock", type="Electric", power=40, accuracy=100, max_pp=30)
    move_peck = Move(name="Peck", type="Flying", power=35, accuracy=100, max_pp=35)
    move_rock_throw = Move(name="Rock Throw", type="Rock", power=50, accuracy=90, max_pp=15)
    move_poison_sting = Move(name="Poison Sting", type="Poison", power=15, accuracy=100, max_pp=35)
    move_lick = Move(name="Lick", type="Ghost", power=30, accuracy=100, max_pp=30)

    # --- 2. Criação dos Times (6 Pokémon cada) ---

    # Time do Jogador (Ash)
    ash_team = [
        Pokemon(
            name="Bulbasaur", primary_type="Grass", level=5, xp=0, pokedex_id=1,
            base_hp=45, atk=49, defense=49, speed=45,
            moves=[move_tackle, move_vine_whip, move_growl, move_leer]
        ),
        Pokemon(
            name="Pikachu", primary_type="Electric", level=5, xp=0, pokedex_id=25,
            base_hp=35, atk=55, defense=40, speed=90,
            moves=[move_scratch, move_thunder_shock, move_growl, move_tackle]
        ),
        Pokemon(
            name="Pidgey", primary_type="Normal", secondary_type="Flying", level=5, xp=0, pokedex_id=16,
            base_hp=40, atk=45, defense=40, speed=56,
            moves=[move_peck, move_scratch, move_growl, move_leer]
        ),
        Pokemon(
            name="Geodude", primary_type="Rock", secondary_type="Ground", level=5, xp=0, pokedex_id=74,
            base_hp=40, atk=80, defense=100, speed=20,
            moves=[move_rock_throw, move_tackle, move_scratch, move_growl]
        ),
        Pokemon(
            name="Gastly", primary_type="Ghost", secondary_type="Poison", level=5, xp=0, pokedex_id=92,
            base_hp=30, atk=35, defense=30, speed=80,
            moves=[move_lick, move_poison_sting, move_leer, move_tackle]
        ),
        Pokemon(
            name="Squirtle", primary_type="Water", level=5, xp=0, pokedex_id=7,
            base_hp=44, atk=48, defense=65, speed=43,
            moves=[move_water_gun, move_tackle, move_scratch, move_growl]
        )
    ]

    gary_team = [
        Pokemon(
            name="Charmander", primary_type="Fire", level=5, xp=0, pokedex_id=4,
            base_hp=39, atk=52, defense=43, speed=65,
            moves=[move_tackle, move_ember, move_growl, move_scratch]
        ),
        Pokemon(
            name="Rattata", primary_type="Normal", level=5, xp=0, pokedex_id=19,
            base_hp=30, atk=56, defense=35, speed=72,
            moves=[move_tackle, move_scratch, move_growl, move_leer]
        ),
        Pokemon(
            name="Spearow", primary_type="Normal", secondary_type="Flying", level=5, xp=0, pokedex_id=21,
            base_hp=40, atk=60, defense=30, speed=70,
            moves=[move_peck, move_scratch, move_tackle, move_leer]
        ),
        Pokemon(
            name="Onix", primary_type="Rock", secondary_type="Ground", level=5, xp=0, pokedex_id=95,
            base_hp=35, atk=45, defense=160, speed=70,
            moves=[move_rock_throw, move_tackle, move_scratch, move_growl]
        ),
        Pokemon(
            name="Zubat", primary_type="Poison", secondary_type="Flying", level=5, xp=0, pokedex_id=41,
            base_hp=40, atk=45, defense=35, speed=55,
            moves=[move_poison_sting, move_tackle, move_scratch, move_leer]
        ),
        Pokemon(
            name="Mankey", primary_type="Fighting", level=5, xp=0, pokedex_id=56,
            base_hp=40, atk=80, defense=35, speed=70,
            moves=[move_scratch, move_tackle, move_growl, move_leer]
        )
    ]

    player = Trainer(name="Ash", xp=0, initial_team=ash_team)
    trainer = Trainer(name="Gary", xp=0, initial_team=gary_team)

    battle_scene = BattleScene()
    print("Controller inicializado.")
    controller = BattleController(battle_scene, trainer, player)

    controller.run_battle_loop()

if __name__ == "__main__":
    main()
