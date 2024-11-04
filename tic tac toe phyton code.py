import random

# Initialize the board
board = [" " for _ in range(9)]

def print_board():
    """Prints the current state of the Tic Tac Toe board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(player):
    """Checks if a player has won the game."""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def check_draw():
    """Checks if the game is a draw."""
    return " " not in board

def minimax(is_maximizing):
    """Implements the minimax algorithm for AI moves."""
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if check_draw():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def ai_move():
    """Finds the best move for the AI using minimax."""
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"

def player_move(player):
    """Allows a player to make a move."""
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if board[move] == " ":
                board[move] = player
                break
            else:
                print("This spot is already taken.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number between 1 and 9.")

def main():
    print("Welcome to Advanced Tic Tac Toe!")
    game_mode = input("Choose game mode: '1' for Player vs Player, '2' for Player vs AI: ")

    print_board()
    while True:
        player_move("X")
        print_board()
        if check_winner("X"):
            print("Player X wins!")
            break
        if check_draw():
            print("It's a draw!")
            break

        if game_mode == '1':
            player_move("O")
        else:
            ai_move()
            print("AI has made a move:")
        print_board()

        if check_winner("O"):
            print("Player O wins!" if game_mode == '1' else "AI wins!")
            break
        if check_draw():
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()