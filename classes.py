class Pokemon:
    def __init__(self, name, primary_type, xp, pokedex_id, base_hp, moves, secondary_type=None):
        self.pokedex_id = pokedex_id
        self.primary_type = primary_type
        self.secondary_type = secondary_type
        self.name = name
        self.xp = xp
        self.base_hp = base_hp
        self.current_hp = base_hp
        self.moves = moves

    def show_status(self):
        tipo_str = self.primary_type
        if self.secondary_type:
            tipo_str += f"/{self.secondary_type}"

        return {"id": self.pokedex_id, "name": self.name, "hp": self.current_hp/self.base_hp}

    def attack(self, move):
        if move.use():
            return move
        return False

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0
        return self.current_hp > 0


class Trainer:
    def __init__(self, name, xp, initial_team=None):
        self.name = name
        self.xp = xp

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


class Move:
    def __init__(self, name, type_move, power, accuracy, max_pp):
        self.name = name
        self.type_move = type_move
        self.power = power
        self.accuracy = accuracy
        self.max_pp = max_pp
        self.current_pp = max_pp

    def use(self):
        if self.current_pp > 0:
            self.current_pp -= 1
            return True
        else:
            return False
