from src.config import DATA_DIR, IMAGES_DIR
import json

class WorldLogic:
    def __init__(
        self,
        screen_width,
        screen_height,
        map_name="pallet_town",
        map_width = 2752,
        map_height = 1536,
        velocity = 10,
        anim_speed = 2,
        start_x = None,
        start_y = None
    ):
        map_file = DATA_DIR / "map_data.json"
        with open(map_file, 'r') as f:
            data = json.load(f)

        if map_name not in data:
            raise ValueError(f"O mapa '{map_name}' não foi encontrado em map_data.json")

        current_map = data[map_name]

        self.obstacles = current_map.get("obstacles", [])
        self.occluders = current_map.get("occluders", [])

        self.map_width = current_map.get("width", map_width)
        self.map_height = current_map.get("height", map_height)

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.assets_dir = IMAGES_DIR / "characters" / "player"

        if start_x is not None:
            self.player_world_x = start_x
        else:
            self.player_world_x = self.map_width / 2

        if start_y is not None:
            self.player_world_y = start_y
        else:
            self.player_world_y = self.map_height / 2

        self.velocity = velocity
        self.current_sprite_name = "up"
        self.walk_index = 0
        self.anim_timer = 0
        self.anim_speed = anim_speed

        self.is_visible = True
        self.keys = {"w": False, "s": False, "a": False, "d": False}

        self.cam_x, self.cam_y = self._calculate_camera(self.player_world_x, self.player_world_y)

    def set_key(self, key, pressed):
        k = key.lower()
        if k in self.keys:
            self.keys[k] = pressed

    def get_sprite_filename(self, direction = None, index = None):
        d = direction if direction is not None else self.current_sprite_name
        i = index if index is not None else self.walk_index
        return f"player_sprite_{d}_{i}.png"

    def get_sprite_path(self, direction = None, index = None):
        return str(self.assets_dir / self.get_sprite_filename(direction, index))

    def _is_free(self, x, y):
        hitbox_w = 40
        hitbox_h = 20
        p_rect = (x - hitbox_w / 2, y - hitbox_h / 2, x + hitbox_w / 2, y + hitbox_h / 2)

        for obs in self.obstacles:
            if (
                p_rect[0] < obs[2] and p_rect[2] > obs[0] and
                p_rect[1] < obs[3] and p_rect[3] > obs[1]
            ):
                return False
        return True

    def _is_occluded(self, x, y):
        for occ in self.occluders:
            if (occ[0] <= x <= occ[2] and occ[1] <= y <= occ[3]):
                return True
        return False

    def _calculate_camera(self, target_x, target_y):
        desired_cam_x = target_x - (self.screen_width / 2)
        desired_cam_y = target_y - (self.screen_height / 2)

        if self.map_width < self.screen_width:
            cam_x = (self.map_width - self.screen_width) / 2
        else:
            cam_x = max(0, min(desired_cam_x, self.map_width - self.screen_width))

        if self.map_height < self.screen_height:
            cam_y = (self.map_height - self.screen_height) / 2
        else:
            cam_y = max(0, min(desired_cam_y, self.map_height - self.screen_height))

        return cam_x, cam_y

    def update(self):
        old_world_x = self.player_world_x
        old_world_y = self.player_world_y
        old_cam_x = self.cam_x
        old_cam_y = self.cam_y
        old_visible = self.is_visible

        is_moving = False
        new_direction = self.current_sprite_name
        dx, dy = 0, 0

        if self.keys["w"]:
            dy -= self.velocity
            is_moving = True
            new_direction = "up"
        elif self.keys["s"]:
            dy += self.velocity
            is_moving = True
            new_direction = "down"
        elif self.keys["a"]:
            dx -= self.velocity
            is_moving = True
            new_direction = "left"
        elif self.keys["d"]:
            dx += self.velocity
            is_moving = True
            new_direction = "right"

        sprite_changed = False
        if is_moving:
            self.anim_timer += 1
            if self.anim_timer > self.anim_speed:
                self.walk_index = 2 if self.walk_index == 1 else 1
                self.anim_timer = 0
                sprite_changed = True

            if new_direction != self.current_sprite_name:
                self.walk_index = 1
                self.anim_timer = 0
                sprite_changed = True
        else:
            if self.walk_index != 0:
                self.walk_index = 0
                sprite_changed = True
            self.anim_timer = 0

        self.current_sprite_name = new_direction

        future_x = self.player_world_x + dx
        future_y = self.player_world_y + dy

        if dx != 0 and self._is_free(future_x, self.player_world_y):
            self.player_world_x = future_x
        if dy != 0 and self._is_free(self.player_world_x, future_y):
            self.player_world_y = future_y

        self.cam_x, self.cam_y = self._calculate_camera(self.player_world_x, self.player_world_y)

        diff_cam_x = self.cam_x - old_cam_x
        diff_cam_y = self.cam_y - old_cam_y

        diff_world_x = self.player_world_x - old_world_x
        diff_world_y = self.player_world_y - old_world_y

        background_dx = -diff_cam_x
        background_dy = -diff_cam_y

        player_dx = diff_world_x - diff_cam_x
        player_dy = diff_world_y - diff_cam_y

        occluded = self._is_occluded(self.player_world_x, self.player_world_y)
        if occluded and self.is_visible:
            self.is_visible = False
        elif not occluded and not self.is_visible:
            self.is_visible = True
        visibility_changed = (self.is_visible != old_visible)

        sprite_path = self.get_sprite_path() if sprite_changed else None

        return {
            "background_dx": background_dx,
            "background_dy": background_dy,
            "player_dx": player_dx,
            "player_dy": player_dy,
            "sprite_changed": sprite_changed,
            "sprite_path": sprite_path,
            "sprite_visible": self.is_visible,
            "visibility_changed": visibility_changed,
            "world_x": self.player_world_x,
            "world_y": self.player_world_y,
            "cam_x": self.cam_x,
            "cam_y": self.cam_y,
            "direction": self.current_sprite_name,
            "walk_index": self.walk_index,
        }
