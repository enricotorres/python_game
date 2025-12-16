import graphics as gf
from pathlib import Path
from src.classes import Trainer
from src.world_logic import WorldLogic

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

    def unload(self):
        self.back.undraw()
        self.battle_hud.undraw()


class BaseWalkingScene:
    def __init__(self, window, player: Trainer, map_name: str, bg_image_rel_path: str, start_x=None, start_y=None):
        self.window = window
        self.player = player
        self.screen_width = self.window.getWidth()
        self.screen_height = self.window.getHeight()
        self.root_dir = Path(__file__).resolve().parent.parent

        self.logic = WorldLogic(
            self.screen_width,
            self.screen_height,
            map_name=map_name,
            start_x=start_x,
            start_y=start_y
        )

        self.background = self._load_background(bg_image_rel_path)
        self.background.draw(self.window)

        initial_sprite_x = self.logic.player_world_x - self.logic.cam_x
        initial_sprite_y = self.logic.player_world_y - self.logic.cam_y

        self.player_sprite = gf.Image(
            gf.Point(initial_sprite_x, initial_sprite_y),
            self.logic.get_sprite_path()
        )

        self.player_sprite.draw(self.window)
        self.is_visible = True

        self.window.master.bind("<KeyPress>", self._on_key_press)
        self.window.master.bind("<KeyRelease>", self._on_key_release)
        self.window.master.focus_set()
        self.window.master.bind("p", lambda event: self.toggle_debug())

    def _load_background(self, relative_path):

        full_path = self.root_dir / "assets" / "images" / relative_path
        return gf.Image(gf.Point(self.screen_width / 2, self.screen_height / 2), str(full_path))

    def _on_key_press(self, event):
        key = event.keysym.lower()
        self.logic.set_key(key, True)

    def _on_key_release(self, event):
        key = event.keysym.lower()
        self.logic.set_key(key, False)

    def update(self):
        result = self.logic.update()

        if result["background_dx"] != 0 or result["background_dy"] != 0:
            self.background.move(result["background_dx"], result["background_dy"])

        if result["sprite_changed"]:
            current_pos = self.player_sprite.getAnchor()
            if self.is_visible:
                self.player_sprite.undraw()
            self.player_sprite = gf.Image(current_pos, result["sprite_path"])
            if self.is_visible:
                self.player_sprite.draw(self.window)

        if result["player_dx"] != 0 or result["player_dy"] != 0:
            self.player_sprite.move(result["player_dx"], result["player_dy"])

        if result["visibility_changed"]:
            if result["sprite_visible"] and not self.is_visible:
                self.player_sprite.draw(self.window)
            elif not result["sprite_visible"] and self.is_visible:
                self.player_sprite.undraw()
            self.is_visible = result["sprite_visible"]

    def unload(self):
        self.background.undraw()
        self.player_sprite.undraw()
        self.is_visible = False
        self.window.master.unbind("<KeyPress>")
        self.window.master.unbind("<KeyRelease>")

    def toggle_debug(self):

        if not hasattr(self, "debug_shapes"):
            self.debug_shapes = []

        if self.debug_shapes:
            for shape in self.debug_shapes:
                shape.undraw()
            self.debug_shapes = []
            return

        cam_x = self.logic.cam_x
        cam_y = self.logic.cam_y

        for obs in self.logic.obstacles:
            x1 = obs[0] - cam_x
            y1 = obs[1] - cam_y
            x2 = obs[2] - cam_x
            y2 = obs[3] - cam_y

            rect = gf.Rectangle(gf.Point(x1, y1), gf.Point(x2, y2))
            rect.setOutline("red")
            rect.setWidth(2)
            rect.draw(self.window)
            self.debug_shapes.append(rect)


class WorldScene(BaseWalkingScene):
    def __init__(self, window, player: Trainer):
        super().__init__(
            window,
            player,
            map_name="pallet_town",
            bg_image_rel_path="environment/maps/worldscene2.png"
        )


class PokecenterScene(BaseWalkingScene):
    def __init__(self, window, player: Trainer):
        super().__init__(
            window,
            player,
            map_name="pokecenter",
            bg_image_rel_path="environment/maps/pokecenter.png",
            start_y=800
        )
