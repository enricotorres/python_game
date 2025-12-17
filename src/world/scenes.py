from src.lib import graphics as gf
from src import Trainer
from src.world.logic import WorldLogic
from src import IMAGES_DIR, SCREEN_WIDTH, SCREEN_HEIGHT

class BaseWalkingScene:
    def __init__(self, window, player: Trainer, map_name: str, bg_image_rel_path: str, start_x=None, start_y=None):
        self.window = window
        self.player = player
        self.manager = getattr(self, "manager", None)
        self.npcs = []
        self.show_npc_markers = True
        self.screen_width = self.window.getWidth()
        self.screen_height = self.window.getHeight()

        px = getattr(self.player, "x", None)
        py = getattr(self.player, "y", None)
        if px == 0 and py == 0:
            px = None
            py = None
        sx = start_x if start_x is not None else px
        sy = start_y if start_y is not None else py

        self.logic = WorldLogic(
            self.screen_width,
            self.screen_height,
            map_name=map_name,
            start_x=sx,
            start_y=sy
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
        self.window.master.bind("<Return>", self._on_interact)
        self.window.master.bind("p", lambda event: self.toggle_debug())

    def _load_background(self, relative_path):

        full_path = IMAGES_DIR / relative_path
        return gf.Image(gf.Point(self.screen_width / 2, self.screen_height / 2), str(full_path))

    def _on_key_press(self, event):
        key = event.keysym.lower()
        self.logic.set_key(key, True)

    def _on_key_release(self, event):
        key = event.keysym.lower()
        self.logic.set_key(key, False)

    def add_npc(self, trainer: Trainer, x: int, y: int):
        npc = {"trainer": trainer, "x": x, "y": y}
        self.npcs.append(npc)


    def _find_nearby_npc(self, max_dist: int = 80):
        px = self.logic.player_world_x
        py = self.logic.player_world_y
        for npc in self.npcs:
            dx = npc["x"] - px
            dy = npc["y"] - py
            if (dx * dx + dy * dy) ** 0.5 <= max_dist:
                return npc
        return None

    def _on_interact(self, event):
        npc = self._find_nearby_npc()
        if npc is None:
            return
        if getattr(self, "manager", None) is None:
            return
        enemy_trainer = npc.get("trainer")
        if enemy_trainer is None:
            return
        self.player.x = self.logic.player_world_x
        self.player.y = self.logic.player_world_y
        if hasattr(self.player, "save_position"):
            self.player.save_position()
        from src.battle.scene import BattleScene
        self.manager.change_scene(BattleScene, enemy=enemy_trainer)

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
        self.window.master.unbind("<Return>")

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
