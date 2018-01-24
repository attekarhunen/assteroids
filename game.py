import pygame
import sys
from math import sin, cos, radians, pi
from random import randint

#handle input from pressed keys here
def handle_input(pressedKeys):
  if pressedKeys[pygame.K_UP]:
    player.thrusting = True
    player.thrust()
  if not pressedKeys[pygame.K_UP]:
    player.thrusting = False
    player.decelerate()
  if pressedKeys[pygame.K_LEFT]:
    player.turn('left')
  if pressedKeys[pygame.K_RIGHT]:
    player.turn('right')

#draw ship geometry
def draw_ship(pos, direction):
  geometry = translate_graphics(player.geometry, pos, direction)
  pygame.draw.aalines(gameDisplay, WHITE, True, geometry, 2)

  
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
    self.movement = [0.0, 0.0]
    self.thrusting = False
    self.speed = 0
    self.dx = 0.0
    self.dy = 0.0
  
  def accelerate(self):
    if self.speed < 4.5:
      self.speed(self.speed+THRUST)

  def decelerate(self):
    if(self.speed > 0):
      self.speed -= FRICTION
    if(self.speed < 0):
      self.speed = 0
  
  def turn(self, direction):
    if direction == 'left':
      self.direction = self.direction + TURN_RATE
    else:
      self.direction = self.direction - TURN_RATE

  def move(self):
    self.movement = [0.0,0.0]
    
    self.movement[0] += self.speed * angle_to_vector(self.direction)[0]
    self.movement[1] += self.speed * angle_to_vector(self.direction)[1]

    self.pos = ((self.pos[0]+self.movement[0],self.pos[1]+self.movement[1]))
    
  def is_alive(self):
    if self.health < 0:
      self.alive = False
      self.set_speed(0)
    return self.alive
    
  def thrust(self):
    if(self.speed < 4):
      self.speed += THRUST
  
pygame.init()

myfont = pygame.font.SysFont("monospace", 15)


#init some constants
DISPLAY_W = 1200
DISPLAY_H = 800
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
TURN_RATE = 0.15
THRUST = 0.5
FRICTION = 0.01

player = playerShip((randint(10,DISPLAY_W-10),randint(10,DISPLAY_H-10)))

gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))

pygame.display.set_caption('ASSTEROIDS')
ticker = pygame.time.Clock()
debug = False
if len(sys.argv) > 1:
  if sys.argv[1] == 'debug':
    debug = True

game_running = True

while game_running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game_running = False
  
  direction_debug = "Direction: " + str(player.direction)
  thrusting_debug = "Thrusting: " + str(player.thrusting) + ", (" + str(THRUST) + ")"
  movement_debug = "Movement vector: " + str(player.movement)
  ship_debug = "Ship vector: " + str(angle_to_vector(player.direction))
  pos_debug = "Ship position: " + str(player.pos)
  speed_debug = "Ship speed: " + str(player.speed)
  direction_label = myfont.render(direction_debug, 1, (255,255,0))
  thrusting_label = myfont.render(thrusting_debug, 1, (255,255,0))
  movement_label = myfont.render(movement_debug, 1, (255,255,0))
  ship_label = myfont.render(ship_debug, 1, (255,255,0))
  pos_label = myfont.render(pos_debug, 1, (255,255,0))
  speed_label = myfont.render(speed_debug, 1, (255,255,0))
        
  pressedKeys = pygame.key.get_pressed()
  handle_input(pressedKeys)

  gameDisplay.fill(BLACK)  
  
  player.move()
  
  draw_ship(player.pos, player.direction)
  
  if debug:
    gameDisplay.blit(direction_label, (50, 50))
    gameDisplay.blit(thrusting_label, (50, 70))
    gameDisplay.blit(movement_label, (50, 90))
    gameDisplay.blit(ship_label, (50, 110))
    gameDisplay.blit(pos_label, (50, 130))
    gameDisplay.blit(speed_label, (50, 150))

  pygame.display.update()

  ticker.tick(50)

pygame.quit()
quit()
