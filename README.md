# Roguelike Game

A single-player roguelike game developed in Python using the Pygame library. Built as part of my qualification work to demonstrate game design principles such as procedural map generation, permadeath, and player progression.

## 🎯 Game Overview

- **Genre:** Roguelike, RPG
- **Platform:** Windows & Linux
- **Technologies:** Python, Pygame
- **Key Concepts:** Procedural generation, OOP, sprite management, real-time combat

The game offers unique runs every time thanks to procedurally generated maps and randomized enemy encounters. Play as either a **Knight** or **Mage**, each with distinct combat styles, and try to survive against hordes of enemies with increasing difficulty.

## 🕹️ Controls

| Action | Input |
|--------|-------|
| Move   | `W`, `A`, `S`, `D` |
| Attack | Left Mouse Button |
| Pause  | `ESC` |
| Interact | Automatic on contact (e.g. potions, experience) |

## 🧩 Features

- 🗺️ **Procedural Map Generation** – Each playthrough features a unique map layout.
- 💀 **Permadeath** – When you die, your progress is lost—start again!
- ⚔️ **Playable Classes** – Choose between:
  - **Knight**: Melee-focused
  - **Mage**: Ranged attacks
- 📈 **Leveling & Upgrades** – Gain XP, level up, and upgrade your stats.
- 🧟‍♂️ **Dynamic Enemy Scaling** – Enemies grow stronger as you do.
- 🧪 **Item Drops** – Health potions and XP crystals drop from enemies.
- 🧙‍♂️ **Horde Attacks** – Face groups of weaker enemies in tense survival moments.
- 🪟 **Resizable Window / Fullscreen Mode** – Configurable screen options.

## 📦 Installation

### Run from source

> Requires Python 3.10+ and Pygame

```bash
pip install pygame
python main.py
```

## 🛠️ Development Notes
This project was built from scratch and includes:
-Modular OOP design using custom classes for characters, items, projectiles, and enemies
-Real-time collision and interaction logic
-Dynamic camera and background tile rendering
-Custom-designed enemy AI that tracks player position
-Hand-crafted procedural map generation logic
