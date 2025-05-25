# 🐦 Flappy Bird Game



## 📄 Introduction

**My program is a remake of Flappy Bird — the viral mobile game that once had the whole world tapping their screens trying to beat their high scores.**

In my version, you control a little bird that flaps through gaps between pipes. Sounds simple, but the timing can be tricky — one wrong move and you crash! At the start, you can choose between three difficulty levels: Easy, Medium, or Hard. Each one changes how fast the pipes move and how wide the gaps are, so there’s a challenge for everyone.

The game includes smooth background scrolling, a live score counter, and a slightly forgiving hitbox so you don’t die from just grazing a pipe. Every time you make it past a pipe, your score goes up by one. If you hit a pipe or fall to the ground, the game ends and sends you back to the menu to try again.

It’s a fast, fun, and addictive game that’s all about reflexes and rhythm.
 Here’s my code below — feel free to check it out and try to beat your best score!

## 🎮 Gameplay Overview

- **Objective**: Navigate the bird through gaps between pipes without crashing.
- **Controls**: Click to make the bird flap upward.
- **Difficulty Levels**: Choose from Easy, Medium, or Hard, affecting pipe speed and gap size.
- **Scoring**: Earn points by successfully passing through pipe pairs.
- **Game Over**: Occurs upon collision with a pipe or the ground, followed by a return to the main menu.

## 🛠️ Project Structure

- `game_setup.py`: Handles asset loading, defines constants, and contains helper functions.
- `main.py`: Contains the main game loop, event handling, and game state management.
