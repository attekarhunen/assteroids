from asteroid import Asteroid


class Model(object):
    DISPLAY_W = 1200
    DISPLAY_H = 800
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    TURN_RATE = 0.15
    THRUST = 0.25
    FRICTION = 0.005
    BULLET_SPEED = 20
    asteroids = []

    def __init__(self):
        # init some constants
        print("Model initialized")

        for i in range(0, 5):
            self.asteroids.append(Asteroid.Asteroid((50, 50)))