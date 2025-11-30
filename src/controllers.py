
import random
import json
import os
import math

from src.classes import Item, Move

class BattleController:
    def __init__(self, battle_scene, trainer, player):
        self.player = player
        self.trainer = trainer
        self.battle_scene = battle_scene
        self.types_damage = self.load_types_from_json()
        self.cancel_action = -1

        self.player_action_type = None
        self.player_chosen_move = None
        self.enemy_chosen_move = None
        self.switch_target_idx = None

        self.state = "START"


    def run_battle_loop(self):
        self.state = "PLAYER_TURN"
        self.player_pkmn_idx = 0
        self.trainer_pkmn_idx = 0

        self.player_pkmn = self.player.team[self.player_pkmn_idx]
        self.trainer_pkmn = self.trainer.team[self.trainer_pkmn_idx]

        while self.state != "EXIT":
            self.player_pkmn = self.player.team[self.player_pkmn_idx]
            self.trainer_pkmn = self.trainer.team[self.trainer_pkmn_idx]
            for _ in range(4):
                print()
            print(f"{self.player_pkmn.name} de {self.player.name} vs {self.trainer_pkmn.name} de {self.trainer.name}")
            print(f"{self.player_pkmn.name} esta com {self.player_pkmn.current_hp} de vida de {self.player_pkmn.max_hp}")
            print(f"{self.trainer_pkmn.name} esta com {self.trainer_pkmn.current_hp} de vida de {self.trainer_pkmn.max_hp}")

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
        hp_percent = self.trainer_pkmn.current_hp / self.trainer_pkmn.max_hp

        if hp_percent < 0.30:
            healing_items = ["Full Restore", "Hyper Potion", "Super Potion", "Potion"]

            for item_name in healing_items:
                if self.trainer.bag.get(item_name, 0) > 0:
                    self.enemy_action_type = "bag"
                    self.enemy_chosen_item = Item(item_name)
                    return

        self.enemy_action_type = "attack"

        valid_moves = [m for m in self.trainer_pkmn.moves if m.current_pp > 0]
        if not valid_moves:
            self.enemy_chosen_move = Move("Struggle")
            return

        best_move = None
        best_damage = -1

        for move in valid_moves:
            damage = self.calculate_damage(self.trainer_pkmn, self.player_pkmn, move)
            if damage > best_damage:
                best_damage = damage
                best_move = move

        self.enemy_chosen_move = best_move


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

            if getattr(self, "enemy_action_type", "attack") == "bag":
                item = self.enemy_chosen_item
                if item.use(self.trainer_pkmn):
                    self.trainer.use_item(item.name)

            elif self.player_action_type == "bag":
                if self.check_battle_status():
                     self.perform_attack(self.trainer_pkmn, self.player_pkmn, self.enemy_chosen_move)

            elif self.player_action_type == "attack":
                p_speed = self.player_pkmn.speed
                e_speed = self.trainer_pkmn.speed

                p_prio = self.player_chosen_move.priority
                e_prio = self.enemy_chosen_move.priority

                first = None
                second = None
                player_goes_first = False

                if p_prio > e_prio:
                    player_goes_first = True
                elif e_prio > p_prio:
                    player_goes_first = False

                else:
                    if p_speed > e_speed:
                        player_goes_first = True
                    elif e_speed > p_speed:
                        player_goes_first = False
                    else:
                        player_goes_first = random.choice([True, False])

                if player_goes_first:
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


            critical_states = ["VICTORY", "DEFEAT", "EXIT", "FORCE_SWITCH"]

            if self.state not in critical_states:
                self.end_of_turn_resolution()

            if self.state not in critical_states:
                self.state = "PLAYER_TURN"

        elif self.state == "VICTORY":
            self.state = "EXIT"

        elif self.state == "DEFEAT":
            self.state = "EXIT"


    def perform_attack(self, attacker, defender, move):
        if attacker.status == "sleep":
            if random.randint(1, 100) >=50:
                attacker.status = None
            else:
                return False

        elif attacker.status == "freeze":
            if random.randint(1, 100) <= 25:
                attacker.status = None
            else:
                return False

        elif attacker.status == "paralysis":
            if random.randint(1, 100) <= 30:
                return False


        if not attacker.attack(move):
            return

        hit_chance = random.randint(1, 100)

        acc_stage = attacker.stat_mods.get("accuracy", 0)
        eva_stage = defender.stat_mods.get("evasion", 0)
        combined = acc_stage - eva_stage
        multipliers = { -6: 0.33, -5: 0.37, -4: 0.43, -3: 0.50, -2: 0.60, -1: 0.75, 0: 1.0, 1: 1.33, 2: 1.66, 3: 2.0, 4: 2.33, 5: 2.66, 6: 3.0 }

        if combined < -6: combined = -6
        if combined > 6: combined = 6

        accuracy_multiplier = multipliers.get(combined, 1.0)
        final_accuracy = move.accuracy * accuracy_multiplier

        if hit_chance > final_accuracy:
            return

        damage = self.calculate_damage(attacker, defender, move)
        if damage > 0:
            defender.take_damage(damage)
                # animacao de dano

        if move.effect:
            self.process_move_effect(move, attacker, defender)


    def process_move_effect(self, move, attacker, defender):
        effect_data = move.effect

        chance = effect_data.get("chance", 100)
        if random.randint(1, 100) > chance:
            return

        target_str = effect_data.get("target")
        target_pkmn = None

        if target_str == "enemy":
            target_pkmn = defender
        elif target_str == "self":
            target_pkmn = attacker
        else:
            return

        effect_type = effect_data.get("type")

        if effect_type == "stat_change":
            stat_name = effect_data.get("stat")
            amount = effect_data.get("amount")

            if target_pkmn.apply_stat_change(stat_name, amount):
                print(f"{target_pkmn.name} teve seu {stat_name} alterado em {amount}!")

        elif effect_type == "status_condition":
            condition = effect_data.get("condition")

            if target_pkmn.status is None:
                target_pkmn.status = condition
                print(f"{target_pkmn.name} agora está {condition}!")
            else:
                print(f"{target_pkmn.name} já tem um problema de status!")


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


    def calculate_damage(self, attacker, defender, chosen_move):

        hits = 1
        if hasattr(chosen_move, "mechanics"):
            if "multi_hit" in chosen_move.mechanics:
                min_hits = chosen_move.mechanics["multi_hit"]["min"]
                max_hits = chosen_move.mechanics["multi_hit"]["max"]
                hits = random.randint(min_hits, max_hits)

        if chosen_move.category == "Special":
            attack_stat = attacker.get_current_stat("special-attack")
            defense_stat = defender.get_current_stat("special-defense")
        else:
            attack_stat = attacker.get_current_stat("attack")
            defense_stat = defender.get_current_stat("defense")

        level_factor = ((2 * attacker.level // 5) + 2)
        raw_damage_part = level_factor * (chosen_move.power * attack_stat // defense_stat)
        damage_base = (raw_damage_part // 50) + 2
        type_rules = self.types_damage.get(chosen_move.type, {})
        prim_type_name = defender.types[0]
        type_effectiveness_primary = type_rules.get(prim_type_name, 1.0)

        type_effectiveness_secondary = 1.0
        if len(defender.types) > 1:
            sec_type_name = defender.types[1]
            type_effectiveness_secondary = type_rules.get(sec_type_name, 1.0)

        final_type_multiplier = type_effectiveness_primary * type_effectiveness_secondary

        stab_bonus = 1.0
        if chosen_move.type in attacker.types:
            stab_bonus = 1.5

        damage_pre_random = damage_base * final_type_multiplier * stab_bonus
        damage_pre_random = math.floor(damage_pre_random)

        random_factor = random.randint(85, 100) / 100.0

        crit_chance = 6
        if hasattr(chosen_move, "mechanics"):
            if "crit_rate_bonus" in chosen_move.mechanics:
                crit_chance = 12

        crit_multiplier = 1.0
        if random.randint(1, 100) <= crit_chance:
            crit_multiplier = 1.5

        final_calculated_damage = damage_pre_random * random_factor * crit_multiplier * hits

        if final_type_multiplier == 0:
            return 0

        return max(1, int(final_calculated_damage))


    def end_of_turn_resolution(self):
        for pkmn in [self.player_pkmn, self.trainer_pkmn]:
            if not pkmn.is_alive():
                continue


            if pkmn.status == "burn":
                damage = pkmn.max_hp // 16
                pkmn.take_damage(damage)

            elif pkmn.status == "poison":
                damage = pkmn.max_hp // 8
                pkmn.take_damage(damage)

        self.check_battle_status()
