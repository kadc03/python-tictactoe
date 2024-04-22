from tkinter import *
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 10
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
symbol_green_color = '#7BC043'


class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Cờ Caro - Chơi với máy')
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0
        
        if not self.player_X_turns:
            self.make_ai_move()

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))
        
        if not self.player_X_turns:
            self.make_ai_move()

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        radius = symbol_size
        self.canvas.create_oval(
            grid_position[0] - radius, grid_position[1] - radius,
            grid_position[0] + radius, grid_position[1] + radius,
            width=symbol_thickness, outline=symbol_O_color
        )

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        offset = symbol_size
        self.canvas.create_line(
            grid_position[0] - offset, grid_position[1] - offset,
            grid_position[0] + offset, grid_position[1] + offset,
            width=symbol_thickness, fill=symbol_X_color
        )
        self.canvas.create_line(
            grid_position[0] - offset, grid_position[1] + offset,
            grid_position[0] + offset, grid_position[1] - offset,
            width=symbol_thickness, fill=symbol_X_color
        )

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text = 'Thắng: Người chơi 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Thắng: Máy (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Cả hai hoà nhau'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 30 bold", fill=color, text=text)

        score_text = 'Điểm \n'
        self.canvas.create_text(size_of_board / 2, 4 * size_of_board / 8, font="cmr 25 bold", fill=symbol_green_color,
                                text=score_text)

        score_text = 'Người chơi 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Máy (O)                : ' + str(self.O_score) + '\n'
        score_text += 'Hoà                      : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 5, font="cmr 20 bold", fill=symbol_green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Nhấn để chơi lại \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 25 bold", fill="gray",
                                text=score_text)

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):
        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):
        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        return gameover

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns

                    if not self.is_gameover():
                        self.make_ai_move()
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                self.display_gameover()
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def make_ai_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board_status[i][j] == 0:
                    self.board_status[i][j] = 1
                    score = self.minimax(self.board_status, 0, False)
                    self.board_status[i][j] = 0

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.board_status[best_move[0]][best_move[1]] = 1
            logical_position = (best_move[0], best_move[1])
            self.draw_O(logical_position)
            self.player_X_turns = not self.player_X_turns

    def minimax(self, board, depth, is_maximizing):
        scores = {
            -1: -1,
            0: 0,
            1: 1
        }

        if self.is_winner('X'):
            return -1
        elif self.is_winner('O'):
            return 1
        elif self.is_tie():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = -1
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = 0
                        best_score = min(score, best_score)
            return best_score


game_instance = Tic_Tac_Toe()
game_instance.mainloop()
