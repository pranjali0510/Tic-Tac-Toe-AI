import sys
import pygame
import random
import copy
import numpy as np

from constants import *

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC-TAC-TOE AI')
screen.fill( BG_COLOR )

class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLUMNS) ) 
        self.empty_squares = self.squares #[squares]
        self.marked_squares = 0

    def final_state(self, show = False):
       #return 0 if there is no win yet
       #return 1 if player 1 wins
       #return 2 if player 2 wins

       #vertical wins
       for column in range(COLUMNS):
           if self.squares[0][column] == self.squares[1][column] == self.squares[2][column] != 0:
               if show:
                   color = CIRC_COLOR if self.squares[0][column] == 2 else CROSS_COLOR
                   iPos = (column * SQSIZE + SQSIZE // 2, 20)
                   fPos = (column * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                   pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
               return self.squares[0][column]
           
        #horizontal wins
       for row in range(ROWS):
           if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
               if show:
                   color = CIRC_COLOR if self.squares[0][row] == 2 else CROSS_COLOR
                   iPos = (20, row * SQSIZE + SQSIZE // 2)
                   fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                   pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
               return self.squares[row][0]
           
        #diagonal wins
        #desc diagonal
       if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
           if show:
                   color = CIRC_COLOR if self.squares[1][1]== 2 else CROSS_COLOR
                   iPos = (20, 20)
                   fPos = (WIDTH - 20, HEIGHT - 20)
                   pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
                   
           return self.squares[1][1]
       
       #asc diagonal
       if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                   color = CIRC_COLOR if self.squares[1][1]== 2 else CROSS_COLOR
                   iPos = (20, HEIGHT-20)
                   fPos = (WIDTH - 20, 20)
                   pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)

            return self.squares[1][1]
       #no win yet
       return 0
        
    def mark_squares(self, row, column, player):
        self.squares[row][column] = player
        self.marked_squares += 1

    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.empty_square(row, column):
                    empty_squares.append( (row, column) )
        return empty_squares

    def empty_square(self, row, column):
        return self.squares[row, column] == 0
    
    def isfull(self):
        return self.marked_squares == ROWS * COLUMNS
    
    def isempty(self):
        return self.marked_squares == 0
    
class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index]
    
    def minimax(self, board, maximizing):
        #terminal cases
        case = board.final_state()

        #player 1 wins
        if case == 1:
            return 1, None #evaluation,move
        
        #player 2 wins
        if case == 2:
            return -1, None
        
        #a draw
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_evaluation = -100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, column) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_squares(row, column, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_evaluation:
                    max_evaluation = eval
                    best_move = (row, column)

            return max_evaluation, best_move

        elif not maximizing:
            min_evaluation = 100
            best_move = None
            empty_squares = board.get_empty_squares()

            for (row, column) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_squares(row, column, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_evaluation:
                    min_evaluation = eval
                    best_move = (row, column)

            return min_evaluation, best_move





    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)


        else:
            #minimax algo
            eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move #row & column


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # 1-cross 2-circles # for self.player = 2 AI STARTS THE GAME FIRST
        self.gamemode = 'ai' #pvp or ai
        self.running = True
        self.show_lines()


    def make_moves(self, row, column):
        if self.board.empty_square(row, column) and self.running:
          self.board.mark_squares(row, column, self.player)
          self.draw_fig(row, column)
        if self.is_over():
            self.running = False
        self.next_turn()
        
        

    def show_lines(self):

        # bg
        screen.fill( BG_COLOR )
        #VERTICAL
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQSIZE, 0), (WIDTH-SQSIZE, HEIGHT), LINE_WIDTH)


        #HORIZONTAL
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT-SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, column):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (column * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (column * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # asc line
            start_asc = (column * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (column * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)


        elif self.player == 2:
            # draw circle
            center = (column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)


    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def is_over(self):
        return self.board.final_state(show = True) != 0 or self.board.isfull()
    
    
    def reset(self):
        self.__init__()



def main():
    game = Game()
    board = game.board
    ai = game.ai



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-reset
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1
                     
            if event.type == pygame.MOUSEBUTTONDOWN:
               pos = event.pos
               row = pos[1] // SQSIZE
               column = pos[0] // SQSIZE

               if board.empty_square(row, column) and game.running:
                   game.make_moves(row, column)

                   if game.is_over():
                       game.running = False

            

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #update the screen
            pygame.display.update()   

            #ai methods
            row, column = ai.eval(board)        
            game.make_moves(row, column)

            if game.is_over():
                game.running = False

        pygame.display.update()
              




        


main()
