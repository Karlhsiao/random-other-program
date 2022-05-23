import sys
global turn
global put
turn = 'X'
count = 0

def user_input():
    while True:
        put = input("Enter a position(enter 'exit' for exit): ")
        if put == "q" or put == "w" or put == "e" or put == "a" or put == "s" or put == "d" or put == "z" or put == "x" or put == "c":
            break
        elif put == "exit":
            print("program ended")
            sys.exit(0)
            break
        else:
            print("invalid input, please reinput again")
    return put

theBoard = {'7': ' ' , '8': ' ' , '9': ' ' ,
            '4': ' ' , '5': ' ' , '6': ' ' ,
            '1': ' ' , '2': ' ' , '3': ' ' }
            
def printBoard(board):
    print(board['7'] + '|' + board['8'] + '|' + board['9'])
    print('-+-+-')
    print(board['4'] + '|' + theBoard['5'] + '|' + board['6'])
    print('-+-+-')
    print(theBoard['1'] + '|' + theBoard['2'] + '|' + theBoard['3'])

def assign_ans(put):
    if put == "q" and theBoard["7"] == " ":
        theBoard["7"] = turn
        return True
    elif put == "w" and theBoard["8"] == " ":
        theBoard["8"] = turn
        return True
    elif put == "e" and theBoard["9"] == " ":
        theBoard["9"] = turn
        return True
    elif put == "a" and theBoard["4"] == " ":
        theBoard["4"] = turn
        return True
    elif put == "s" and theBoard["5"] == " ":
        theBoard["5"] = turn
        return True
    elif put == "d" and theBoard["6"] == " ":
        theBoard["6"] = turn
        return True
    elif put == "z" and theBoard["1"] == " ":
        theBoard["1"] = turn
        return True
    elif put == "x" and theBoard["2"] == " ":
        theBoard["2"] = turn
        return True
    elif put == "c" and theBoard["3"] == " ":
        theBoard["3"] = turn
        return True
    else:
        print("Please reinput, the place is occupied")
        return False

    


test = False
printBoard(theBoard)
while True:
    count = count + 1
    while test == False:
        put = user_input()
        test = assign_ans(put)
    printBoard(theBoard)

    if count >= 5:
        if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ': # across the top
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print(" **** " +turn + " won. ****")
            break
        elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ': # across the middle
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print(" **** " +turn + " won. ****")
            break
        elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ': # across the bottom
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print(" **** " +turn + " won. ****")
            break
        elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ': # down the left side
            printBoard(theBoard)
            print("\nGame Over.\n")
            print(" **** " +turn + " won. ****")
            break
        elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ': # down the middle
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print(" **** " +turn + " won. ****")
            break
        elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ': # down the right side
            printBoard(theBoard)
            print("\nGame Over.\n")
            print(" **** " +turn + " won. ****")
            break 
        elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ': # diagonal
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print(" **** " +turn + " won. ****")
            break
        elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ': # diagonal
            printBoard(theBoard)
            print("\nGame Over.\n")                
            print(" **** " +turn + " won. ****")
            break 

        # If neither X nor O wins and the theBoard is full, we'll declare the result as 'tie'.
    if count == 9:
        print("\nGame Over.\n")                
        print("It's a Tie!!")
        break
        
        # we have to change the player after every move.
    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X'
    test = False
