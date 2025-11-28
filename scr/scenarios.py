import time
import os
import graphics as gf

class BattleScene:
    def __init__(self):
        self.width = 1408
        self.height = 768

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.p1, self.p2 = gf.Point(826, 612), gf.Point(1000, 647)
        self.p3, self.p4 = gf.Point(826, 710), gf.Point(1068, 676)
        self.p5, self.p6 = gf.Point(1303, 647), gf.Point(1197, 612)
        self.p7, self.p8 = gf.Point(1303, 710), gf.Point(1197, 676)

        self.pk_back_pos1, self.pk_back_pos2 = gf.Point(1132, 653), gf.Point(1400, 753)
        self.pk_slots = [
            (gf.Point(90, 232), gf.Point(478, 387)),
            (gf.Point(512, 232), gf.Point(897, 387)),
            (gf.Point(927, 231), gf.Point(1319, 387)),
            (gf.Point(89, 418), gf.Point(481, 580)),
            (gf.Point(508, 418), gf.Point(900, 580)),
            (gf.Point(929, 418), gf.Point(1319, 580))
        ]

        self.atk_option1_pos1, self.atk_option1_pos2 = gf.Point(228, 628), gf.Point(344, 651)
        self.atk_option2_pos1, self.atk_option2_pos2 = gf.Point(513, 628), gf.Point(632, 651)
        self.atk_option3_pos1, self.atk_option3_pos2 = gf.Point(802, 628), gf.Point(921, 651)
        self.atk_option4_pos1, self.atk_option4_pos2 = gf.Point(1118, 628), gf.Point(1178, 651)
        self.atk_back_pos1, self.atk_back_pos2 = gf.Point(1132, 653), gf.Point(1400, 753)

        self.janela = self.win()

        self.draw_initial_screen()

    def get_path(self, filename):
        return os.path.join(self.base_dir, filename)

    def win(self):
        return gf.GraphWin("PokePy", self.width, self.height)

    def draw_initial_screen(self):
        center_bg = gf.Point(self.width / 2, self.height / 2)
        self.bg_img = gf.Image(center_bg, self.get_path("battlefield_final.png"))
        self.bg_img.draw(self.janela)

        center_hud = gf.Point(704, 675)
        self.hud_img = gf.Image(center_hud, self.get_path("battle_hud_final.png"))
        self.hud_img.draw(self.janela)

    def verificar_clique(self, click, p1, p2):
        x, y = click.getX(), click.getY()
        x_min, x_max = min(p1.getX(), p2.getX()), max(p1.getX(), p2.getX())
        y_min, y_max = min(p1.getY(), p2.getY()), max(p1.getY(), p2.getY())
        return (x_min <= x <= x_max) and (y_min <= y <= y_max)

    def fight_btn_img(self):
        return gf.Image(gf.Point(704, 675), self.get_path("white_hud.png"))

    def pokemon_btn_img(self):
        return gf.Image(gf.Point(self.width / 2, self.height / 2), self.get_path("pokemon_hud.png"))

    def bag_btn_img(self):
        return gf.Image(gf.Point(704, 675), self.get_path("white_hud.png"))

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

    # MÉTODOS DE AÇÃO (Chamados pelo Controller)

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
        f_win = self.fight_btn_img()
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
        p_win = self.pokemon_btn_img()
        p_win.draw(self.janela)

        choice = -1
        while True:
            click = self.janela.getMouse()

            if self.verificar_clique(click, self.pk_back_pos1, self.pk_back_pos2):
                choice = -1
                break

            for i, (p1, p2) in enumerate(self.pk_slots):
                if self.verificar_clique(click, p1, p2):
                    choice = i
                    break

            if choice != -1:
                break

        p_win.undraw()
        return choice

    def run(self):
        self.janela.close()
