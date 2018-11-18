mat = [[' ']*3]*3

def printMat():
    for i in range(3):
        for j in range(3):
            print(mat[i][j],end=' ')
            if not j == 2:
                print('|',end = ' ')
        print()
        if not i == 2:
            print('---------')
        
        
        
print('Welcome to Tic Tac Toe the game')
print('-------------------------------')

move = 0
for i in range(9):
    if move = 0:
        sym = 'O'
    else:
        sym = 'X'
    ('Player',sym,'Enter your move(row[1-3] column[1-3]):')
