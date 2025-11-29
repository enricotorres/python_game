from src.database import MOVES_DB, POKEDEX_DB

class Pokemon:
    def __init__(self, name, level):
        if name not in POKEDEX_DB:
            raise ValueError(f"Pokémon '{name}' não encontrado no Pokedex JSON.")

        data = POKEDEX_DB[name]

        self.name = name
        self.id = data['id']
        self.level = level
        self.xp = 0
        self.types = data['types']
        self.sprite = data.get('sprite')

        base_stats = data['stats']

        self.max_hp = int(((base_stats['hp'] * 2 * level) / 100) + level + 10)
        self.current_hp = self.max_hp

        self.atk = int(((base_stats['attack'] * 2 * level) / 100) + 5)
        self.defense = int(((base_stats['defense'] * 2 * level) / 100) + 5)
        self.sp_atk = int(((base_stats['special_attack'] * 2 * level) / 100) + 5)
        self.sp_def = int(((base_stats['special_defense'] * 2 * level) / 100) + 5)
        self.speed = int(((base_stats['speed'] * 2 * level) / 100) + 5)

        self.moves = []
        self.learn_moves_by_level(data['moves'])

    def learn_moves_by_level(self, moves_list_from_json):
        available_moves = [m for m in moves_list_from_json if m['level'] <= self.level]

        available_moves.sort(key=lambda x: x['level'])

        recent_moves = available_moves[-4:]

        for m_data in recent_moves:
            try:
                new_move = Move(m_data['name'])
                self.moves.append(new_move)
            except Exception as e:
                print(f"Erro ao ensinar {m_data['name']} para {self.name}: {e}")

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
        return False

    def take_damage(self, amount):
        self.current_hp -= int(amount)
        if self.current_hp < 0:
            self.current_hp = 0
        return self.current_hp > 0

    def is_alive(self):
            return self.current_hp > 0

    def __repr__(self):
        return f"<{self.name} Lv.{self.level} | HP:{self.current_hp}>"


class Trainer:
    def __init__(self, name, xp=0, money=0, initial_team=None):
        self.name = name
        self.xp = xp
        self.money = money
        self.bag = {}

        if initial_team is None:
            self.team = []
        else:
            self.team = initial_team

    def add_pokemon(self, pokemon):
        if len(self.team) < 6:
            self.team.append(pokemon)
            return True
        else:
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
            raise ValueError(f"O ataque '{name}' não existe no moves.json!")

        data = MOVES_DB[name]

        self.name = name
        self.type = data['type']
        self.category = data['category']
        self.power = data['power']
        self.accuracy = data['accuracy']
        self.max_pp = data['pp']
        self.current_pp = data['pp']

        self.effect = data.get('effect')

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
