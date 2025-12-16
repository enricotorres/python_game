import graphics as gf

class WorldManager:
    def __init__(self, player=None):
        self.width = 1600
        self.height = 900
        self.window = gf.GraphWin("PokePy", self.width, self.height, autoflush=False)
        self.current_scene = None
        self.player = player


    def change_scene(self, new_scene_class, player=None):
        if self.current_scene is not None:
            if hasattr(self.current_scene, "unload"):
                self.current_scene.unload()

        if player is not None:
            self.player = player

        try:
            self.current_scene = new_scene_class(self.window, self.player)
        except TypeError:
            self.current_scene = new_scene_class(self.window)
