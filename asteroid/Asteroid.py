import random
from model import Model
from helper import functions


class Asteroid(object):
    def __init__(self, position):
        self.move_vector = functions.angle_to_vector(random.uniform(-3, 3))
        self.geometry = ((-25, -25), (25, -25), (25, 25), (-25, 25))
        self.pos = position
        self.direction = random.uniform(-3, 3)
        self.turning = random.uniform(-0.01, 0.01)
        self.life = 100
        self.model = Model.Model

    def move(self):
        self.direction += self.turning

        x = self.pos[0] + (self.move_vector[0] * 0.5)
        y = self.pos[1] + (self.move_vector[1] * 0.5)

        newpos = ((x, y))
        self.pos = newpos

    def getGraphics(self):
        return functions.translate_graphics(self.geometry, self.pos, self.direction)