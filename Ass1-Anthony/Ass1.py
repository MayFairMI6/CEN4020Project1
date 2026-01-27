#!/usr/bin/env python

class CLI:
    def __init__(self):
        pass

    def display_board(self, board, score, current_num):   #display the board


        #print the board
        print("\n  |        Matrix Game        |")
        print("     1     2     3     4     5")
        print("  +-----+-----+-----+-----+-----+")
        for row in range(5):
            row_str = str(row + 1) + " |"
            for col in range(5):
                val = board[row][col]
                if val == 0:
                    row_str += "     |"
                else:
                    row_str += " %3d |" % val
            print(row_str)
            print("  +-----+-----+-----+-----+-----+")
        print("Score: %d  |  Next number: %d" % (score, current_num))
        print()

    def get_input(self, allow_load=False):   #get the input from the user
        if allow_load:     #if the game is in the first move, allow the user to load the game
            print("Enter:    row col (e.g., 3 2)   |   Save   |   Load   |   Quit")
        else:
            print("Enter:    row col (e.g., 3 2)   |   Save   |   Quit")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'save':   #save the game
            return ('save', None, None)
        elif user_input.lower() == 'load' and allow_load:   #load the game
            return ('load', None, None)
        elif user_input.lower() == 'quit':   #quit the game
            return ('quit', None, None)
        else:
            parts = user_input.split()
            if len(parts) != 2:
                return ('invalid', None, None)   #if the input is invalid, return invalid
            try:
                row = int(parts[0]) - 1   #convert the input to the row and column
                col = int(parts[1]) - 1
                return ('move', row, col)
            except ValueError:
                return ('invalid', None, None)

    def show_message(self, msg):   #prints a message
        print(msg)

    def get_filename(self, prompt):
        filename = input(prompt).strip()
        if filename == "":   #if the filename is empty, return None
            return None
        return filename

    def show_game_over(self, reason, score):   #shows the game over message
        print("\n--- GAME OVER ---")
        print(reason)
        print("Final Score: %d" % score)

    def show_win(self, score):   #shows the win message
        print("\n--- CONGRATULATIONS ---")
        print("Matrix completed!")
        print("Total Score: %d" % score)


class AppLogic:
    def __init__(self):
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.current_num = 1   #initializing the current number to 1
        self.score = 0
        self.last_pos = None
        self.game_over = False
        self.win = False

    def is_valid_move(self, row, col):
        #check bounds
        if row < 0 or row > 4 or col < 0 or col > 4:
            return (False, "out_of_bounds")
        #check if cell is empty
        if self.board[row][col] != 0:
            return (False, "cell_occupied")
        # first move can be anywhere
        if self.current_num == 1:
            return (True, None)
        #check if one step away from last position
        last_row, last_col = self.last_pos
        row_diff = abs(row - last_row)
        col_diff = abs(col - last_col)
        if row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff) > 0:
            return (True, None)
        return (False, "not_adjacent")

    def is_diagonal_move(self, row, col):   #checks if the move is diagonal
        if self.last_pos is None:
            return False
        last_row, last_col = self.last_pos
        row_diff = abs(row - last_row)
        col_diff = abs(col - last_col)
        return row_diff == 1 and col_diff == 1

    def place_number(self, row, col):
        valid, error = self.is_valid_move(row, col)
        if not valid:
            self.game_over = True
            return (False, error)
        
        #if the move is diagonal, add 1 to the score
        if self.is_diagonal_move(row, col):
            self.score += 1

        self.board[row][col] = self.current_num   #place the number on the board
        self.last_pos = (row, col)   #update the last position
        self.current_num += 1

        if self.current_num > 25:   #if the user has placed all the numbers, they win
            self.win = True

        return (True, None)

    def get_state(self):
        return {
            'board': self.board,
            'current_num': self.current_num,
            'score': self.score,
            'last_pos': self.last_pos
        }

    def set_state(self, state):
        self.board = state['board']
        self.current_num = state['current_num']
        self.score = state['score']
        self.last_pos = state['last_pos']
        self.game_over = False
        self.win = False


class FileHandler:
    def __init__(self):
        pass

    def save_game(self, state, filename):
        try:
            with open(filename, 'w') as f:
                #save board
                for row in state['board']:
                    f.write(' '.join(str(x) for x in row) + '\n')
                #save current number
                f.write(str(state['current_num']) + '\n')
                #save score
                f.write(str(state['score']) + '\n')
                #save last position
                if state['last_pos'] is None:
                    f.write('None\n')
                else:
                    f.write('%d %d\n' % (state['last_pos'][0], state['last_pos'][1]))
            return True
        except:
            return False

    def load_game(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                #read board
                board = []
                for i in range(5):
                    row = [int(x) for x in lines[i].strip().split()]
                    board.append(row)
                #read current number
                current_num = int(lines[5].strip())
                #read score
                score = int(lines[6].strip())
                #read last position
                last_line = lines[7].strip()
                if last_line == 'None':
                    last_pos = None
                else:
                    parts = last_line.split()
                    last_pos = (int(parts[0]), int(parts[1]))
                
                return {
                    'board': board,
                    'current_num': current_num,
                    'score': score,
                    'last_pos': last_pos
                }
        except:
            return None


def main():
    cli = CLI()
    game = AppLogic()
    file_mgr = FileHandler()

    cli.show_message("\n5x5 Matrix Game!")
    cli.show_message("Rules:")
    cli.show_message("- Place numbers 1-25 consecutively.")
    cli.show_message("- Each number must be one step away from the previous.")
    cli.show_message("- Diagonal moves earn 1 point.\n")

    while not game.game_over and not game.win:
        cli.display_board(game.board, game.score, game.current_num)
        if game.current_num == 1:
            allow_load = True   #if still in the first move, allow the user to load the game
        else:
            allow_load = False

        action, row, col = cli.get_input(allow_load)  #get the input from the user

        if action == 'move':   #if the user wants to make a move
            success, error = game.place_number(row, col)   #place the number on the board
            
            #if the move is invalid, show the user the reason why it is invalid
            if not success:
                cli.display_board(game.board, game.score, game.current_num)
                if error == "out_of_bounds":
                    cli.show_game_over("Cell is out of bounds.", game.score)
                elif error == "cell_occupied":
                    cli.show_game_over("Cell is already occupied.", game.score)
                elif error == "not_adjacent":
                    cli.show_game_over("Cell is not adjacent to the previous number.", game.score)
                break

        elif action == 'save':     #if the user wants to save the game
            filename = cli.get_filename("Enter filename to save: ")
            if filename is None:
                cli.show_message("Save cancelled.")
            else:
                filename = filename + ".txt"   #add the .txt extension to the filename
                state = game.get_state()
                if file_mgr.save_game(state, filename):   #save the game and end the game
                    cli.show_message("Game saved to '%s'." % filename)
                    cli.show_message("Goodbye!")
                    break
                else:
                    cli.show_message("Error saving game.")   

        elif action == 'load':   #if the user wants to load the game

            #get the full filename from the user including the .txt extension
            filename = cli.get_filename("Enter the full filename to load: ")
            if filename is None:
                cli.show_message("Load cancelled.")
            elif not filename.endswith(".txt"):
                cli.show_message("Error: Only .txt files can be loaded.")
            else:
                state = file_mgr.load_game(filename)
                if state is not None:
                    game.set_state(state)  #load the game and set states
                    cli.show_message("Game loaded from '%s'." % filename)
                else:
                    cli.show_message("Error loading game or file not found.")

        elif action == 'quit':   #if the user wants to quit the game
            cli.show_message("Goodbye!")
            break

        elif action == 'invalid':   #if the input is invalid
            cli.show_message("Invalid input. Try again.")

    if game.win:   #if the user wins the game
        cli.display_board(game.board, game.score, 26)
        cli.show_win(game.score)


if __name__ == "__main__":
    main()
