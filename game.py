import pygame
import sys
from math import sin, cos, pi, hypot
from helper import functions
from model import Model


# handle input from pressed keys here
def handle_input(pressedKeys):
    if pressedKeys[pygame.K_UP]:
        player.thrusting = True
    if not pressedKeys[pygame.K_UP]:
        player.thrusting = False
    if pressedKeys[pygame.K_LEFT]:
        player.turn('left')
    if pressedKeys[pygame.K_RIGHT]:
        player.turn('right')


# draw ship geometry
def draw_ship(pos, direction):
    geometry = functions.translate_graphics(player.geometry, pos, direction)
    pygame.draw.aalines(gameDisplay, model.WHITE, True, geometry, 2)
    if player.thrusting:
        jet = functions.translate_graphics(player.jet, pos, direction)
        pygame.draw.aalines(gameDisplay, model.YELLOW, True, jet, 2)


class playerShip(object):
    def __init__(self, pos):
        self.pos = pos
        self.direction = 0.0
        self.health = 1000
        self.alive = True
        self.geometry = ((-8.0, -12.0), (0.0, 12.0), (8.0, -12.0), (0.0, -10.0))
        self.jet = ((-4.0, -13.0), (0.0, -12.0), (4.0, -13.0), (0.0, -20.0))
        self.movement = [0.0, 0.0]
        self.thrusting = False

    def turn(self, direction):
        if direction == 'left':
            self.direction = self.direction + model.TURN_RATE
        else:
            self.direction = self.direction - model.TURN_RATE

    def move(self):
        move = [0.0, 0.0]

        if self.thrusting:
            move[0] += model.THRUST * functions.angle_to_vector(self.direction)[0]
            move[1] += model.THRUST * functions.angle_to_vector(self.direction)[1]
            self.movement[0] += move[0]
            self.movement[1] += move[1]

        self.movement[0] -= model.FRICTION * self.movement[0]
        self.movement[1] -= model.FRICTION * self.movement[1]

        self.pos = ((self.pos[0] + self.movement[0], self.pos[1] + self.movement[1]))

    def is_alive(self):
        if self.health < 0:
            self.alive = False
            self.set_speed(0)
        return self.alive

    def shoot(self):
        bullet = laserBullet(self.pos, functions.angle_to_vector(self.direction))
        return bullet


# faster than a laser bullet
class laserBullet(object):
    def __init__(self, pos, vector):
        self.life = 25
        self.prevPos = pos
        self.pos = pos
        self.move_vector = vector

    def draw(self):
        pygame.draw.aaline(gameDisplay, model.RED, self.pos, self.prevPos, 3)

    def move(self):
        self.life -= 1
        newPos = ((
            self.pos[0] + (self.move_vector[0] * model.BULLET_SPEED),
            self.pos[1] + (self.move_vector[1] * model.BULLET_SPEED)
        ))
        self.prevPos = self.pos
        self.pos = newPos


pygame.init()

myfont = pygame.font.SysFont("monospace", 15)

model = Model.Model()

player = playerShip((model.DISPLAY_W / 2, model.DISPLAY_H / 2))

gameDisplay = pygame.display.set_mode((model.DISPLAY_W, model.DISPLAY_H))

pygame.display.set_caption('ASSTEROIDS')
ticker = pygame.time.Clock()
debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        debug = True

game_running = True
bullets = []

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(player.shoot())

    direction_debug = "Direction: " + str(player.direction)
    thrusting_debug = "Thrusting: " + str(player.thrusting) + ", (" + str(model.THRUST) + ")"
    movement_debug = "Movement vector: " + str(player.movement)
    ship_debug = "Ship vector: " + str(functions.angle_to_vector(player.direction))
    pos_debug = "Ship position: " + str(player.pos)
    direction_label = myfont.render(direction_debug, 1, (255, 255, 0))
    thrusting_label = myfont.render(thrusting_debug, 1, (255, 255, 0))
    movement_label = myfont.render(movement_debug, 1, (255, 255, 0))
    ship_label = myfont.render(ship_debug, 1, (255, 255, 0))
    pos_label = myfont.render(pos_debug, 1, (255, 255, 0))

    pressedKeys = pygame.key.get_pressed()
    handle_input(pressedKeys)

    gameDisplay.fill(model.BLACK)

    player.move()

    draw_ship(player.pos, player.direction)

    for bullet in bullets:
        bullet.move()
        if bullet.life > 0:
            bullet.draw()
        else:
            bullets.remove(bullet)
            del bullet

    for asteroid in model.asteroids:
        if asteroid.life > 0:
            asteroid.move()
            pygame.draw.aalines(gameDisplay, model.CYAN, True, asteroid.getGraphics(), 2)
            for bullet in bullets:
                if hypot(asteroid.pos[0] - bullet.pos[0], asteroid.pos[1] - bullet.pos[1]) < 25:
                    asteroid.life = 0
                    bullet.life = 0

        else:
            model.asteroids.remove(asteroid)
            del asteroid

    if debug:
        gameDisplay.blit(direction_label, (50, 50))
        gameDisplay.blit(thrusting_label, (50, 70))
        gameDisplay.blit(movement_label, (50, 90))
        gameDisplay.blit(ship_label, (50, 110))
        gameDisplay.blit(pos_label, (50, 130))

        for asteroid in model.asteroids:
            if hypot(asteroid.pos[0] - player.pos[0], asteroid.pos[1] - player.pos[1]) < 50:
                pygame.draw.aaline(gameDisplay, model.RED, asteroid.pos, player.pos, 1)
            else:
                pygame.draw.aaline(gameDisplay, model.WHITE, asteroid.pos, player.pos, 1)

    pygame.display.update()

    ticker.tick(50)

pygame.quit()
quit()
