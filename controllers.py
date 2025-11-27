#from graphics import *
from classes import Pokemon, Trainer, Move
import random
import json

class BattleController:
    def __init__(self, BattleScene, trainer=None, player=None):
        #self.trainer = trainer
        #self.player = player
        self.states = ["player_turn", "trainer_turn", "attack", "bag", "pokemon", "run", "victory", "defeat"]
        self.state = self.states[0]
        self.types_damage = self.load_types_from_json()
        self.all_moves = self.load_moves_from_json()
        self.battle_scene = BattleScene
        self.trainer, self.player = self.setup_game()
        self.run_battle_loop()


    def run_battle_loop(self):
        self.player_turn = True
        self.player_pkmn_idx = 0
        self.trainer_pkmn_idx = 0

        self.is_active = True
        while self.is_active:
            if self.check_end_condition():
                self.is_team_alive = False
                continue
            self.process_battle_state()
            self.handle_state_logic()

            if self.player_turn:
                self.state = "trainer_turn"
                self.player_turn = False
            else:
                self.state = "player_turn"
                self.player_turn = True

    def check_end_condition(self):
        if not self.is_team_alive(self.trainer) or not self.is_team_alive(self.player):
            return True
        return False


    def process_battle_state(self):
        self.player_pkmn = self.player.team[self.player_pkmn_idx]
        self.trainer_pkmn = self.trainer.team[self.trainer_pkmn_idx]

        if self.player_turn:
            print(self.player_pkmn.show_status())
            print(self.trainer_pkmn.show_status())

        if self.state == "player_turn":
            if not self.is_team_alive(self.player):
                self.state = "defeat"

            self.attacking_pkmn = self.player_pkmn
            self.defender_pkmn = self.trainer_pkmn

            action = self.battle_scene.chose_action()

            match action:
                case "attack":
                    self.state = "attack"
                case "bag":
                    self.state = "bag"
                case "pokemon":
                    self.state = "pokemon"
                case "run":
                    self.state = "run"

        elif self.state == "trainer_turn":
            if not self.is_team_alive(self.trainer):
                self.state = "victory"

            self.attacking_pkmn = self.trainer_pkmn
            self.defender_pkmn = self.player_pkmn

            #implementar logica do adversario


    def handle_state_logic(self):
        if self.state == "attack":
            attack_index = self.battle_scene.chose_attack()
            self.chosen_move = self.player_pkmn.moves[attack_index]

            if self.player_pkmn.attack(self.chosen_move):
                hit_chance = random.randint(1, 100)
                if hit_chance <= self.chosen_move.accuracy:
                    damage = self.calculate_damage(self.chosen_move)
                    self.trainer_pkmn.take_damage(damage)
                else:
                    pass
                    #nao acertou

        elif self.state == "pokemon":
            self.player_pkmn_idx = self.battle_scene.chose_pokemon()

        elif self.state == "bag":
            self.item_index = self.battle_scene.chose_item()

        elif self.state == "run":
            self.battle_scene.run()
            self.is_active = False

        elif self.state == "defeat":
            self.battle_scene.defeat()

        elif self.state == "victory":
            self.battle_scene_victory()


        if self.player_turn:
            self.state = "trainer_turn"
        else:
            self.state = "player_turn"


    def is_team_alive(self, trainer):
        for pokemon in trainer.team:
            if pokemon.current_hp > 0:
                return True
        return False


    def load_types_from_json(self):
        with open("types.json", "r", encoding="utf-8" ) as file:
            return json.load(file)


    def load_moves_from_json(self):
        with open("moves.json", "r", encoding="utf-8") as file:
            moves_data = json.load(file)

        all_moves = {}
        for data in moves_data:
            new_move = Move(**data)
            all_moves[new_move.name] = new_move

        return all_moves


    def calculate_damage(self, chosen_move):
        multiplier_1 = ((2 * self.attacking_pkmn.level/5) + 2)
        multiplier_2 = multiplier_1 * (chosen_move.power * self.attacking_pkmn.atk / self.defender_pkmn.defense)
        multiplier_3 = (multiplier_2 /50) + 2
        attack_type_rules = self.types_damage.get(chosen_move.type, {})
        multiplier_4 = attack_type_rules.get(self.defender_pkmn.primary_type, 1.0)
        multiplier_5 = 1.0

        if self.defender_pkmn.secondary_type:
            multiplier_5 = attack_type_rules.get(self.defender_pkmn.secondary_type, 1.0)

        final_multiplier = multiplier_4 * multiplier_5

        stab = 1.0
        if self.attacking_pkmn.primary_type == self.chosen_move.type or self.attacking_pkmn.secondary_type == self.chosen_move.type:
            stab = 1.5

        damage = multiplier_3 * final_multiplier * stab
        return int(damage)

    def setup_game(self):

        # Time do ash
        pikachu = Pokemon("Pikachu", "Electric", 20, 0, 25, 35, 55, 40, 90, [self.all_moves["Thunder Shock"], self.all_moves["Tackle"]])
        pidgey = Pokemon("Pidgey", "Normal", 20, 0, 16, 40, 45, 40, 56, [self.all_moves["Gust"], self.all_moves["Tackle"]], secondary_type="Flying")
        bulbasaur = Pokemon("Bulbasaur", "Grass", 20, 0, 1, 45, 49, 49, 45, [self.all_moves["Vine Whip"], self.all_moves["Tackle"]], secondary_type="Poison")

        # Time do gary
        squirtle = Pokemon("Squirtle", "Water", 20, 0, 7, 44, 48, 65, 43, [self.all_moves["Water Gun"], self.all_moves["Tackle"]])
        geodude = Pokemon("Geodude", "Rock", 20, 0, 74, 40, 80, 100, 20, [self.all_moves["Rock Throw"], self.all_moves["Tackle"]], secondary_type="Ground")
        charmander = Pokemon("Charmander", "Fire", 20, 0, 4, 39, 52, 43, 65, [self.all_moves["Ember"], self.all_moves["Scratch"]])

        player = Trainer("Ash", 0)
        player.add_pokemon(pikachu)
        player.add_pokemon(pidgey)
        player.add_pokemon(bulbasaur)

        enemy = Trainer("Gary", 0)
        enemy.add_pokemon(squirtle)
        enemy.add_pokemon(geodude)
        enemy.add_pokemon(charmander)

        return player, enemy



class BattleScene:
    def __init__(self, scene):
        self.scene = scene

    def chose_action(self):
        return input("escolha a acao  ")

    def chose_pokemon(self):
        return int(input("escolha o pokemon por indice "))

    def chose_item(self):
        return int(input("escolha o item por indice "))

    def chose_attack(self):
        return int(input("escolha o ataque por indice "))

    def run(self):
        return

battle_scene = BattleScene("scene")

battle_controller = BattleController(battle_scene)
