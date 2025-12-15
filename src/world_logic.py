from pathlib import Path

class WorldLogic:
    def __init__(
        self,
        screen_width,
        screen_height,
        map_width = 2752,
        map_height = 1536,
        velocity = 10,
        anim_speed = 2,
    ):
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.root_dir = Path(__file__).resolve().parent.parent
        self.assets_dir = self.root_dir / "assets" / "images" / "characters" / "player"

        self.player_world_x = self.map_width / 2
        self.player_world_y = self.map_height / 2

        self.cam_x = self.player_world_x - (self.screen_width / 2)
        self.cam_y = self.player_world_y - (self.screen_height / 2)

        self.velocity = velocity
        self.current_sprite_name = "up"
        self.walk_index = 0
        self.anim_timer = 0
        self.anim_speed = anim_speed

        self.is_visible = True

        self.keys = {"w": False, "s": False, "a": False, "d": False}

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
            (941, 820, 1270, 949),   # Pokemarket (Topo e Telhado)
            (1481, 820, 1925, 900)   # Lab. carvalho (Topo e Telhado)
        ]

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

        target_cam_x = self.player_world_x - (self.screen_width / 2)
        target_cam_y = self.player_world_y - (self.screen_height / 2)

        self.cam_x = max(0, min(target_cam_x, self.map_width - self.screen_width))
        self.cam_y = max(0, min(target_cam_y, self.map_height - self.screen_height))

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
