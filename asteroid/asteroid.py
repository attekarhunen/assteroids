import random
from helper import functions


class Asteroid(object):
    def __init__(self):
        self.move_vector = functions.angle_to_vector(random.uniform(-3, 3))
        self.geometry = ((-25, -25), (25, -25), (25, 25), (-25, 25))
        self.pos = ((random.uniform(200, DISPLAY_W - 200)), (random.uniform(200, DISPLAY_H - 200)))
        self.direction = random.uniform(-3, 3)
        self.turning = random.uniform(-0.01, 0.01)
        self.life = 100

    def move(self):
        self.direction += self.turning

        x = self.pos[0] + (self.move_vector[0] * 0.5)
        y = self.pos[1] + (self.move_vector[1] * 0.5)

        if x > DISPLAY_W:
            x -= DISPLAY_W
        if x < 0:
            x += DISPLAY_W
        if y > DISPLAY_H:
            y -= DISPLAY_H
        if y < 0:
            y -= DISPLAY_H

        newpos = ((x, y))
        self.pos = newpos

    def draw(self):
        translated_graphics = functions.translate_graphics(self.geometry, self.pos, self.direction)
        pygame.draw.aalines(gameDisplay, CYAN, True, translated_graphics, 2)