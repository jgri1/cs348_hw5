import common

#helpful, but not needed
class variables:
    counter=0

def sudoku_backtracking(sudoku):
    variables.counter = 0
    solved_sudoku = backtracking_recurse(sudoku)
    return variables.counter

def backtracking_recurse(sudoku):
    variables.counter += 1

    if board_finished(sudoku):
        return sudoku
    
    for y in range(9):  # check all board spots
        for x in range(9):
            if sudoku[y][x] == 0:  # empty spot
                for value in range(1,10):  # check values 1-9
                    if common.can_yx_be_z(sudoku, y, x, value):
                        sudoku[y][x] = value
                        result = backtracking_recurse(sudoku)
                        if result != False:
                            return result
                sudoku[y][x] = 0
                return False  # go back to the last selection and retry
    return False  # if the board isn't finished but nothing more can fit, soln is incorrect

def sudoku_forwardchecking(sudoku):
    variables.counter = 0
    # Make a dictionary of domains
    domains = [[] for _ in range(81)]
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                domains[9*y+x] = []
                for i in range(1, 10):
                    if common.can_yx_be_z(sudoku, y, x, i):
                        domains[9*y+x].append(i)  # start off with all values possible
    solved_sudoku = forward_recurse(sudoku, domains)
    return variables.counter

def forward_recurse(sudoku, domains):
    variables.counter += 1 # only make recursive call if forward check leaves no domains empty
    if board_finished(sudoku):
        return sudoku
    
    for y in range(9):  # check all board spots
        for x in range(9):
            if sudoku[y][x] == 0:  # empty spot found
                for value in range(1,10):  # check possible values
                    if common.can_yx_be_z(sudoku, y, x, value) and value in domains[9*y+x]:  # has to be in domain
                        # do forward propagation and update domains on new, copied version
                        copied_domains = [[] for _ in range(81)]
                        for i in range(81):
                            for j in range(len(domains[i])):
                                copied_domains[i].append(domains[i][j])
                        fprop_result = forward_prop(sudoku, y, x, value, copied_domains)
                        if fprop_result != False: # if no empty domain reached
                            # Finished forward propagation, now update board
                            sudoku[y][x] = value
                            # only do recursive call if forward check leaves no empty domains
                            result = forward_recurse(sudoku, copied_domains)
                            if result != False:
                                return result

                sudoku[y][x] = 0
                return False  # go back to the last selection and retry


def forward_prop(sudoku, y, x, value, domains):
    for i in range(9):
        # vertical, horizontal, and then square
        checks = [(i, x), (y, i), (int(y/3)*3 + int(i/3), int(x/3)*3 + i%3)]
        for pair in checks:
            ycheck = pair[0]
            xcheck = pair[1]
            if sudoku[ycheck][xcheck] == 0:
                curr = domains[9*ycheck + xcheck]
                if value in curr:
                    if not (ycheck == y and xcheck == x):
                        curr.remove(value)
                        if curr == []:
                            return False # notify main function that empty domain was found

def board_finished(sudoku):
    finished = True
    for row in sudoku:
        if 0 in row:
            finished = False
    return finished

def print_board(sudoku, recenty, recentx):
    msg = ""
    for y in range(9):
        row = sudoku[y]
        row_msg = "\n"
        for x in range(9):
            v = str(row[x])
            if y == recenty and x == recentx:
                v += "\x1b[31m"
            row_msg += v + " "
        msg += row_msg
    print(msg+"\x1b[0m"+"\n")
