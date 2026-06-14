WINS = [(0,1,2),(3,4,5),(6,7,8),   # rows
        (0,3,6),(1,4,7),(2,5,8),   # cols
        (0,4,8),(2,4,6)]           # diagonals

def print_board(b):
    sym = {" ": " ", "X": "X", "O": "O"}
    r = lambda i: sym[b[i]]
    print(f"\n {r(0)} | {r(1)} | {r(2)}")
    print("---+---+---")
    print(f" {r(3)} | {r(4)} | {r(5)}")
    print("---+---+---")
    print(f" {r(6)} | {r(7)} | {r(8)}\n")
    
def winner(b):
    for a,c,d in WINS:
        if b[a] == b[c] == b[d] != " ":
            return b[a]
    return None

    

def is_full(b):
    return " " not in b



def minimax(b, is_max):
    w = winner(b)
    if w == "O":  return  1
    if w == "X":  return -1
    if is_full(b): return 0

    scores = []
    for i in range(9):
        if b[i] == " ":
            b[i] = "O" if is_max else "X"
            scores.append(minimax(b, not is_max))
            b[i] = " "

    return max(scores) if is_max else min(scores)



def best_move(b):
    best_score, move = -999, None
    for i in range(9):
        if b[i] == " ":
            b[i] = "O"
            s = minimax(b, False)
            b[i] = " "
            if s > best_score:
                best_score, move = s, i
    return move

def play():
    board = [" "] * 9
    print("=" * 35)
    print("  TIC-TAC-TOE  —  You: X   AI: O")
    print("=" * 35)
    print("\nCell positions:")
    print(" 1 | 2 | 3")
    print("---+---+---")
    print(" 4 | 5 | 6")
    print("---+---+---")
    print(" 7 | 8 | 9")

    while True:
        # Human turn
        print_board(board)
        while True:
            try:
                move = int(input("Your move (1-9): ")) - 1
                if 0 <= move <= 8 and board[move] == " ":
                    break
                print("Invalid — try again.")
            except ValueError:
                print("Enter a number 1-9.")
        board[move] = "X"

        w = winner(board)
        if w:
            print_board(board)
            print("You win!" if w == "X" else "AI wins!")
            break
        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # AI turn
        ai = best_move(board)
        board[ai] = "O"
        print(f"\n  AI plays position {ai+1}")

        w = winner(board)
        if w:
            print_board(board)
            print("AI wins!" if w == "O" else "You win!")
            break
        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break

    if input("\nPlay again? (y/n): ").strip().lower() == "y":
        play()

play()