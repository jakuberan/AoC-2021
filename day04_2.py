# Define path
data_path = "data/input04"

# Counters
boards = []
numbers = None
board = []

# Read line-by-line
f = open(data_path, "r")
for x in f:
    row = x.strip().split()
    if numbers is None:
        numbers = [int(a) for a in row[0].split(',')]
    elif len(row) > 1:
        board.append([int(r) for r in row])
        if len(board) == 5:
            boards.append(board)
            board = []
            
def verify_board(board, i, j, dim = 5):
    if sum(board[i]) == -5: return True
    if sum([board[c][j] for c in range(dim)]) == -5: return True
    return False

def board_sum(board, dim = 5):
    out = 0
    for i in range(dim):
        for j in range(dim):
            if board[i][j] > 0:
                out += board[i][j]
    return out
            
def remove_num(boards, num, dim = 5):
    boards_out = []
    out = None
    for board_num, board in enumerate(boards):
        pending = True
        still_playing = True
        for i in range(dim):
            for j in range(dim):
                if pending:
                    if board[i][j] == num:
                        pending = False
                        board[i][j] = -1
                        if verify_board(board, i, j):
                            still_playing = False
                            if len(boards) == 1:
                                 out = board_sum(board)
        if still_playing:
            boards_out.append(board)
    return boards_out, out
                        
                        
for num in numbers:
    boards, out = remove_num(boards, num, dim = 5)
    if out is not None:
        print(f'Score: {out * num}')
        break
        
        
        
        