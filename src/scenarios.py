import graphics as gf
import time
from pathlib import Path

class BattleScene:
    def __init__(self, window, player, enemy):
        self.width = 1408
        self.height = 768

        self.root_dir = Path(__file__).resolve().parent.parent
        self.assets_dir = self.root_dir / "assets" / "images"

        self.p1 = gf.Point(826, 612)
        self.p2 = gf.Point(1000, 647)
        self.p3 = gf.Point(826, 710)
        self.p4 = gf.Point(1068, 676)
        self.p5 = gf.Point(1303, 647)
        self.p6 = gf.Point(1197, 612)
        self.p7 = gf.Point(1303, 710)
        self.p8 = gf.Point(1197, 676)

        self.pk_back_pos1 = gf.Point(1132, 653)
        self.pk_back_pos2 = gf.Point(1400, 753)
        self.pk_option1_pos1 = gf.Point(90, 232)
        self.pk_option1_pos2 = gf.Point(478, 387)
        self.pk_option2_pos1 = gf.Point(512, 232)
        self.pk_option2_pos2 = gf.Point(897, 387)
        self.pk_option3_pos1 = gf.Point(927, 231)
        self.pk_option3_pos2 = gf.Point(1319, 387)
        self.pk_option4_pos1 = gf.Point(89, 418)
        self.pk_option4_pos2 = gf.Point(481, 580)
        self.pk_option5_pos1 = gf.Point(508, 418)
        self.pk_option5_pos2 = gf.Point(900, 580)
        self.pk_option6_pos1 = gf.Point(929, 418)
        self.pk_option6_pos2 = gf.Point(1319, 580)

        self.atk_option1_pos1 = gf.Point(228, 628)
        self.atk_option1_pos2 = gf.Point(344, 651)
        self.atk_option2_pos1 = gf.Point(513, 628)
        self.atk_option2_pos2 = gf.Point(632, 651)
        self.atk_option3_pos1 = gf.Point(802, 628)
        self.atk_option3_pos2 = gf.Point(921, 651)
        self.atk_option4_pos1 = gf.Point(1118, 628)
        self.atk_option4_pos2 = gf.Point(1178, 651)
        self.atk_back_pos1 = gf.Point(1132, 653)
        self.atk_back_pos2 = gf.Point(1400, 753)

        self.select_poke_pos1 = gf.Point(175, 315)
        self.select_poke_pos2 = gf.Point(605, 315)
        self.select_poke_pos3 = gf.Point(1035, 315)
        self.select_poke_pos4 = gf.Point(175, 500)
        self.select_poke_pos5 = gf.Point(605, 500)
        self.select_poke_pos6 = gf.Point(1035, 500)



        self.p_life_rect = None
        self.e_life_rect = None
        self.pokemon_player_name = None
        self.pokemon_enemy_name = None
        self.pokemon_player_level = None
        self.pokemon_enemy_level = None

        self.janela = window

        self.player = player
        self.enemy = enemy
        self.allow_cancel = True

        back = self.bg()
        back.draw(self.janela)

        self.player_index = 0
        self.enemy_index = 0

        self.sprite()


        self.p_life_rect, self.e_life_rect = self.health_bar()
        self.p_life_rect.draw(self.janela)
        self.e_life_rect.draw(self.janela)

        self.battle_hud = self.hud()
        self.battle_hud.draw(self.janela)

    def get_path(self, filename):
        full_path = self.assets_dir / filename
        return str(full_path)

    def bg(self):
        return gf.Image(gf.Point(self.width / 2, self.height / 2), self.get_path("battlefield_final.png"))

    def hud(self):
        return gf.Image(gf.Point(704, 675), self.get_path("battle_hud_final.png"))

    def sprite(self):
        # ------------------ PLAYER ---------------------
        index_atual = self.player.active_slot
        self.player_pokemon = self.player.team[index_atual]

        pos_player = gf.Point(500, 500)
        sprite = self.player_pokemon.sprite
        if isinstance(sprite, dict):
            filename = sprite["back"]
        else:
            filename = sprite

        path = self.get_path(f"pokemon/{filename}")

        self.img_player = gf.Image(pos_player, path)
        self.img_player.draw(self.janela)

        # ------------------ INIMIGO ---------------------
        index_enemy = self.enemy.active_slot
        self.enemy_pokemon = self.enemy.team[index_enemy]

        pos_enemy = gf.Point(800, 380)
        sprite_enemy = self.enemy_pokemon.sprite
        if isinstance(sprite_enemy, dict):
            filename = sprite_enemy["front"]
        else:
            filename = sprite_enemy

        path = self.get_path(f"pokemon/{filename}")

        self.img_enemy = gf.Image(pos_enemy, path)
        self.img_enemy.draw(self.janela)

    def update_sprites(self):
        if hasattr(self, 'img_player'):
            self.img_player.undraw()

        if hasattr(self, 'img_enemy'):
            self.img_enemy.undraw()

        self.sprite()

    def pokemon_infos(self):
        self.player_pokemon = self.player.get_active_pokemon()
        self.enemy_pokemon = self.enemy.get_active_pokemon()

        p_pkname_pos = gf.Point(60, 35)
        p_lvl_pos = gf.Point(280, 35)

        e_pkname_pos = gf.Point(60, 35)
        e_lvl_pos = gf.Point(280, 35)

        name = self.player_pokemon.name
        player_p_name = gf.Text(p_pkname_pos, name)
        player_p_name.setSize(18)
        p_level = self.player_pokemon.level
        player_p_lvl = gf.Text(p_lvl_pos, f"LVL {p_level}")
        player_p_lvl.setSize(18)

        e_pkname_pos = gf.Point(1107, 35)
        e_lvl_pos = gf.Point(1318, 35)
        name = self.enemy_pokemon.name
        enemy_p_name = gf.Text(e_pkname_pos, name)
        enemy_p_name.setSize(18)
        e_level = self.enemy_pokemon.level
        enemy_p_lvl = gf.Text(e_lvl_pos, f"LVL {e_level}")
        enemy_p_lvl.setSize(18)


        return player_p_name, enemy_p_name, player_p_lvl, enemy_p_lvl

    def update_info(self):
        if hasattr(self, 'pokemon_player_name') and self.pokemon_player_name:
            self.pokemon_player_name.undraw()
        if hasattr(self, 'pokemon_player_level') and self.pokemon_player_level:
            self.pokemon_player_level.undraw()
        if hasattr(self, 'pokemon_enemy_name') and self.pokemon_enemy_name:
            self.pokemon_enemy_name.undraw()
        if hasattr(self, 'pokemon_enemy_level') and self.pokemon_enemy_level:
            self.pokemon_enemy_level.undraw()

        (self.pokemon_player_name, self.pokemon_enemy_name,
         self.pokemon_player_level, self.pokemon_enemy_level) = self.pokemon_infos()

        self.pokemon_player_name.draw(self.janela)
        self.pokemon_enemy_name.draw(self.janela)
        self.pokemon_player_level.draw(self.janela)
        self.pokemon_enemy_level.draw(self.janela)

    def health_bar(self):
        p_poke = self.player.get_active_pokemon()
        if p_poke is None:
            p_poke = self.player_pokemon
        else:
            self.player_pokemon = p_poke

        pct_player = p_poke.current_hp / p_poke.max_hp
        width_player = 317 * pct_player
        size_player_p1 = gf.Point(25, 65)
        size_player_p2 = gf.Point(25 + width_player, 80)
        hbar_player_rect = gf.Rectangle(size_player_p1, size_player_p2)
        hbar_player_rect.setFill("green")
        if pct_player < 0.2:
            hbar_player_rect.setFill("red")

        e_poke = self.enemy.get_active_pokemon()
        if e_poke is None:
            e_poke = self.enemy_pokemon
        else:
            self.enemy_pokemon = e_poke

        pct_enemy = e_poke.current_hp / e_poke.max_hp
        width_enemy = 317 * pct_enemy
        size_enemy_p1 = gf.Point(1063, 65)
        size_enemy_p2 = gf.Point(1063 + width_enemy, 80)
        hbar_enemy_rect = gf.Rectangle(size_enemy_p1, size_enemy_p2)
        hbar_enemy_rect.setFill("green")

        return hbar_player_rect, hbar_enemy_rect

    def update_health_bar(self):
        if hasattr(self, 'p_life_rect') and self.p_life_rect:
            self.p_life_rect.undraw()
        if hasattr(self, 'e_life_rect') and self.e_life_rect:
            self.e_life_rect.undraw()

        self.p_life_rect, self.e_life_rect = self.health_bar()

        self.p_life_rect.draw(self.janela)
        self.e_life_rect.draw(self.janela)

    def verificar_clique(self, click, p1, p2):
        x, y = click.getX(), click.getY()
        x_min, x_max = min(p1.getX(), p2.getX()), max(p1.getX(), p2.getX())
        y_min, y_max = min(p1.getY(), p2.getY()), max(p1.getY(), p2.getY())
        return (x_min <= x <= x_max) and (y_min <= y <= y_max)

    def fight_btn(self):
        img = gf.Image(gf.Point(704, 675), self.get_path("atk_hud.png"))
        txt = gf.Text(gf.Point(286.1, 675), "ATAQUE 1")
        txt.setSize(18)

        return img

    def bag_btn(self):
        return gf.Image(gf.Point(704, 675), self.get_path("white_hud.png"))

    def pokemon_btn(self):
        return gf.Image(gf.Point(self.width / 2, self.height / 2), self.get_path("pokemon_hud.png"))

    def import_controller(self, BattleController):
        self.battle_controller = BattleController
        return self.battle_controller

    def fight_txt(self):
        self.player_pokemon = self.player.get_active_pokemon()

        texts = []
        moves = self.player_pokemon.moves
        for i in range(4):
            p = gf.Point(286.1 + (i * 286.1), 640)
            if i < len(moves):
                label = moves[i].name
            else:
                label = ""
            t = gf.Text(p, label)
            t.setSize(24)
            t.setTextColor("black")
            texts.append(t)
        return texts

    def chose_action(self):
        while True:
            click = self.janela.getMouse()

            if self.verificar_clique(click, self.p1, self.p2):
                return "attack"
            elif self.verificar_clique(click, self.p3, self.p4):
                return "pokemon"
            elif self.verificar_clique(click, self.p5, self.p6):
                return "bag"
            elif self.verificar_clique(click, self.p7, self.p8):
                return "run"

    def chose_attack(self):
        f_win = self.fight_btn()
        f_win.draw(self.janela)

        f_txt = self.fight_txt()
        for item in f_txt:
            item.draw(self.janela)

        choice = -1
        while True:
            click = self.janela.getMouse()
            if self.verificar_clique(click, self.atk_option1_pos1, self.atk_option1_pos2):
                choice = 0
                break
            elif self.verificar_clique(click, self.atk_option2_pos1, self.atk_option2_pos2):
                choice = 1
                break
            elif self.verificar_clique(click, self.atk_option3_pos1, self.atk_option3_pos2):
                choice = 2
                break
            elif self.verificar_clique(click, self.atk_option4_pos1, self.atk_option4_pos2):
                choice = 3
                break
            elif self.verificar_clique(click, self.atk_back_pos1, self.atk_back_pos2):
                choice = -1
                break

        for item in f_txt:
            item.undraw()
        f_win.undraw()
        return choice

    def chose_pokemon(self):
        p_win = self.pokemon_btn()
        p_win.draw(self.janela)

        icon1, icon2, icon3, icon4, icon5, icon6 = self.select_pk_sprites()
        icon1.draw(self.janela)
        icon2.draw(self.janela)
        icon3.draw(self.janela)
        icon4.draw(self.janela)
        icon5.draw(self.janela)
        icon6.draw(self.janela)

        choice = -1
        while True:
            click = self.janela.getMouse()

            if self.verificar_clique(click, self.pk_back_pos1, self.pk_back_pos2) and self.allow_cancel == True:
                choice = -1
                icon1.undraw()
                icon2.undraw()
                icon3.undraw()
                icon4.undraw()
                icon5.undraw()
                icon6.undraw()
                break
            elif self.verificar_clique(click, self.pk_option1_pos1, self.pk_option1_pos2):
                choice = 0
                icon1.undraw()
                icon2.undraw()
                icon3.undraw()
                icon4.undraw()
                icon5.undraw()
                icon6.undraw()
                break
            elif self.verificar_clique(click, self.pk_option2_pos1, self.pk_option2_pos2):
                choice = 1
                icon1.undraw()
                icon2.undraw()
                icon3.undraw()
                icon4.undraw()
                icon5.undraw()
                icon6.undraw()
                break
            elif self.verificar_clique(click, self.pk_option3_pos1, self.pk_option3_pos2):
                choice = 2
                icon1.undraw()
                icon2.undraw()
                icon3.undraw()
                icon4.undraw()
                icon5.undraw()
                icon6.undraw()
                break
            elif self.verificar_clique(click, self.pk_option4_pos1, self.pk_option4_pos2):
                choice = 3
                icon1.undraw()
                icon2.undraw()
                icon3.undraw()
                icon4.undraw()
                icon5.undraw()
                icon6.undraw()
                break
            elif self.verificar_clique(click, self.pk_option5_pos1, self.pk_option5_pos2):
                choice = 4
                icon1.undraw()
                icon2.undraw()
                icon3.undraw()
                icon4.undraw()
                icon5.undraw()
                icon6.undraw()
                break
            elif self.verificar_clique(click, self.pk_option6_pos1, self.pk_option6_pos2):
                choice = 5
                icon1.undraw()
                icon2.undraw()
                icon3.undraw()
                icon4.undraw()
                icon5.undraw()
                icon6.undraw()
                break

        p_win.undraw()
        return choice
    
    def select_pk_sprites(self):
        self.player_pokemon1 = self.player.team[0]
        self.player_pokemon2 = self.player.team[1]
        self.player_pokemon3 = self.player.team[2]
        self.player_pokemon4 = self.player.team[3]
        self.player_pokemon5 = self.player.team[4]
        self.player_pokemon6 = self.player.team[5]
        
        sprite1 = self.player_pokemon1.sprite
        sprite2 = self.player_pokemon2.sprite
        sprite3 = self.player_pokemon3.sprite
        sprite4 = self.player_pokemon4.sprite
        sprite5 = self.player_pokemon5.sprite
        sprite6 = self.player_pokemon6.sprite

        #PK1---------------------------------
        if isinstance(sprite1, dict):
            if self.player_pokemon1.is_alive():
                filename = sprite1["icon"]
            else:
                filename = sprite1["icon_dead"]
        else:
            filename = sprite1

        path = self.get_path(f"pokemon/{filename}")

        self.pk_select_icon1 = gf.Image(self.select_poke_pos1, path)

        #PK2---------------------------------
        if isinstance(sprite2, dict):
            if self.player_pokemon2.is_alive():
                filename = sprite2["icon"]
            else:
                filename = sprite2["icon_dead"]
        else:
            filename = sprite2

        path = self.get_path(f"pokemon/{filename}")

        self.pk_select_icon2 = gf.Image(self.select_poke_pos2, path)

        #PK3---------------------------------
        if isinstance(sprite3, dict):
            if self.player_pokemon3.is_alive():
                filename = sprite3["icon"]
            else:
                filename = sprite3["icon_dead"]
        else:
            filename = sprite3

        path = self.get_path(f"pokemon/{filename}")

        self.pk_select_icon3 = gf.Image(self.select_poke_pos3, path)

        #PK4---------------------------------
        if isinstance(sprite4, dict):
            if self.player_pokemon4.is_alive():
                filename = sprite4["icon"]
            else:
                filename = sprite4["icon_dead"]
        else:
            filename = sprite4

        path = self.get_path(f"pokemon/{filename}")

        self.pk_select_icon4 = gf.Image(self.select_poke_pos4, path)

        #PK5---------------------------------
        if isinstance(sprite5, dict):
            if self.player_pokemon5.is_alive():
                filename = sprite5["icon"]
            else:
                filename = sprite5["icon_dead"]
        else:
            filename = sprite5

        path = self.get_path(f"pokemon/{filename}")

        self.pk_select_icon5 = gf.Image(self.select_poke_pos5, path)

        #PK6---------------------------------
        if isinstance(sprite6, dict):
            if self.player_pokemon6.is_alive():
                filename = sprite6["icon"]
            else:
                filename = sprite6["icon_dead"]
        else:
            filename = sprite6

        path = self.get_path(f"pokemon/{filename}")

        self.pk_select_icon6 = gf.Image(self.select_poke_pos6, path)
        

        return self.pk_select_icon1, self.pk_select_icon2, self.pk_select_icon3, self.pk_select_icon4, self.pk_select_icon5, self.pk_select_icon6

    def run(self):
        self.battle_hud.undraw()
        msg = gf.Image(gf.Point(self.width/2, self.height/2), self.get_path("run_msg.png"))
        msg.draw(self.janela)
        time.sleep(1)
        self.janela.close()
