from cmu_graphics import *
import copy
import random
'''
Author: Sudeep Rawal
Creation Date: 2/28/2025
Last Modified: 3/14/2025
Project Description:
    This project is a tetris game project that consists of
    falling tetris pieces that players must rotate and position
    to try and survive for as long as possible. When the pieces
    stack up and the player isn't able to place anymore pieces,
    they lose. In order to combat this, the player must strategically
    fill rows in order to "clear" them and earn points. Every ten rows
    a player clears, they progress to the next level where the pieces
    fall quicker. A piece is considered placed on the board only when it
    cannot fall any longer.
Instructions:
    Players control the falling pieces by using the arrow keys, spacebar, c,
    and p. By using the up arrow, the player car rotate the tetris piece 
    clockwise. By using the left and right arrows, the player can move the 
    tetris piece leftand right respectively. By using the down arrow, the 
    player can perform a soft drop: a move that brings down the falling 
    piece one step further. By pressing spacebar, the player hard drops the 
    tetris piece, this forces the piece to be placed at the lowest legal 
    point right under it. The player is able to press c to store a falling
    piece and load the next piece; however, if there is already a piece stored,
    the player swaps their current piece with the one that is stored. With
    either case, the player may not store a piece again before fully dropping a
    piece on the board. The player scores a certain amount of points that
    depends on the level that the player is currently on and the amount of rows
    that the player cleared at once. The amount of points that the player gains
    from scoring multiple rows at once grows exponentially: clearing two rows
    grants the player twice the points of clearing one row, clearing three rows
    gives twice the points gained from clearing two, and so on. Every ten rows
    that the player clears, they progress one level further. As the player
    levels up, they are faced with faster dropping pieces; however, they are
    also able to gain much more points.
Credits: Brian Son
Updates: Brian inspired me to depict the stored piece in a grid format. Helped
         With visual updates on the board as well.
Rubric Items:
    Full-size Board: 54
    Random Pieces: 383
    Auto-stepping with Pause: 635
    Keep Score: 552
    Game Over: 424
    Bonus Feature:
        savePiece: 573
'''
# start app (app.properties)
def onAppStart(app):
    #initalizes the variables
    app.rows = 15
    app.cols = 10
    app.boardLeft = 185
    app.boardTop = 50
    app.boardWidth = 210
    app.boardHeight = 280
    app.boardCX = 290
    app.boardCY = 181
    app.cellBorderWidth = 0.5
    app.highScores = []
    app.savedLeft = 50
    app.savedTop = 50
    app.savedWidth = 100
    app.savedHeight = 100
    app.savedRowsAndCols = 5
    app.highScoresLeft = 50
    app.highScoresTop = 175
    app.highScoresWidth = 100
    app.highScoresHeight = 200
    app.showInstructions = True
    resetApp(app)

# draw graphics (redrawAll)
def redrawAll(app):
    #draws everything, instructions overlap other drawings when placed
    drawInstructions(app)
    drawLabel(f'Tetris \n Score: {app.playerScore} \n level: {app.level}', 
                                                app.boardCX, 20, size=16)
    drawBoard(app)
    drawGhostPiece(app)
    drawPiece(app)
    drawBoardBorder(app)
    drawGameOver(app)
    drawSavedPieceBox(app)
    drawSavedBoard(app)
    drawHighScoresBorder(app)
    drawHighScores(app)
    drawPaused(app)
    drawNextBorder(app)
    drawNextPieces(app)
    drawInstructions(app)

def drawInstructions(app):
    #Draws out all the instructions on scoring and controls.
    if app.showInstructions:
        drawRect(0,0,600,400, fill = 'white')
        drawLabel("Welcome To Tetris!", 300, 50, size = 32)
        Controls = ["Left & Right: Moving", "Up: Rotate", "Down: Soft Drop", 
                    "Space: Hard Drop","C: Store Piece", "P: Pause", 
                                                            "R: Restart Game"]
        Scoring = ["Clear lines = Points!!!", "10 lines = Next Level",
                    "Next Level = Faster Drop Speed", "Higher Level = More Points"]
        drawLabel("Controls:", 150, 100, size = 25)
        drawLabel("Scoring:", 450, 100, size = 25)
        drawLabel("Press k to start and return to these instructions", 300, 375, 
                                                                        size = 16)
        for i in range(len(Controls)):
            y = 130 + 25 * i
            drawLabel(f'{Controls[i]}', 150, y, size = 16)
        for i in range(len(Scoring)):
            y = 130 + 25*i
            drawLabel(f'{Scoring[i]}', 450, y, size = 16)

def drawNextBorder(app):
    #draws the border where the next pieces will be placed
    drawRect(440, 50, 150, 325, fill = None, border = 'black', 
                                        borderWidth = 2* app.cellBorderWidth)
def drawNextPieces(app):
    #Draws all seven next pieces in order, pieces are all displayed in the same
    #x.
    cellHeight, cellWidth = getCellSize(app)
    startingLeft = 480
    startingTop = 60
    pieceTop = startingTop - 45
    #loop through the 7 pieces
    numPieces = len(app.tetrisPieces)
    prevPieceIndex = None
    for i in range(numPieces):
        #When the piece we want to draw is still in the current bag
        #Index will be useful for the color
        if i < len(app.bag):
            currPiece = app.tetrisPieces[app.bag[i]]
            currIndex = app.bag[i]
        #When the bag doesn't have the piece we want to draw (the bag is short)
        #we must use the next bag instead.
        else:
            currPiece = app.tetrisPieces[app.nextBag[i-len(app.bag)]]
            currIndex = app.nextBag[i-len(app.bag)]
        #artificial app.pieceTop and app.pieceleft
        pieceTop += (45)
        if prevPieceIndex == 0:
            pieceTop -= 45/2
        pieceLeft = startingLeft
        #now lets iterate through the actual piece and draw it
        for row in range(len(currPiece)):
            for col in range(len(currPiece[row])):
                cellLeft = pieceLeft + col * cellWidth
                cellTop = pieceTop  + row * cellHeight
                color = app.tetrisPieceColors[currIndex]
                if currPiece[row][col]:
                    drawRect(cellLeft, cellTop, cellWidth, cellHeight, 
                    fill = color,border = 'black', 
                    borderWidth = app.cellBorderWidth)
        prevPieceIndex = currIndex
def drawPaused(app):
    #draws the pause button, indicates when the game is paused.
    if app.paused:
        drawCircle(app.boardCX, app.boardCY, 30, fill = 'gray')
        
        drawRect(275, 165, 10, 30, fill = 'white')
        drawRect(295, 165, 10, 30, fill = 'white')
def drawSavedBoard(app):
    #Draws the empty cells in the board along with whatever piece may be saved
    #inside of it by calling drawSavedCell
    for row in range(app.savedRowsAndCols):
        for col in range(app.savedRowsAndCols):
            color = app.savedBoard[row][col]
            borderColor = 'black'
            drawSavedCell(app, row, col, color, borderColor)
def drawSavedPieceBox(app):
    #draws the border of the saved board
    drawRect(app.savedLeft, app.savedTop, app.savedWidth, app.savedHeight, 
            fill = 'white', border = 'black', 
            borderWidth = 2 * app.cellBorderWidth)

def drawSavedCell(app, row, col, color, borderColor):
    #copied drawCell with a couple adjustments
    #those adjustments were in getLeftTpo and getSize
    #this just draws each cell of the saved piece inside the save box
    cellLeft, cellTop = getSavedCellLeftTop(app, row, col)
    cellWidth, cellHeight = getSavedCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill= color, border= borderColor,
             borderWidth=app.cellBorderWidth)

def drawBoard(app):
    #draws the board with all the pieces that are already placed for main board
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            if color == None: color = 'black'
            borderColor = 'blue'
            drawCell(app, row, col, color, borderColor)

def drawPiece(app):
    #Just looping through app.piece and findingthe locations of the piece that
    #would be on the board and drawing that piece before it gets placed onto the
    #board and is still falling
    if not app.gameOver:
        for row in range(len(app.piece)):
            for col in range(len(app.piece[0])):
                if app.piece[row][col]:
                    #If its none then it doesn't matter, it wont obstruct already
                    #placed pieces too. Keep track of its board location by using
                    #app.pieceTopRow and app.pieceTopCol
                    boardRow = app.pieceTopRow + row
                    boardCol = app.pieceLeftCol + col
                    drawCell(app, boardRow, boardCol, app.pieceColor, 'black')

def drawBoardBorder(app):
  # Draws the board's outline in pink, then draws a gameboy surrounding the main
  #board to outline the pieces.
  drawRect(160, 30, 260, 20, fill = 'green')
  drawRect(160, 30, 25, 330, fill = 'green')
  drawRect(395, 30, 25, 330, fill = 'green')
  drawRect(185, 330, 210, 60, fill = 'green')
  drawCircle(370, 350, 15, fill = 'cyan', border = 'pink')
  drawCircle(340, 365, 15, fill = 'yellow', border = 'pink')
  drawRect(240, 360, 50, 18, align = 'center', fill = 'pink')
  drawRect(240, 360, 50, 18, align = 'center', fill = None, border = 'yellow',
            borderWidth = 3)
  drawRect(240, 360, 18, 50, align = 'center', fill = 'pink')
  drawRect(240, 360, 18, 50, align = 'center', fill = None, border = 'yellow',
            borderWidth = 3)
  drawCircle(240, 360, 10, fill = 'cyan', border = 'green')
  for i in range(7):
      x = 227 + i * 20
      y1 = 35
      y2 = 45
      drawCircle(x, y1, 5, fill = 'yellow', border = 'black')
      drawCircle(x, y2, 5, fill = 'yellow', border = 'black')
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='pink',
           borderWidth=4)

def drawCell(app, row, col, color, borderColor):
    #calls for the dimensions of the cell and its location in order to draw
    #a rectangle that depends on the color given by its parameter.
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill= color, border= borderColor,
             borderWidth=app.cellBorderWidth)

def drawGameOver(app):
    #when the game is finished, this draw function puts a game over message
    #under the tetris board with instructions on how to restart.
    if app.gameOver:
        drawRect(185, 143, 210, 60, fill = 'gray')
        drawLabel(f'Game Over \n Score: {app.playerScore}', app.boardCX, 181, 
                                                        size = 16, bold = True)
        drawLabel("Press r to restart", app.boardCX, 170, 
                                size = 16, bold = True)

def drawGhostPiece(app):
    #Draws a piece that indicates the position of the current tetris piece if it
    #were to reach its lowest point at that moment in time.
    if not app.gameOver:
        topRow, leftCol = ghostPieceBottom(app)
        for row in range(len(app.piece)):
            for col in range(len(app.piece[0])):
                if app.piece[row][col]:
                    boardRow = topRow + row
                    boardCol = leftCol + col
                    drawCell(app, boardRow, boardCol, 'black', 
                                        borderColor = 'white')

def drawHighScoresBorder(app):
    #Draws the box where the highscores are stored
    drawRect(app.highScoresLeft, app.highScoresTop, app.highScoresWidth, app.highScoresHeight, 
            fill = 'white', border = 'black', 
            borderWidth = 2 * app.cellBorderWidth)

def drawHighScores(app):
    #Putting the highscores inside the box, they are already sorted how I want
    #Highest to lowest, top to bottom.
    drawLabel('Highest Scores:', 100, 190, size = 10)
    for score in range(len(app.highScores)):
        y = 190 + 30 * (score + 1)
        drawLabel(f'{app.highScores[score]}', 100, y, size = 16, bold = True)
#helper functions

def getCellLeftTop(app, row, col):
    #returns the x and y position of the cell's topleft point
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getSavedCellLeftTop(app, row, col):
    #Copied getCellLeftTop but adjusted it for the mini board where I stored
    #the saved cell.
    cellWidth, cellHeight = getSavedCellSize(app)
    cellLeft = app.savedLeft + col * cellWidth
    cellTop = app.savedTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    #returns the dimensions of the board's size
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def getSavedCellSize(app):
    #Adjusted getCellSize to fit the mini board I made
    cellWidth = app.savedWidth / app.savedRowsAndCols
    cellHeight = app.savedHeight / app.savedRowsAndCols
    return (cellWidth, cellHeight)

def switcheroo(obj1, obj2):
    #very useful helper function, allows me to skip the process of making a temp
    #variable. Returns the two objects in swapped positions.
    return (obj2, obj1)

#functions

def rotate2dListClockwise(L):
    #Rotates a 2d list clockwise by switching the rows with cols then looping
    #through the inital shape and setting the new shape to a rotated version
    #of the old shape.
    oldRows, oldCols = len(L), len(L[0])
    newRows, newCols = oldCols, oldRows
    result = [[None for row in range(newCols)] for col in range(newRows)]
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow = oldCol
            newCol = oldRows - 1 - oldRow
            result[newRow][newCol] = copy.deepcopy(L[oldRow][oldCol])
    return result
    
def rotatePieceClockwise(app):
    #Rotating the piece while storing the old piece in case the rotation is
    #illegal.
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    oldRows = len(app.piece)
    oldCols = len(app.piece[0])
    app.piece = rotate2dListClockwise(app.piece)
    newRows = len(app.piece)
    newCols = len(app.piece[0])
    centerRow = oldTopRow + oldRows//2
    app.pieceTopRow = centerRow - newRows//2
    centerCol = oldLeftCol + oldCols//2
    app.pieceLeftCol = centerCol - newCols//2\
    #if its not legal, we have to undo the process and return false
    if not pieceIsLegal(app):
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol
        return False
    return True

def resetApp(app):
    #Called in startApp, initalizes variables that are bound to be set back to
    #their initial state.
    #When it is called in mouse press, it resets these variables that were able
    #to be changed in a normal playthrough.
    app.stepsPerSecond = 2
    app.gameOver = False
    app.level = 1
    app.rowBar = 0
    app.paused = False
    app.playerScore = 0
    app.savedBoard = [([None] *5 ) for row in range(5)]
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.savedPiece = None
    app.savedPieceColor = None
    app.savedPieceIndex = None
    app.canSave = True
    loadTetrisPieces(app)

def fillBag(app):
    #Stores the indexes for each tetris piece then shuffles it.
    #The shuffle brings randomness and the bag makes sure every piece is played.
    app.bag = list(range(len(app.tetrisPieces)))
    app.nextBag = list(range(len(app.tetrisPieces)))
    random.shuffle(app.nextBag)
    random.shuffle(app.bag)
def refillBag(app):
    #when the bag becomes empty, it copies the elements of the next bag and
    #reshuffles the next bag. (Happens every seven pieces)
    app.bag = app.nextBag
    app.nextBag = list(range(len(app.tetrisPieces)))
    random.shuffle(app.nextBag)
def loadTetrisPieces(app):
    #initializes the tetris pieces and gets the game started by loading
    #variables, and the next piece.
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]
    fillBag(app)
    loadNextPiece(app)

def loadPiece(app, pieceNum):
    #initializes the values and selected piece given through pieceNum. If the
    #piece can't be placed when its loading, the player lost the game.
    app.piece = app.tetrisPieces[pieceNum]
    app.pieceTopRow = 0
    app.pieceLeftCol = 0
    pieceCols = len(app.piece[0])
    pieceRows = len(app.piece)
    app.pieceLeftCol = (app.cols - pieceCols)//2
    app.pieceColor = app.tetrisPieceColors[pieceNum]
    if not pieceIsLegal(app):
        app.gameOver = True
    
def loadNextPiece(app):
    #Utilizes the bag array to randomly select a new piece to be loaded
    if not app.bag:
        refillBag(app)
    nextPieceIndex = app.bag.pop(0)
    app.pieceIndex = nextPieceIndex
    loadPiece(app, nextPieceIndex)

def hardDropPiece(app):
    #Forces current piece to be placed at its lowest possible point without
    #changing its x position.
    while movePiece(app, +1, 0):
        pass
    placePieceOnBoard(app)
    removeFullRows(app)
    
def movePiece(app, drow, dcol):
    #changes the piece's top row and left col when called
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if not pieceIsLegal(app):
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
    return True

def pieceIsLegal(app):
    #loops through the piece, checking if its outside of the grid or placed in
    #another piece. Returns True if it isn't, returns False otherwise.
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col]:
                boardRow = app.pieceTopRow + row
                boardCol = app.pieceLeftCol + col
                if ((boardRow >= app.rows or boardRow < 0) or 
                                        (boardCol >= app.cols or boardCol < 0)):
                    return False
                if app.board[boardRow][boardCol] != None:
                    return False
    return True

def ghostPieceBottom(app):
    #Utilized like hard drop. While looping, it checks if the ghost piece can be
    #placed. When it cannot be placed, the function backtracks by one row and
    #returns the lowest point that the ghost piece could be placed.
    topRow = app.pieceTopRow
    leftCol = app.pieceLeftCol
    while(ghostPieceIsLegal(app, topRow, leftCol)):
        topRow += 1
    topRow -= 1
    return (topRow, leftCol)

def ghostPieceIsLegal(app, topRow, leftCol):
    #just adjusted pieceIsLegal to work for the ghostPiece.
    #the lowest possible positions that the ghost piece can be placed.
    #cannot be placed outside of the grid nor inside of another piece.
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col]:
                boardRow = topRow + row
                boardCol = leftCol + col
                if ((boardRow >= app.rows or boardRow < 0) or 
                                        (boardCol >= app.cols or boardCol < 0)):
                    return False
                if app.board[boardRow][boardCol] != None:
                    return False
    return True

def placePieceOnBoard(app):
    #When a piece is placed, it allows the player to store a piece again. Also
    #this loops over the piece and finds the location it would be on the board
    #by utilizing app.pieceTopRow and app.pieceLeftCol. Then it sets the value
    #on the board that matches the current piece to app.pieceColor.
    app.canSave = True
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            boardRow = app.pieceTopRow + row
            boardCol = app.pieceLeftCol + col
            if(app.piece[row][col]):
                app.board[boardRow][boardCol] = app.pieceColor
    loadNextPiece(app)
    
def placeSavedPiece(app):
    #Everytime a piece is placed, the mini board made for the saved piece clears
    #itself, then calculates the location where the piece can be placed, working
    #similar to load piece. Then the saved piece is placed onto app.savedBoard
    app.savedBoard = [([None] *5 ) for row in range(5)]
    left = (5 - len(app.savedPiece[0]))//2
    top = (5 - len(app.savedPiece))//2
    for row in range(len(app.savedPiece)):
        for col in range(len(app.savedPiece[0])):
            saveRow = top + row
            saveCol = left + col
            if(app.savedPiece[row][col]):
                app.savedBoard[saveRow][saveCol] = app.savedPieceColor

def removeFullRows(app):
    #While counting the amount of rows popped, this function pops rows that are
    #full, then it calculates addedscores using the amount of rows popped,
    #finally the function loops over the amount of rows popped and appends empty
    #rows of the same size. Also calls for level ups whenever a "bar" of rows is
    #filled. The bar is filled every 10 rows.
    rowsPopped = 0
    row, col = 0, 0
    while(row < app.rows):
        remove = True
        while(col < app.cols):
            if app.board[row][col] == None:
                remove = False
            col += 1
        col = 0
        if remove:
            app.board.pop(row)
            rowsPopped += 1
            row -=1
            app.rows -=1
        else:
            row+=1
    app.rowBar += rowsPopped
    for i in range(rowsPopped):
        app.board = [[None for cols in range(app.cols)]] + app.board
        app.rows += 1
    addScore(app, rowsPopped)
    if app.rowBar >= 10 and app.rowBar != 0:
        levelUp(app)

def addScore(app, rowsPopped):
    #Calculates the gain in score for the player depending on the amount of rows
    #that the player popped and the stage of the game. If the game is finished,
    #it appends the score to a list of 5 highscores depending on the score that
    #the player recieved. Then it sorts the highscores.
    if rowsPopped != 0:
        app.playerScore += (10 * 2 ** rowsPopped) * app.level
    if app.gameOver:
        app.highScores.append(app.playerScore)
        if len(app.highScores) > 5:
            app.highScores.remove(min(app.highScores))
        app.highScores = sorted(app.highScores)
        app.highScores = app.highScores[::-1]

def levelUp(app):
    #Removes 10 from the bar then increases speed of the fall, then increases
    #level which is used to calculate scores.
    app.rowBar -= 10
    app.stepsPerSecond += 0.3
    app.level += 1

def savePiece(app):
    #stores a piece, its index, and color. Then loads the next piece. However; 
    #if a piece is already stored, the function then calls loadSavedPiece(app).
    #Finally, the function calls placeSavedPiece(app) and disallows for future
    #saves without placing a piece down.
    if app.canSave:
        if app.savedPiece == None:
            app.savedPiece = copy.deepcopy(app.tetrisPieces[app.pieceIndex])
            app.savedPieceColor = app.pieceColor
            app.savedPieceIndex = app.pieceIndex
            loadNextPiece(app)
        else:
            loadSavedPiece(app)
        placeSavedPiece(app)
    app.canSave = False

def loadSavedPiece(app):
    #Just switches all the variables that were stored using the switcheroo
    #helper function. Then loads the piece that was just swapped in.
    app.pieceColor, app.savedPieceColor = switcheroo(app.pieceColor, app.savedPieceColor)
    app.pieceIndex, app.savedPieceIndex = switcheroo(app.pieceIndex, app.savedPieceIndex)
    app.savedPiece, app.piece = switcheroo(app.savedPiece, app.piece)
    app.savedPiece = app.tetrisPieces[app.savedPieceIndex]
    loadPiece(app, app.pieceIndex)

def takeStep(app):
    #Moves the piece one step downwards. If it is placed, the function calls
    #for the piece to be placed on the board.
    if not movePiece(app, +1, 0) and not app.gameOver:
        placePieceOnBoard(app)
        removeFullRows(app)

#Working on showing nextPieces
#main function
def main():
    runApp(600, 400)
#events

def onKeyPress(app, key):
    #cannot be called if the game is over
    #Piece cannot be moved if the game is paused
    # arrow keys call takeStep and moveStep respectively
    key = key.lower()
    if not app.showInstructions:
        if not app.gameOver and not app.paused:
            if key == 'up': rotatePieceClockwise(app)
            elif key == 'down': takeStep(app)
            elif key == 'left': movePiece(app, 0, -1)
            elif key == 'right': movePiece(app, 0, 1)
            elif key == 'space': hardDropPiece(app)
            elif key == 's': takeStep(app)
            #saves the piece which calls a lot of other functions
            elif key == 'c': savePiece(app)
        #pauses the game
        if key == 'p': app.paused = not app.paused
        if key == 'k':
            app.showInstructions = True
        #Calls for resetApp, can be called anytime
        if key == 'r': resetApp(app)
    elif key == 'k':
        app.showInstructions = False

def onStep(app):
    #Calls takeStep unless the game is over or paused.
    if not app.paused and not app.gameOver and not app.showInstructions:
        takeStep(app)
main()
