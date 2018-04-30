import numpy as np
import time

'''
A matrix is arrangd in 9*9 square grid divided on 3*3 blocks.
'''
# order is to take location of element of sq grid and detect the block
order = lambda x,y: ([3*int(x/3),3*int(x/3)+3],[3*int(y/3),3*int(y/3)+3])

# Find the elements that are allowed in a square grid (any of 9*9)
def allowed_elements(x, y):
    # get the submatrix of the block in which element is present
    submatrix = matrix[order(x,y)[0][0]:order(x,y)[0][1], order(x,y)[1][0]:order(x,y)[1][1]]
    # obtain all the forbidden element because which lie on same block
    list_submatrix = [_ for _ in submatrix.ravel().tolist() if _ != 0]

    # Now to obtain fobidden element in a row or column
    row = matrix[x,:]
    column = matrix[:,y]
    rowpluscol = list(set([_ for _ in row.tolist()+column.tolist() if _ != 0]))
    # total forbidden elements
    adjoint = list(set(list_submatrix+ rowpluscol))
    #total allowed elements (total - forbidden) then return
    neg_adj = list(set(list(range(1,10)))-set(adjoint))
    return neg_adj

# Now to pass a matrix and solve
def solve_this(matrix):
    # print(matrix)
    while True:
        # var to check if all the matrix has been solved
        element_zero = 0
        # loop along the rows
        for i in range(9):
            # loop along the columns
            for j in range(9):
                # if element is empty then find returned elements
                if matrix[i,j] == 0:
                    #check allowed elements
                    returned = allowed_elements(i, j)
                    # print('matrix[%d ,%d]'%(i,j),':', returned)
                    # if only one possible element then fill the matrix
                    if len(returned)== 1: matrix[i, j]= returned[0]
                    # if more than one then leave empty and ask for another loop
                    else: element_zero += 1
        # remove this if you dont want a delay
        time.sleep(1)
        print('\n\n', matrix)
        # if solved return
        if element_zero == 0: return matrix

# Not my piece of code
def print_sudoku(board):
    print("-"*37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")

sudoku = """
1 - 6 - 4 8 - - 9
7 9 - - 5 6 - - -
5 - 8 - 3 - - 7 - 
4 - - 2 - - 5 - - 
- - 9 - 6 - 8 - -
- - 2 - - 4 - - 7
- 7 - - 2 - 4 - 1
- - - 4 7 - - 2 8
2 - - 8 9 - 7 - 5
"""
# converting list to array. found that there was an easier method but eh!
list_sudoku = [_ for _ in sudoku if _!=' ' if _!='\n']
for _ in range(len(list_sudoku)):
    if list_sudoku[_] == '-': list_sudoku[_] = 0
    else: list_sudoku[_] = int(list_sudoku[_])
list_sudoku_grid = [list_sudoku[0+9*x : 9+9*x] for x in range(9)]
matrix = np.array(list_sudoku_grid)

final_result = solve_this(matrix)
print_sudoku(final_result)




# Sample question for this sudoku it cant solve:
# http://www.7sudoku.com/view-puzzle?date=20180404
# The code coulnt solve this
sudoku = """
2 9 - 3 - 8 - - -
- - 6 4 - - - 5 - 
- - - 7 - - - 9 - 
- - 1 - - - - - 8
7 - - - 9 - 3 - - 
3 - - - - - - - 5
- - - - - 2 - - 6
- 8 - - 1 - 5 - -
5 2 - - 8 - - - -
"""
