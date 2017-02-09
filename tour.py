#!/usr/bin/env python

"""
This code generates the path required for a knight's tour
around a chessboard with user-specified dimensions

Written by Sophie Li, 2017
http://blog.justsophie.com/algorithm-for-knights-tour-in-python/
"""
import sys
import time

try:
    import pygame
    from tour_visualizer import Model, View
    GUI_ON = True
except ImportError:
    GUI_ON = False

class PathFound(RuntimeError):
    pass

class KnightsTour:
    def __init__(self, size, rules):
        """
        size = size of the chessboard
        rules = rules the tour must follow. Type is a dictionary where the key is
        the move number (int) and the value is the location of the square.

        i.e:

        rules = {1: (0,0), 5: (4,5)} etc..
        """
        self.w = size[0]
        self.h = size[1]
        self.initial_pos = (0, 0)

        self.rules = rules
        self.reserved_positions = []

        self.closed_tour = False
        self.closed_positions = []

        self.board = []
        self.generate_board()

    def generate_board(self):
        """
        Creates a nested list to represent the game board
        Each element is a two element tuple (x1, x2) where:
        x1: what step of tour landed on this square
        x2: square is reserved in rules/no
        """
        for i in range(self.h):
            self.board.append([0]*self.w)

        for k in rules.keys():
            self.reserved_positions.append(rules[k])

    def print_board(self):
        print "  "
        print "------"
        for elem in self.board:
            print elem
            # print [x for (x,y) in elem]
        print "------"
        print "  "

    def generate_legal_moves(self, cur_pos):
        """
        Generates a list of legal moves for the knight to take next
        """
        possible_pos = []
        move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                        (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for move in move_offsets:
            new_x = cur_pos[0] + move[0]
            new_y = cur_pos[1] + move[1]

            if (new_x >= self.h):
                continue
            elif (new_x < 0):
                continue
            elif (new_y >= self.w):
                continue
            elif (new_y < 0):
                continue
            else:
                possible_pos.append((new_x, new_y))

        return possible_pos

    def sort_lonely_neighbors(self, to_visit):
        """
        It is more efficient to visit the lonely neighbors first,
        since these are at the edges of the chessboard and cannot
        be reached easily if done later in the traversal
        """
        neighbor_list = self.generate_legal_moves(to_visit)
        empty_neighbours = []

        for neighbor in neighbor_list:
            np_value = self.board[neighbor[0]][neighbor[1]]
            if (np_value == 0) and (neighbor not in self.reserved_positions):
                empty_neighbours.append(neighbor)

        scores = []
        for empty in empty_neighbours:
            score = [empty, 0]
            moves = self.generate_legal_moves(empty)
            for m in moves:
                if self.board[m[0]][m[1]] == 0:
                    score[1] += 1
            scores.append(score)

        scores_sort = sorted(scores, key = lambda s: s[1])
        sorted_neighbours = [s[0] for s in scores_sort]
        return sorted_neighbours

    def tour(self, n, path, to_visit):
        """
        Recursive definition of knights tour. Inputs are as follows:
        n = current depth of search tree
        path = current path taken
        to_visit = node to visit
        """
        self.board[to_visit[0]][to_visit[1]] = n
        path.append(to_visit) #append the newest vertex to the current point
        print "Visiting: ", to_visit

        if n == self.w * self.h: #if every grid is filled
            if self.closed_tour:
                if path[-1] in self.closed_positions:
                    self.path = path
                    raise PathFound
                else:
                    print "Not a tour"
                    self.board[to_visit[0]][to_visit[1]] = 0
                    try:
                        path.pop()
                    except IndexError:
                        raise Exception("No successful path was found")
            else:
                self.path = path
                raise PathFound
        else:
            rule_location = self.rules.get(n+1, None)
            if rule_location is None:
                sorted_neighbours = self.sort_lonely_neighbors(to_visit)
                for neighbor in sorted_neighbours:
                    self.tour(n+1, path, neighbor)
            else:
                if rule_location in self.generate_legal_moves(to_visit):
                    print "Obeying rule: ", rule_location
                    self.tour(n+1, path, rule_location)

            #If we exit this loop, all neighbours failed so we reset
            self.board[to_visit[0]][to_visit[1]] = 0
            try:
                path.pop()
                print "Going back to: ", path[-1]
            except IndexError:
                raise Exception("No successful path was found")

    def find_path(self, n, path, start):
        try:
            if self.closed_tour:
                self.closed_positions = self.generate_legal_moves(self.initial_pos)
            self.tour(n, path, start)
        except PathFound:
            if GUI_ON:
                pygame.init()
                size = (60*self.w, 60*self.h)

                model = Model(self.w, self.h, path)

                view = View(model, size)
                view.animate_path()

            return self.path

if __name__ == '__main__':
    # rules = {2:(2,1), 3:(3,3)} #example possible ruleset
    # rules = {2:(2,1), 3:(4,4)} #example impossible ruleset
    rules = {}

    #Define the size of grid. We are currently solving for an 8x8 grid
    kt = KnightsTour(size=(8, 8), rules=rules)
    # kt.closed_tour = True #uncomment if you want a closed tour
    kt.initial_pos = (0,0)

    kt.find_path(1, [], kt.initial_pos)
    kt.print_board()
