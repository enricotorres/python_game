import json
from src.config import DATA_DIR
import logging

logger = logging.getLogger(__name__)

# Using DATA_DIR from central config
MOVES_FILE = DATA_DIR / "moves.json"
POKEDEX_FILE = DATA_DIR / "pokedex.json"
ITEMS_FILE = DATA_DIR / "items.json"
TYPES_FILE = DATA_DIR / "types.json"

def load_data():
    moves_data = {}
    pokedex_data = {}
    items_data = {}

    try:
        if not MOVES_FILE.exists() or not POKEDEX_FILE.exists() or not ITEMS_FILE.exists():
            logger.critical(f"Arquivos de dados não encontrados em: {DATA_DIR}")
            return {}, {}, {}, {}

        moves_data = json.loads(MOVES_FILE.read_text(encoding="utf-8"))
        pokedex_data = json.loads(POKEDEX_FILE.read_text(encoding="utf-8"))
        items_data = json.loads(ITEMS_FILE.read_text(encoding="utf-8"))
        types_data = json.loads(TYPES_FILE.read_text(encoding="utf-8"))

        logger.info("Banco de dados carregado com sucesso")
        return moves_data, pokedex_data, items_data, types_data

    except json.JSONDecodeError as e:
        logger.error(f"Erro de sintaxe nos arquivos JSON: {e}")
        return {}, {}, {}, {}

    except Exception as e:
        logger.error(f"Erro fatal ao carregar dados: {e}")
        return {}, {}, {}, {}

MOVES_DB, POKEDEX_DB, ITEMS_DB, TYPES_DB = load_data()
