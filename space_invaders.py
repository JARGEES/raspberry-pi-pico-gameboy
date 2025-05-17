from PicoGameBoy import PicoGameBoy
from time import sleep, ticks_ms

pgb = PicoGameBoy()

# 🎨 Define colors
BLACK = PicoGameBoy.color(0, 0, 0)
WHITE = PicoGameBoy.color(255, 255, 255)
RED = PicoGameBoy.color(255, 0, 0)
GREEN = PicoGameBoy.color(0, 255, 0)
BLUE = PicoGameBoy.color(0, 0, 255)
YELLOW = PicoGameBoy.color(255, 255, 0)

# 🎮 Define Sprites (10x8 pixels, RGB565 format)
def make_sprite_from_pixels(pixel_data, color):
    buffer = bytearray(10 * 8 * 2)
    for y in range(8):
        for x in range(10):
            idx = 2 * (y * 10 + x)
            if pixel_data[y][x]:
                buffer[idx] = color & 0xFF
                buffer[idx + 1] = (color >> 8) & 0xFF
            else:
                buffer[idx] = BLACK & 0xFF
                buffer[idx + 1] = (BLACK >> 8) & 0xFF
    return buffer

# 👾 Invader sprite
invader_pixels = [
    [0,1,0,0,0,0,0,0,1,0],
    [0,0,1,1,1,1,1,1,0,0],
    [1,1,1,0,1,1,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,1],
    [0,0,0,1,1,1,1,0,0,0],
    [0,0,1,0,0,0,0,1,0,0]
]

# 🚀 Player sprite
player_pixels = [
    [0,0,0,0,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1],
    [0,0,0,1,1,1,1,0,0,0],
    [0,0,0,1,0,0,1,0,0,0],
    [0,0,1,1,0,0,1,1,0,0]
]

# Create & store sprites
pgb.add_sprite(make_sprite_from_pixels(invader_pixels, GREEN), 10, 8)  # Sprite 0
pgb.add_sprite(make_sprite_from_pixels(player_pixels, BLUE), 10, 8)    # Sprite 1

# Game state
player_x = 120
player_y = 220
invaders = [{"x": x * 20 + 20, "y": 30} for x in range(8)]
bullets = []
cooldown = 300  # milliseconds
last_shot_time = 0
invader_direction = 1

# Game loop
while True:
    pgb.fill(BLACK)

    # Move player
    if pgb.button_left() and player_x > 0:
        player_x -= 2
    if pgb.button_right() and player_x < (240 - 10):
        player_x += 2

    # Shooting
    now = ticks_ms()
    if pgb.button_A() and (now - last_shot_time) > cooldown:
        bullets.append({"x": player_x + 4, "y": player_y - 2})
        last_shot_time = now
        pgb.sound(1000)

    # Draw player
    pgb.sprite(1, player_x, player_y)

    # Update and draw bullets
    new_bullets = []
    for bullet in bullets:
        bullet["y"] -= 4
        if bullet["y"] > 0:
            new_bullets.append(bullet)
            pgb.fill_rect(bullet["x"], bullet["y"], 2, 6, YELLOW)
    bullets = new_bullets

    # Move invaders
    edge_hit = False
    for inv in invaders:
        inv["x"] += invader_direction
        if inv["x"] <= 0 or inv["x"] >= (240 - 10):
            edge_hit = True

    if edge_hit:
        invader_direction *= -1
        for inv in invaders:
            inv["y"] += 10

    # Draw invaders
    new_invaders = []
    for inv in invaders:
        hit = False
        for bullet in bullets:
            if inv["x"] < bullet["x"] < inv["x"] + 10 and inv["y"] < bullet["y"] < inv["y"] + 8:
                hit = True
                break
        if not hit:
            new_invaders.append(inv)
            pgb.sprite(0, inv["x"], inv["y"])
    invaders = new_invaders

    if not invaders:
        pgb.center_text("YOU WIN!", GREEN)
        pgb.show()
        sleep(3)
        break

    # Update screen
    pgb.show()
    sleep(0.02)
