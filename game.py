import pygame
from math import sin, cos, radians
from random import randint

#handle input from pressed keys here
def handle_input(pressedKeys):
  if pressedKeys[pygame.K_UP]:
    player.accelerate()
  if not pressedKeys[pygame.K_UP]:
    player.decelerate()
  if pressedKeys[pygame.K_LEFT]:
	player.turn('left')
  if pressedKeys[pygame.K_RIGHT]:
	player.turn('right')
	
def draw_ship(pos, direction):
  graphics = translate_graphics(player.get_graphics(), pos, direction)
  pygame.draw.aalines(gameDisplay, WHITE, True, graphics, 2)

  
def translate_graphics(graphics, pos, direction):
  translated_graphics = ()
  for t_pos in graphics:
    t_pos = rotate_point(t_pos, direction)
    x = t_pos[0] + pos[0]
    y = t_pos[1] + pos[1]
    translated_graphics = ((x,y),) + (translated_graphics)

  return translated_graphics
  
def rotate_point(point, angle):
  angle_rad = radians(angle)
  rotated_point = (point[0] * cos(-angle) - point[1] * sin(-angle),
                 point[0] * sin(-angle) + point[1] * cos(-angle))                 
  return rotated_point
		
class playerShip(object):
  def __init__(self,pos):
    self.pos = pos
    self.direction = 0.0
    self.speed = 0
    self.health = 1000
    self.alive = True
    self.graphics = ((-8.0,-12.0),(0.0,12.0),(8.0,-12.0),(0.0,-10.0))

  def get_pos(self):
    return self.pos
    
  def set_pos(self, pos):
	 self.pos = pos
  
  def set_speed(self, speed):
    self.speed = speed
    
  def get_speed(self):
	return self.speed
	
  def get_direction(self):
    return self.direction

  def accelerate(self):
    if self.get_speed() < 4.5:
	  self.set_speed(self.get_speed()+0.1)

  def decelerate(self):
    if(self.get_speed() > 0):
	  self.set_speed(self.get_speed()*0.98)
	  
  def turn(self, direction):
    if direction == 'left':
   	  self.direction = self.direction + TURN_RATE
    else:
	  self.direction = self.direction - TURN_RATE
		
  def move(self):
    x = self.pos[0] + (self.get_speed() * sin(self.direction)) 
    y = self.pos[1] + (self.get_speed() * cos(self.direction))
    self.set_pos((x,y))
	  
  def is_alive(self):
	  if self.health < 0:
		  self.alive = False
		  self.set_speed(0)
		  
	  return self.alive
	  
  def get_graphics(self):
	  return self.graphics;
	  
pygame.init()

DISPLAY_W = 1200
DISPLAY_H = 800

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
TURN_RATE = 0.15

player = playerShip((randint(10,DISPLAY_W-10),randint(10,DISPLAY_H-10)))

gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))

pygame.display.set_caption('ASSTEROIDS')
ticker = pygame.time.Clock()

game_running = True

while game_running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game_running = False
        
  pressedKeys = pygame.key.get_pressed()
  handle_input(pressedKeys)
	
  if player.get_speed() != 0:
	  player.move()

  gameDisplay.fill(BLACK)  

  draw_ship(player.get_pos(), player.get_direction())

  pygame.display.update()

  ticker.tick(45)

pygame.quit()
quit()
