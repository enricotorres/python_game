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
