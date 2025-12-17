import math
import random
import logging

from src import Item, Move, Pokemon, Trainer

logger = logging.getLogger(__name__)

class DamageCalculator:
    def __init__(self, type_chart: dict) -> None:
        self.type_chart: dict = type_chart

    def calculate(self, attacker: Pokemon, defender: Pokemon, chosen_move: Move, weather_condition: str | None = None) -> tuple[int, int]:
        if chosen_move.category == "Status":
            return 0, 0

        # Obter dados iniciais
        hits_count: int = self._calculate_hits(chosen_move)
        atk_stat, def_stat = self._get_attack_defense_stats(attacker, defender, chosen_move)

        # Base e Multiplicadores
        damage_base: int = self._calculate_base_damage(attacker.level, chosen_move.power, atk_stat, def_stat)
        type_mult: float = self._get_type_effectiveness(chosen_move.type, defender.types)
        stab_bonus: float = 1.5 if chosen_move.type in attacker.types else 1.0

        # Fatores Aleatórios e Ambientais
        random_mult: float = random.randint(85, 100) / 100.0
        crit_mult, is_crit = self._calculate_critical(chosen_move)
        weather_mult: float = self._get_weather_modifier(chosen_move.type, weather_condition)

        # Cálculo Final
        damage_pre_random = math.floor(damage_base * type_mult * stab_bonus)
        final_damage: int = int(damage_pre_random * random_mult * crit_mult * hits_count * weather_mult)
        final_damage = max(1, final_damage)

        # Imunidade
        if type_mult == 0:
            final_damage = 0

        self._log_battle_info(type_mult, is_crit)

        return final_damage, hits_count

    def _calculate_hits(self, move: Move) -> int:
        if hasattr(move, "mechanics") and move.mechanics and "multi_hit" in move.mechanics:
            min_hits: int = move.mechanics["multi_hit"]["min"]
            max_hits: int = move.mechanics["multi_hit"]["max"]
            return random.randint(min_hits, max_hits)
        return 1

    def _get_attack_defense_stats(self, attacker: Pokemon, defender: Pokemon, move: Move) -> tuple[int, int]:
        if move.category == "Special":
            return (attacker.get_current_stat("special-attack"),
                    defender.get_current_stat("special-defense"))
        else:
            return (attacker.get_current_stat("attack"),
                    defender.get_current_stat("defense"))

    def _calculate_base_damage(self, level: int, power: int, atk: int, defense: int) -> int:
        level_factor = ((2 * level) // 5) + 2
        raw = level_factor * (power * atk // defense)
        return (raw // 50) + 2

    def _get_type_effectiveness(self, move_type: str, defender_types: list[str]) -> float:
        multiplier: float = 1.0
        type_rules: dict = self.type_chart.get(move_type, {})

        for def_type in defender_types:
            multiplier *= type_rules.get(def_type, 1.0)

        return multiplier

    def _calculate_critical(self, move: Move) -> tuple[float, bool]:
        crit_chance: int = 6
        if hasattr(move, "mechanics") and move.mechanics and "crit_rate_bonus" in move.mechanics:
            crit_chance = 12

        if random.randint(1, 100) <= crit_chance:
            return 1.5, True
        return 1.0, False

    def _get_weather_modifier(self, move_type: str, weather: str | None) -> float:
        if weather == "rain":
            if move_type == "Water": return 1.5
            if move_type == "Fire": return 0.5
        elif weather == "sun":
            if move_type == "Fire": return 1.5
            if move_type == "Water": return 0.5
        return 1.0

    def _log_battle_info(self, type_mult: float, is_crit: bool) -> None:
        if type_mult > 1.0:
            logger.info("É super efetivo!")
        elif 0.0 < type_mult < 1.0:
            logger.info("Não é muito efetivo...")
        elif type_mult == 0.0:
            logger.info("Não afetou o alvo...")

        if is_crit:
            logger.info("Um acerto crítico!")


class MoveEffectResolver:
    def __init__(self, battle_controller) -> None:
        self.controller = battle_controller
        self.handlers: dict = {
            "stat_change": self._handle_stat_change,
            "status_condition": self._handle_status_condition,
            "weather_change": self._handle_weather_change,
        }

    def resolve(self, move: Move, attacker: Pokemon, defender: Pokemon) -> None:
        if not move.effect:
            return

        effect_type: str | None = move.effect.get("type")
        handler = self.handlers.get(effect_type)

        if handler:
            handler(move.effect, attacker, defender)
        else:
            logger.warning(f"Handler não encontrado para o efeito: {effect_type}")

    def _handle_stat_change(self, effect_data: dict, attacker: Pokemon, defender: Pokemon) -> None:
        target = attacker if effect_data.get("target") == "self" else defender
        stat: str | None = effect_data.get("stat")
        stages: int = effect_data.get("stages", 0)

        if stat and stages != 0:
            target.apply_stat_change(stat, stages)
            logger.info(f"{target.name} teve o {stat} alterado em {stages} estágio(s)!")

    def _handle_status_condition(self, effect_data: dict, attacker: Pokemon, defender: Pokemon) -> None:
        target = defender
        status: str | None = effect_data.get("status")
        chance: int = effect_data.get("chance", 100)

        if random.randint(1, 100) <= chance and target.status is None:
            target.status = status
            logger.info(f"{target.name} foi afetado por {status}!")

    def _handle_weather_change(self, effect_data: dict, attacker: Pokemon, defender: Pokemon) -> None:
        weather: str | None = effect_data.get("weather")
        turns: int = effect_data.get("turns", 5)

        self.controller.weather_condition = weather
        self.controller.weather_turns = turns
        logger.info(f"O clima mudou para {weather} por {turns} turnos.")


class BattleAI:
    def __init__(self, damage_calculator: DamageCalculator) -> None:
        self.damage_calculator = damage_calculator

    def choose_action(self, enemy_trainer: Trainer, player_pokemon: Pokemon) -> tuple[str, Move | Item]:
        enemy_pokemon: Pokemon = enemy_trainer.get_active_pokemon()
        hp_percent: float = enemy_pokemon.current_hp / enemy_pokemon.max_hp
        logger.debug(f"[AI] HP Inimigo: {hp_percent:.2%}")

        if hp_percent < 0.30 and enemy_pokemon.current_hp > 0:
            healing_items: list[str] = ["Full Restore", "Hyper Potion", "Super Potion", "Potion"]

            for item_name in healing_items:
                if enemy_trainer.has_item(item_name) and enemy_pokemon.current_hp < enemy_pokemon.max_hp:
                    logger.info(f"[AI] Decisão: Usar item {item_name}")
                    return "bag", Item(item_name)

        valid_moves: list[Move] = [m for m in enemy_pokemon.moves if m.current_pp > 0]

        if not valid_moves:
            logger.info("[AI] Sem PP. Usando Struggle.")
            return "attack", Move("Struggle")

        best_move: Move | None = None
        best_damage: int = -1

        logger.debug(f"[AI] Calculando melhor movimento entre: {[m.name for m in valid_moves]}")

        for move in valid_moves:
            damage, hits_count = self.damage_calculator.calculate(enemy_pokemon, player_pokemon, move)

            if damage > best_damage:
                best_damage = damage
                best_move = move

        logger.info(f"[AI] Ataque escolhido: {best_move.name} (Dano Previsto: {best_damage})")
        return "attack", best_move


class AccuracyCalculator:
    def check_hit(self, move: Move, attacker: Pokemon, defender: Pokemon) -> bool:
        if move.effect and move.effect.get("type") == "always_hit":
            return True

        hit_chance: int = random.randint(1, 100)

        accuracy_stage: int = attacker.stat_mods.get("accuracy", 0)
        evasion_stage: int = defender.stat_mods.get("evasion", 0)

        accuracy_modifier: int = accuracy_stage - evasion_stage
        accuracy_modifier = max(-6, min(6, accuracy_modifier))

        multipliers: dict[int, float] = {
            -6: 0.33, -5: 0.37, -4: 0.43, -3: 0.50, -2: 0.60, -1: 0.75,
             0: 1.0,
             1: 1.33, 2: 1.66, 3: 2.0, 4: 2.33, 5: 2.66, 6: 3.0
        }

        accuracy_multiplier: float = multipliers.get(accuracy_modifier, 1.0)
        final_accuracy: float = move.accuracy * accuracy_multiplier

        return hit_chance <= final_accuracy
