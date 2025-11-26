class Pokemon:
    def __init__(self, name, primary_type, xp, pokedex_id, base_hp, current_hp,secondary_type=None):
        self.pokedex_id = pokedex_id
        self.primary = primary_type
        self.secondary_type = secondary_type
        self.name = name
        self.xp = xp
        self.base_hp = base_hp
        self.current_hp = base_hp

    def show_status(self):
        tipo_str = self.primary_type
        if self.secondary_type:
            tipo_str += f"/{self.secondary_type}"

        print(f"ID: {self.pokedex_id} | {self.name} ({tipo_str}) | HP: {self.current_hp}/{self.base_hp}")

    def attack(self):
        return self.attack_damage


class Trainer:
    def __init__(self, name, xp):
        self.name = name
        self.xp = xp


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
            return self.power
        else:
            return 0
