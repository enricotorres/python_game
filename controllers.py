#from graphics import *
from math import e
from classes import Pokemon, Trainer, Move
import random
import json

class BattleController:
    def __init__(self, BattleScene, trainer, player):
        self.trainer = trainer
        self.player = player
        self.states = ["player_turn", "trainer_turn", "attack", "bag", "pokemon", "run", "victory", "defeat"]
        self.state = self.states[0]
        self.types_damage = load_types_from_json()
        self.all_moves = load_moves_from_json()
        self.battle_scene = BattleScene

        run_battle_loop()


    def run_battle_loop(self, trainer, player):
        player_turn = True
        player_pkmn_idx = 0
        trainer_pkmn_idx = 0

        self.is_active = True
        while self.is_active:
            if self.check_end_condition():
                self.is_team_alive = False
                continue
            process_battle_state()
            handle_state_logic()


    def check_end_condition():
        if not is_team_alive(trainer) or not is_team_alive(player):
            return True
        return False


    def process_battle_state(self, trainer,player):
        player_pkmn = player.team[player_pkmn_idx]
        trainer_pkmn = trainer.team[trainer_pkmn_idx]

        if self.state == "player_turn":
            if not is_team_alive(player):
                self.state = "defeat"

            action = self.battle_scene.chose_action()

            match action:
                case "attack":
                    self.state = "attack"
                case "bag":
                    self.state = "bag"
                case "pokemon":
                    self.state = "pokemon"
                case "run":
                    self.state = "run"

            self.state == "trainer_turn"

        elif self.state == "trainer_turn":
            if not is_team_alive(trainer):
                self.state = "victory"

            #implementar logica do adversario
            self.state = "player_turn"


    def handle_state_logic():
        if self.state == "attack":
            attack_index = self.battle_scene.chose_attack()
            chosen_move = self.player.team[attack_index]

            if self.player_pkmn.attack(chosen_move):
                hit_chance = random.randint(1, 100)
                if hit_chance <= chosen_move.accuracy:
                    damage = calculate_damage(chosen_move, player_pkmn, trainer_pkmn)
                    alive = trainer_pkmn.take_damage(damage)
                else:
                    pass
                    #nao acertou

        elif self.state == "pokemon":
            pokemon_index = self.self.battle_scene.chose_pokemon()

        elif self.state == "bag":
            item_index = self.battle_scene.chose_item()

        elif self.state == "run":
            self.battle_scene.run()

        elif self.state == "defeat":
            self.battle_scene.defeat()

        elif self.state == "victory":
            self.battle_scene_victory()


    def is_team_alive(trainer):
        for pokemon in trainer.team:
            if pokemon.current_hp > 0:
                return True
        return False


    def load_types_from_json():
        with open("types.json", "r", encoding="utf-8" ) as file:
            return json.load(file)


    def load_moves_from_json():
        with open("moves.json", "r", encoding="utf-8") as file:
            moves_data = json.load(file)

        all_moves = {}
        for data in moves_data:
            new_move = Move(**data)
            all_moves[new_move.name] = new_move

        return all_moves


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
