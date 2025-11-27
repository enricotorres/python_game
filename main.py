#from graphics import *
from classes import Pokemon, Trainer, Move
import random
import json

def load_types_from_json():
    with open("types.json", "r", encoding="utf-8" ) as file:
        return json.load(file)

types_damage = load_types_from_json()

def load_moves_from_json():
    with open("moves.json", "r", encoding="utf-8") as file:
        moves_data = json.load(file)

    all_moves = {}
    for data in moves_data:
        new_move = Move(**data)
        all_moves[new_move.name] = new_move

    return all_moves

all_moves = load_moves_from_json()

#funcao apenas para testes
def chose_attack():
    attack = input("escolha o ataque ")
    obj_attack = all_moves[attack]
    return obj_attack

#funcao apenas para testes
def chose_pokemon():
    pokemon_idx = int(input("escolha o indice do pokemon"))
    return pokemon_idx


def battle(player, trainer):
    player_turn = True
    player_pkmn_idx = 0
    trainer_pkmn_idx = 0

    while True:

        if not is_team_alive(player):
            break

        if not is_team_alive(trainer):
            break

        alive = True
        player_pkmn = player.team[player_pkmn_idx]
        trainer_pkmn = trainer.team[trainer_pkmn_idx]

        if player_turn:
            pkmn_info = player_pkmn.show_status()
            print(pkmn_info)
            pkmn_info = trainer_pkmn.show_status()
            print(pkmn_info)

        if player_turn:
            if player_pkmn.current_hp <= 0:
                player_pkmn_idx = chose_pokemon() #funcao do cassiano

            action = input("escolha, run, pokemon, bag, attack: ")
            if action == "attack":
                chosen_move = chose_attack() #funcao do cassiano

                if player_pkmn.attack(chosen_move):
                    hit_chance = random.randint(1, 100)
                    if hit_chance <= chosen_move.accuracy:
                        damage = calculate_damage(chosen_move, player_pkmn, trainer_pkmn)
                        alive = trainer_pkmn.take_damage(damage)
                    else:
                        pass
                        #nao acertou

                    if not alive:
                        print("pokemon derrotado")
                        trainer_pkmn_idx = chose_pokemon() #funcao do cassiano

            if action == "run":
                break

            if action == "pokemon":
                player_pkmn_idx = chose_pokemon() #funcao do cassiano

            if action == "bag":
                item = chose_item() #funcao cassiano

            player_turn = False

        else:
            player_turn = True

        print("uma rodada")


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


#funcao teste
def setup_game():


    # Time do ash
    pikachu = Pokemon("Pikachu", "Electric", 0, 25, 35, 55, 40, 90, [all_moves["Thunder Shock"], all_moves["Tackle"]])
    pidgey = Pokemon("Pidgey", "Normal", 0, 16, 40, 45, 40, 56, [all_moves["Gust"], all_moves["Tackle"]], secondary_type="Flying")
    bulbasaur = Pokemon("Bulbasaur", "Grass", 0, 1, 45, 49, 49, 45, [all_moves["Vine Whip"], all_moves["Tackle"]], secondary_type="Poison")

    # Time do gary
    squirtle = Pokemon("Squirtle", "Water", 0, 7, 44, 48, 65, 43, [all_moves["Water Gun"], all_moves["Tackle"]])
    geodude = Pokemon("Geodude", "Rock", 0, 74, 40, 80, 100, 20, [all_moves["Rock Throw"], all_moves["Tackle"]], secondary_type="Ground")
    charmander = Pokemon("Charmander", "Fire", 0, 4, 39, 52, 43, 65, [all_moves["Ember"], all_moves["Scratch"]])

    player = Trainer("Ash", 0)
    player.add_pokemon(pikachu)
    player.add_pokemon(pidgey)
    player.add_pokemon(bulbasaur)

    enemy = Trainer("Gary", 0)
    enemy.add_pokemon(squirtle)
    enemy.add_pokemon(geodude)
    enemy.add_pokemon(charmander)

    return player, enemy


def main():
    player, enemy = setup_game()
    battle(player, enemy)



if __name__ == "__main__":
    main()
