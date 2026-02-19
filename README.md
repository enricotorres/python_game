# 🎮 PokéPy

A Pokémon-inspired RPG built entirely in Python, featuring an explorable overworld, turn-based battles, NPC trainers, and a PokéCenter — all rendered with a custom graphics engine.

---

## 📸 Preview

```
Overworld ──► Enter Building ──► Battle NPC ──► Return to World
                    │
              PokéCenter
              (Heal Team)
```

---

## ✨ Features

- **Explorable Overworld** — Walk around Pallet Town with smooth tile-based movement and collision detection
- **Turn-Based Battles** — Full damage formula with STAB, type effectiveness, critical hits, weather, and multi-hit moves
- **Battle AI** — Enemy trainer uses the best move by calculated damage, and heals when HP is low
- **NPC Trainers** — Interact with trainers in the world to trigger battles
- **PokéCenter** — Enter the building and heal your whole team at the counter
- **Scene Warps** — Walk through doors and transition between maps seamlessly
- **Occlusion System** — Player sprite hides behind buildings and objects automatically
- **Animated Player Sprite** — 4-directional walking animation (idle, walk frames)
- **Type Chart** — All 18 types with full effectiveness table
- **Item System** — Potions, Revives, status cures, and more, usable in battle
- **Debug Mode** — Press `P` in-game to toggle collision box and warp zone overlays

---

## 🗂️ Project Structure

```
.
├── assets/
│   └── images/
│       ├── characters/player/     # Player walk sprites (4 directions × 3 frames)
│       ├── environment/maps/      # Map backgrounds (worldscene2.png, pokecenter.png, ...)
│       ├── pokemon/               # Pokémon front/back/dead sprites
│       └── ui/battle/             # HUD images for the battle screen
├── data/
│   ├── map_data.json              # Obstacle and occluder zones per map
│   ├── moves.json                 # Move database (power, accuracy, type, effect, PP)
│   ├── pokedex.json               # Pokémon base stats and types
│   ├── items.json                 # Item database (heal, revive, capture, status)
│   └── types.json                 # Type effectiveness chart
└── src/
    ├── app.py                     # Entry point — creates trainers and starts the game
    ├── config.py                  # Screen resolution, paths, constants
    ├── core/
    │   ├── database.py            # Loads all JSON data at startup
    │   └── models/entities.py     # Pokémon, Move, Item, Trainer classes
    ├── engine/
    │   └── manager.py             # SceneManager — handles scene transitions and NPC persistence
    ├── world/
    │   ├── logic.py               # WorldLogic — movement, camera, collision (pure logic, no rendering)
    │   └── scenes.py              # BaseWalkingScene, WorldScene, PokecenterScene
    ├── battle/
    │   ├── scene.py               # BattleScene — renders and drives the battle loop
    │   ├── controller.py          # BattleController — turn order, action resolution, end conditions
    │   └── mechanics.py           # DamageCalculator, BattleAI, AccuracyCalculator, MoveEffectResolver
    └── lib/
        └── graphics.py            # Tkinter-based graphics engine wrapper
```

---

## ⚙️ Requirements

- **Python 3.10+**
- No external libraries required — uses only the Python standard library (`tkinter`, `json`, `math`, `random`, `logging`)

---

## 🚀 Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/your-username/pokepy.git
cd pokepy
```

**2. Run the game**

```bash
python src/app.py
```

> Make sure you run from the project root so that relative paths to `assets/` and `data/` resolve correctly.

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| `W` | Move up |
| `S` | Move down |
| `A` | Move left |
| `D` | Move right |
| `Enter` | Interact (warp / talk to NPC / trigger battle) |
| `P` | Toggle debug overlay (collision boxes, warp zones) |

---

## 🗺️ Maps

| Map | Description |
|-----|-------------|
| `pallet_town` | Overworld — explore, find NPCs, enter buildings |
| `pokecenter` | Interior — walk to the counter and press Enter to heal your team |

Map data (obstacle rectangles, occluder zones, dimensions) is defined in `data/map_data.json`. New maps can be added there and referenced in `scenes.py`.

---

## ⚔️ Battle System

Damage is calculated using a formula faithful to the main series games:

```
Damage = floor(((2×Level/5 + 2) × Power × Atk/Def) / 50 + 2)
       × TypeEffectiveness × STAB × CritMultiplier × RandomFactor × WeatherModifier
```

**Supported mechanics:**
- Physical vs Special category split
- STAB (Same Type Attack Bonus) — 1.5×
- Full type effectiveness table (immune / 0.5× / 1× / 2×)
- Critical hits — 6% base rate, 12% with high-crit moves
- Weather — Rain boosts Water/weakens Fire; Sun boosts Fire/weakens Water
- Multi-hit moves
- Stat stage modifiers (±6 stages)
- Status conditions (burn, paralysis, poison, sleep, freeze)
- Accuracy and evasion checks

---

## 🧠 Battle AI

The enemy AI evaluates every available move and selects the one with the highest expected damage against the player's active Pokémon. If the enemy's HP drops below 30%, it will attempt to use a healing item before attacking.

---

## 📦 Item System

Items can be used in battle from the Bag menu. Supported effects:

| Category | Examples |
|----------|---------|
| Healing | Potion, Super Potion, Hyper Potion, Max Potion, Full Restore |
| Revive | Revive (50% HP), Max Revive (full HP) |
| Status Cure | Antidote, Paralyze Heal, Burn Heal, Awakening, Full Heal |
| Capture | Poké Ball, Great Ball, Ultra Ball, Master Ball |

---

## 🔧 Configuration

Key constants are defined in `src/config.py`:

```python
SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 900
POKECENTER_HEAL_ZONE = (573, 328, 841, 364)  # Rectangle (x1, y1, x2, y2) in world coords
```

---

## 🗺️ Adding Content

### New Pokémon
Add an entry to `data/pokedex.json` with base stats, types, and learnset. Add front/back/dead sprites to `assets/images/pokemon/`.

### New Moves
Add an entry to `data/moves.json` with power, accuracy, type, category, PP, and optional effect payload.

### New Map
Add an entry to `data/map_data.json` with `width`, `height`, `obstacles`, and `occluders`. Create a scene class in `src/world/scenes.py` extending `BaseWalkingScene`.

### New NPC
In `src/app.py`, create a `Trainer` with a team and call `scene.add_npc(trainer, x=..., y=...)`.

---

## 🐛 Known Limitations

- Defeated NPCs respawn after scene transitions
- No save/load system
- Graphics engine is Tkinter-based — performance is limited compared to Pygame

---

## 📄 License

This project is for educational and personal use. Pokémon is a registered trademark of Nintendo / Creatures Inc. / GAME FREAK inc. This project is not affiliated with or endorsed by them.
