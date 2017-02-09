import pygame
from pygame.locals import QUIT, KEYDOWN
import time
import random

class View(object):
    """ Provides a view of the chessboard with specified model """
    def __init__(self, model, size):
        """ Initialize with the specified model """
        self.model = model
        self.screen = pygame.display.set_mode(size)

        self.lines = []

    def draw(self):
        """ Draw the game to the pygame window """
        self.screen.fill(pygame.Color('white'))

        for j in self.model.chessboard:
            for r in j:
                pygame.draw.rect(self.screen, pygame.Color('black'), r, 1)

        pygame.display.update()

    def center_pixel(self, r):
        c_pix = (r.x+(self.model.box_height/2), r.y+(self.model.box_height/2))
        return c_pix

    def color_square(self, prev_square, square):
        i = square[1]
        j = square[0]

        r = self.model.chessboard[i][j]

        pygame.draw.rect(self.screen, (255, 204, 255), r)
        pygame.draw.rect(self.screen, pygame.Color('black'), r, 1)

        if prev_square != None:
            i_p = prev_square[1]
            j_p = prev_square[0]
            r_p = self.model.chessboard[i_p][j_p]

            c_pix_p = self.center_pixel(r_p)
            c_pix = self.center_pixel(r)

            self.lines.append((c_pix_p, c_pix))

            for l in self.lines:
                pygame.draw.line(self.screen, pygame.Color('black'), l[0], l[1], 3)

        pygame.display.update()


    def animate_path(self):
        running = True
        while running:
            self.draw()
            self.color_square(None, self.model.path[0])

            i = 1
            print "LENGTH PATH: ", len(self.model.path)
            while i < (len(self.model.path)):
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        running = False
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        running = False

                self.color_square(self.model.path[i-1], self.model.path[i])

                if i == (len(self.model.path) - 2):
                    self.color_square(self.model.path[i], self.model.path[i+1])

                i += 1
                time.sleep(0.25)
            running = False

        j = raw_input("Press enter to end")

class Model(object):
    """ Represents the state of the chessboard"""
    def __init__(self, w, h, path):
        self.w = w
        self.h = h
        self.path = path

        self.box_height = 60
        self.chessboard = []

        for i in range(self.w):
            row = []
            for j in range(self.h):
                r = pygame.Rect(i*self.box_height, j*self.box_height, self.box_height, self.box_height)
                row.append(r)
            self.chessboard.append(row)


if __name__ == '__main__':
    #Define the size of grid.
    m = int(raw_input("M dimension: "))
    n = int(raw_input("N dimension: "))

    kt = KnightsTour(m, n)
    kt.initial_pos = (0,0)

    #Flip the following variables depending use case
    kt.closed_tour = True
    kt.visualize = True

    kt.closed_positions = kt.generate_legal_moves(kt.initial_pos)
    kt.tour(1, [], kt.initial_pos)
