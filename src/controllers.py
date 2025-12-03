import random
import math
import logging

from src.classes import Item, Move
from src.database import TYPES_DB

logger = logging.getLogger(__name__)

class BattleController:
    def __init__(self, battle_scene, enemy, player):
        self.player = player
        self.enemy = enemy
        self.battle_scene = battle_scene
        self.types_damage = TYPES_DB
        self.cancel_action = -1

        self.player_action_type = None
        self.player_chosen_move = None
        self.player_chosen_item = None
        self.enemy_chosen_move = None
        self.switch_target_index = None

        self.enemy_action_type = "attack"
        self.enemy_chosen_item = None

        self.weather_condition = None
        self.weather_turns = 0

        self.state = "START"
        logger.info(f"Controlador de Batalha iniciado: {self.player.name} vs {self.enemy.name}")


    def run_battle_loop(self):
        self.state = "PLAYER_TURN"
        self.player_pokemon_index = 0
        self.enemy_pokemon_index = 0

        self.player_pokemon = self.player.team[self.player_pokemon_index]
        self.enemy_pokemon = self.enemy.team[self.enemy_pokemon_index]

        logger.info("Iniciando loop de batalha...")

        while self.state != "EXIT":
            self.player_pokemon = self.player.team[self.player_pokemon_index]
            self.enemy_pokemon = self.enemy.team[self.enemy_pokemon_index]

            logger.info("-" * 30)
            logger.info(f"BATTLE STATUS: {self.player_pokemon.name} (HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}) vs {self.enemy_pokemon.name} (HP: {self.enemy_pokemon.current_hp}/{self.enemy_pokemon.max_hp})")

            input_states = ["PLAYER_TURN", "SELECT_MOVE", "POKEMON_MENU", "BAG_MENU", "FORCE_SWITCH"]

            logger.debug(f"Estado Atual: {self.state}")

            if self.state in input_states:
                self.handle_state_logic()
            else:
                self.process_battle_state()


    def handle_state_logic(self):
        if self.state == "PLAYER_TURN":
            if not self.is_team_alive(self.player):
                logger.warning("O time do jogador foi derrotado. Mudando estado para DEFEAT.")
                self.state = "DEFEAT"
                return

            logger.debug("Aguardando input do jogador (chose_action)...")
            action = self.battle_scene.chose_action()
            logger.debug(f"Ação escolhida pelo jogador: {action}")

            match action:
                case "attack":
                    self.state = "SELECT_MOVE"
                case "bag":
                    self.state = "BAG_MENU"
                case "pokemon":
                    self.state = "POKEMON_MENU"
                case "run":
                    logger.info("Jogador tentou fugir da batalha.")
                    self.player_action_type = "run"
                    self.state = "RESOLVE_TURN"
                case _:
                    pass

        elif self.state == "SELECT_MOVE":
            attack_index = self.battle_scene.chose_attack()
            if attack_index == self.cancel_action:
                self.state = "PLAYER_TURN"
                return

            self.player_chosen_move = self.player_pokemon.moves[attack_index]
            self.player_action_type = "attack"
            logger.info(f"Jogador selecionou o ataque: {self.player_chosen_move.name}")

            self.decide_enemy_move()
            self.state = "RESOLVE_TURN"

        elif self.state == "POKEMON_MENU":
            selected_index = self.battle_scene.chose_pokemon()

            if selected_index == self.cancel_action:
                self.state = "PLAYER_TURN"
                return

            if 0 <= selected_index < len(self.player.team) and self.player.team[selected_index].is_alive() and selected_index != self.player_pokemon_index:
                self.switch_target_index = selected_index
                self.player_action_type = "switch"
                logger.info(f"Jogador escolheu trocar para: {self.player.team[selected_index].name}")

                self.decide_enemy_move()
                self.state = "RESOLVE_TURN"
            else:
                logger.warning("Seleção de troca inválida (Pokémon desmaiado ou já ativo).")
                self.state = "PLAYER_TURN"

        elif self.state == "BAG_MENU":
            if self.player.bag.get("Potion", 0) > 0 and self.player_pokemon.current_hp < self.player_pokemon.max_hp:
                logger.info("Jogador decidiu usar uma Poção.")
                self.player_chosen_item = Item("Potion")

                if self.player_chosen_item.use(self.player_pokemon):
                    self.player.use_item("Potion")
                    logger.info(f"Jogador usou Potion em {self.player_pokemon.name}!")

                    self.player_action_type = "bag"
                    self.decide_enemy_move()
                    self.state = "RESOLVE_TURN"
                else:
                    logger.warning("Falha ao usar a Poção.")
                    self.state = "PLAYER_TURN"
            else:
                logger.info("Jogador não tem 'Potion' ou o Pokémon está com HP cheio. Retornando.")
                self.state = "PLAYER_TURN"

        elif self.state == "FORCE_SWITCH":
            logger.info("Jogador precisa escolher um novo Pokémon (Force Switch).")
            selected_index = self.battle_scene.chose_pokemon()

            if selected_index == self.cancel_action:
                return

            if 0 <= selected_index < len(self.player.team):
                if self.player.team[selected_index].is_alive():
                    self.player_pokemon_index = selected_index
                    self.player_pokemon = self.player.team[self.player_pokemon_index]
                    logger.info(f"Novo Pokémon ativo: {self.player_pokemon.name}")
                    self.state = "PLAYER_TURN"
                else:
                    logger.warning("Não pode trocar para um Pokémon desmaiado.")
            else:
                pass


    def decide_enemy_move(self):
        hp_percent = self.enemy_pokemon.current_hp / self.enemy_pokemon.max_hp
        logger.debug(f"[IA] HP Inimigo: {hp_percent:.2%}")

        if hp_percent < 0.30:
            healing_items = ["Full Restore", "Hyper Potion", "Super Potion", "Potion"]

            for item_name in healing_items:
                if self.enemy.bag.get(item_name, 0) > 0:
                    self.enemy_action_type = "bag"
                    self.enemy_chosen_item = Item(item_name)
                    logger.info(f"[IA] Decisão: Usar item {item_name}")
                    return

        self.enemy_action_type = "attack"

        valid_moves = [m for m in self.enemy_pokemon.moves if m.current_pp > 0]
        if not valid_moves:
            self.enemy_chosen_move = Move("Struggle")
            logger.info("[IA] Sem PP. Usando Struggle.")
            return

        best_move = None
        best_damage = -1

        logger.debug(f"[IA] Calculando melhor movimento entre: {[m.name for m in valid_moves]}")

        for move in valid_moves:
            damage, hits_count = self.calculate_damage(self.enemy_pokemon, self.player_pokemon, move)
            logger.debug(f"[IA] Simulação: {move.name} causaria aprox. {damage} de dano.")

            if damage > best_damage:
                best_damage = damage
                best_move = move

        self.enemy_chosen_move = best_move
        logger.info(f"[IA] Ataque escolhido: {self.enemy_chosen_move.name} (Dano Previsto: {best_damage})")


    def process_battle_state(self):
        if self.state == "RESOLVE_TURN":
            logger.info("--- Resolução do Turno ---")

            if self.player_action_type == "run":
                self.battle_scene.run()
                logger.info("Batalha encerrada por fuga.")
                self.state = "EXIT"
                return

            elif self.player_action_type == "switch":
                self.player_pokemon_index = self.switch_target_index
                self.player_pokemon = self.player.team[self.player_pokemon_index]
                logger.info(f"Troca realizada. Vai! {self.player_pokemon.name}!")

                if self.check_battle_status():
                     self.perform_attack(self.enemy_pokemon, self.player_pokemon, self.enemy_chosen_move)

            if getattr(self, "enemy_action_type", "attack") == "bag":
                item = self.enemy_chosen_item
                logger.info(f"O Inimigo usou {item.name}!")
                if item.use(self.enemy_pokemon):
                    self.enemy.use_item(item.name)

            elif self.player_action_type == "bag":
                if self.check_battle_status():
                     self.perform_attack(self.enemy_pokemon, self.player_pokemon, self.enemy_chosen_move)

            elif self.player_action_type == "attack":
                player_speed = self.player_pokemon.get_current_stat("speed")
                enemy_speed = self.enemy_pokemon.get_current_stat("speed")

                player_priority = self.player_chosen_move.priority
                enemy_priority = self.enemy_chosen_move.priority

                logger.debug(f"Speed Check -> Player: {player_speed} | Enemy: {enemy_speed}")
                logger.debug(f"Priority Check -> Player: {player_priority} | Enemy: {enemy_priority}")

                first = None
                second = None
                player_goes_first = False

                if player_priority > enemy_priority:
                    player_goes_first = True
                elif enemy_priority > player_priority:
                    player_goes_first = False
                else:
                    if player_speed > enemy_speed:
                        player_goes_first = True
                    elif enemy_speed > player_speed:
                        player_goes_first = False
                    else:
                        player_goes_first = random.choice([True, False])
                        logger.debug(f"Speed Tie! Sorteio aleatório: {player_goes_first}")

                if player_goes_first:
                    first = (self.player_pokemon, self.enemy_pokemon, self.player_chosen_move)
                    second = (self.enemy_pokemon, self.player_pokemon, self.enemy_chosen_move)
                else:
                    first = (self.enemy_pokemon, self.player_pokemon, self.enemy_chosen_move)
                    second = (self.player_pokemon, self.enemy_pokemon, self.player_chosen_move)

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
            logger.info("VITÓRIA! O treinador inimigo foi derrotado.")
            self.state = "EXIT"

        elif self.state == "DEFEAT":
            logger.info("DERROTA... Você não tem mais Pokémons.")
            self.state = "EXIT"


    def perform_attack(self, attacker, defender, move):
        logger.info(f"> {attacker.name} usou {move.name}!")

        if attacker.status == "sleep":
            if random.randint(1, 100) >= 50:
                attacker.status = None
                logger.info(f"{attacker.name} acordou!")
            else:
                logger.info(f"{attacker.name} está dormindo e não atacou.")
                return False

        elif attacker.status == "freeze":
            if random.randint(1, 100) <= 25:
                attacker.status = None
                logger.info(f"{attacker.name} descongelou!")
            else:
                logger.info(f"{attacker.name} está congelado e não atacou.")
                return False

        elif attacker.status == "paralysis":
            if random.randint(1, 100) <= 30:
                logger.info(f"{attacker.name} está paralisado e não consegue se mover!")
                return False

        if not attacker.attack(move):
            logger.warning(f"{move.name} falhou por falta de PP!")
            return

        always_hit = False
        if move.effect and move.effect.get("type") == "always_hit":
            always_hit = True

        hit_chance = 0
        if not always_hit:
            hit_chance = random.randint(1, 100)

            accuracy_stage = attacker.stat_mods.get("accuracy", 0)
            evasion_stage = defender.stat_mods.get("evasion", 0)
            accuracy_modifier = accuracy_stage - evasion_stage

            multipliers = { -6: 0.33, -5: 0.37, -4: 0.43, -3: 0.50, -2: 0.60, -1: 0.75,
                             0: 1.0, 1: 1.33, 2: 1.66, 3: 2.0, 4: 2.33, 5: 2.66, 6: 3.0 }

            if accuracy_modifier < -6: accuracy_modifier = -6
            if accuracy_modifier > 6: accuracy_modifier = 6

            accuracy_multiplier = multipliers.get(accuracy_modifier, 1.0)
            final_accuracy = move.accuracy * accuracy_multiplier

            logger.debug(f"Accuracy Check: Chance={hit_chance}, MoveAcc={move.accuracy}, Mod={accuracy_multiplier}, Final={final_accuracy}")

            if hit_chance > final_accuracy:
                logger.info(f"O ataque de {attacker.name} errou!")
                return

        damage, hits_count = self.calculate_damage(attacker, defender, move)

        if damage > 0:
            defender.take_damage(damage)
            logger.info(f"Causou {damage} de dano em {defender.name}!")

            if hits_count > 1:
                logger.info(f"Atingiu {hits_count} vezes!")

        if hasattr(move, "mechanics") and move.mechanics:
            if "drain_percent" in move.mechanics:
                percent = move.mechanics["drain_percent"] / 100.0
                change_amount = int(damage * percent)

                if change_amount > 0:
                    attacker.restore_hp(change_amount)
                    logger.info(f"{attacker.name} recuperou {change_amount} de HP!")

                elif change_amount < 0:
                    recoil_damage = abs(change_amount)
                    attacker.take_damage(recoil_damage)
                    logger.info(f"{attacker.name} sofreu {recoil_damage} de recuo!")

        if move.effect:
            self.process_move_effect(move, attacker, defender)


    def process_move_effect(self, move, attacker, defender):
        effect_data = move.effect

        chance = effect_data.get("chance", 100)
        roll = random.randint(1, 100)

        if roll > chance:
            logger.debug(f"Efeito secundário não ativado (Roll: {roll} > Chance: {chance})")
            return

        target_str = effect_data.get("target")
        target_pokemon = None

        if target_str == "enemy":
            target_pokemon = defender
        elif target_str == "self":
            target_pokemon = attacker
        else:
            return

        effect_type = effect_data.get("type")

        if effect_type == "stat_change":
            stat_name = effect_data.get("stat")
            amount = effect_data.get("amount")

            if target_pokemon.apply_stat_change(stat_name, amount):
                logger.info(f"{target_pokemon.name} teve seu {stat_name} alterado em {amount}!")
            else:
                logger.info(f"O status de {target_pokemon.name} não pode ir mais longe!")

        elif effect_type == "status_condition":
            condition = effect_data.get("condition")

            if target_pokemon.status is None:
                target_pokemon.status = condition
                logger.info(f"{target_pokemon.name} agora está {condition}!")
            else:
                logger.info(f"{target_pokemon.name} já tem um problema de status!")

        elif effect_type == "weather":
            condition = effect_data.get("condition")
            turns = effect_data.get("turns", 5)
            logger.info(f"O clima mudou para {condition}!")
            self.weather_condition = condition
            self.weather_turns = turns


    def check_battle_status(self):
        if not self.is_team_alive(self.player):
            logger.info("Time do jogador completamente derrotado.")
            self.state = "DEFEAT"
            return False

        if not self.is_team_alive(self.enemy):
            logger.info("Time do inimigo completamente derrotado.")
            self.state = "VICTORY"
            return False

        if not self.player_pokemon.is_alive():
            logger.info(f"{self.player_pokemon.name} desmaiou!")
            self.state = "FORCE_SWITCH"
            return False

        if not self.enemy_pokemon.is_alive():
            logger.info(f"{self.enemy_pokemon.name} inimigo desmaiou!")
            xp_gained = self.calculate_battle_xp()
            logger.info(f"Ganhou {xp_gained} de experiência!")
            if self.swap_enemy_pokemon():
                logger.info(f"Inimigo enviou {self.enemy_pokemon.name}!")
            return False

        return True


    def swap_enemy_pokemon(self):
        for i, pokemon in enumerate(self.enemy.team):
            if pokemon.is_alive():
                self.enemy_pokemon_index = i
                self.enemy_pokemon = pokemon
                return True
        return False


    def is_team_alive(self, trainer):
        for pokemon in trainer.team:
            if pokemon.current_hp > 0:
                return True
        return False


    def calculate_damage(self, attacker, defender, chosen_move):

        hits_count = 1
        if hasattr(chosen_move, "mechanics") and chosen_move.mechanics:
            if "multi_hit" in chosen_move.mechanics:
                min_hits = chosen_move.mechanics["multi_hit"]["min"]
                max_hits = chosen_move.mechanics["multi_hit"]["max"]
                hits_count = random.randint(min_hits, max_hits)

        # Determina Stats de Ataque e Defesa
        if chosen_move.category == "Special":
            attack_stat = attacker.get_current_stat("special-attack")
            defense_stat = defender.get_current_stat("special-defense")
        else:
            attack_stat = attacker.get_current_stat("attack")
            defense_stat = defender.get_current_stat("defense")

        # Fórmula Básica
        level_factor = ((2 * attacker.level // 5) + 2)
        raw_damage_part = level_factor * (chosen_move.power * attack_stat // defense_stat)
        damage_base = (raw_damage_part // 50) + 2

        # Multiplicadores de Tipo
        type_rules = self.types_damage.get(chosen_move.type, {})
        primary_type = defender.types[0]
        type_effectiveness_primary = type_rules.get(primary_type, 1.0)

        type_effectiveness_secondary = 1.0
        if len(defender.types) > 1:
            secondary_type = defender.types[1]
            type_effectiveness_secondary = type_rules.get(secondary_type, 1.0)

        final_type_multiplier = type_effectiveness_primary * type_effectiveness_secondary

        # STAB
        stab_bonus = 1.0
        if chosen_move.type in attacker.types:
            stab_bonus = 1.5

        damage_pre_random = damage_base * final_type_multiplier * stab_bonus
        damage_pre_random = math.floor(damage_pre_random)

        # Aleatoriedade e Crítico
        random_factor = random.randint(85, 100) / 100.0

        crit_chance = 6
        if hasattr(chosen_move, "mechanics") and chosen_move.mechanics:
            if "crit_rate_bonus" in chosen_move.mechanics:
                crit_chance = 12

        crit_multiplier = 1.0
        is_crit = False
        if random.randint(1, 100) <= crit_chance:
            crit_multiplier = 1.5
            is_crit = True

        weather_mod = 1.0
        if self.weather_condition == "rain":
            if chosen_move.type == "Water": weather_mod = 1.5
            elif chosen_move.type == "Fire": weather_mod = 0.5
        elif self.weather_condition == "sun":
            if chosen_move.type == "Fire": weather_mod = 1.5
            elif chosen_move.type == "Water": weather_mod = 0.5

        final_calculated_damage = damage_pre_random * random_factor * crit_multiplier * hits_count * weather_mod
        final_int_damage = max(1, int(final_calculated_damage))

        if final_type_multiplier == 0:
            final_int_damage = 0

        if final_type_multiplier > 1.0:
            logger.info("É super efetivo!")
        elif final_type_multiplier < 1.0 and final_type_multiplier > 0:
            logger.info("Não é muito efetivo...")
        elif final_type_multiplier == 0:
            logger.info("Não afetou o alvo...")

        if is_crit:
            logger.info("Um acerto crítico!")

        return final_int_damage, hits_count


    def end_of_turn_resolution(self):
        logger.debug("Resolvendo efeitos de fim de turno...")
        for pokemon in [self.player_pokemon, self.enemy_pokemon]:
            if not pokemon.is_alive():
                continue

            if pokemon.status == "burn":
                damage = pokemon.max_hp // 16
                pokemon.take_damage(damage)
                logger.info(f"{pokemon.name} sofreu dano pela queimadura.")

            elif pokemon.status == "poison":
                damage = pokemon.max_hp // 8
                pokemon.take_damage(damage)
                logger.info(f"{pokemon.name} sofreu dano pelo veneno.")

        self.check_battle_status()

    def calculate_battle_xp(self):
        base_xp = self.enemy_pokemon.base_experience
        enemy_level = self.enemy_pokemon.level
        raw_xp = (base_xp * enemy_level) / 7
        xp_amount = int(raw_xp)
        self.player_pokemon.gain_xp(xp_amount)
        return xp_amount
