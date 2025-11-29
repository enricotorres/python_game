import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(ROOT_DIR, 'data')

MOVES_FILE = os.path.join(DATA_DIR, 'moves.json')
POKEDEX_FILE = os.path.join(DATA_DIR, 'pokedex.json')

def load_data():
    moves_data = {}
    pokedex_data = {}

    try:
        with open(MOVES_FILE, 'r', encoding='utf-8') as f:
            moves_data = json.load(f)

        with open(POKEDEX_FILE, 'r', encoding='utf-8') as f:
            pokedex_data = json.load(f)

        return moves_data, pokedex_data

    except FileNotFoundError as e:
        return {}, {}

MOVES_DB, POKEDEX_DB = load_data()
