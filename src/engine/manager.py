from src.lib import graphics as gf
from src import SCREEN_WIDTH, SCREEN_HEIGHT

class SceneManager:
    def __init__(self, player=None):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.window = gf.GraphWin("PokePy", self.width, self.height, autoflush=False)
        self.current_scene = None
        self.player = player
        # Armazena NPCs por cena (chave = nome da classe da cena) para persistência entre trocas
        self._npcs_by_scene: dict[str, list[dict]] = {}

    def change_scene(self, new_scene_class, *args, **kwargs):
        if self.current_scene is not None:
            # Antes de descarregar, persistimos os NPCs da cena atual (por tipo de cena)
            try:
                scene_key = self.current_scene.__class__.__name__
                current_npcs = getattr(self.current_scene, "npcs", [])
                to_save: list[dict] = []
                for npc in current_npcs or []:
                    if isinstance(npc, dict):
                        trainer = npc.get("trainer")
                        x = npc.get("x")
                        y = npc.get("y")
                        if trainer is not None:
                            to_save.append({"trainer": trainer, "x": x, "y": y})
                # Dedup por identidade do objeto trainer
                seen = set()
                deduped = []
                for entry in to_save:
                    tid = id(entry["trainer"])
                    if tid in seen:
                        continue
                    seen.add(tid)
                    deduped.append(entry)
                self._npcs_by_scene[scene_key] = deduped
            except Exception:
                pass

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
            # Sinaliza o "map_name" na cena (usando o nome da classe como identificador do mapa)
            try:
                setattr(self.current_scene, "map_name", self.current_scene.__class__.__name__)
            except Exception:
                pass

            # 4. Restaura NPCs persistidos desta cena, evitando duplicação
            try:
                restore_key = self.current_scene.__class__.__name__
                restore_list = self._npcs_by_scene.get(restore_key, []) or []
                if hasattr(self.current_scene, "add_npc") and hasattr(self.current_scene, "npcs"):
                    existing = getattr(self.current_scene, "npcs", []) or []

                    def has_trainer(tr):
                        for ex in existing:
                            try:
                                t_ex = ex.get("trainer")
                                if t_ex is tr:
                                    return True
                                # fallback por nome caso sejam instâncias iguais por valor
                                if hasattr(t_ex, "name") and hasattr(tr, "name") and t_ex.name == tr.name:
                                    return True
                            except Exception:
                                continue
                        return False

                    for entry in restore_list:
                        tr = entry.get("trainer")
                        x = entry.get("x", 0)
                        y = entry.get("y", 0)
                        if tr is not None and not has_trainer(tr):
                            self.current_scene.add_npc(tr, x=x, y=y)
            except Exception:
                pass

        except Exception as e:
            print(f"ERRO CRÍTICO ao criar a cena {new_scene_class.__name__}: {e}")
            raise e

    def close(self):
        self.window.close()
