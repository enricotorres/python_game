from graphics import *
from classes import Pokemon, Trainer, Move

def battle():

    while is_battle_active(player, enemy):

        if action == "attack":
            chosen_move = chose_attack()
            move = pokemon.attack(chosen_move)

            damage = calculate_damange(move, attacking_pkmn, defender_pkmn)






def main():
    pass



if __name__ == "__main__":
    main()
