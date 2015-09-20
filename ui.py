import pygame
from pygame.locals import *
import sys
import numpy as np

CELL_WIDTH = 24
CELL_HEIGHT = 16

CELL_BORDER = 2
CELL_PADDING = 3


colorPalette1 = {
  "background" : pygame.Color(255, 255, 255),
  "cell_border" : pygame.Color(152,152,152),
  "cell_body_empty" : pygame.Color(240,240,240),
  "cell_body_empty_cursor" : pygame.Color(200,200,200),
  "cell_body_filled" : pygame.Color(255,0,0),
  "cell_body_filled_cursor" : pygame.Color(200,0,0),
  "cell_cursor" : pygame.Color(255,0,255),
  "display_text" : pygame.Color(0,0,0)
}

CURRENT_PALETTE = colorPalette1


class Grid(object):
  def __init__(self, (dataWidth, dataHeight), (gridWidth, gridHeight), (gridX, gridY)):
    self.dataWidth = dataWidth
    self.dataHeight = dataHeight

    self.gridWidth = gridWidth
    self.gridHeight = gridHeight

    self.gridX = gridX
    self.gridY = gridY

    self.data = np.zeros( (dataWidth, dataHeight) )

    self.cellEdges = []
    self.cellInners = []

    for x in range(0, self.gridWidth):
      self.cellEdges.append([])
      self.cellInners.append([])

      for y in range(0, self.gridHeight):
        cell_x = self.gridX + (CELL_WIDTH + CELL_PADDING) * x
        cell_y = self.gridY + (CELL_HEIGHT + CELL_PADDING) * y

        edge_r = pygame.Rect( (cell_x, cell_y), (CELL_WIDTH, CELL_HEIGHT) )
        inner_r = pygame.Rect( (cell_x + CELL_BORDER, cell_y + CELL_BORDER), (CELL_WIDTH - CELL_BORDER * 2, CELL_HEIGHT - CELL_BORDER * 2) )

        self.cellEdges[x].append(edge_r)
        self.cellInners[x].append(inner_r)


  def draw(self, screen, cursor, offset):
    assert len(cursor) == 2
    assert type(cursor) == tuple

    assert len(offset) == 2
    assert type(offset) == tuple

    offset_x, offset_y = offset

    for x in range(0, self.gridWidth):
      for y in range(0, self.gridHeight):
        cell_x = offset_x + x
        cell_y = offset_y + y
        cursor_on_cell = cursor == (cell_x,cell_y)

        if cursor_on_cell:
          edge_color = CURRENT_PALETTE["cell_cursor"]
        else:
          edge_color = CURRENT_PALETTE["cell_border"]

        if self.isEmpty( (cell_x, cell_y) ):
          if cursor_on_cell:
            inner_color = CURRENT_PALETTE["cell_body_empty_cursor"]
          else:
            inner_color = CURRENT_PALETTE["cell_body_empty"]
          
        else:
          if cursor_on_cell:
            inner_color = CURRENT_PALETTE["cell_body_filled_cursor"]
          else:
            inner_color = CURRENT_PALETTE["cell_body_filled"]

        edge_r = self.cellEdges[x][y]
        inner_r = self.cellInners[x][y]

        pygame.draw.rect(screen, edge_color, edge_r, 0)
        pygame.draw.rect(screen, inner_color, inner_r, 0)

  def get(self, (x,y) ):
    return self.data[x,y]

  def isFilled(self, (x,y)):
    s = self.get( (x,y) )
    return s == 1.0

  def isEmpty(self, (x,y)):
    return not self.isFilled( (x,y) )

  def setFilled(self, (x,y)):
    self.data[x,y] = 1

  def setEmpty(self, (x,y)):
    self.data[x,y] = 0
  
  def clearGrid(self):
    self.data = np.zeros( (self.dataWidth, self.dataHeight) )

  def toggleFilled(self, (x,y)):
    if self.isFilled( (x, y) ):
      self.setEmpty( (x, y) )
    else:
      self.setFilled( (x, y) )


class NoteLetters(object):
  def __init__(self, (x,y)):
    self.x = x
    self.y = y

    self.font = pygame.font.Font(None,12)

    # in ascending order
    self.letters = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

  def draw(self, screen):
    for i, l in enumerate(reversed(self.letters)):
      t = self.font.render(l, False, CURRENT_PALETTE["display_text"])
      text_x = self.x
      text_y  = self.y + (CELL_HEIGHT + CELL_PADDING) * i
      screen.blit(t, (text_x, text_y))

class TimeLetters(object):
  def __init__(self, (x,y)):
    self.x = x
    self.y = y

    self.font = pygame.font.Font(None,12)


  def draw(self, screen, letters):
    for i, l in enumerate(letters):
      t = self.font.render(l, False, CURRENT_PALETTE["display_text"])
      text_x = self.x + (CELL_WIDTH + CELL_PADDING) * i
      text_y  = self.y
      screen.blit(t, (text_x, text_y))


def run():
  pygame.init()
  fpsClock = pygame.time.Clock()

  screen = pygame.display.set_mode( (1024, 600) )

  songWidth, songHeight = 64, 36

  gridWidth, gridHeight = 32, 12

  grid = Grid( (songWidth, songHeight), (gridWidth, gridHeight), (20, 20) )
  noteLetters = NoteLetters( (5, 24) )
  timeLetters = TimeLetters( (23, 10) )

  cursor = 0,0
  gridLocation = 0,0

  while True:
    # handle events
    events = pygame.event.get()

    for event in events:
      if event.type == QUIT:
        sys.exit()
      elif event.type == KEYDOWN:
        cursor_x, cursor_y = cursor
        grid_x, grid_y = gridLocation
 
        if event.key == K_ESCAPE:
          pygame.event.post(pygame.event.Event(QUIT))
        elif event.key == K_LEFT:
          # move cursor left
          if cursor_x > 0:
            if cursor_x == grid_x:
              grid_x -= 1
            cursor_x -= 1

        elif event.key == K_RIGHT:
          # move cursor right
          if cursor_x < songWidth - 1:
            if cursor_x == (grid_x + gridWidth - 1):
              grid_x += 1
            cursor_x += 1

        elif event.key == K_UP:
          print grid_y, cursor_y
          # move cursor up
          if cursor_y > 0:
            if cursor_y == grid_y:
              grid_y -= 1
            cursor_y -= 1

        elif event.key == K_DOWN:
          print grid_y, cursor_y
          # move cursor down
          if cursor_y < songHeight - 1:
            if cursor_y == (grid_y + gridHeight - 1):
              grid_y += 1
            cursor_y += 1

        elif event.key == K_SPACE:
          grid.toggleFilled( (cursor_x, cursor_y) )
        elif event.key == K_a:
          # move grid left
          if grid_x > 0:
            grid_x -= 1
        elif event.key == K_d:
          # move grid right
          if grid_x < (songWidth - gridWidth) - 1:
            grid_x += 1
        elif event.key == K_w:
          # move grid up
          if grid_y > 0:
            grid_y -= 1
        elif event.key == K_s:
          # move grid down
          if grid_y < (songHeight - gridHeight) - 1:
            grid_y += 1

        gridLocation = (grid_x, grid_y)
        cursor = (cursor_x, cursor_y)

    # draw stuff
    screen.fill( CURRENT_PALETTE["background"] )

    grid.draw(screen, cursor, gridLocation)

    t = [str(l) for l in range(gridLocation[0], gridLocation[0]+gridWidth)]
    timeLetters.draw(screen,t)
    noteLetters.draw(screen)

    pygame.display.update()

    # fps tick!
    fpsClock.tick(30)


if __name__ == "__main__":
  run()
