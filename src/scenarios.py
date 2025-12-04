import graphics as gf
from pathlib import Path
from src.classes import Pokemon
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
    def __init__(self, window, player: "Pokemon"):
        self.window = window
        self.player = player
        self.width = 2752
        self.height = 1536

        self.root_dir = Path(__file__).resolve().parent.parent
        self.assets_dir = self.root_dir / "assets" / "images"

        self.background = self._get_background()
        self.background.draw(self.window)

        self.velocity = 15

        self.current_x = self.window.getWidth() / 2
        self.current_y = self.window.getHeight() / 2


    def _get_background(self):
        center_x = self.window.getWidth() / 2
        center_y = self.window.getHeight() / 2
        return gf.Image(gf.Point(center_x, center_y), self._get_path("worldscene.png"))

    def _get_path(self, filename):
        full_path = self.assets_dir / filename
        return str(full_path)

    def update(self):
        key = self.window.checkKey()
        dx = 0
        dy = 0
        print(key)

        if key == "w":
            dy =+ self.velocity
        elif key == "s":
            dy =- self.velocity
        elif key == "a":
            dx =+ self.velocity
        elif key == "d":
            dx =- self.velocity

        if dx != 0 or dy != 0:
            self.background.move(dx, dy)
            self.current_x += dx
            self.current_y += dy
