import pygame
import math
from queue import PriorityQueue


WIDTH,HEIGHT = 800,800

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Path Finding')


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self,row,col,size,total_rows):
        self.row = row #pozycja numer wiersza
        self.col = col #pozycja numer kolumny
        self.size = size #szerokosc i wysokosc bloczku
        self.x = row*size #pozycja na ekranie X
        self.y = col*size #pozycja na ekranie Y
        self.color = WHITE #kolor bloku, jesli bialy to nie byl on sprawdzany
        self.total_rows = total_rows #boczna ilosc wierszy w gridzie

        self.neighbours = [] #lista sasiadow z danego Node


    def get_position(self):
        return self.row, self.col
    #################LOGIKA KOLOROW
    def is_checked(self):
        return self.color == RED #jesli dany Node byl sprawdzony to przypisano mu kolor RED
    
    def is_unchecked(self):
        return self.color == GREEN

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_checked(self):
        self.color = RED

    def make_unchecked(self):
        self.color = GREEN

    def make_wall(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = TURQUOISE

    ########RYSOWANIE NODOW NA OKNIE
    def drawNode(self,win):
        pygame.draw.rect(win, self.color,(self.x, self.y,self.size,self.size))


def make_NodeGrid(rows,width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])

        for j in range(rows):
            node = Node(i,j,gap,rows)
            grid[i].append(node)

    return grid

############RYSOWANIE SIATKI W OKNIE

def draw_gridLines(win,rows,width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap), (width, i*gap))

    for i in range(rows):
        pygame.draw.line(win,GREY,(i*gap,0), (i*gap,width))


def draw(win,grid,rows,width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.drawNode(win)
    
    draw_gridLines(win,rows,width)

    pygame.display.update()

def get_mouse_position(pos,rows,width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap

    return row,col
    


def main(win,width):
    run = True
    clock = pygame.time.Clock()
    ROWS = 16 #dzielenie szerowkosci okna przez ilosc wierszy musi dawac inta, bez tego dzieje sie smierdziawa
    nodeGrid = make_NodeGrid(ROWS,width)
    start = None
    end = None

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos,ROWS,width)
                node = nodeGrid[row][col]

                if not start:
                    if node != end:
                        start = node
                        start.make_start()
                
                elif not end:
                    if node != start:
                        end = node
                        end.make_end()
                
                else:
                    if node != start and node != end:
                        node.make_wall()
            
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos,ROWS,width)
                node = nodeGrid[row][col]

                if start == node:
                    start = None
                    node.reset()
                
                elif end == node:
                    end = None
                    node.reset()

                else:
                    node.reset()

                


        draw(win,nodeGrid,ROWS,width)

    pygame.quit()
                 
if __name__ == '__main__':

    main(WIN,WIDTH)

