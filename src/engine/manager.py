from src.lib import graphics as gf
from src import SCREEN_WIDTH, SCREEN_HEIGHT

class SceneManager:
    def __init__(self, player=None):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.window = gf.GraphWin("PokePy", self.width, self.height, autoflush=False)
        self.current_scene = None
        self.player = player


    def change_scene(self, new_scene_class, player=None, enemy=None):
        if self.current_scene is not None:
            if hasattr(self.current_scene, "unload"):
                self.current_scene.unload()

        if player is not None:
            self.player = player

        if enemy is not None:
            self.current_scene = new_scene_class(self.window, self.player, enemy)
        else:
            try:
                self.current_scene = new_scene_class(self.window, self.player)
            except TypeError:
                self.current_scene = new_scene_class(self.window)
