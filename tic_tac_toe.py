import random


class TicTacToe:

    def __init__(self):
        self.board = []

    def create_board(self):
        """Create a 3x3 board initialized with '-' symbols"""
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

    def get_random_first_player(self):
        """Randomly select which player goes first"""
        return random.randint(0, 1)

    def fix_spot(self, row, col, player):
        """Place the player's symbol on the board"""
        self.board[row][col] = player

    def is_player_win(self, player):
        """Check if the player has won the game"""
        win = None
        n = len(self.board)

        # Check rows
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # Check columns
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # Check diagonal (top-left to bottom-right)
        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        # Check diagonal (top-right to bottom-left)
        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win

        return False

    def is_board_filled(self):
        """Check if the board is completely filled"""
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def swap_player_turn(self, player):
        """Switch between players X and O"""
        return 'X' if player == 'O' else 'O'

    def show_board(self):
        """Display the current state of the board"""
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def start(self):
        """Main game loop"""
        self.create_board()

        # Randomly select first player
        player = 'X' if self.get_random_first_player() == 1 else 'O'
        
        while True:
            print(f"Player {player} turn")

            self.show_board()

            # Get user input with validation
            try:
                row, col = list(
                    map(int, input("Enter row and column numbers to fix spot (1-3): ").split()))
                print()

                # Validate input range
                if row < 1 or row > 3 or col < 1 or col > 3:
                    print("Invalid input! Please enter numbers between 1 and 3.")
                    continue

                # Check if spot is already taken
                if self.board[row - 1][col - 1] != '-':
                    print("Spot already taken! Choose another spot.")
                    continue

                # Fix the spot
                self.fix_spot(row - 1, col - 1, player)

            except ValueError:
                print("Invalid input! Please enter two numbers separated by space (e.g., 1 2)")
                continue
            except IndexError:
                print("Invalid input! Please enter numbers between 1 and 3.")
                continue

            # Check if current player won
            if self.is_player_win(player):
                print(f"Player {player} wins the game!")
                break

            # Check if game is draw
            if self.is_board_filled():
                print("Match Draw!")
                break

            # Swap player turn
            player = self.swap_player_turn(player)

        # Show final view of the board
        print()
        self.show_board()


# Start the game
if __name__ == "__main__":
    tic_tac_toe = TicTacToe()
    tic_tac_toe.start()
