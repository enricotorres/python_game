#from graphics import *
from classes import Pokemon, Trainer, Move
import random
import json

class BattleController:
    def __init__(self, BattleScene, trainer, player):
        self.trainer = trainer
        self.player = player
        self.states = ["player_turn", "trainer_turn", "attack", "bag", "pokemon", "run", "victory", "defeat"]
        self.state = self.states[0]
        self.types_damage = self.load_types_from_json()
        self.all_moves = self.load_moves_from_json()
        self.battle_scene = BattleScene

        self.run_battle_loop()


    def run_battle_loop(self):
        self.player_turn = True
        self.player_pkmn_idx = 0
        self.trainer_pkmn_idx = 0

        self.is_active = True
        while self.is_active:
            if self.check_end_condition():
                self.is_team_alive = False
                continue
            self.process_battle_state()
            self.handle_state_logic()


    def check_end_condition(self):
        if not self.is_team_alive(self.trainer) or not self.is_team_alive(self.player):
            return True
        return False


    def process_battle_state(self):
        self.player_pkmn = self.player.team[self.player_pkmn_idx]
        self.trainer_pkmn = self.trainer.team[self.trainer_pkmn_idx]

        if self.state == "player_turn":
            if not self.is_team_alive(self.player):
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
            if not self.is_team_alive(self.trainer):
                self.state = "victory"

            #implementar logica do adversario
            self.state = "player_turn"


    def handle_state_logic(self):
        if self.state == "attack":
            attack_index = self.battle_scene.chose_attack()
            chosen_move = self.player.team[attack_index]

            if self.player_pkmn.attack(chosen_move):
                hit_chance = random.randint(1, 100)
                if hit_chance <= chosen_move.accuracy:
                    damage = self.calculate_damage(chosen_move, self.player_pkmn, self.trainer_pkmn)
                    self.trainer_pkmn.take_damage(damage)
                else:
                    pass
                    #nao acertou

        elif self.state == "pokemon":
            self.pokemon_index = self.self.battle_scene.chose_pokemon()

        elif self.state == "bag":
            self.item_index = self.battle_scene.chose_item()

        elif self.state == "run":
            self.battle_scene.run()

        elif self.state == "defeat":
            self.battle_scene.defeat()

        elif self.state == "victory":
            self.battle_scene_victory()


    def is_team_alive(self):
        for pokemon in self.trainer.team:
            if pokemon.current_hp > 0:
                return True
        return False


    def load_types_from_json(self):
        with open("types.json", "r", encoding="utf-8" ) as file:
            return json.load(file)


    def load_moves_from_json(self):
        with open("moves.json", "r", encoding="utf-8") as file:
            moves_data = json.load(file)

        all_moves = {}
        for data in moves_data:
            new_move = Move(**data)
            all_moves[new_move.name] = new_move

        return all_moves


    def calculate_damage(self):
        attack_type_rules = self.types_damage.get(self.move.type, {})
        multiplier_1 = attack_type_rules.get(self.defender_pkmn.primary_type, 1.0)
        multiplier_2 = 1.0

        if self.defender_pkmn.secondary_type:
            multiplier_2 = attack_type_rules.get(self.defender_pkmn.secondary_type, 1.0)

        final_multiplier = multiplier_1 * multiplier_2

        stab = 1.0
        if self.attacking_pkmn.primary_type == self.move.type or self.attacking_pkmn.secondary_type == self.move.type:
            stab = 1.5

        damage = self.move.power * final_multiplier * stab
        return int(damage)
