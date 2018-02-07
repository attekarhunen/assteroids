import pygame
import sys
import random
from math import sin, cos, radians, pi, hypot


#handle input from pressed keys here
def handle_input(pressedKeys):
  if pressedKeys[pygame.K_UP]:
    player.thrusting = True
  if not pressedKeys[pygame.K_UP]:
    player.thrusting = False
  if pressedKeys[pygame.K_LEFT]:
    player.turn('left')
  if pressedKeys[pygame.K_RIGHT]:
    player.turn('right')

#draw ship geometry
def draw_ship(pos, direction):
  geometry = translate_graphics(player.geometry, pos, direction)
  pygame.draw.aalines(gameDisplay, WHITE, True, geometry, 2)
  if player.thrusting:
    jet = translate_graphics(player.jet, pos, direction)
    pygame.draw.aalines(gameDisplay, YELLOW, True, jet, 2)

def translate_graphics(graphics, pos, direction):
  translated_graphics = ()
  for t_pos in graphics:
    t_pos = rotate_point(t_pos, direction)
    x = t_pos[0] + pos[0]
    y = t_pos[1] + pos[1]
    translated_graphics = ((x,y),) + (translated_graphics)
  return translated_graphics
  
def angle_to_vector(angle):
  return [sin(angle), cos(angle)]
  
def rotate_point(point, angle):
  angle_rad = radians(angle)
  rotated_point = (point[0] * cos(-angle) - point[1] * sin(-angle),
                   point[0] * sin(-angle) + point[1] * cos(-angle))                 
  return rotated_point

class playerShip(object):
  def __init__(self,pos):
    self.pos = pos
    self.direction = 0.0
    self.health = 1000
    self.alive = True
    self.geometry = ((-8.0,-12.0),(0.0,12.0),(8.0,-12.0),(0.0,-10.0))
    self.jet = ((-4.0,-13.0),(0.0,-12.0),(4.0,-13.0),(0.0,-20.0))
    self.movement = [0.0, 0.0]
    self.thrusting = False

  def turn(self, direction):
    if direction == 'left':
      self.direction = self.direction + TURN_RATE
    else:
      self.direction = self.direction - TURN_RATE

  def move(self):
    move = [0.0,0.0]
    
    if self.thrusting:
      move[0] += THRUST * angle_to_vector(self.direction)[0]
      move[1] += THRUST * angle_to_vector(self.direction)[1]
      self.movement[0] += move[0]
      self.movement[1] += move[1]
      
    self.movement[0] -= FRICTION*self.movement[0]
    self.movement[1] -= FRICTION*self.movement[1]

    self.pos = ((self.pos[0]+self.movement[0],self.pos[1]+self.movement[1]))
    
  def is_alive(self):
    if self.health < 0:
      self.alive = False
      self.set_speed(0)
    return self.alive
    
  def shoot(self):
    bullet = laserBullet(self.pos, angle_to_vector(self.direction))
    return bullet

#faster than a laser bullet
class laserBullet(object):
  def __init__(self,pos,vector):
    self.life = 25
    self.prevPos = pos
    self.pos = pos
    self.move_vector = vector
  
  def draw(self):
    pygame.draw.aaline(gameDisplay, RED, self.pos, self.prevPos, 3)
    
  def move(self):
    self.life -= 1
    newPos = ((
    self.pos[0]+(self.move_vector[0]*BULLET_SPEED),
    self.pos[1]+(self.move_vector[1]*BULLET_SPEED)
    ))
    self.prevPos = self.pos
    self.pos = newPos
    
class asteroid(object):
  def __init__(self):
    self.move_vector = angle_to_vector(random.uniform(-3,3))
    self.geometry = ((-25,-25),(25,-25),(25,25),(-25,25))
    self.pos = ((random.uniform(200,DISPLAY_W-200)),(random.uniform(200,DISPLAY_H-200)))
    self.direction = random.uniform(-3,3)
    self.turning = random.uniform(-0.01,0.01)
    
  def move(self):
    self.direction += self.turning
    
    x = self.pos[0]+(self.move_vector[0]*0.5)
    y = self.pos[1]+(self.move_vector[1]*0.5)
    
    if x > DISPLAY_W:
      x -= DISPLAY_W
    if x < 0:
      x += DISPLAY_W
    if y > DISPLAY_H:
      y -= DISPLAY_H
    if y < 0:
      y -= DISPLAY_H
    
    
    newPos = ((x,y))
    self.pos = newPos
    
  def draw(self):
    translated_graphics = translate_graphics(self.geometry, self.pos,self.direction)
    pygame.draw.aalines(gameDisplay, CYAN, True, translated_graphics, 2)
    
pygame.init()

myfont = pygame.font.SysFont("monospace", 15)

#init some constants
DISPLAY_W = 1200
DISPLAY_H = 800
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
CYAN = (0,255,255)

TURN_RATE = 0.15
THRUST = 0.25
FRICTION = 0.005
BULLET_SPEED = 20

player = playerShip((DISPLAY_W/2,DISPLAY_H/2))

gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))

pygame.display.set_caption('ASSTEROIDS')
ticker = pygame.time.Clock()
debug = False
if len(sys.argv) > 1:
  if sys.argv[1] == 'debug':
    debug = True

game_running = True
bullets = []
asteroids = []
asteroids.append(asteroid())
asteroids.append(asteroid())
asteroids.append(asteroid())
asteroids.append(asteroid())
asteroids.append(asteroid())
asteroids.append(asteroid())

while game_running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game_running = False
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        bullets.append(player.shoot())
  
  direction_debug = "Direction: " + str(player.direction)
  thrusting_debug = "Thrusting: " + str(player.thrusting) + ", (" + str(THRUST) + ")"
  movement_debug = "Movement vector: " + str(player.movement)
  ship_debug = "Ship vector: " + str(angle_to_vector(player.direction))
  pos_debug = "Ship position: " + str(player.pos)
  direction_label = myfont.render(direction_debug, 1, (255,255,0))
  thrusting_label = myfont.render(thrusting_debug, 1, (255,255,0))
  movement_label = myfont.render(movement_debug, 1, (255,255,0))
  ship_label = myfont.render(ship_debug, 1, (255,255,0))
  pos_label = myfont.render(pos_debug, 1, (255,255,0))
        
  pressedKeys = pygame.key.get_pressed()
  handle_input(pressedKeys)

  gameDisplay.fill(BLACK)  
  
  player.move()
  
  draw_ship(player.pos, player.direction)
  
  for bullet in bullets:
    bullet.move()
    if bullet.life > 0:
      bullet.draw()
    else:
      bullets.remove(bullet)
      del bullet
      
  for asteroid in asteroids:
    asteroid.move()
    asteroid.draw()

  
  if debug:
    gameDisplay.blit(direction_label, (50, 50))
    gameDisplay.blit(thrusting_label, (50, 70))
    gameDisplay.blit(movement_label, (50, 90))
    gameDisplay.blit(ship_label, (50, 110))
    gameDisplay.blit(pos_label, (50, 130))
    
    for asteroid in asteroids:
      if hypot(asteroid.pos[0] - player.pos[0], asteroid.pos[1] - player.pos[1]) < 50:
        pygame.draw.aaline(gameDisplay, RED, asteroid.pos, player.pos, 1)
      else:
        pygame.draw.aaline(gameDisplay, WHITE, asteroid.pos, player.pos, 1)

  pygame.display.update()

  ticker.tick(50)

pygame.quit()
quit()
