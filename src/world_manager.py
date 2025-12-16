import graphics as gf

class WorldManager:
    def __init__(self):
        self.width = 1600
        self.height = 900
        self.window = gf.GraphWin("PokePy", self.width, self.height, autoflush=False)
        self.current_scene = None


    def change_scene(self, new_scene_class):
        if self.current_scene is not None:
            if hasattr(self.current_scene, "unload"):
                self.current_scene.unload()

        self.current_scene = new_scene_class(self.window)
