from src.lib import graphics as gf
from src import Trainer
from src.world.logic import WorldLogic
from src import IMAGES_DIR, SCREEN_WIDTH, SCREEN_HEIGHT
from src.config import POKECENTER_HEAL_ZONE
import time

class BaseWalkingScene:
    def __init__(self, window, player: Trainer, map_name: str, bg_image_rel_path: str, start_x=None, start_y=None, **kwargs):
        self.window = window
        self.player = player
        self.manager = kwargs.get("manager", getattr(self, "manager", None))
        self.warps = []
        self.npcs = []
        self.show_npc_markers = True
        if hasattr(self.window, "resize"):
            self.window.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
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
        center_x = (self.logic.map_width / 2) - self.logic.cam_x
        center_y = (self.logic.map_height / 2) - self.logic.cam_y
        return gf.Image(gf.Point(center_x, center_y), str(full_path))

    def _on_key_press(self, event):
        key = event.keysym.lower()
        self.logic.set_key(key, True)

    def _on_key_release(self, event):
        key = event.keysym.lower()
        self.logic.set_key(key, False)

    def add_npc(self, trainer: Trainer, x: int, y: int):
        trainer.x = x
        trainer.y = y
        npc = {"trainer": trainer, "x": x, "y": y}
        self.npcs.append(npc)

    def add_warp(self, x: int, y: int, target_scene_class, target_x=None, target_y=None):
        warp = {
            "x": x, "y": y,
            "target_scene": target_scene_class,
            "tx": target_x, "ty": target_y
        }
        self.warps.append(warp)

    def _find_nearby_warp(self, max_dist: int = 120):
        px = self.logic.player_world_x
        py = self.logic.player_world_y
        for warp in self.warps:
            dx = warp["x"] - px
            dy = warp["y"] - py
            if (dx * dx + dy * dy) ** 0.5 <= max_dist:
                return warp
        return None

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
        warp = self._find_nearby_warp()
        if warp:
            self.player.x = self.logic.player_world_x
            self.player.y = self.logic.player_world_y

            self.manager.change_scene(
                warp["target_scene"],
                manager=self.manager,
                player=self.player,
                start_x=warp["tx"],
                start_y=warp["ty"]
            )
            return

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
        self.manager.change_scene(BattleScene, player=self.player, enemy=enemy_trainer)

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

        for warp in self.warps:
            wx, wy = warp["x"]-cam_x, warp["y"]-cam_y
            circ = gf.Circle(gf.Point(wx, wy), 30)
            circ.setOutline("blue")
            circ.setWidth(3)
            circ.draw(self.window)
            self.debug_shapes.append(circ)


class WorldScene(BaseWalkingScene):
    def __init__(self, window, player: Trainer, **kwargs):
        super().__init__(
            window,
            player,
            map_name="pallet_town",
            bg_image_rel_path="environment/maps/worldscene2.png",
            **kwargs
        )
        self.add_warp(
            x=1122,
            y=1106,
            target_scene_class=PokecenterScene,
            target_x=780,
            target_y=800
        )


class PokecenterScene(BaseWalkingScene):
    def __init__(self, window, player: Trainer, **kwargs):
        sy = kwargs.pop("start_y", 800)
        sx = kwargs.pop("start_x", None)
        super().__init__(
            window,
            player,
            map_name="pokecenter",
            bg_image_rel_path="environment/maps/pokecenter.png",
            start_x=sx,
            start_y=sy,
            **kwargs
        )
        self.add_warp(
            x=750,
            y=810,
            target_scene_class=WorldScene,
            target_x=1122,
            target_y=1140
        )
        self.heal_zone = POKECENTER_HEAL_ZONE

    def _is_in_heal_zone(self, x: float, y: float) -> bool:
        x1, y1, x2, y2 = self.heal_zone
        return (x1 <= x <= x2) and (y1 <= y <= y2)

    def _show_heal_message(self, text: str = "Seus Pokémon foram curados!"):
        cx = self.screen_width / 2
        cy = self.screen_height / 2
        bg = gf.Rectangle(gf.Point(cx - 240, cy - 50), gf.Point(cx + 240, cy + 50))
        bg.setFill("white")
        bg.setOutline("black")
        msg = gf.Text(gf.Point(cx, cy), text)
        msg.setSize(20)
        msg.setTextColor("black")

        bg.draw(self.window)
        msg.draw(self.window)
        gf.update()
        time.sleep(1.0)
        msg.undraw()
        bg.undraw()

    def _on_interact(self, event):
        px = self.logic.player_world_x
        py = self.logic.player_world_y

        if self._is_in_heal_zone(px, py):
            self.player.heal_team()
            self._show_heal_message()
            return
