from pathlib import Path

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
TILE_SIZE = 64

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
DATA_DIR = ROOT_DIR / "data"

POKECENTER_HEAL_ZONE = (573, 328, 841, 364)
