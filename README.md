# <img src="bootdev-removebg-preview.png" alt="Asteroid Game Logo" width="40" style="margin-right: 5px;" /> Asteroids Game

A small Python game inspired by the classic *Asteroids*. Built using Pygame, and extended from 
*Build Asteroids using Python and Pygame*, a guided project from the learning platform **`Boot.dev`**

## 🧱 Original Guided Project Scope

The original project provided the foundational Asteroids game structure, including:

- Core game architecture with setup, game loop, and player movement

- Use of Pygame sprites and groups to manage game objects

- Asteroid spawning and splitting (large → medium → small)

- Basic shooting mechanics and asteroid destruction

- Collision detection (bullet–asteroid, player–asteroid)

## ✨ Extensions Beyond the Guided Project

I’ve expanded the original foundation with the following enhancements:

- Added a scoring system that rewards player accuracy 
 
- Implemented multiple lives and respawning mechanics  
- Added explosion effects when asteroids are destroyed  
- Introduced acceleration and deceleration to player movement  
- Asteroids now wrap around the screen instead of disappearing    
  *Not for the player — to simulate the feeling of being lost in tutorial hell*  
- Added a galaxy background for visual depth  
- Designed asteroids with 3 lumpy shapes instead of perfect circles  
- Introduced a shield power-up that destroys asteroids on contact  
- Added a laser power-up that removes the shooting cooldown  

## 🎥 Gameplay Demo

[![Watch the demo](https://img.youtube.com/vi/tTWmnWmyi64/hqdefault.jpg)](https://youtu.be/tTWmnWmyi64)

## 🛠 Requirements

- Python 3.8+
- Pygame

## 🚀 How to Run

1. Clone the repository into your current directory:

   ```bash
   git clone https://github.com/junhonglim49791/asteroids.git
   ```
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the game:
    ```bash
    python3 main.py
    ```
### 📝 Notes on Difficulty Settings

If you'd like to tweak the game difficulty, you can adjust the following constants in the `constants.py` :

- **`ASTEROID_SPAWN_RATE`**  
  Controls how frequently asteroids appear.  
  ⏱ *Lower values = faster spawn rate = harder*

- **`SHOT_RADIUS`**  
  Sets the size of the bullet.  
  🎯 *Larger bullets = easy kills*

- **`SHIELD_TRIGGER_COMBO`** or **`LASER_TRIGGER_COMBO`**  
  Number of **consecutive hits without missing** required to unlock the relevant power-up.  
  ⚡ *Lower value = easier to get*

- **`SHIELD_TIMER`** or **`LASER_TIMER`**   
  Duration that the power up remains active once triggered.  
  ⏳ *Higher value = longer activation time*