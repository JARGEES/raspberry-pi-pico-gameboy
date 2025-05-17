from PicoGameBoy import PicoGameBoy
from time import sleep, ticks_ms, ticks_diff
import random
import math

# Initialize game
pgb = PicoGameBoy()

# Define colors
BLACK = PicoGameBoy.color(0, 0, 0)
WHITE = PicoGameBoy.color(255, 255, 255)
RED = PicoGameBoy.color(255, 0, 0)
GREEN = PicoGameBoy.color(0, 255, 0)
BLUE = PicoGameBoy.color(0, 0, 255)
YELLOW = PicoGameBoy.color(255, 255, 0)
PURPLE = PicoGameBoy.color(255, 0, 255)
CYAN = PicoGameBoy.color(0, 255, 255)
ORANGE = PicoGameBoy.color(255, 128, 0)

# Define sprites (authentic Space Invaders style)
def make_sprite_from_pixels(pixel_data, width, height, color):
    buffer = bytearray(width * height * 2)
    for y in range(height):
        for x in range(width):
            idx = 2 * (y * width + x)
            if y < len(pixel_data) and x < len(pixel_data[y]) and pixel_data[y][x]:
                buffer[idx] = color & 0xFF
                buffer[idx + 1] = (color >> 8) & 0xFF
            else:
                buffer[idx] = BLACK & 0xFF
                buffer[idx + 1] = (BLACK >> 8) & 0xFF
    return buffer

# Invader Type 1 (Squid) - 12x8 pixels
invader1_pixels = [
    [0,0,0,0,1,1,1,1,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,0,0,1,1,1,1,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,1,1,1,0,0,1,1,1,0,0],
    [0,1,1,0,0,1,1,0,0,1,1,0],
    [0,0,1,1,0,0,0,0,1,1,0,0]
]

# Invader Type 2 (Crab) - 12x8 pixels
invader2_pixels = [
    [0,0,1,0,0,0,0,0,0,1,0,0],
    [0,0,0,1,0,0,0,0,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,0,1,1,1,1,0,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,1],
    [0,0,0,1,1,0,0,1,1,0,0,0]
]

# Invader Type 3 (Octopus) - 12x8 pixels
invader3_pixels = [
    [0,0,0,1,1,1,1,1,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,1,1,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,1,1,0,0,1,1,0,0,0],
    [0,0,1,1,0,1,1,0,1,1,0,0],
    [1,1,0,0,0,0,0,0,0,0,1,1]
]

# Invader alternate frames for animation
invader1_alt_pixels = [
    [0,0,0,0,1,1,1,1,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,0,0,1,1,1,1,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,1,1,1,0,0,1,1,1,0,0],
    [0,1,1,0,0,1,1,0,0,1,1,0],
    [1,1,0,0,0,0,0,0,0,0,1,1]
]

invader2_alt_pixels = [
    [0,0,1,0,0,0,0,0,0,1,0,0],
    [1,0,0,1,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1],
    [1,1,1,0,1,1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,1,0,0,0,0,0,0,1,0,0],
    [0,1,0,0,0,0,0,0,0,0,1,0]
]

invader3_alt_pixels = [
    [0,0,0,1,1,1,1,1,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,1,1,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,1,1,0,1,1,0,1,1,0,0],
    [0,1,1,0,1,1,1,1,0,1,1,0],
    [0,0,1,1,0,0,0,0,1,1,0,0]
]

# Boss enemy - 20x16 pixels
boss_pixels = [
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0],
    [0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0]
]

boss_alt_pixels = [
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0],
    [0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0]
]

# Player ship - 16x8 pixels
player_pixels = [
    [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Shield part - 8x8 pixels
shield_pixels = [
    [0,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,0,0,1,1,1],
    [1,1,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,1]
]

# Mystery ship - 16x7 pixels
mystery_pixels = [
    [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0]
]

# Explosion - 12x8 pixels
explosion_pixels = [
    [0,1,0,0,0,1,0,0,1,0,1,0],
    [0,0,1,0,0,0,0,1,0,0,0,1],
    [0,0,0,1,0,0,1,0,0,0,1,0],
    [1,1,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,1,1],
    [1,0,0,0,1,0,1,0,0,1,0,0],
    [0,1,1,0,0,0,0,0,1,0,0,0],
    [0,0,0,1,0,1,0,1,0,0,1,0]
]

# Missile powerup - 6x10 pixels
missile_pixels = [
    [0,0,1,1,0,0],
    [0,1,1,1,1,0],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [0,1,1,1,1,0],
    [0,1,1,1,1,0],
    [0,0,1,1,0,0],
    [0,0,1,1,0,0],
    [0,0,1,1,0,0]
]

# Heat indicator - 3x8 pixels
heat_pixel = [
    [1,1,1],
    [1,1,1],
    [1,1,1],
    [1,1,1],
    [1,1,1],
    [1,1,1],
    [1,1,1],
    [1,1,1]
]

# Define dimensions
INVADER_WIDTH = 12
INVADER_HEIGHT = 8
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 8
SHIELD_SIZE = 8
MYSTERY_WIDTH = 16
MYSTERY_HEIGHT = 7
BOSS_WIDTH = 20
BOSS_HEIGHT = 16
MISSILE_WIDTH = 6
MISSILE_HEIGHT = 10
HEAT_WIDTH = 3
HEAT_HEIGHT = 8

# Create all sprites
pgb.add_sprite(make_sprite_from_pixels(invader1_pixels, INVADER_WIDTH, INVADER_HEIGHT, GREEN), INVADER_WIDTH, INVADER_HEIGHT)  # Sprite 0
pgb.add_sprite(make_sprite_from_pixels(invader1_alt_pixels, INVADER_WIDTH, INVADER_HEIGHT, GREEN), INVADER_WIDTH, INVADER_HEIGHT)  # Sprite 1
pgb.add_sprite(make_sprite_from_pixels(invader2_pixels, INVADER_WIDTH, INVADER_HEIGHT, CYAN), INVADER_WIDTH, INVADER_HEIGHT)  # Sprite 2
pgb.add_sprite(make_sprite_from_pixels(invader2_alt_pixels, INVADER_WIDTH, INVADER_HEIGHT, CYAN), INVADER_WIDTH, INVADER_HEIGHT)  # Sprite 3
pgb.add_sprite(make_sprite_from_pixels(invader3_pixels, INVADER_WIDTH, INVADER_HEIGHT, PURPLE), INVADER_WIDTH, INVADER_HEIGHT)  # Sprite 4
pgb.add_sprite(make_sprite_from_pixels(invader3_alt_pixels, INVADER_WIDTH, INVADER_HEIGHT, PURPLE), INVADER_WIDTH, INVADER_HEIGHT)  # Sprite 5
pgb.add_sprite(make_sprite_from_pixels(player_pixels, PLAYER_WIDTH, PLAYER_HEIGHT, GREEN), PLAYER_WIDTH, PLAYER_HEIGHT)  # Sprite 6
pgb.add_sprite(make_sprite_from_pixels(shield_pixels, SHIELD_SIZE, SHIELD_SIZE, GREEN), SHIELD_SIZE, SHIELD_SIZE)  # Sprite 7
pgb.add_sprite(make_sprite_from_pixels(mystery_pixels, MYSTERY_WIDTH, MYSTERY_HEIGHT, RED), MYSTERY_WIDTH, MYSTERY_HEIGHT)  # Sprite 8
pgb.add_sprite(make_sprite_from_pixels(explosion_pixels, INVADER_WIDTH, INVADER_HEIGHT, YELLOW), INVADER_WIDTH, INVADER_HEIGHT)  # Sprite 9
pgb.add_sprite(make_sprite_from_pixels(boss_pixels, BOSS_WIDTH, BOSS_HEIGHT, RED), BOSS_WIDTH, BOSS_HEIGHT)  # Sprite 10
pgb.add_sprite(make_sprite_from_pixels(boss_alt_pixels, BOSS_WIDTH, BOSS_HEIGHT, RED), BOSS_WIDTH, BOSS_HEIGHT)  # Sprite 11
pgb.add_sprite(make_sprite_from_pixels(missile_pixels, MISSILE_WIDTH, MISSILE_HEIGHT, YELLOW), MISSILE_WIDTH, MISSILE_HEIGHT)  # Sprite 12
pgb.add_sprite(make_sprite_from_pixels(heat_pixel, HEAT_WIDTH, HEAT_HEIGHT, RED), HEAT_WIDTH, HEAT_HEIGHT)  # Sprite 13

# Create a pixel font for score display
def draw_digit(x, y, digit, color=WHITE):
    # Simple 3x5 pixel font
    patterns = [
        # 0
        [[1,1,1],
         [1,0,1],
         [1,0,1],
         [1,0,1],
         [1,1,1]],
        # 1
        [[0,1,0],
         [1,1,0],
         [0,1,0],
         [0,1,0],
         [1,1,1]],
        # 2
        [[1,1,1],
         [0,0,1],
         [1,1,1],
         [1,0,0],
         [1,1,1]],
        # 3
        [[1,1,1],
         [0,0,1],
         [0,1,1],
         [0,0,1],
         [1,1,1]],
        # 4
        [[1,0,1],
         [1,0,1],
         [1,1,1],
         [0,0,1],
         [0,0,1]],
        # 5
        [[1,1,1],
         [1,0,0],
         [1,1,1],
         [0,0,1],
         [1,1,1]],
        # 6
        [[1,1,1],
         [1,0,0],
         [1,1,1],
         [1,0,1],
         [1,1,1]],
        # 7
        [[1,1,1],
         [0,0,1],
         [0,1,0],
         [1,0,0],
         [1,0,0]],
        # 8
        [[1,1,1],
         [1,0,1],
         [1,1,1],
         [1,0,1],
         [1,1,1]],
        # 9
        [[1,1,1],
         [1,0,1],
         [1,1,1],
         [0,0,1],
         [1,1,1]]
    ]
    
    pattern = patterns[digit]
    for py in range(5):
        for px in range(3):
            if pattern[py][px]:
                pgb.pixel(x + px, y + py, color)

def draw_score(x, y, score, color=WHITE):
    # Convert score to digits
    digits = []
    if score == 0:
        digits = [0]
    else:
        temp = score
        while temp > 0:
            digits.insert(0, temp % 10)
            temp //= 10
    
    # Draw each digit
    for i, digit in enumerate(digits):
        draw_digit(x + i*4, y, digit, color)

def draw_text(x, y, text, color=WHITE):
    pgb.text(text, x, y, color)

def draw_logo():
    # Draw "SPACE" at the top
    pgb.text("SPACE", 100, 40, GREEN)
    # Draw "INVADERS" below
    pgb.text("INVADERS", 90, 55, GREEN)

def draw_intro_screen():
    pgb.fill(BLACK)
    draw_logo()
    
    # Draw aliens and their point values
    pgb.sprite(8, 80, 90)  # Mystery ship
    pgb.text("? pts", 140, 90, RED)
    
    pgb.sprite(0, 80, 110)  # Invader type 1
    pgb.text("30 pts", 140, 110, GREEN)
    
    pgb.sprite(2, 80, 130)  # Invader type 2
    pgb.text("20 pts", 140, 130, CYAN)
    
    pgb.sprite(4, 80, 150)  # Invader type 3
    pgb.text("10 pts", 140, 150, PURPLE)
    
    # Draw boss info
    pgb.sprite(10, 75, 170)  # Boss
    pgb.text("500 pts", 140, 175, RED)
    
    # Draw difficulty options
    pgb.text("SELECT DIFFICULTY:", 60, 195, WHITE)
    pgb.text("A: EASY", 90, 210, WHITE)
    pgb.text("LEFT: MEDIUM", 90, 220, WHITE)
    pgb.text("B: HARD", 90, 225, WHITE)
    
    pgb.show()

def wait_for_key():
    while True:
        if pgb.button_A() or pgb.button_B() or pgb.button_left():
            if pgb.button_left():
                difficulty = "MEDIUM"
            if pgb.button_B():
                difficulty = "HARD"
            if pgb.button_A():
                difficulty = "EASY"        
            # Wait for button release to avoid immediate input in game
            while pgb.button_A() or pgb.button_B():
                sleep(0.05)
            return difficulty
        sleep(0.05)

def create_invaders(level):
    # Create formation of invaders
    invaders = []
    rows = 5
    cols = 11
    
    # In higher levels, some invaders require multiple hits
    extra_health = max(0, level - 2)  # From level 3 onwards
    
    # First row: Type 1 (squid)
    for col in range(cols):
        invaders.append({
            "x": col * (INVADER_WIDTH + 4) + 30,
            "y": 40,
            "type": 0,
            "sprite_pair": (0, 1),
            "points": 30,
            "active": True,
            "frame": 0,
            "health": 1 + (extra_health if col % 3 == 0 else 0),  # Some invaders have extra health in higher levels
            "size_factor": 1.0 + (0.2 * min(extra_health, 2) if col % 3 == 0 else 0)  # Slightly bigger in higher levels
        })
    
    # Second and third rows: Type 2 (crab)
    for row in range(2):
        for col in range(cols):
            invaders.append({
                "x": col * (INVADER_WIDTH + 4) + 30,
                "y": 40 + (row + 1) * (INVADER_HEIGHT + 4),
                "type": 1,
                "sprite_pair": (2, 3),
                "points": 20,
                "active": True,
                "frame": 0,
                "health": 1 + (extra_health if (col % 4 == 0 and level > 3) else 0),
                "size_factor": 1.0 + (0.2 * min(extra_health, 2) if (col % 4 == 0 and level > 3) else 0)
            })
    
    # Fourth and fifth rows: Type 3 (octopus)
    for row in range(2):
        for col in range(cols):
            invaders.append({
                "x": col * (INVADER_WIDTH + 4) + 30,
                "y": 40 + (row + 3) * (INVADER_HEIGHT + 4),
                "type": 2,
                "sprite_pair": (4, 5),
                "points": 10,
                "active": True,
                "frame": 0,
                "health": 1 + (extra_health if (col % 5 == 0 and level > 4) else 0),
                "size_factor": 1.0 + (0.2 * min(extra_health, 2) if (col % 5 == 0 and level > 4) else 0)
            })
    
    return invaders

def create_boss(level):
    # Boss appears in level 5, 10, 15, etc.
    if level % 5 == 0:
        return {
            "x": 120 - BOSS_WIDTH // 2,
            "y": 30,
            "health": 10 + (level // 5) * 5,  # Scales with level
            "max_health": 10 + (level // 5) * 5,
            "active": True,
            "frame": 0,
            "points": 500 * (level // 5),
            "last_attack": 0,
            "attack_cooldown": 1500,  # Time in ms between attacks
            "movement_pattern": random.choice(["sine", "zigzag", "linear", "cosine", "circular", "avoid"])
        }
    return None

def create_shields(num_shields=4):
    shields = []
    shield_width = 24  # 3 parts wide
    spacing = (240 - (shield_width * num_shields)) // (num_shields + 1)
    shield_y = 180
    
    for i in range(num_shields):
        x_pos = spacing + i * (shield_width + spacing)
        # Create a shield with multiple parts
        for row in range(2):
            for col in range(3):
                shields.append({
                    "x": x_pos + col * SHIELD_SIZE,
                    "y": shield_y + row * SHIELD_SIZE,
                    "health": 3
                })
    
    return shields

def run_game(difficulty):
    # Set up game parameters based on difficulty
    if difficulty == "EASY":
        lives = 3
        invader_speed_start = 0.5  # slower
        bullet_cooldown = 150
        bomb_chance = 0.005  # Lower chance of invaders dropping bombs
        heat_increase = 0.25  # How much heat is generated per shot
        heat_cooldown = 15  # How fast the gun cools down
        missile_chance = 0.1  # Chance of missile powerup appearing    
    
    if difficulty == "MEDIUM":
        lives = 2
        invader_speed_start = 0.65
        bullet_cooldown = 350
        bomb_chance = 0.01  # Increased chance of invaders dropping bombs
        heat_increase = 3  # Gun heats up faster
        heat_cooldown = 10  # Cools down slower
        missile_chance = 0.02  # Lower chance of missile powerup
    else:  # HARD
        lives = 1
        invader_speed_start = 0.8  # faster
        bullet_cooldown = 500
        bomb_chance = 0.025  # Higher chance of invaders dropping bombs
        heat_increase = 3  # Gun heats up faster
        heat_cooldown = 5  # Cools down slower
        missile_chance = 0.03  # Lower chance of missile powerup
    
    # Game state variables
    score = 0
    level = 1
    game_over = False
    
    player_x = 120 - PLAYER_WIDTH // 2
    player_y = 220
    player_speed = 2
    
    bullets = []
    bombs = []
    explosions = []
    missiles = []  # For powerful missile attacks
    powerups = []  # For missile powerups
    
    # Gun heat system (prevent spam shooting)
    gun_heat = 0
    max_heat = 100
    overheated = False
    overheat_cooldown = 0
    has_missiles = 0  # Missile count
    
    mystery_ship = None
    mystery_timer = 0
    shields = create_shields()

    invaders = create_invaders(level)
    invader_direction = 1
    invader_speed = invader_speed_start
    animation_timer = 0
    animation_frame = 0
    move_timer = 0
    move_delay = 30  # ms between invader movements
    
    last_shot_time = 0
    game_start_time = ticks_ms()
    boss = create_boss(level) if level % 5 == 0 else None
    
    # Main game loop
    while not game_over:
        current_time = ticks_ms()
        
        # Input handling
        if pgb.button_left() and player_x > 0:
            player_x -= player_speed
        if pgb.button_right() and player_x < (240 - PLAYER_WIDTH):
            player_x += player_speed
        
        # Gun heat cooldown (when not shooting)
        if gun_heat > 0 and not pgb.button_A():
            gun_heat -= heat_cooldown
            if gun_heat < 0:
                gun_heat = 0
            if gun_heat < max_heat * 0.7:  # Gun cools down enough to use again
                overheated = False
        
        # Player shooting
        if pgb.button_A() and not overheated and ticks_diff(current_time, last_shot_time) > bullet_cooldown:
            # Regular bullets
            bullets.append({
                "x": player_x + PLAYER_WIDTH // 2 - 1,
                "y": player_y - 4,
                "active": True,
                "type": "regular"
            })
            last_shot_time = current_time
            pgb.sound(1000, 100)  # Shoot sound
            
            # Increase gun heat
            gun_heat += heat_increase
            if gun_heat >= max_heat:
                gun_heat = max_heat
                overheated = True
                overheat_cooldown = current_time
        
        # Missile shooting (B button)
        if pgb.button_B() and has_missiles > 0 and ticks_diff(current_time, last_shot_time) > bullet_cooldown:
            bullets.append({
                "x": player_x + PLAYER_WIDTH // 2 - 3,
                "y": player_y - 6,
                "active": True,
                "type": "missile",
                "width": 6,
                "height": 10
            })
            has_missiles -= 1
            last_shot_time = current_time
            pgb.sound(2000, 200)  # Missile sound
        
        # Clear screen
        pgb.fill(BLACK)
        
        # Update and draw bullets
        for bullet in bullets:
            if bullet["active"]:
                bullet["y"] -= 5
                
                # Check for collision with invaders
                for invader in invaders:
                    if invader["active"]:
                        bullet_width = 6 if bullet["type"] == "missile" else 2
                        if (bullet["x"] + bullet_width/2 >= invader["x"] and 
                            bullet["x"] + bullet_width/2 < invader["x"] + INVADER_WIDTH and
                            bullet["y"] >= invader["y"] and 
                            bullet["y"] < invader["y"] + INVADER_HEIGHT):
                            
                            # Mark as hit
                            explosions.append({
                                "x": invader["x"],
                                "y": invader["y"],
                                "time": current_time,
                                "duration": 200  # Show explosion for 200ms
                            })
                            
                            # Reduce health for multi-hit enemies
                            invader["health"] -= 1
                            
                            if invader["health"] <= 0:
                                score += invader["points"]
                                invader["active"] = False
                            
                            # Missiles can go through multiple enemies
                            if bullet["type"] == "regular":
                                bullet["active"] = False
                            
                            # Play explosion sound
                            pgb.sound(150, 200)
                            sleep(0.05)
                            pgb.sound(0)
                            
                            # Speed up remaining invaders slightly
                            if sum(1 for inv in invaders if inv["active"]) > 0:
                                invader_speed *= 1.02
                
                # Check for collision with boss
                if boss and boss["active"]:
                    damage = 2 if bullet["type"] == "missile" else 1
                    if (bullet["y"] < boss["y"] + BOSS_HEIGHT and 
                        bullet["x"] >= boss["x"] and 
                        bullet["x"] < boss["x"] + BOSS_WIDTH):
                        
                        boss["health"] -= damage
                        explosions.append({
                            "x": boss["x"] + random.randint(0, BOSS_WIDTH - INVADER_WIDTH),
                            "y": boss["y"] + random.randint(0, BOSS_HEIGHT - INVADER_HEIGHT),
                            "time": current_time,
                            "duration": 200
                        })
                        
                        bullet["active"] = False
                        
                        # Play hit sound
                        pgb.sound(200, 150)
                        sleep(0.05)
                        pgb.sound(0)
                        
                        # Check if boss is defeated
                        if boss["health"] <= 0:
                            explosions.append({
                                "x": boss["x"] + BOSS_WIDTH//4,
                                "y": boss["y"] + BOSS_HEIGHT//4,
                                "time": current_time,
                                "duration": 500
                            })
                            explosions.append({
                                "x": boss["x"] + 3*BOSS_WIDTH//4,
                                "y": boss["y"] + BOSS_HEIGHT//4,
                                "time": current_time,
                                "duration": 500
                            })
                            explosions.append({
                                "x": boss["x"] + BOSS_WIDTH//4,
                                "y": boss["y"] + 3*BOSS_HEIGHT//4,
                                "time": current_time,
                                "duration": 500
                            })
                            explosions.append({
                                "x": boss["x"] + 3*BOSS_WIDTH//4,
                                "y": boss["y"] + 3*BOSS_HEIGHT//4,
                                "time": current_time,
                                "duration": 500
                            })
                            score += boss["points"]
                            boss["active"] = False
                            
                            # Big explosion sound
                            pgb.sound(60, 2000)
                            sleep(0.2)
                            pgb.sound(0)
                
                # Check for collision with mystery ship
                if mystery_ship and bullet["y"] < mystery_ship["y"] + MYSTERY_HEIGHT and bullet["x"] >= mystery_ship["x"] and bullet["x"] < mystery_ship["x"] + MYSTERY_WIDTH:
                    explosions.append({
                        "x": mystery_ship["x"],
                        "y": mystery_ship["y"],
                        "time": current_time,
                        "duration": 300
                    })
                    score += mystery_ship["points"]
                    
                    # Mystery ship sometimes drops powerups
                    if random.random() < 0.7:  # 70% chance
                        powerups.append({
                            "x": mystery_ship["x"] + MYSTERY_WIDTH // 2 - MISSILE_WIDTH // 2,
                            "y": mystery_ship["y"],
                            "type": "missile",
                            "active": True
                        })
                    
                    mystery_ship = None
                    bullet["active"] = False
                    
                    # Play mystery explosion sound
                    pgb.sound(80, 300)
                    sleep(0.1)
                    pgb.sound(0)
                
                # Check for collision with shields
                for shield in shields:
                    if (shield["health"] > 0 and
                        bullet["x"] >= shield["x"] and
                        bullet["x"] < shield["x"] + SHIELD_SIZE and
                        bullet["y"] >= shield["y"] and
                        bullet["y"] < shield["y"] + SHIELD_SIZE):
                        
                        shield["health"] -= 1
                        bullet["active"] = False
                
                # Draw active bullets
                if bullet["active"]:
                    if bullet["y"] > 0:
                        if bullet["type"] == "missile":
                            pgb.sprite(12, bullet["x"], bullet["y"])
                        else:
                            pgb.fill_rect(bullet["x"], bullet["y"], 2, 6, WHITE)
                    else:
                        bullet["active"] = False
        
        # Filter out inactive bullets
        bullets = [b for b in bullets if b["active"]]
        
        # Update and draw invader bombs
        for bomb in bombs:
            if bomb["active"]:
                # Update position based on bomb type
                bomb["y"] += 3
                
                # For advanced bombs (angled shots)
                if "dx" in bomb:
                    bomb["x"] += bomb["dx"]
                    
                    # Bounce off walls
                    if bomb["x"] <= 0 or bomb["x"] >= 238:
                        bomb["dx"] *= -1
                
                # Check collision with player
                if (bomb["y"] + 5 > player_y and
                    bomb["x"] >= player_x and
                    bomb["x"] < player_x + PLAYER_WIDTH):
                    
                    # Player hit
                    lives -= 1
                    bomb["active"] = False
                    
                    # Play player explosion sound
                    pgb.sound(60, 500)
                    sleep(0.2)
                    pgb.sound(0)
                    
                    # Player death animation
                    explosions.append({
                        "x": player_x,
                        "y": player_y,
                        "time": current_time,
                        "duration": 1000  # Longer explosion for player
                    })
                    
                    # Reset player position
                    player_x = 120 - PLAYER_WIDTH // 2
                    
                    # Pause briefly
                    pgb.fill(BLACK)
                    for exp in explosions:
                        if ticks_diff(current_time, exp["time"]) < exp["duration"]:
                            pgb.sprite(9, exp["x"], exp["y"])
                    pgb.show()
                    sleep(1)
                
                # Check collision with shields
                for shield in shields:
                    if (shield["health"] > 0 and
                        bomb["x"] >= shield["x"] and
                        bomb["x"] < shield["x"] + SHIELD_SIZE and
                        bomb["y"] >= shield["y"] and
                        bomb["y"] < shield["y"] + SHIELD_SIZE):
                        
                        shield["health"] -= 1
                        bomb["active"] = False
                
                # Draw active bombs
                if bomb["active"]:
                    if bomb["y"] < 240:
                        # Different colors based on type
                        color = RED if "dx" in bomb else YELLOW
                        pgb.fill_rect(bomb["x"], bomb["y"], 2, 5, color)
                    else:
                        bomb["active"] = False
        
        # Filter out inactive bombs
        bombs = [b for b in bombs if b["active"]]
        
        # Update and draw powerups
        for powerup in powerups:
            if powerup["active"]:
                powerup["y"] += 1
                
                # Check if player collected powerup
                if (powerup["y"] + MISSILE_HEIGHT > player_y and
                    powerup["y"] < player_y + PLAYER_HEIGHT and
                    powerup["x"] + MISSILE_WIDTH > player_x and
                    powerup["x"] < player_x + PLAYER_WIDTH):
                    
                    if powerup["type"] == "missile":
                        has_missiles += 3
                        pgb.sound(1500, 200)
                    
                    powerup["active"] = False
                
                # Draw powerup
                if powerup["active"]:
                    if powerup["y"] < 240:
                        pgb.sprite(12, powerup["x"], powerup["y"])
                    else:
                        powerup["active"] = False
        
        # Filter out inactive powerups
        powerups = [p for p in powerups if p["active"]]
        
        # Update and draw mystery ship
        if mystery_ship:
            mystery_ship["x"] += mystery_ship["direction"]
            if (mystery_ship["x"] < -MYSTERY_WIDTH or 
                mystery_ship["x"] > 240):
                mystery_ship = None
            else:
                pgb.sprite(8, mystery_ship["x"], mystery_ship["y"])
        elif random.random() < 0.001:  # Small chance to spawn mystery ship
            direction = 1 if random.random() < 0.5 else -1
            start_x = -MYSTERY_WIDTH if direction > 0 else 240
            mystery_ship = {
                "x": start_x,
                "y": 20,
                "direction": direction,
                "points": random.choice([50, 100, 150, 300])
            }
            # Play mystery ship sound
            pgb.sound(440, 50)
        
        # Update and draw boss if active
        if boss and boss["active"]:
            # Update boss movement pattern
            if boss["movement_pattern"] == "sine":
                boss["x"] = 120 - BOSS_WIDTH//2 + int(math.sin(current_time/1000) * 60)
            elif boss["movement_pattern"] == "zigzag":
                t = current_time / 2000
                boss["x"] = 120 - BOSS_WIDTH//2 + int((t % 2 - 1) * 80)
            else:  # linear
                boss["x"] += 1 if (current_time // 2000) % 2 == 0 else -1
                if boss["x"] < 20 or boss["x"] > 200:
                    boss["x"] = max(20, min(200, boss["x"]))
            
            # Boss attacks
            if ticks_diff(current_time, boss["last_attack"]) > boss["attack_cooldown"]:
                boss["last_attack"] = current_time
                
                # Different attack patterns based on health percentage
                health_percent = boss["health"] / boss["max_health"]
                
                if health_percent < 0.3:  # Below 30% health - multi-directional attack
                    for angle in [-0.4, -0.2, 0, 0.2, 0.4]:
                        bombs.append({
                            "x": boss["x"] + BOSS_WIDTH // 2,
                            "y": boss["y"] + BOSS_HEIGHT,
                            "active": True,
                            "dx": angle * 5  # Angled shots
                        })
                elif health_percent < 0.7:  # Below 70% health - triple attack
                    bombs.append({
                        "x": boss["x"] + BOSS_WIDTH // 4,
                        "y": boss["y"] + BOSS_HEIGHT,
                        "active": True,
                        "dx": -0.5
                    })
                    bombs.append({
                        "x": boss["x"] + BOSS_WIDTH // 2,
                        "y": boss["y"] + BOSS_HEIGHT,
                        "active": True
                    })
                    bombs.append({
                        "x": boss["x"] + 3 * BOSS_WIDTH // 4,
                        "y": boss["y"] + BOSS_HEIGHT,
                        "active": True,
                        "dx": 0.5
                    })
                else:  # Above 70% health - single attack
                    bombs.append({
                        "x": boss["x"] + BOSS_WIDTH // 2,
                        "y": boss["y"] + BOSS_HEIGHT,
                        "active": True
                    })
            
            # Draw boss with alternating frames for animation
            frame = (current_time // 500) % 2
            pgb.sprite(10 + frame, boss["x"], boss["y"])
            
            # Draw boss health bar
            health_pct = boss["health"] / boss["max_health"]
            bar_width = 100
            pgb.fill_rect(70, 15, bar_width, 5, RED)
            pgb.fill_rect(70, 15, int(bar_width * health_pct), 5, GREEN)
        
        # Update invaders
        if ticks_diff(current_time, move_timer) > move_delay:
            move_timer = current_time
            
            # Move invaders
            move_down = False
            for invader in invaders:
                if invader["active"]:
                    # Check if any invader would hit the edge
                    if ((invader_direction > 0 and invader["x"] + INVADER_WIDTH * invader["size_factor"] + invader_direction > 238) or
                        (invader_direction < 0 and invader["x"] + invader_direction < 2)):
                        move_down = True
                        break
            
            if move_down:
                invader_direction *= -1
                for invader in invaders:
                    if invader["active"]:
                        invader["y"] += 8
                        
                        # Check if invaders reached the bottom (player level)
                        if invader["y"] + INVADER_HEIGHT >= player_y:
                            game_over = True
            else:
                # Move all invaders horizontally
                for invader in invaders:
                    if invader["active"]:
                        invader["x"] += invader_direction
            
            # Animation frame update
            animation_frame = 1 - animation_frame  # Toggle between 0 and 1
            
            # Random bomb dropping from invaders
            if random.random() < bomb_chance:
                # Find lowest invader in each column
                columns = {}
                for inv in invaders:
                    if inv["active"]:
                        col = inv["x"] // (INVADER_WIDTH + 4)
                        if col not in columns or inv["y"] > columns[col]["y"]:
                            columns[col] = inv
                
                if columns:
                    # Randomly select a column
                    bombing_invader = random.choice(list(columns.values()))
                    
                    # In higher levels, have chance for angled shots
                    if level > 2 and random.random() < 0.3:
                        # Angled shot that aims in player's general direction
                        dx = (player_x - bombing_invader["x"]) / 40  # Dividing to make it not too accurate
                        dx = max(-2, min(2, dx))  # Limit angle
                        bombs.append({
                            "x": bombing_invader["x"] + INVADER_WIDTH // 2,
                            "y": bombing_invader["y"] + INVADER_HEIGHT,
                            "active": True,
                            "dx": dx
                        })
                    else:
                        # Regular straight-down bomb
                        bombs.append({
                            "x": bombing_invader["x"] + INVADER_WIDTH // 2,
                            "y": bombing_invader["y"] + INVADER_HEIGHT,
                            "active": True
                        })
            
            # Random powerup drop chance
            if random.random() < missile_chance and len(powerups) < 1:
                # Find random active invader
                active_invaders = [inv for inv in invaders if inv["active"]]
                if active_invaders:
                    inv = random.choice(active_invaders)
                    powerups.append({
                        "x": inv["x"],
                        "y": inv["y"],
                        "type": "missile",
                        "active": True
                    })
        
        # Draw invaders
        active_count = 0
        for invader in invaders:
            if invader["active"]:
                active_count += 1
                sprite_idx = invader["sprite_pair"][animation_frame]
                # Draw with size factor for tougher enemies
                if invader["size_factor"] > 1.0:
                    # Draw slightly larger and with tint based on health
                    pgb.sprite(sprite_idx, invader["x"], invader["y"])
                    # Add a health indicator glow
                    health_color = GREEN if invader["health"] > 2 else YELLOW if invader["health"] > 1 else RED
                    pgb.fill_rect(invader["x"], invader["y"], INVADER_WIDTH, INVADER_HEIGHT, health_color)
                else:
                    pgb.sprite(sprite_idx, invader["x"], invader["y"])
        
        # Check if all invaders and boss are defeated
        if active_count == 0 and (not boss or not boss["active"]):
            # Level completed - advance to next level
            level += 1
            invaders = create_invaders(level)
            invader_speed = invader_speed_start * (1 + (level - 1) * 0.3)  # Speed increases with level
            invader_direction = 1
            
            # Create boss for levels 5, 10, 15, etc.
            boss = create_boss(level)
            
            # Display level message
            pgb.fill(BLACK)
            pgb.text(f"LEVEL {level}", 100, 120, WHITE)
            pgb.show()
            sleep(2)
        
        # Draw shields
        for shield in shields:
            if shield["health"] > 0:
                # Vary the shield color based on health
                shield_colors = [RED, YELLOW, GREEN]
                shield_color = shield_colors[shield["health"] - 1]
                pgb.sprite(7, shield["x"], shield["y"])
                # Apply color tint based on health
                if shield["health"] < 3:
                    pgb.fill_rect(shield["x"], shield["y"], SHIELD_SIZE, SHIELD_SIZE, shield_color)
        
        # Draw player
        pgb.sprite(6, player_x, player_y)
        
        # Draw explosions
        for explosion in explosions:
            if ticks_diff(current_time, explosion["time"]) < explosion["duration"]:
                pgb.sprite(9, explosion["x"], explosion["y"])
        
        # Remove expired explosions
        explosions = [e for e in explosions if ticks_diff(current_time, e["time"]) < e["duration"]]
        
        # Draw UI elements
        # Draw score
        pgb.text(f"SCORE:{score}", 5, 5, WHITE)
        
        # Draw lives
        pgb.text("LIVES:", 170, 5, WHITE)
        for i in range(lives):
            pgb.sprite(6, 215 - (i * 18), 5)
        
        # Draw level indicator
        pgb.text(f"LV:{level}", 5, 230, WHITE)
        
        # Draw gun heat meter
        if gun_heat > 0:
            # Draw heat bar
            bar_width = 30
            bar_height = 8
            bar_x = 90
            bar_y = 230
            
            # Background
            pgb.fill_rect(bar_x, bar_y, bar_width, bar_height, WHITE)
            
            # Heat level
            heat_width = int((gun_heat / max_heat) * bar_width)
            heat_color = GREEN
            if gun_heat > max_heat * 0.7:
                heat_color = YELLOW
            if gun_heat > max_heat * 0.9:
                heat_color = RED
            
            pgb.fill_rect(bar_x, bar_y, heat_width, bar_height, heat_color)
            
            # Draw "HEAT" text
            pgb.text("HEAT", 60, 230, WHITE)
            
            # Warning for overheated
            if overheated:
                pgb.text("COOL DOWN!", 125, 230, RED)
        
        # Draw missile count
        if has_missiles > 0:
            pgb.text(f"MISSILES:{has_missiles}", 150, 230, YELLOW)
        
        # Check for game over
        if lives <= 0:
            game_over = True
            pgb.fill(BLACK)
            pgb.text("GAME OVER", 95, 110, RED)
            pgb.text(f"FINAL SCORE: {score}", 75, 130, WHITE)
            pgb.text("PRESS A TO CONTINUE", 55, 180, WHITE)
            pgb.show()
            
            # Wait for button press
            while not pgb.button_A():
                sleep(0.1)
            
            # Debounce
            while pgb.button_A():
                sleep(0.05)
            
            return score  # Return to main menu
        
        # Update display
        pgb.show()
        
        # Frame timing for consistent speed
        sleep(0.016)  # ~60fps
    
    return score

def show_high_scores(scores):
    pgb.fill(BLACK)
    pgb.text("HIGH SCORES", 85, 40, YELLOW)
    
    y = 60
    for i, score in enumerate(scores):
        pgb.text(f"{i+1}. {score}", 90, y, WHITE)
        y += 20
    
    pgb.text("PRESS A TO CONTINUE", 55, 200, WHITE)
    pgb.show()
    
    while not pgb.button_A():
        sleep(0.1)
    
    # Debounce
    while pgb.button_A():
        sleep(0.05)

# Main game flow
def main():
    high_scores = [0, 0, 0, 0, 0]  # Top 5 high scores
    
    while True:
        # Show intro screen
        draw_intro_screen()
        difficulty = wait_for_key()
        
        # Countdown
        pgb.fill(BLACK)
        pgb.text("GET READY!", 90, 120, GREEN)
        pgb.show()
        sleep(1)
        
        for i in range(3, 0, -1):
            pgb.fill(BLACK)
            pgb.text(str(i), 115, 120, WHITE)
            pgb.show()
            pgb.sound(440, 100)
            sleep(0.1)
            pgb.sound(0)
            sleep(0.9)
        
        # Run the game
        score = run_game(difficulty)
        
        # Check if it's a high score
        if score > min(high_scores):
            # Insert into high scores and sort
            high_scores.append(score)
            high_scores.sort(reverse=True)
            high_scores = high_scores[:5]  # Keep only top 5
            
            pgb.fill(BLACK)
            pgb.text("NEW HIGH SCORE!", 70, 110, YELLOW)
            pgb.text(f"SCORE: {score}", 90, 130, WHITE)
            pgb.show()
            sleep(2)
        
        # Show high scores
        show_high_scores(high_scores)

# Start the game
if __name__ == "__main__":
    main()


