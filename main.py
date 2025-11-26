from graphics import *
from classes import Pokemon, Trainer, Move
from types import types_damage
import random

def battle(player, trainer):

    player_turn = True
    player_pkmn_idx = 0
    trainer_pkmn_idx = 0

    while True:

        if not is_team_alive(player):
            break

        if not is_team_alive(trainer):
            break

        player_pkmn = player.team[player_pkmn_idx]
        trainer_pkmn = trainer.team[trainer_pkmn_idx]

        if player_turn:
            if player_pkmn.current_hp <= 0:
                chose_pokemon() #funcao do cassiano

            if action == "attack":
                chosen_move = chose_attack() #funcao do cassiano
                move = pokemon.attack(chosen_move)

                if player_pkmn.attack(chosen_move):
                    hit_chance = random.randint(1, 100)
                    if hit_chance <= chosen_move.accuracy:
                        damage = calculate_damage(chosen_move, player_pkmn, trainer_pkmn)
                        alive = trainer_pkmn.take_damage(damage)
                    else:
                        #nao acertou

                    if not alive:
                        player_pkmn = chose_pokemon() #funcao do cassiano

            if action == "run":
                break

            if action == "pokemon":
                chose_pokemon() #funcao do cassiano

            if action == "bag":
                chose_item() #funcao cassiano

            player_turn = False

        else:
            player_turn = True



def is_team_alive(trainer):

    for pokemon in trainer.team:
        if pokemon.current_hp > 0:
            return True
    return False


def calculate_damage(move, attacking_pkmn, defender_pkmn):
    attack_type_rules = types_damage.get(move.type, {})
    multiplier_1 = attack_type_rules.get(defender_pkmn.primary_type, 1.0)
    multiplier_2 = 1.0

    if defender_pkmn.secondary_type:
        multiplier_2 = attack_type_rules.get(defender_pkmn.secondary_type, 1.0)

    final_multiplier = multiplier_1 * multiplier_2

    stab = 1.0
    if attacking_pkmn.primary_type == move.type or attacking_pkmn.secondary_type == move.type:
        stab = 1.5

    damage = move.power * final_multiplier * stab
    return int(damage)


def main():
    player = Trainer()
    enemy = Trainer()

    battle(player, enemy)
    pass


if __name__ == "__main__":
    main()
