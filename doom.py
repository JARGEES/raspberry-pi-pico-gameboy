from PicoGameBoy import PicoGameBoy
from math import sin, cos, pi
import random
from time import sleep

class DoomOptimized:
    def __init__(self):
        self.pgb = PicoGameBoy()
        
        # Reduce resolution significantly
        self.SCREEN_WIDTH = 60  # Reduced from 120
        self.SCREEN_HEIGHT = 60  # Reduced from 120
        self.SCALE = 4  # Increased from 2
        
        # Reduce number of rays
        self.FOV = pi / 3
        self.HALF_FOV = self.FOV / 2
        self.NUM_RAYS = 30  # Reduced from 60
        self.MAX_DEPTH = 8
        self.DELTA_ANGLE = self.FOV / self.NUM_RAYS
        
        # Simplified colors
        self.COLORS = {
            'BLACK': PicoGameBoy.color(0, 0, 0),
            'WHITE': PicoGameBoy.color(255, 255, 255),
            'RED': PicoGameBoy.color(255, 0, 0),
            'DARK_GRAY': PicoGameBoy.color(64, 64, 64),
            'SKY': PicoGameBoy.color(100, 100, 255)
        }
        
        # Player setup
        self.player = {
            'x': 1.5,
            'y': 1.5,
            'angle': 0,
            'speed': 0.1,  # Increased for better response
            'rot_speed': 0.1,  # Increased for better response
            'health': 100,
            'ammo': 50
        }
        
        # Simplified map (smaller)
        self.MAP = [
            [1,1,1,1,1,1],
            [1,0,0,0,0,1],
            [1,0,1,0,0,1],
            [1,0,0,0,0,1],
            [1,0,0,1,0,1],
            [1,1,1,1,1,1]
        ]
        
        self.is_firing = False
        self.frame_count = 0

    def ray_cast(self, angle):
        x, y = self.player['x'], self.player['y']
        map_x, map_y = int(x), int(y)
        
        sin_a = sin(angle)
        cos_a = cos(angle)
        
        # Simplified raycasting
        for depth in range(self.MAX_DEPTH):
            x += cos_a * 0.1
            y += sin_a * 0.1
            
            map_x, map_y = int(x), int(y)
            
            if self.MAP[map_y][map_x]:
                return depth + 1
                
        return self.MAX_DEPTH

    def render_frame(self):
        # Clear screen (simplified)
        self.pgb.fill(self.COLORS['SKY'])
        
        # Ray casting
        ray_angle = self.player['angle'] - self.HALF_FOV
        for ray in range(self.NUM_RAYS):
            depth = self.ray_cast(ray_angle)
            
            # Simplified wall rendering
            wall_height = min(int((1 / depth) * self.SCREEN_HEIGHT), self.SCREEN_HEIGHT)
            wall_pos = (self.SCREEN_HEIGHT - wall_height) // 2
            
            # Draw wall column
            x = ray * self.SCALE
            color = self.COLORS['DARK_GRAY'] if depth > 3 else self.COLORS['WHITE']
            
            self.pgb.fill_rect(x, wall_pos * self.SCALE, 
                             self.SCALE, wall_height * self.SCALE, 
                             color)
            
            ray_angle += self.DELTA_ANGLE
        
        # Simple HUD
        self.pgb.text(f'HP:{self.player["health"]}', 5, 5, self.COLORS['WHITE'])
        
        self.pgb.show()

    def update(self):
        # Movement
        if self.pgb.button_up():
            new_x = self.player['x'] + cos(self.player['angle']) * self.player['speed']
            new_y = self.player['y'] + sin(self.player['angle']) * self.player['speed']
            if not self.MAP[int(new_y)][int(new_x)]:
                self.player['x'] = new_x
                self.player['y'] = new_y
        
        if self.pgb.button_down():
            new_x = self.player['x'] - cos(self.player['angle']) * self.player['speed']
            new_y = self.player['y'] - sin(self.player['angle']) * self.player['speed']
            if not self.MAP[int(new_y)][int(new_x)]:
                self.player['x'] = new_x
                self.player['y'] = new_y
        
        if self.pgb.button_left():
            self.player['angle'] -= self.player['rot_speed']
        
        if self.pgb.button_right():
            self.player['angle'] += self.player['rot_speed']
        
        if self.pgb.button_A() and not self.is_firing and self.player['ammo'] > 0:
            self.is_firing = True
            self.player['ammo'] -= 1
            self.pgb.sound(440, 500)
            self.is_firing = False

    def run(self):
        while True:
            if self.player['health'] <= 0:
                self.pgb.fill(self.COLORS['BLACK'])
                self.pgb.center_text('GAME OVER', self.COLORS['RED'])
                self.pgb.show()
                sleep(2)
                break
            
            self.update()
            self.render_frame()
            self.frame_count += 1

if __name__ == "__main__":
    game = DoomOptimized()
    game.run()