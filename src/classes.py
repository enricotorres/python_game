import logging
from src.database import MOVES_DB, POKEDEX_DB, ITEMS_DB

logger = logging.getLogger(__name__)

class Pokemon:
    def __init__(self, name, level, moves=None):
        if name not in POKEDEX_DB:
            logger.error(f"Erro Crítico: Pokémon '{name}' não encontrado no DB.")
            raise ValueError(f"Pokémon '{name}' não encontrado no Pokedex JSON.")

        data = POKEDEX_DB[name]

        self.status = None
        self.is_caught = False
        self.name = name
        self.id = data["id"]
        self.level = level
        self.xp = 0
        self.types = data["types"]
        self.sprite = data.get("sprite")
        self.base_experience = data["base_experience"]

        base_stats = data["stats"]

        self.max_hp = int(((base_stats["hp"] * 2 * level) / 100) + level + 10)
        self.current_hp = self.max_hp

        self.atk = int(((base_stats["attack"] * 2 * level) / 100) + 5)
        self.defense = int(((base_stats["defense"] * 2 * level) / 100) + 5)
        self.sp_atk = int(((base_stats["special_attack"] * 2 * level) / 100) + 5)
        self.sp_def = int(((base_stats["special_defense"] * 2 * level) / 100) + 5)
        self.speed = int(((base_stats["speed"] * 2 * level) / 100) + 5)

        self.stat_mods = {
                "attack": 0,
                "defense": 0,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 0,
                "accuracy": 0,
                "evasion": 0
                }

        self.moves = []
        if moves is not None and len(moves) > 0:
            self.learn_moves_manually(moves)
        else:
            self.learn_moves_by_level(data["moves"])

        logger.debug(f"Pokémon criado: {self.name} (Lv.{self.level}) HP:{self.max_hp}")

    def learn_moves_manually(self, moves_list_names):
            chosen_moves = moves_list_names[:4]

            for move_name in chosen_moves:
                try:
                    new_move = Move(move_name)
                    self.moves.append(new_move)
                except Exception as e:
                    logger.error(f"Erro ao ensinar movimento manual '{move_name}': {e}")

    def learn_moves_by_level(self, moves_list_from_json):
        available_moves = [m for m in moves_list_from_json if m["level"] <= self.level]
        available_moves.sort(key=lambda x: x["level"])
        recent_moves = available_moves[-4:]

        for m_data in recent_moves:
            try:
                new_move = Move(m_data["name"])
                self.moves.append(new_move)
            except Exception as e:
                logger.error(f"Erro ao ensinar {m_data['name']} para {self.name}: {e}")

    def show_status(self):
        type_str = "/".join(self.types)
        return {
                "id": self.id,
                "name": self.name,
                "hp_percent": self.current_hp / self.max_hp,
                "current_hp": self.current_hp,
                "max_hp": self.max_hp,
                "types": type_str
            }

    def attack(self, move):
        if move.use():
            return True
        logger.debug(f"{self.name} tentou usar {move.name} mas falhou (sem PP).")
        return False

    def take_damage(self, amount):
        old_hp = self.current_hp
        self.current_hp -= int(amount)
        if self.current_hp < 0:
            self.current_hp = 0

        logger.debug(f"{self.name} tomou {amount} dano. HP: {old_hp} -> {self.current_hp}")
        return self.current_hp

    def restore_hp(self, amount):
        old_hp = self.current_hp
        self.current_hp += int(amount)
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        logger.debug(f"{self.name} curou {amount} ponto de vida. HP: {old_hp} -> {self.current_hp}")
        return self.current_hp

    def is_alive(self):
            return self.current_hp > 0


    def get_current_stat(self, stat_name):
        base_value = 0
        if stat_name == "attack": base_value = self.atk
        elif stat_name == "defense": base_value = self.defense
        elif stat_name == "special-attack": base_value = self.sp_atk
        elif stat_name == "special-defense": base_value = self.sp_def
        elif stat_name == "speed": base_value = self.speed

        stage = self.stat_mods.get(stat_name, 0)
        multiplier = 1.0

        if stage >= 0:
            multiplier = (2 + stage) / 2
        else:
            multiplier = 2 / (2 + abs(stage))

        final_value = int(base_value * multiplier)

        if stat_name == "speed" and self.status == "paralysis":
            final_value = int(final_value * 0.5)
        if stat_name == "attack" and self.status == "burn":
            final_value = int(final_value * 0.5)

        return final_value

    def apply_stat_change(self, stat_name, amount):
        if stat_name not in self.stat_mods:
            return False

        old_stage = self.stat_mods[stat_name]
        self.stat_mods[stat_name] += amount

        if self.stat_mods[stat_name] > 6: self.stat_mods[stat_name] = 6
        if self.stat_mods[stat_name] < -6: self.stat_mods[stat_name] = -6

        if old_stage != self.stat_mods[stat_name]:
            logger.debug(f"{self.name} stat {stat_name}: {old_stage} -> {self.stat_mods[stat_name]}")
            return True
        else:
            logger.debug(f"{self.name} stat {stat_name} já atingiu o limite ({self.stat_mods[stat_name]}).")
            return False

    def calculate_required_xp(self):
        next_level = self.level + 1
        if next_level <= 1:
            return 0
        return next_level ** 3

    def gain_xp(self, xp_amount):
        if self.level == 100:
            return

        self.current_xp += xp_amount
        logger.info(f"{self.name} ganhou {xp_amount} XP!")

        while self.level < 100:
            xp_for_next_level = self.calculate_required_xp()

            if self.xp <= xp_for_next_level:
                self.level += 1
                logger.info(f"Parabéns! {self.name} subiu para o Nível {self.level}!")
                self.recalculate_stats()
                if self.can_evolve_at_level(self.level):
                    self.evolve()
            else:
                break


    def __repr__(self):
        return f"<{self.name} Lv.{self.level} | HP:{self.current_hp}>"


class Trainer:
    def __init__(self, name, xp=0, money=0, initial_team=None):
        self.name = name
        self.xp = xp
        self.money = money
        self.bag = {}
        self.active_slot = 0

        if initial_team is None:
            self.team = []
        else:
            self.team = initial_team

    def add_pokemon(self, pokemon):
        if len(self.team) < 6:
            self.team.append(pokemon)
            logger.info(f"{pokemon.name} adicionado ao time de {self.name}.")
            return True
        else:
            logger.warning(f"Time de {self.name} está cheio! Não foi possível adicionar {pokemon.name}.")
            return False

    def get_active_pokemon(self):
        if 0 <= self.active_slot < len(self.team):
            return self.team[self.active_slot]
        return None

    def add_item(self, item_name, quantity=1):
        if item_name in self.bag:
            self.bag[item_name] += quantity
        else:
            self.bag[item_name] = quantity
        logger.debug(f"Item adicionado: {item_name} (x{quantity})")

    def use_item(self, item_name):
        if self.bag.get(item_name, 0) > 0:
            self.bag[item_name] -= 1
            if self.bag[item_name] == 0:
                del self.bag[item_name]
            return True
        return False


class Move:
    def __init__(self, name):
        if name not in MOVES_DB:
            logger.error(f"Erro: O ataque '{name}' não existe no moves.json!")
            raise ValueError(f"O ataque '{name}' não existe no moves.json!")

        data = MOVES_DB[name]

        self.name = name
        self.type = data["type"]
        self.category = data["category"]
        self.power = data["power"]
        self.accuracy = data["accuracy"]
        self.max_pp = data["pp"]
        self.current_pp = data["pp"]
        self.effect = data.get("effect")
        self.priority = data.get("priority", 0)
        self.mechanics = data.get("mechanics")

    def use(self):
        if self.current_pp > 0:
            self.current_pp -= 1
            return True
        else:
            return False

    def restore_pp(self):
        self.current_pp = self.max_pp

    def __repr__(self):
        return f"<{self.name} ({self.type}) Power:{self.power} PP:{self.current_pp}/{self.max_pp}>"


class Item:
    def __init__(self, name):
        if name not in ITEMS_DB:
            logger.error(f"Erro: Item '{name}' não encontrado no DB.")
            raise ValueError(f"Item '{name}' não encontrado no JSON.")

        data = ITEMS_DB[name]

        self.id = data["id"]
        self.name = data["name"]
        self.category = data["category"]
        self.price = data["price"]
        self.description = data["description"]
        self.effect = data["effect"]

    def use(self, target_pokemon):
        effect_type = self.effect.get("type")
        logger.debug(f"Item {self.name} sendo usado em {target_pokemon.name}...")

        if effect_type == "heal_hp":
            if target_pokemon.current_hp >= target_pokemon.max_hp:
                logger.debug(f"Falha: {target_pokemon.name} já está com HP cheio.")
                return False

            amount = self.effect.get("amount", 0)
            target_pokemon.restore_hp(amount)

            logger.debug(f"Sucesso: Curou HP para {target_pokemon.current_hp}.")
            return True

        elif effect_type == "revive":
            if target_pokemon.is_alive():
                logger.debug(f"Falha: {target_pokemon.name} não está desmaiado.")
                return False

            percent = self.effect.get("amount_percent", 0.5)
            target_pokemon.current_hp = int(target_pokemon.max_hp * percent)
            logger.debug(f"Sucesso: Reviveu com {target_pokemon.current_hp} HP.")
            return True

        elif effect_type == "cure_status":
            condition_to_cure = self.effect.get("condition")

            if target_pokemon.status is None:
                logger.debug(f"Falha: {target_pokemon.name} não tem problemas de status.")
                return False

            if condition_to_cure == "all":
                logger.debug(f"Sucesso: Curou status '{target_pokemon.status}'.")
                target_pokemon.status = None
                return True

            if target_pokemon.status == condition_to_cure:
                logger.debug(f"Sucesso: Curou status '{target_pokemon.status}'.")
                target_pokemon.status = None
                return True

            logger.debug(f"Falha: Item cura '{condition_to_cure}', mas alvo tem '{target_pokemon.status}'.")
            return False

        elif effect_type == "heal_hp_status":
            if target_pokemon.current_hp >= target_pokemon.max_hp and target_pokemon.status is None:
                logger.debug(f"Falha: {target_pokemon.name} já está com saúde perfeita.")
                return False

            target_pokemon.status = None
            target_pokemon.current_hp = target_pokemon.max_hp
            logger.debug(f"Sucesso: {self.name} restaurou HP e Status.")
            return True

        logger.warning(f"Tipo de efeito desconhecido no item: {effect_type}")
        return False

    def __repr__(self):
        return f"<Item: {self.name}>"
