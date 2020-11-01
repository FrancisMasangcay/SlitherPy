# pygame module installed in virtual env not on local machine 
# so you must run snake.py in terminal while the env is active
import pygame, sys, random

#game config vars
w = 800 #width of game screen
h = 920 #height of game screen
board_h = h - w #score board height
numRows = 20
numCols = 20
offset = 2 #gridline pixel offset
step_x = int(w / numCols) #width of boxes, 120 is the height of the score board
step_y = int((h - board_h) / numRows) #height of boxes
HEAD_C = (34,139,34) #snake head color
BODY_C = (50,205,50) #snake body color
high_score = 0

class Cube():
  def __init__(self, color, x, y):
    self.surf = pygame.Surface((step_x - offset, step_y - offset)) #sets a cube surface with width and height of step
    self.surf.fill(color) #fills the cube wih the desired color
    self.rect = self.surf.get_rect(topleft = (x + offset, y + offset)) #creates a rect object at coordinates x, y
    
  #cube rects only ever get manipulated using the top and left sides of the rect
  #move function takes in a new position value and a direction (up, down, left or right) which is a char
  #depending on the direction the position is added/subtracted from the top or left position of the rect
  def move(self, newPos, dir):
    if(dir == 0 or dir == 1):
      self.rect.top += newPos
    else:
      self.rect.left += newPos

class Snake():
  def __init__(self):
    self.head = Cube(HEAD_C, 0, board_h)
    self.body = [] #list of cubes to represent body
    self.body.append(self.head) #attach head to body
    self.direction = 3

  def grow(self):
    tail = self.body[-1]
    x = tail.rect.left
    y = tail.rect.top

    if len(self.body) == 1: #there is only a head segment of the snake
      #check for direction of snake
      if self.direction == 0:
        y += step_y
      elif self.direction == 1:
        y -= step_y
      elif self.direction == 2:
        x -= step_x
      else:
        x += step_x
    elif(self.body[-2].rect.top < tail.rect.top): #tail is directly below next segment
      y += step_y
    elif(self.body[-2].rect.top > tail.rect.top): #directly above next segment
      y -= step_y
    elif(self.body[-2].rect.left < tail.rect.left): #tail is right of the next segment
      x += step_x
    else: #tail is left of next segment
      x -= step_x
    c = Cube(BODY_C, x, y) 
    self.body.append(c)

  
  #direction denotes snake movement direction (0, 1, 2, 3)->(up, down, left, right)
  def move(self, game_state):
    #store original coord of head
    previous = self.head.rect.topleft
    #move the head
    if self.direction == 0:
      self.head.rect.top -= step_y
    elif self.direction == 1:
      self.head.rect.top += step_y
    elif self.direction == 2:
      self.head.rect.left -= step_x
    else:
      self.head.rect.left += step_x

    #check if head ran out of bounds, if so end the game
    if (self.head.rect.left > w) or (self.head.rect.left < 0):
      game_state = False

    if(self.head.rect.top > h) or (self.head.rect.top < board_h):
      game_state = False
    
    #move the body
    for s in range(1, len(self.body)):
      if self.head.rect.colliderect(self.body[s].rect):
        game_state = False
      temp = self.body[s].rect.topleft #stores current segment coord
      self.body[s].rect.topleft = previous
      previous = temp

    return game_state

#make an instance of a cube to represent a snack, 
#coordinates will be at a random location, returns the cube
#takes snake body list as a param
def mkSnack(body):
  found = False
  #ensure morsel is not generated on top of snake
  while not found:
    x = random.randint(0, numCols - 1) * step_x
    y = (random.randint(0, numRows - 1) * step_y) + board_h
    morsel = Cube((220,20,60), x, y)
    found = True
    for cube in body:
      cRect = cube.rect
      mRect = morsel.rect
      if mRect.colliderect(cRect):
        found = False
        break

  return morsel

def scores_display(score, h_score, screen):
  if score > h_score:
    global high_score
    high_score = score

  score_surf = game_font.render("Score: " + str(score), True, (196, 232, 197))
  score_rect = score_surf.get_rect(center = (int(w / 2),int(board_h / 4)))
  screen.blit(score_surf, score_rect)

  hScore_surf = game_font.render("HighScore: " + str(high_score), True, (196, 232, 197))
  h_rect = hScore_surf.get_rect(center = (int(w / 2),int(3 * board_h / 4)))
  screen.blit(hScore_surf, h_rect)

def make_btn(screen, label, x, y, width, height, inactiveC, activeC, action = None):
  mouse = pygame.mouse.get_pos()
  clicked  = pygame.mouse.get_pressed()
  btn = game_font.render(label, True, (0, 0, 0))
  btnRect = btn.get_rect(center = ((x + int(width / 2)),(3*board_h+int(h/10))))

  #mouse hovering over play button
  if (x < mouse[0] < (x + width)) and (y < mouse[1] < (y + height)): #checks vertical bounds
    pygame.draw.rect(screen, activeC, (x, y, width, height))
    if clicked[0] == 1 and action != None:
      action()
  else:
      pygame.draw.rect(screen, inactiveC, (x, y, width, height))

  screen.blit(btn, btnRect)

def game_over(screen):
  global big_font
  big_font = pygame.font.Font('./fonts/BebasNeue-Regular.ttf', 64)
  msg = big_font.render("Game Over", True, (0, 0, 0))
  msg_rect = msg.get_rect(center = (int(w / 2), int(2*board_h+int(h/10))))

  #the main modal
  pygame.draw.rect(screen, (211, 238, 211), (int((w/4)), int(2*board_h), int(w/2), int(h/3)))
  pygame.draw.rect(screen, (160, 218, 160), (int((w/4)+5), 2*board_h+4, int(w/2)-10, int(h/3)-8))
  #button rectangles
  btnW = int(w / 8)
  btnH = int(3 / 40 * h)
  t = 3 * board_h + int(h / 10) - int(btnH / 2)
  play_left = int(3 /8 * w) - int(btnW / 2)
  quit_left = int(5 /8 * w) - int(btnW / 2)

  #make the btns
  inactive = (115, 157, 66)
  active = (115, 135, 66)
  make_btn(screen, "Play", play_left, t, btnW, btnH, inactive, active, main)
  make_btn(screen, "Quit", quit_left, t, btnW, btnH, inactive, active, exitGame)

  screen.blit(msg, msg_rect)

def exitGame():
  pygame.quit() #quits the game
  sys.exit() #exits while loop and terminates game
  
def main():
  #game initialization
  pygame.init()
  screen = pygame.display.set_mode((w, h)) #sets game display to w by h box
  clock = pygame.time.Clock() #used to track frame rate
  MOVE = pygame.USEREVENT + 1  #move event
  #loads font and sets size to 32
  global game_font
  game_font = pygame.font.Font('./fonts/BebasNeue-Regular.ttf', 32) 
  WHITE = (255, 255, 255) #grid color
  
  #game vars
  s = Snake()
  food = mkSnack(s.body)
  score = len(s.body)

  pygame.time.set_timer(MOVE, 125)
  game_state = True
  
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exitGame()
      
      #handle key states and snake movements
      if event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_UP:
          s.direction = 0
        elif event.key == pygame.K_DOWN:
          s.direction = 1
        elif event.key == pygame.K_LEFT:
          s.direction = 2
        elif event.key == pygame.K_RIGHT:
          s.direction = 3

      if event.type == MOVE:
        game_state = s.move(game_state)

    screen.fill((0,0,0)) #clear screen
    #draw score board
    pygame.draw.line(screen, (116, 201, 117), (0, 0), (w, 0), 12)
    pygame.draw.line(screen, (116, 201, 117), (0, 0), (0, board_h), 12)
    pygame.draw.line(screen, (116, 201, 117), (w, 0), (w, board_h), 12)
    pygame.draw.line(screen, (116, 201, 117), (0, board_h - 4), (w, board_h - 4), 6)
    #draw vertical lines for gird
    x = 0
    while x <= w:
      pygame.draw.line(screen, WHITE, (x, board_h), (x, h), 3) #draws line on screen 
      x += step_x

    #draw horizontal lines for grid
    y = board_h
    while  y <= h:
      pygame.draw.line(screen, WHITE, (0, y), (w, y), 3) #draws line on screen
      y += step_y

    #if game is running
    if game_state == True:
      if s.head.rect.colliderect(food.rect):
        score += 1
        s.grow()
        food = mkSnack(s.body)

      scores_display(score, high_score, screen)
      for segment in s.body:
        screen.blit(segment.surf, segment.rect)
      
      screen.blit(food.surf, food.rect)
    else: #game over screen
      scores_display(score, high_score, screen)
      game_over(screen)

    pygame.display.update()
    clock.tick(120) #sets max frame rate to 120 fps

if __name__ == "__main__":
  main()