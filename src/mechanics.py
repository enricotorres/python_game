import math
import random
import logging

logger = logging.getLogger(__name__)

class DamageCalculator:
    def __init__(self, type_chart: dict):
        self.type_chart = type_chart

    def calculate(self, attacker, defender, chosen_move, weather_condition=None):
        # 1. Obter dados iniciais
        hits_count = self._calculate_hits(chosen_move)
        atk_stat, def_stat = self._get_attack_defense_stats(attacker, defender, chosen_move)

        # 2. Base e Multiplicadores
        damage_base = self._calculate_base_damage(attacker.level, chosen_move.power, atk_stat, def_stat)
        type_mult = self._get_type_effectiveness(chosen_move.type, defender.types)
        stab_bonus = 1.5 if chosen_move.type in attacker.types else 1.0

        # 3. Fatores Aleatórios e Ambientais
        random_mult = random.randint(85, 100) / 100.0
        crit_mult, is_crit = self._calculate_critical(chosen_move)
        weather_mult = self._get_weather_modifier(chosen_move.type, weather_condition)

        # 4. Cálculo Final
        damage_pre_random = math.floor(damage_base * type_mult * stab_bonus)
        final_damage = int(damage_pre_random * random_mult * crit_mult * hits_count * weather_mult)
        final_damage = max(1, final_damage)

        # Imunidade
        if type_mult == 0:
            final_damage = 0

        self._log_battle_info(type_mult, is_crit)

        return final_damage, hits_count


    def _calculate_hits(self, move) -> int:
        if hasattr(move, "mechanics") and move.mechanics and "multi_hit" in move.mechanics:
            min_hits = move.mechanics["multi_hit"]["min"]
            max_hits = move.mechanics["multi_hit"]["max"]
            return random.randint(min_hits, max_hits)
        return 1

    def _get_attack_defense_stats(self, attacker, defender, move):
        if move.category == "Special":
            return (attacker.get_current_stat("special-attack"),
                    defender.get_current_stat("special-defense"))
        else:
            return (attacker.get_current_stat("attack"),
                    defender.get_current_stat("defense"))

    def _calculate_base_damage(self, level, power, atk, defense):
        level_factor = ((2 * level) // 5) + 2
        raw = level_factor * (power * atk // defense)
        return (raw // 50) + 2

    def _get_type_effectiveness(self, move_type, defender_types) -> float:
        multiplier = 1.0
        type_rules = self.type_chart.get(move_type, {})

        for def_type in defender_types:
            multiplier *= type_rules.get(def_type, 1.0)

        return multiplier

    def _calculate_critical(self, move) -> tuple[float, bool]:
        crit_chance = 6
        if hasattr(move, "mechanics") and move.mechanics and "crit_rate_bonus" in move.mechanics:
            crit_chance = 12

        if random.randint(1, 100) <= crit_chance:
            return 1.5, True
        return 1.0, False

    def _get_weather_modifier(self, move_type, weather) -> float:
        if weather == "rain":
            if move_type == "Water": return 1.5
            if move_type == "Fire": return 0.5
        elif weather == "sun":
            if move_type == "Fire": return 1.5
            if move_type == "Water": return 0.5
        return 1.0

    def _log_battle_info(self, type_mult, is_crit):
        if type_mult > 1.0:
            logger.info("É super efetivo!")
        elif 0.0 < type_mult < 1.0:
            logger.info("Não é muito efetivo...")
        elif type_mult == 0.0:
            logger.info("Não afetou o alvo...")

        if is_crit:
            logger.info("Um acerto crítico!")
