import graphics as gf
from pathlib import Path
from src.classes import Trainer
import time

class BattleScene:
    def __init__(self, window):
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

        self.janela = window

        back = self.bg()
        battle_hud = self.hud()
        back.draw(self.janela)
        battle_hud.draw(self.janela)

    def get_path(self, filename):
        full_path = self.assets_dir / filename
        return str(full_path)

    def bg(self):
        return gf.Image(gf.Point(self.width / 2, self.height / 2), self.get_path("battlefield_final.png"))

    def hud(self):
        return gf.Image(gf.Point(704, 675), self.get_path("battle_hud_final.png"))

    def verificar_clique(self, click, p1, p2):
        x, y = click.getX(), click.getY()
        x_min, x_max = min(p1.getX(), p2.getX()), max(p1.getX(), p2.getX())
        y_min, y_max = min(p1.getY(), p2.getY()), max(p1.getY(), p2.getY())
        return (x_min <= x <= x_max) and (y_min <= y <= y_max)

    def fight_btn(self):
        img = gf.Image(gf.Point(704, 675), self.get_path("white_hud.png"))
        txt = gf.Text(gf.Point(286.1, 675), "ATAQUE 1")
        txt.setSize(18)
        return img

    def bag_btn(self):
        return gf.Image(gf.Point(704, 675), self.get_path("white_hud.png"))

    def pokemon_btn(self):
        return gf.Image(gf.Point(self.width / 2, self.height / 2), self.get_path("pokemon_hud.png"))

    def fight_txt(self):
        texts = []
        labels = ["ATAQUE 1", "ATAQUE 2", "ATAQUE 3", "ATAQUE 4"]
        for i, label in enumerate(labels):
            p = gf.Point(286.1 + (i * 286.1), 640)
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

        f_win.undraw()
        for item in f_txt:
            item.undraw()

        return choice

    def chose_pokemon(self):
        p_win = self.pokemon_btn()
        p_win.draw(self.janela)

        choice = -1
        while True:
            click = self.janela.getMouse()

            if self.verificar_clique(click, self.pk_back_pos1, self.pk_back_pos2):
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
        self.janela.close()


class WorldScene:
    def __init__(self, window, player: Trainer):
        self.window = window
        self.player = player
        self.map_width = 2752
        self.map_height = 1536
        self.screen_width = self.window.getWidth()
        self.screen_height = self.window.getHeight()

        self.root_dir = Path(__file__).resolve().parent.parent
        self.assets_dir = self.root_dir / "assets" / "images" / "characters" / "player"

        self.player_world_x = self.map_width / 2
        self.player_world_y = self.map_height / 2

        self.cam_x = self.player_world_x - (self.screen_width / 2)
        self.cam_y = self.player_world_y - (self.screen_height / 2)

        self.velocity = 10
        self.obstacles = [
            (0, 0, 2752, 20),      # Borda Superior
            (0, 0, 20, 1536),      # Borda Esquerda
            (2732, 0, 2752, 1536), # Borda Direita
            (0, 1516, 2752, 1536), # Borda Inferior
            (959, 514, 1275, 690), # Casa do Ash
            (1543, 518, 1862, 690), # Casa marrom
            (895, 648, 944, 690), # Caixa correio Ash
            (1483, 648, 1526, 690), # caixa correio marrom
            (941, 949, 1270, 1102), # Pokemarket
            (954, 1122, 1009, 1139), # placa pokemarket
            (1224, 1108, 1279, 1153), # placa pokemarket
            (1273, 1005, 1335, 1101), # barril pokemarket
            (857, 977, 935, 1030), # caixa grande pokemarket
            (877, 1030, 943, 1091), # caixa pequena pokemarket
            (1481, 900, 1925, 1072), # Lab. carvalho
            (711, 328, 1300, 328), # limite superior
            (1439, 328, 2085, 328), # limite superior
            (710, 328, 710, 1324), # Limite esquerda
            (2087, 328, 2087, 1412), # Limite direita
            (1343, 1410, 2080, 1410), # Limite inferir direita
            (710, 1306, 1311, 1306), # Limite inferior esquerda
            (1330, 1317, 1330, 1416), # limite inferior agua
            (1300, 0, 1300, 328), # saida superior
            (1439, 0, 1439, 328), # saida superior
            (1473, 1256, 1876, 1276), # cerca
            (820, 1179, 867, 1233), # npc mulher
            (1523, 1309, 1573, 1348) # npc homem

        ]
        self.occluders = [
            (959, 420, 1275, 690),   # Casa do Ash (Topo e Telhado)
            (1543, 420, 1862, 690),  # Casa Marrom (Topo e Telhado)
            (941, 820, 1270, 949),  # Pokemarket (Topo e Telhado)
            (1481, 820, 1925, 900)   # Lab. carvalho (Topo e Telhado)
        ]

        self.background = self._get_background()
        self.background.draw(self.window)

        self.player_sprite = self._get_player_sprite()
        self.player_sprite.draw(self.window)
        self.is_visible = True
        self.current_sprite_name = "up"

        self.keys = {"w": False, "s": False, "a": False, "d": False}
        self.window.master.bind("<KeyPress>", self._on_key_press)
        self.window.master.bind("<KeyRelease>", self._on_key_release)
        self.window.master.focus_set()

    def _on_key_press(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = True

    def _on_key_release(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys[key] = False

    def _get_background(self):
        map_path = self.root_dir / "assets" / "images" / "environment" / "maps" / "worldscene.png"
        return gf.Image(gf.Point(self.screen_width / 2, self.screen_height / 2), str(map_path))

    def _get_player_sprite(self):
        return gf.Image(gf.Point(self.screen_width / 2, self.screen_height / 2), self._get_path("player_sprite_up.png"))

    def _get_path(self, filename):
        full_path = self.assets_dir / filename
        return str(full_path)

    def _is_free(self, x, y):
        hitbox_w = 40
        hitbox_h = 20

        p_rect = (x - hitbox_w/2, y - hitbox_h/2, x + hitbox_w/2, y + hitbox_h/2)
        for obs in self.obstacles:
            if (p_rect[0] < obs[2] and p_rect[2] > obs[0] and
                p_rect[1] < obs[3] and p_rect[3] > obs[1]):
                return False
        return True

    def _is_occluded(self, x, y):
        for occ in self.occluders:
            if (occ[0] <= x <= occ[2] and occ[1] <= y <= occ[3]):
                return True
        return False

    def _set_player_sprite(self, direction_name):
        sprite_map = {
            "up": "player_sprite_up.png",
            "down": "player_sprite_down.png",
            "left": "player_sprite_left.png",
            "right": "player_sprite_right.png"
        }

        if direction_name != self.current_sprite_name:
            new_file = sprite_map.get(direction_name)

            if self.is_visible:
                self.player_sprite.undraw()

            new_sprite = gf.Image(
                gf.Point(self.screen_width / 2, self.screen_height / 2),
                self._get_path(new_file)
            )

            self.player_sprite = new_sprite
            self.current_sprite_name = direction_name

            if self.is_visible:
                self.player_sprite.draw(self.window)


    def update(self):
        is_moving = False
        old_world_x = self.player_world_x
        old_world_y = self.player_world_y
        old_cam_x = self.cam_x
        old_cam_y = self.cam_y

        dx, dy = 0, 0
        if self.keys["w"]:
            dy -= self.velocity
            is_moving = True
        elif self.keys["s"]:
            dy += self.velocity
            is_moving = True
        elif self.keys["a"]:
            dx -= self.velocity
            is_moving = True
        elif self.keys["d"]:
            dx += self.velocity
            is_moving = True

        future_x = self.player_world_x + dx
        future_y = self.player_world_y + dy

        if is_moving:
            if dy < 0:
                self._set_player_sprite("up")
            elif dy > 0:
                self._set_player_sprite("down")
            elif dx < 0:
                self._set_player_sprite("left")
            elif dx > 0:
                self._set_player_sprite("right")

        if dx != 0 and self._is_free(future_x, self.player_world_y):
            self.player_world_x = future_x

        if dy != 0 and self._is_free(self.player_world_x, future_y):
            self.player_world_y = future_y

        target_cam_x = self.player_world_x - (self.screen_width / 2)
        target_cam_y = self.player_world_y - (self.screen_height / 2)

        self.cam_x = max(0, min(target_cam_x, self.map_width - self.screen_width))
        self.cam_y = max(0, min(target_cam_y, self.map_height - self.screen_height))

        diff_cam_x = self.cam_x - old_cam_x
        diff_cam_y = self.cam_y - old_cam_y

        if diff_cam_x != 0 or diff_cam_y != 0:
            self.background.move(-diff_cam_x, -diff_cam_y)

        diff_world_x = self.player_world_x - old_world_x
        diff_world_y = self.player_world_y - old_world_y

        screen_move_x = diff_world_x - diff_cam_x
        screen_move_y = diff_world_y - diff_cam_y

        if screen_move_x != 0 or screen_move_y != 0:
            self.player_sprite.move(screen_move_x, screen_move_y)

        occluded = self._is_occluded(self.player_world_x, self.player_world_y)
        if occluded and self.is_visible:
            self.player_sprite.undraw()
            self.is_visible = False
        elif not occluded and not self.is_visible:
            self.player_sprite.draw(self.window)
            self.is_visible = True
