# Tic-Tac-Toe Game (Human vs Computer)

board = [" " for i in range(9)]

def print_board():
    print()
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")
    print(board[6] + " | " + board[7] + " | " + board[8])
    print()

def check_winner(player):
    win_positions = [
        [0,1,2],[3,4,5],[6,7,8],   # rows
        [0,3,6],[1,4,7],[2,5,8],   # columns
        [0,4,8],[2,4,6]            # diagonals
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
            return True
    return False

def check_draw():
    return " " not in board

def minimax(is_max):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if check_draw():
        return 0

    if is_max:
        best = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                if score > best:
                    best = score
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                if score < best:
                    best = score
        return best

def computer_move():
    best_score = -100
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"

def human_move():
    while True:
        choice = int(input("Enter position (1-9): ")) - 1
        if 0 <= choice <= 8 and board[choice] == " ":
            board[choice] = "X"
            break
        else:
            print("Invalid move. Try again.")

# Game Loop
print("You are X, Computer is O")
print_board()

while True:
    human_move()
    print_board()

    if check_winner("X"):
        print("You win!")
        break
    if check_draw():
        print("It's a draw!")
        break

    computer_move()
    print_board()

    if check_winner("O"):
        print("Computer wins!")
        break
    if check_draw():
        print("It's a draw!")
        break
