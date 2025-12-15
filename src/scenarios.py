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
        path = self.get_path(filename)

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
        path = self.get_path(filename)
        
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

        p_pos = gf.Point(60, 35)
        name = self.player_pokemon.name
        player_p_name = gf.Text(p_pos, name)
        player_p_name.setSize(18)
        p_lvl_pos = gf.Point(280, 35)
        p_level = self.player_pokemon.level
        player_p_lvl = gf.Text(p_lvl_pos, f"LVL {p_level}")
        player_p_lvl.setSize(18)

        e_pos = gf.Point(1107, 35)
        name = self.enemy_pokemon.name
        enemy_p_name = gf.Text(e_pos, name)
        enemy_p_name.setSize(18)
        e_lvl_pos = gf.Point(1318, 35)
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

        choice = -1
        while True:
            click = self.janela.getMouse()

            if self.verificar_clique(click, self.pk_back_pos1, self.pk_back_pos2) and self.allow_cancel == True:
                choice = -1
                break
            elif self.verificar_clique(click, self.pk_option1_pos1, self.pk_option1_pos2):
                choice = 0
                break
            elif self.verificar_clique(click, self.pk_option2_pos1, self.pk_option2_pos2):
                choice = 1
                break
            elif self.verificar_clique(click, self.pk_option3_pos1, self.pk_option3_pos2):
                choice = 2
                break
            elif self.verificar_clique(click, self.pk_option4_pos1, self.pk_option4_pos2):
                choice = 3
                break
            elif self.verificar_clique(click, self.pk_option5_pos1, self.pk_option5_pos2):
                choice = 4
                break
            elif self.verificar_clique(click, self.pk_option6_pos1, self.pk_option6_pos2):
                choice = 5
                break

        p_win.undraw()
        return choice

    def run(self):
        self.battle_hud.undraw()
        msg = gf.Image(gf.Point(self.width/2, self.height/2), self.get_path("run_msg.png"))
        msg.draw(self.janela)
        time.sleep(1)
        self.janela.close()
