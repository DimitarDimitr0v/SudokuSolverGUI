board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - -')

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def solve(bo):
    find = find_empty_location(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    for i in range(len(bo)):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for j in range(len(bo)):
        if bo[j][pos[1]] == num and pos[0] != j:
            return False

    box_x = pos[0] // 3
    box_y = pos[1] // 3

    for x in range(box_x * 3, box_x * 3 + 3):
        for y in range(box_y * 3, box_y * 3 + 3):
            if bo[x][y] == num and (x, y) != [pos]:
                return False
    return True


def find_empty_location(bo):
    for r in range(len(bo)):
        for c in range(len(bo[r])):
            if bo[r][c] == 0:
                return r, c


print("_________|RAW|__________")
print_board(board)

solve(board)
print(board)

print("________|SOLVED|________")
print_board(board)

