from src.lib import graphics as gf
from src import SCREEN_WIDTH, SCREEN_HEIGHT

class SceneManager:
    def __init__(self, player=None):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.window = gf.GraphWin("PokePy", self.width, self.height, autoflush=False)
        self.current_scene = None
        self.player = player

    def change_scene(self, new_scene_class, *args, **kwargs):
        if self.current_scene is not None:
            if hasattr(self.current_scene, "unload"):
                self.current_scene.unload()

        # 1. Se quem chamou passou um novo player, atualizamos o nosso
        if "player" in kwargs:
            self.player = kwargs["player"]

        # 2. AUTO-CORREÇÃO: Se quem chamou ESQUECEU de passar o player
        if "player" not in kwargs and self.player is not None:
            kwargs["player"] = self.player

        # --- O ERRO ESTÁ AQUI: FALTOU ESTA LINHA ---
        # O Manager precisa se passar para a próxima cena, senão a próxima cena
        # não consegue chamar o change_scene depois.
        kwargs["manager"] = self 
        # -------------------------------------------

        # 3. Cria a nova cena
        try:
            self.current_scene = new_scene_class(self.window, *args, **kwargs)
        except Exception as e:
            print(f"ERRO CRÍTICO ao criar a cena {new_scene_class.__name__}: {e}")
            raise e

    def close(self):
        self.window.close()