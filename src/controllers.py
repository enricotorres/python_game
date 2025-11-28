
from classes import Pokemon, Trainer, Move
from scenarios import BattleScene
import random
import json
import os

class BattleController:
    def __init__(self, battle_scene, trainer, player):
        self.player = player
        self.trainer = trainer
        self.battle_scene = battle_scene
        self.types_damage = self.load_types_from_json()
        self.all_moves = self.load_moves_from_json()
        self.cancel_action = -1

        self.player_action_type = None
        self.player_chosen_move = None
        self.enemy_chosen_move = None
        self.switch_target_idx = None

        self.state = "START"
        self.run_battle_loop()

    def run_battle_loop(self):
        self.state = "PLAYER_TURN"
        self.player_pkmn_idx = 0
        self.trainer_pkmn_idx = 0

        self.player_pkmn = self.player.team[self.player_pkmn_idx]
        self.trainer_pkmn = self.trainer.team[self.trainer_pkmn_idx]

        while self.state != "EXIT":
            self.player_pkmn = self.player.team[self.player_pkmn_idx]
            self.trainer_pkmn = self.trainer.team[self.trainer_pkmn_idx]

            print(self.player_pkmn.show_status())
            print(self.trainer_pkmn.show_status())

            input_states = ["PLAYER_TURN", "SELECT_MOVE", "POKEMON_MENU", "BAG_MENU", "FORCE_SWITCH"]

            if self.state in input_states:
                self.handle_state_logic()
            else:
                self.process_battle_state()

    def handle_state_logic(self):
        if self.state == "PLAYER_TURN":
            if not self.is_team_alive(self.player):
                self.state = "DEFEAT"
                return

            action = self.battle_scene.chose_action()

            match action:
                case "attack":
                    self.state = "SELECT_MOVE"
                case "bag":
                    self.player_action_type = "bag"
                    self.decide_enemy_move()
                    self.state = "RESOLVE_TURN"
                case "pokemon":
                    self.state = "POKEMON_MENU"
                case "run":
                    self.player_action_type = "run"
                    self.state = "RESOLVE_TURN"
                case _:
                    pass

        elif self.state == "SELECT_MOVE":
            attack_index = self.battle_scene.chose_attack()
            if attack_index == self.cancel_action:
                self.state = "PLAYER_TURN"
                return

            self.player_chosen_move = self.player_pkmn.moves[attack_index]
            self.player_action_type = "attack"

            self.decide_enemy_move()
            self.state = "RESOLVE_TURN"

        elif self.state == "POKEMON_MENU":
            idx = self.battle_scene.chose_pokemon()

            if idx == self.cancel_action:
                self.state = "PLAYER_TURN"
                return

            if 0 <= idx < len(self.player.team) and self.player.team[idx].is_alive() and idx != self.player_pkmn_idx:
                self.switch_target_idx = idx
                self.player_action_type = "switch"

                self.decide_enemy_move()
                self.state = "RESOLVE_TURN"
            else:
                self.state = "PLAYER_TURN"

        elif self.state == "BAG_MENU":
            self.state = "PLAYER_TURN"

        elif self.state == "FORCE_SWITCH":
            idx = self.battle_scene.chose_pokemon()

            if idx == self.cancel_action:
                return

            if 0 <= idx < len(self.player.team):
                if self.player.team[idx].is_alive():
                    self.player_pkmn_idx = idx
                    self.player_pkmn = self.player.team[self.player_pkmn_idx]
                    self.state = "PLAYER_TURN"
                else:
                    pass # Logica visual deve informar que está desmaiado
            else:
                pass

    def decide_enemy_move(self):
        valid_moves = [m for m in self.trainer_pkmn.moves if m.current_pp > 0]
        if valid_moves:
            self.enemy_chosen_move = random.choice(valid_moves)
        else:
            self.enemy_chosen_move = self.trainer_pkmn.moves[0]

    def process_battle_state(self):
        if self.state == "RESOLVE_TURN":
            if self.player_action_type == "run":
                self.battle_scene.run()
                self.state = "EXIT"
                return

            elif self.player_action_type == "switch":
                self.player_pkmn_idx = self.switch_target_idx
                self.player_pkmn = self.player.team[self.player_pkmn_idx]

                if self.check_battle_status():
                     self.perform_attack(self.trainer_pkmn, self.player_pkmn, self.enemy_chosen_move)

            elif self.player_action_type == "bag":
                if self.check_battle_status():
                     self.perform_attack(self.trainer_pkmn, self.player_pkmn, self.enemy_chosen_move)

            elif self.player_action_type == "attack":
                p_speed = self.player_pkmn.speed
                e_speed = self.trainer_pkmn.speed

                first = None
                second = None
                speed_tie = False
                if p_speed == e_speed:
                    speed_tie = random.choice([True, False])

                if p_speed > e_speed or (p_speed == e_speed and speed_tie):
                    first = (self.player_pkmn, self.trainer_pkmn, self.player_chosen_move)
                    second = (self.trainer_pkmn, self.player_pkmn, self.enemy_chosen_move)
                else:
                    first = (self.trainer_pkmn, self.player_pkmn, self.enemy_chosen_move)
                    second = (self.player_pkmn, self.trainer_pkmn, self.player_chosen_move)

                self.perform_attack(first[0], first[1], first[2])

                if self.check_battle_status():
                    if second[0].is_alive():
                        self.perform_attack(second[0], second[1], second[2])
                        self.check_battle_status()

            if self.state not in ["VICTORY", "DEFEAT", "EXIT", "FORCE_SWITCH"]:
                self.state = "PLAYER_TURN"

        elif self.state == "VICTORY":
            self.state = "EXIT"

        elif self.state == "DEFEAT":
            self.state = "EXIT"

    def perform_attack(self, attacker, defender, move):
        if attacker.attack(move):
            if random.randint(1, 100) <= move.accuracy:
                damage = self.calculate_damage(attacker, defender, move)
                defender.take_damage(damage)
                # self.battle_scene.animate_damage()
            else:
                pass # implementar
        else:
            pass # implementar logica sem pp

    def check_battle_status(self):
        if not self.is_team_alive(self.player):
            self.state = "DEFEAT"
            return False

        if not self.is_team_alive(self.trainer):
            self.state = "VICTORY"
            return False

        if not self.player_pkmn.is_alive():
            self.state = "FORCE_SWITCH"
            return False

        if not self.trainer_pkmn.is_alive():
            if self.swap_enemy_pokemon():
                pass # logica visual para trocar de pokemon
            return False

        return True

    def swap_enemy_pokemon(self):
        for i, pkmn in enumerate(self.trainer.team):
            if pkmn.is_alive():
                self.trainer_pkmn_idx = i
                self.trainer_pkmn = pkmn
                return True
        return False

    def is_team_alive(self, trainer):
        for pokemon in trainer.team:
            if pokemon.current_hp > 0:
                return True
        return False

    def load_types_from_json(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, "data", "types.json")
        with open(path, "r", encoding="utf-8" ) as file:
            return json.load(file)

    def load_moves_from_json(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, "data", "moves.json")
        with open(path, "r", encoding="utf-8") as file:
            moves_data = json.load(file)

        all_moves = {}
        for data in moves_data:
            new_move = Move(**data)
            all_moves[new_move.name] = new_move
        return all_moves

    def calculate_damage(self, attacker, defender, chosen_move):
        multiplier_1 = ((2 * attacker.level/ 5) + 2)
        multiplier_2 = multiplier_1 * (chosen_move.power * attacker.atk / defender.defense)
        multiplier_3 = (multiplier_2 / 50) + 2

        attack_type_rules = self.types_damage.get(chosen_move.type, {})
        multiplier_4 = attack_type_rules.get(defender.primary_type, 1.0)
        multiplier_5 = 1.0

        if defender.secondary_type:
            multiplier_5 = attack_type_rules.get(defender.secondary_type, 1.0)

        final_multiplier = multiplier_4 * multiplier_5

        stab = 1.0
        if attacker.primary_type == chosen_move.type or attacker.secondary_type == chosen_move.type:
            stab = 1.5

        damage = multiplier_3 * final_multiplier * stab
        return int(damage)
