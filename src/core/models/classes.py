
import logging
import random
from src.core.database import MOVES_DB, POKEDEX_DB, ITEMS_DB

logger = logging.getLogger(__name__)


class Pokemon:
    def __init__(self, name: str, level: int, moves: list[str] = None):
        if name not in POKEDEX_DB:
            logger.error(f"Erro Crítico: Pokémon '{name}' não encontrado no DB.")
            raise ValueError(f"Pokémon '{name}' não encontrado no Pokedex JSON.")

        data = POKEDEX_DB[name]

        self.name: str = name
        self.id: int = data["id"]
        self.types: list[str] = data["types"]
        self.sprite: str = data.get("sprite", "")

        self.level: int = level
        self.xp: int = 0
        self.base_experience: int = data["base_experience"]
        self.evolution: dict = data.get("evolution")

        self.ivs: dict[str, int] = {
            "hp": random.randint(0, 31),
            "attack": random.randint(0, 31),
            "defense": random.randint(0, 31),
            "special-attack": random.randint(0, 31),
            "special-defense": random.randint(0, 31),
            "speed": random.randint(0, 31)
        }

        self.status: str = None
        self.volatile_status: dict[str, int] = {}

        self.stat_mods: dict[str, int] = {
            "attack": 0, "defense": 0, "special-attack": 0,
            "special-defense": 0, "speed": 0, "accuracy": 0, "evasion": 0
        }

        self.recalculate_stats()
        self.current_hp: int = self.max_hp

        self.moves: list = []
        if moves and len(moves) > 0:
            self.learn_moves_manually(moves)
        else:
            self.learn_moves_by_level(data["moves"])

        logger.debug(f"Pokémon criado: {self.name} (Lv.{self.level}) HP:{self.max_hp} IV_HP:{self.ivs['hp']}")

    def recalculate_stats(self):
        data = POKEDEX_DB[self.name]
        base = data["stats"]
        lvl = self.level

        self.max_hp = int(((2 * base["hp"] + self.ivs["hp"]) * lvl / 100) + lvl + 10)

        if hasattr(self, 'current_hp') and self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        self.atk = int(((2 * base["attack"] + self.ivs["attack"]) * lvl / 100) + 5)
        self.defense = int(((2 * base["defense"] + self.ivs["defense"]) * lvl / 100) + 5)
        self.sp_atk = int(((2 * base["special_attack"] + self.ivs["special-attack"]) * lvl / 100) + 5)
        self.sp_def = int(((2 * base["special_defense"] + self.ivs["special-defense"]) * lvl / 100) + 5)
        self.speed = int(((2 * base["speed"] + self.ivs["speed"]) * lvl / 100) + 5)

    def learn_moves_manually(self, moves_list_names: list[str]):
        chosen_moves = moves_list_names[:4]
        self.moves = []

        for move_name in chosen_moves:
            try:
                new_move = Move(move_name)
                self.moves.append(new_move)
            except Exception as e:
                logger.error(f"Erro ao ensinar movimento manual '{move_name}': {e}")

    def learn_moves_by_level(self, moves_list_from_json: list[dict]):
        available_moves = [m for m in moves_list_from_json if m["level"] <= self.level]
        available_moves.sort(key=lambda x: x["level"])

        recent_moves = available_moves[-4:]

        for m_data in recent_moves:
            try:
                new_move = Move(m_data["name"])
                self.moves.append(new_move)
            except Exception as e:
                logger.error(f"Erro ao ensinar {m_data['name']} para {self.name}: {e}")

    def gain_xp(self, xp_amount: int):
        if self.level >= 100:
            return

        self.xp += xp_amount
        logger.info(f"{self.name} ganhou {xp_amount} XP!")

        while self.level < 100:
            xp_needed = self.calculate_required_xp()

            if self.xp >= xp_needed:
                self.level += 1
                logger.info(f"Parabéns! {self.name} subiu para o Nível {self.level}!")

                old_max = self.max_hp
                self.recalculate_stats()
                hp_gain = self.max_hp - old_max
                if self.current_hp > 0:
                    self.current_hp += hp_gain

                new_moves = self.check_new_moves()
                if new_moves:
                    logger.info(f"{self.name} quer aprender: {new_moves}")
                    for move_name in new_moves:
                        if len(self.moves) < 4:
                            self.moves.append(Move(move_name))
                            logger.info(f"Aprendeu {move_name}!")

                if self.can_evolve_at_level():
                    self.evolve()
            else:
                break

    def calculate_required_xp(self) -> int:
        return (self.level + 1) ** 3

    def check_new_moves(self) -> list[str]:
        if self.name not in POKEDEX_DB:
            return []

        all_moves = POKEDEX_DB[self.name].get("moves", [])
        return [m["name"] for m in all_moves if m["level"] == self.level]

    def can_evolve_at_level(self) -> bool:
        if not self.evolution:
            return False

        trigger = self.evolution.get("trigger")
        at_level = self.evolution.get("at_level")

        if trigger == "level-up" and isinstance(at_level, int):
            return self.level >= at_level
        return False

    def evolve(self):
        target_name = self.evolution.get("target")
        if not target_name or target_name not in POKEDEX_DB:
            logger.error(f"Erro de Evolução: Alvo '{target_name}' inválido.")
            return

        old_name = self.name
        new_data = POKEDEX_DB[target_name]

        self.name = target_name
        self.id = new_data["id"]
        self.types = new_data["types"]
        self.base_experience = new_data["base_experience"]
        self.evolution = new_data.get("evolution")

        self.recalculate_stats()

        self.current_hp = self.max_hp

        logger.info(f"--- O seu {old_name} evoluiu para {self.name}! ---")

    def attack(self, move) -> bool:
        if move.use():
            return True
        logger.debug(f"{self.name} tentou usar {move.name} mas falhou (sem PP).")
        return False

    def take_damage(self, amount: int) -> int:
        self.current_hp = max(0, self.current_hp - int(amount))
        return self.current_hp

    def restore_hp(self, amount: int) -> int:
        self.current_hp = min(self.max_hp, self.current_hp + int(amount))
        return self.current_hp

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def apply_stat_change(self, stat_name: str, amount: int) -> bool:
        if stat_name not in self.stat_mods:
            return False

        old_val = self.stat_mods[stat_name]
        new_val = old_val + amount

        self.stat_mods[stat_name] = max(-6, min(6, new_val))

        if old_val != self.stat_mods[stat_name]:
            logger.debug(f"{self.name} {stat_name}: {old_val} -> {self.stat_mods[stat_name]}")
            return True
        return False

    def get_current_stat(self, stat_name: str) -> int:
        stat_map = {
            "attack": self.atk,
            "defense": self.defense,
            "special-attack": self.sp_atk,
            "special-defense": self.sp_def,
            "speed": self.speed
        }

        base_value = stat_map.get(stat_name, 0)
        stage = self.stat_mods.get(stat_name, 0)

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

    def show_status(self) -> dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "hp_percent": self.current_hp / self.max_hp if self.max_hp > 0 else 0,
            "current_hp": self.current_hp,
            "max_hp": self.max_hp,
            "types": "/".join(self.types),
            "status": self.status
        }

    def can_move(self) -> tuple[bool, str]:
        if self.status == "sleep":
            if random.randint(1, 100) >= 50:
                self.status = None
                return True, f"{self.name} acordou!"
            return False, f"{self.name} está dormindo."

        elif self.status == "freeze":
            if random.randint(1, 100) <= 25:
                self.status = None
                return True, f"{self.name} descongelou!"
            return False, f"{self.name} está congelado e não atacou."

        elif self.status == "paralysis":
            if random.randint(1, 100) <= 25:
                return False, f"{self.name} está paralisado e não consegue se mover!"

        return True, ""

    def apply_status_damage(self) -> str:
        if not self.is_alive():
            return None

        damage = 0
        message = None

        if self.status == "burn":
            damage = max(1, self.max_hp // 16)
            self.take_damage(damage)
            message = f"{self.name} sofreu {damage} de dano pela queimadura."

        elif self.status == "poison":
            damage = max(1, self.max_hp // 8)
            self.take_damage(damage)
            message = f"{self.name} sofreu {damage} de dano pelo veneno."

        return message

    def __repr__(self):
        return f"<{self.name} Lv.{self.level} | HP:{self.current_hp}/{self.max_hp}>"


class Trainer:
    def __init__(self, name: str, is_ai: bool = False, money: int = 1000, initial_team: list = None, x: int = 0, y: int = 0):
        self.name: str = name
        self.money: int = money
        self.bag: dict = {}
        self.active_slot: int = 0

        self.badges: list = []
        self.pokedex_seen: set = set()
        self.pokedex_caught: set = set()

        self.team: list = list()
        if initial_team is not None:
            for pkm in initial_team:
                self.add_pokemon(pkm)

        self.active_slot: int = 0

        self.x: int = x
        self.y:int = y


    def add_pokemon(self, pokemon: "Pokemon") -> bool:
        if len(self.team) < 6:
            self.team.append(pokemon)
            self.pokedex_caught.add(pokemon.id)
            self.pokedex_seen.add(pokemon.id)
            logger.info(f"{pokemon.name} adicionado ao time de {self.name}.")
            return True
        else:
            logger.warning(f"Time de {self.name} está cheio! Não foi possível adicionar {pokemon.name}.")
            return False

    def get_active_pokemon(self) -> "Pokemon":
        if 0 <= self.active_slot < len(self.team):
            pkm = self.team[self.active_slot]
            if pkm.is_alive():
                return pkm
        return None

    def swap_slots(self, index1: int, index2: int):
        if 0 <= index1 < len(self.team) and 0 <= index2 < len(self.team):
            self.team[index1], self.team[index2] = self.team[index2], self.team[index1]
            logger.debug(f"Trocou posição: {self.team[index1].name} <-> {self.team[index2].name}")

    def has_alive_pokemon(self) -> bool:
        return any(p.is_alive() for p in self.team)

    def has_item(self, item_name: str) -> bool:
        return self.bag.get(item_name, 0) > 0

    def add_item(self, item_name: str, quantity: int = 1):
        if quantity <= 0:
              return

        current_qty = self.bag.get(item_name, 0)
        self.bag[item_name] = current_qty + quantity
        logger.debug(f"{self.name} recebeu {quantity}x {item_name}.")

    def consume_item(self, item_name: str) -> bool:
        if self.has_item(item_name):
            self.bag[item_name] -= 1
            if self.bag[item_name] == 0:
                del self.bag[item_name]
            return True
        return False

    def get_active_slot(self) -> int:
        return self.active_slot

    def set_active_pokemon_index(self, new_index: int) -> bool:
        if 0 <= new_index < len(self.team) and self.team[new_index].is_alive():
            self.active_slot = new_index
            return True
        return False

    def switch_to_next_available(self) -> bool:
        for i, pkm in enumerate(self.team):
            if pkm.is_alive():
                self.active_slot = i
                return True
        return False

    def __repr__(self) -> str:
        return f"<Trainer {self.name} | Money: ${self.money} | Team: {len(self.team)}>"


class Move:
    def __init__(self, name: str, data: dict[str, object] = None):
        if data is None:
            if name not in MOVES_DB:
                logger.error(f"Erro: O ataque '{name}' não existe no moves.json!")
                raise ValueError(f"O ataque '{name}' não existe no moves.json!")
            data = MOVES_DB[name]

        self.name: str = name
        self.type: str = data.get("type", "Normal")
        self.category = data.get("category", "Physical")

        self.power: int = data.get("power") or 0
        self.accuracy: int = data.get("accuracy") or 100
        self.max_pp: int = data.get("pp", 0)
        self.current_pp: int = self.max_pp

        self.priority: int = data.get("priority", 0)
        self.effect: dict[str, object] = data.get("effect")
        self.mechanics: dict[str, object] = data.get("mechanics")

    def use(self) -> bool:
        if self.current_pp > 0:
            self.current_pp -= 1
            return True
        return False

    def restore_pp(self, amount: int = None):
        if amount is None:
            self.current_pp = self.max_pp
        else:
            self.current_pp = min(self.max_pp, self.current_pp + amount)


class Item:
    def __init__(self, name: str):
        if name not in ITEMS_DB:
            logger.error(f"Erro: Item '{name}' não encontrado no DB.")
            raise ValueError(f"Item '{name}' não encontrado no JSON.")

        data: dict[str, object] = ITEMS_DB[name]

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.category: str = data["category"]
        self.price: int = data["price"]
        self.description: str = data["description"]
        self.effect: dict[str, object] = data["effect"]

        self._handlers: dict = {
            "heal_hp": self._handle_heal_hp,
            "revive": self._handle_revive,
            "cure_status": self._handle_cure_status,
            "heal_hp_status": self._handle_full_restore
        }

    def use(self, target_pokemon: 'Pokemon') -> bool:
        effect_type: str = self.effect.get("type")

        handler = self._handlers.get(effect_type)

        if handler:
            logger.debug(f"Usando {self.name} ({effect_type}) em {target_pokemon.name}...")
            return handler(target_pokemon)

        logger.warning(f"Tipo de efeito desconhecido ou não implementado: {effect_type}")
        return False

    def _handle_heal_hp(self, target: 'Pokemon') -> bool:
        if target.current_hp >= target.max_hp:
            logger.debug(f"Falha: {target.name} já está com HP cheio.")
            return False

        amount: int = self.effect.get("amount", 0)
        target.restore_hp(amount)
        logger.debug(f"Sucesso: Curou {amount} HP.")
        return True

    def _handle_revive(self, target: 'Pokemon') -> bool:
        if target.is_alive():
            logger.debug(f"Falha: {target.name} não está desmaiado.")
            return False

        percent: float = self.effect.get("amount_percent", 0.5)
        new_hp = int(target.max_hp * percent)
        target.current_hp = max(1, new_hp)

        logger.debug(f"Sucesso: {target.name} reviveu com {target.current_hp} HP.")
        return True

    def _handle_cure_status(self, target: 'Pokemon') -> bool:
        condition_to_cure: str = self.effect.get("condition")

        if target.status is None:
            logger.debug(f"Falha: {target.name} não tem problemas de status.")
            return False

        if condition_to_cure == "all" or target.status == condition_to_cure:
            logger.debug(f"Sucesso: Curou status '{target.status}'.")
            target.status = None
            return True

        logger.debug(f"Falha: Item cura '{condition_to_cure}', mas alvo tem '{target.status}'.")
        return False

    def _handle_full_restore(self, target: 'Pokemon') -> bool:
        if target.current_hp >= target.max_hp and target.status is None:
            logger.debug(f"Falha: {target.name} já está saudável.")
            return False

        target.status = None
        target.current_hp = target.max_hp
        logger.debug(f"Sucesso: {self.name} restaurou totalmente {target.name}.")
        return True

    def __repr__(self) -> str:
        return f"<Item: {self.name}>"
