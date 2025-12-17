import random
import logging

from src import Item, Pokemon, Move, TYPES_DB
from src.battle.mechanics import DamageCalculator, MoveEffectResolver, BattleAI, AccuracyCalculator

logger = logging.getLogger(__name__)

class BattleController:
    def __init__(self, battle_scene, enemy, player) -> None:
        self.player = player
        self.enemy = enemy
        self.battle_scene = battle_scene
        self.types_damage: dict = TYPES_DB
        self.cancel_action: int = -1

        self.damage_calculator = DamageCalculator(TYPES_DB)
        self.move_effect_resolver = MoveEffectResolver(self)
        self.battle_ai = BattleAI(self.damage_calculator)
        self.accuracy_calculator = AccuracyCalculator()

        self.player_action_type: str | None = None
        self.player_chosen_move: Move | None = None
        self.player_chosen_item: Item | None = None

        self.enemy_action_type: str = "attack"
        self.enemy_chosen_move: Move | None = None
        self.enemy_chosen_item: Item | None = None

        self.switch_target_index: int | None = None

        self.weather_condition: str | None = None
        self.weather_turns: int = 0

        self.state: str = "START"

        self.battle_scene.pokemon_player_name, self.battle_scene.pokemon_enemy_name, self.battle_scene.pokemon_player_level, self.battle_scene.pokemon_enemy_level = self.battle_scene.pokemon_infos(custom_pos=None, specific_pokemon=None)
        self.battle_scene.pokemon_player_name.draw(self.battle_scene.janela)
        self.battle_scene.pokemon_enemy_name.draw(self.battle_scene.janela)
        self.battle_scene.pokemon_player_level.draw(self.battle_scene.janela)
        self.battle_scene.pokemon_enemy_level.draw(self.battle_scene.janela)

        logger.info(f"Controlador de Batalha iniciado: {self.player.name} vs {self.enemy.name}")

    def run_battle_loop(self) -> None:
        self.state = "PLAYER_TURN"
        logger.info("Iniciando loop de batalha...")

        while self.state != "EXIT":
            self.player_pokemon: Pokemon = self.player.get_active_pokemon()
            self.enemy_pokemon: Pokemon = self.enemy.get_active_pokemon()

            logger.info("-" * 30)
            p_name = self.player_pokemon.name if self.player_pokemon else "Desmaiado"
            p_hp = f"{self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}" if self.player_pokemon else "0/0"
            e_name = self.enemy_pokemon.name if self.enemy_pokemon else "Desmaiado"
            e_hp = f"{self.enemy_pokemon.current_hp}/{self.enemy_pokemon.max_hp}" if self.enemy_pokemon else "0/0"
            logger.info(f"BATTLE STATUS: {p_name} (HP: {p_hp}) vs {e_name} (HP: {e_hp})")

            input_states: list[str] = ["PLAYER_TURN", "SELECT_MOVE", "POKEMON_MENU", "BAG_MENU", "FORCE_SWITCH"]

            if self.state in input_states:
                self._handle_state_logic()
            else:
                self._process_battle_state()

    def _handle_state_logic(self) -> None:
        if self.state == "PLAYER_TURN":
            if not self.player.has_alive_pokemon():
                logger.warning("O time do jogador foi derrotado. Mudando estado para DEFEAT.")
                self.state = "DEFEAT"
                return

            logger.debug("Aguardando input do jogador (chose_action)...")
            action: str = self.battle_scene.chose_action()
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
            attack_index: int = self.battle_scene.chose_attack()
            if attack_index == self.cancel_action:
                self.state = "PLAYER_TURN"
                return

            if attack_index >= len(self.player_pokemon.moves):
                logger.warning("Jogador selecionou um slot de ataque vazio.")
                return

            self.player_chosen_move = self.player_pokemon.moves[attack_index]
            self.player_action_type = "attack"
            logger.info(f"Jogador selecionou o ataque: {self.player_chosen_move.name}")

            self._decide_enemy_move()
            self.state = "RESOLVE_TURN"

        elif self.state == "POKEMON_MENU":
            selected_index: int = self.battle_scene.chose_pokemon()

            if selected_index == self.cancel_action:
                self.state = "PLAYER_TURN"
                return

            if selected_index != self.player.active_slot and self.player.set_active_pokemon_index(selected_index):
                self.switch_target_index = selected_index
                self.player_action_type = "switch"
                temp_pokemon = self.player.get_active_pokemon()
                logger.info(f"Jogador escolheu trocar para: {temp_pokemon.name}")

                self._decide_enemy_move()
                self.state = "RESOLVE_TURN"
            else:
                logger.warning("Seleção de troca inválida (Pokémon desmaiado ou já ativo).")
                self.state = "PLAYER_TURN"

        elif self.state == "BAG_MENU":
            item_index: int = self.battle_scene.chose_item()
            
            if item_index == self.cancel_action:
                self.state = "PLAYER_TURN"
                return

            bag_keys = list(self.player.bag.keys())
            
            if item_index < len(bag_keys):
                item_name = bag_keys[item_index]
                current_qty = self.player.bag.get(item_name, 0)
                
                if current_qty > 0:
                    logger.info(f"Jogador decidiu usar {item_name}.")
                    self.player_chosen_item = Item(item_name)
                    used_success = False

                    if item_name in ["Potion", "Super Potion", "Hyper Potion"]:
                         if self.player_pokemon.current_hp < self.player_pokemon.max_hp:
                             if self.player_chosen_item.use(self.player_pokemon):
                                 used_success = True
                         else:
                             logger.info("HP já está cheio.")
                    
                    elif item_name == "Revive":
                         logger.info("Revive não pode ser usado no Pokémon ativo (ele está vivo).")
                    
                    elif "Ball" in item_name:
                        logger.info("Lógica de captura ainda não implementada neste controller.")

                    
                    if used_success:
                        self.player.consume_item(item_name)
                        logger.info(f"Jogador usou {item_name} em {self.player_pokemon.name}!")
                        self.player_action_type = "bag"
                        self._decide_enemy_move()
                        self.state = "RESOLVE_TURN"
                    else:
                        self.state = "PLAYER_TURN"
                else:
                    logger.warning("Item sem quantidade.")
                    self.state = "PLAYER_TURN"
            else:
                logger.warning("Slot vazio selecionado.")
                self.state = "PLAYER_TURN"

        elif self.state == "FORCE_SWITCH":
            logger.info("Jogador precisa escolher um novo Pokémon (Force Switch).")
            selected_index: int = self.battle_scene.chose_pokemon()

            if selected_index == self.cancel_action:
                return

            if self.player.set_active_pokemon_index(selected_index):
                self.player_pokemon = self.player.get_active_pokemon()
                logger.info(f"Novo Pokémon ativo: {self.player_pokemon.name}")
                
                self.battle_scene.update_health_bar()
                self.battle_scene.update_info()
                self.battle_scene.update_sprites()

                self.state = "PLAYER_TURN"
            else:
                logger.warning("Não pode trocar para um Pokémon desmaiado.")

    def _decide_enemy_move(self) -> None:
        action_type, chosen_object = self.battle_ai.choose_action(self.enemy, self.player_pokemon)
        self.enemy_action_type = action_type

        if action_type == "attack":
            self.enemy_chosen_move = chosen_object
            self.enemy_chosen_item = None
        elif action_type == "bag":
            self.enemy_chosen_item = chosen_object
            self.enemy_chosen_move = None

    def _process_battle_state(self) -> None:
        if self.state != "RESOLVE_TURN":
            self._handle_end_game_states()
            return

        logger.info("--- Resolução do Turno ---")

        if self.player_action_type == "run":
            self.battle_scene.run()
            logger.info("Batalha encerrada por fuga.")
            self.state = "EXIT"
            return

        if self.player_action_type == "switch":
            self.player_pokemon = self.player.get_active_pokemon()
            logger.info(f"Troca realizada. Vai! {self.player_pokemon.name}!")
            self.battle_scene.update_health_bar()
            self.battle_scene.update_info()
            self.battle_scene.update_sprites()
            if self._check_battle_status():
                 self._perform_attack(self.enemy_pokemon, self.player_pokemon, self.enemy_chosen_move)

        elif self.player_action_type == "bag":
            if self._check_battle_status():
                 self._perform_attack(self.enemy_pokemon, self.player_pokemon, self.enemy_chosen_move)

        if self.enemy_action_type == "bag" and self.player_action_type != "run":
            item = self.enemy_chosen_item
            logger.info(f"O Inimigo usou {item.name}!")
            if item.use(self.enemy_pokemon):
                self.enemy.consume_item(item.name)
                self.enemy_chosen_move = None

        if self.player_action_type == "attack" and self.enemy_chosen_move:
            first, second = self._get_turn_order(
                self.player_pokemon, self.player_chosen_move,
                self.enemy_pokemon, self.enemy_chosen_move
            )

            self._perform_attack(first[0], first[1], first[2])

            if self._check_battle_status() and second[0].is_alive():
                self._perform_attack(second[0], second[1], second[2])
                self._check_battle_status()

        if self.state not in ["VICTORY", "DEFEAT", "EXIT", "FORCE_SWITCH"]:
            self._end_of_turn_resolution()

        if self.state not in ["VICTORY", "DEFEAT", "EXIT", "FORCE_SWITCH"]:
            self.state = "PLAYER_TURN"

    def _handle_end_game_states(self) -> None:
        if self.state == "VICTORY":
            logger.info("VITÓRIA! O treinador inimigo foi derrotado.")
            self.state = "EXIT"
        elif self.state == "DEFEAT":
            logger.info("DERROTA... Você não tem mais Pokémons.")
            self.state = "EXIT"

    def _get_turn_order(self, p_pkm: Pokemon, p_move: Move, e_pkm: Pokemon, e_move: Move) -> tuple[tuple, tuple]:
        if p_move.priority > e_move.priority:
            return (p_pkm, e_pkm, p_move), (e_pkm, p_pkm, e_move)
        if e_move.priority > p_move.priority:
            return (e_pkm, p_pkm, e_move), (p_pkm, e_pkm, p_move)

        p_speed = p_pkm.get_current_stat("speed")
        e_speed = e_pkm.get_current_stat("speed")

        if p_speed > e_speed:
            return (p_pkm, e_pkm, p_move), (e_pkm, p_pkm, e_move)
        elif e_speed > p_speed:
            return (e_pkm, p_pkm, e_move), (p_pkm, e_pkm, p_move)
        else:
            if random.choice([True, False]):
                return (p_pkm, e_pkm, p_move), (e_pkm, p_pkm, e_move)
            return (e_pkm, p_pkm, e_move), (p_pkm, e_pkm, p_move)

    def _perform_attack(self, attacker: Pokemon, defender: Pokemon, move: Move) -> None:
        if not move:
            return

        logger.info(f"> {attacker.name} usou {move.name}!")

        can_move, status_msg = attacker.can_move()
        if status_msg:
            logger.info(status_msg)

        if not can_move:
            return

        if not attacker.attack(move):
            logger.warning(f"{move.name} falhou por falta de PP!")
            return

        if not self.accuracy_calculator.check_hit(move, attacker, defender):
            logger.info(f"O ataque de {attacker.name} errou!")
            return

        damage, hits_count = self.damage_calculator.calculate(
            attacker=attacker,
            defender=defender,
            chosen_move=move,
            weather_condition=self.weather_condition
        )

        if damage > 0:
            defender.take_damage(damage)
            logger.info(f"Causou {damage} de dano em {defender.name}!")
            if hits_count > 1:
                logger.info(f"Atingiu {hits_count} vezes!")
            
            self.battle_scene.update_health_bar()
            

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

        self.move_effect_resolver.resolve(move, attacker, defender)
        self._check_battle_status()

    def _check_battle_status(self) -> bool:
        if not self.player.has_alive_pokemon():
            logger.info("Time do jogador completamente derrotado.")
            self.state = "DEFEAT"
            return False

        if not self.enemy.has_alive_pokemon():
            logger.info("Time do inimigo completamente derrotado.")
            self.state = "VICTORY"
            return False

        if not self.player_pokemon.is_alive():
            logger.info(f"{self.player_pokemon.name} desmaiou!")
            self.state = "FORCE_SWITCH"
            return False

        if not self.enemy_pokemon.is_alive():
            logger.info(f"{self.enemy_pokemon.name} inimigo desmaiou!")
            xp_gained = self._calculate_battle_xp()
            logger.info(f"Ganhou {xp_gained} de experiência!")
            if self._swap_enemy_pokemon():
                logger.info(f"Inimigo enviou {self.enemy_pokemon.name}!")
                self.battle_scene.update_health_bar()
                self.battle_scene.update_info()
                self.battle_scene.update_sprites()
            return False

        return True

    def _swap_enemy_pokemon(self) -> bool:
        if self.enemy.switch_to_next_available():
            self.enemy_pokemon = self.enemy.get_active_pokemon()
            return True
        return False

    def _end_of_turn_resolution(self) -> None:
        logger.debug("Resolvendo efeitos de fim de turno...")
        for pokemon in [self.player_pokemon, self.enemy_pokemon]:
            if pokemon.is_alive():
                msg = pokemon.apply_status_damage()
                if msg:
                    logger.info(msg)
        self._check_battle_status()

    def _calculate_battle_xp(self) -> int:
        base_xp = self.enemy_pokemon.base_experience
        enemy_level = self.enemy_pokemon.level
        raw_xp = (base_xp * enemy_level) / 7
        xp_amount = int(raw_xp)
        self.player_pokemon.gain_xp(xp_amount)
        return xp_amount
