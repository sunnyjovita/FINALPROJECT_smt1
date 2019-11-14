import random, time, pygame, sys
from pygame.locals import *
# time module : handle time related to the game

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10 # for the yellow frame Width
BOARDHEIGHT = 20 # for the yellow frame height
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = ((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
GREEN       = (  0, 155,   0)
BLUE        = (  0,   0, 155)
YELLOW      = (155, 155,   0)

BORDERCOLOR = YELLOW
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GREEN
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                      '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}
class TetrisApp():

    def main(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
        #  global function : inside the block function, we can access variable outside the function, this access is limited just as a read access.
        #  if the function wants to write a variable outside the function, you can use global statement.
        pygame.init()
        # init is is the first process started during booting of the computer system. Init is a process that continues running until the system is shut down.
        FPSCLOCK = pygame.time.Clock()
        # frames per second = FPS (short for Frames Per Second) means the number of frames displayed on the screen each second. This number can be defined by many reasons, your computer is not fast enough to process so many frames or you just want to see certain number of FPS.
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        BASICFONT = pygame.font.Font('OpenSans-ExtraBold.ttf', 18)
        BIGFONT = pygame.font.Font('OpenSans-ExtraBold.ttf', 80)
        pygame.display.set_caption('Tetris Game')

        self.showTextScreen('Block Stacker')
        while True: # game loop
            pygame.mixer.music.load('Ship Wrek  (1).mp3')
            pygame.mixer.music.play()
            self.runGame()
            pygame.mixer.music.stop()
            self.showTextScreen('Game Over')

    def runGame(self):
        # setup variables for the start of the game
        board = self.getBlankBoard()
        lastMoveDownTime = time.time()
        lastMoveSidewaysTime = time.time()
        lastFallTime = time.time()
        # handle the number of the times before the period/time
        movingDown = False
        movingLeft = False
        movingRight = False
        # there is no moving up variable
        score = 0
        level, fallFreq = self.calculateLevelAndFallFreq(score)

        fallingPiece = self.getNewPiece()
        nextPiece = self.getNewPiece()

        while True: # game loop
            if fallingPiece == None:
                # No falling piece in play, so start a new piece at the top
                fallingPiece = nextPiece
                nextPiece = self.getNewPiece()
                lastFallTime = time.time() # reset lastFallTime

                if not self.isValidPosition(board, fallingPiece):
                    return
                    # can't fit a new piece on the board,the frame is fully loaded with the block, so game over
                    # The return statement does not print out the value it returns when the function is called. It however causes the function to exit or terminate immediately,
            self.checkForQuit()
            for event in pygame.event.get(): # event handling loop
                if event.type == KEYUP:
                    # release the button
                    if (event.key == K_p):
                        # K_p is for pausing the game
                        DISPLAYSURF.fill(BGCOLOR)
                        pygame.mixer.music.stop()
                        self.showTextScreen('Paused') # pause until a key press
                        pygame.mixer.music.play()
                        lastFallTime = time.time()
                        lastMoveDownTime = time.time()
                        lastMoveSidewaysTime = time.time()
                    elif (event.key == K_LEFT or event.key == K_a):
                        movingLeft = False
                    elif (event.key == K_RIGHT or event.key == K_d):
                        movingRight = False
                    elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = False

                elif event.type == KEYDOWN:
                    # press the button
                    # moving the piece sideways
                    if (event.key == K_LEFT or event.key == K_a) and self.isValidPosition(board, fallingPiece, adjX=-1):
                        fallingPiece['x'] -= 1
                        movingLeft = True
                        movingRight = False
                        lastMoveSidewaysTime = time.time() # if we don't use this, the block will jump to the 2 next block

                    elif (event.key == K_RIGHT or event.key == K_d) and self.isValidPosition(board, fallingPiece, adjX=1):
                        fallingPiece['x'] += 1
                        movingRight = True
                        movingLeft = False
                        lastMoveSidewaysTime = time.time()

                    # rotating the piece (if there is room to rotate)
                    elif (event.key == K_UP or event.key == K_w): # rotate right to the left
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                        if not self.isValidPosition(board, fallingPiece): # ensure the block is still inside the frame
                            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    elif (event.key == K_q): # rotate the other direction (left to right)
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                        if not self.isValidPosition(board, fallingPiece):
                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                    # making the piece fall faster with the down key
                    elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = True
                        if self.isValidPosition(board, fallingPiece, adjY=1):
                            fallingPiece['y'] += 1
                        lastMoveDownTime = time.time()

                    # move the current piece all the way down
                    elif event.key == K_SPACE:
                        movingDown = False
                        movingLeft = False
                        movingRight = False
                        for i in range(1, BOARDHEIGHT):
                            if not self.isValidPosition(board, fallingPiece, adjY=i):
                                break
                        fallingPiece['y'] += i - 1

            # handle moving the piece because of user input
            # make the user when press the left/right/down button move faster
            if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
                if movingLeft and self.isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                elif movingRight and self.isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                lastMoveSidewaysTime = time.time()

            if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and self.isValidPosition(board, fallingPiece, adjY=1):
                fallingPiece['y'] += 1
                lastMoveDownTime = time.time()

            # make the piece fall if it is time to fall
            #  if we dont use this code,the block won't fall by itself
            if time.time() - lastFallTime > fallFreq:
                # see if the piece has landed
                if not self.isValidPosition(board, fallingPiece, adjY=1):
                    # falling piece has landed, set it on the board
                    self.addToBoard(board, fallingPiece)
                    score += self.removeCompleteLines(board)
                    level, fallFreq = self.calculateLevelAndFallFreq(score)
                    fallingPiece = None # after the piece has fallen, make a new one for ready to fall

                else:
                    # piece did not land, just move the piece down
                    fallingPiece['y'] += 1
                    lastFallTime = time.time()

            # drawing everything on the screen
            DISPLAYSURF.fill(BGCOLOR)
            self.drawBoard(board)
            self.drawStatus(score, level)
            self.drawNextPiece(nextPiece)
            if fallingPiece != None:
                self.drawPiece(fallingPiece)

            pygame.display.update()
            FPSCLOCK.tick(FPS) # control the time
            # clock.tick() specifies how fast you want to change the game display in other words how fast the loop runs


    def makeTextObjs(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()


    def terminate(self):
        pygame.quit()
        sys.exit()


    def checkForKeyPress(self):
        # Go through event queue looking for a KEYUP event.
        # Grab KEYDOWN events to remove them from the event queue.
        self.checkForQuit()

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None


    def showTextScreen(self, text):
        # This function displays large text in the center of the screen until a key is pressed.
        # Draw the text drop shadow
        titleSurf, titleRect = self.makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(titleSurf, titleRect)

        # Draw the text
        # make the big text(block stacker pause, and game over) has shadows
        titleSurf, titleRect = self.makeTextObjs(text, BIGFONT, TEXTCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
        DISPLAYSURF.blit(titleSurf, titleRect)

        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = self.makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

        while self.checkForKeyPress() == None:
            pygame.display.update()
            FPSCLOCK.tick()


    def checkForQuit(self):
        for event in pygame.event.get(QUIT): # get all the QUIT events
            self.terminate() # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate() # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event) # put the other KEYUP event objects back



    def calculateLevelAndFallFreq(self, score):
        # Based on the score, return the level the player is on and
        # how many seconds pass until a falling piece falls one space.
        level = int(score / 10) + 1
        # if the score has already above 10, the level will +1 from the previous level
        fallFreq = 0.3
        # 0.3 = the speed of the piece fall
        return level, fallFreq

    def getNewPiece(self):
        # return a random new piece in a random rotation and color
        shape = random.choice(list(PIECES.keys()))
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(PIECES[shape]) - 1),
                    'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                    'y': -2, # start it above the board (i.e. less than 0)
                    'color': random.randint(0, len(COLORS)-1)}
        return newPiece


    def addToBoard(self, board, piece):
        # fill in the board based on piece's location, shape, and rotation
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                    board[x + piece['x']][y + piece['y']] = piece['color']


    def getBlankBoard(self):
        # create and return a new blank board data structure
        board = []
        for i in range(BOARDWIDTH):
            board.append([BLANK] * BOARDHEIGHT)
        return board


    def isOnBoard(self, x, y):
        return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


    def isValidPosition(self, board, piece, adjX=0, adjY=0):
        # Return True if the piece is within the board and not colliding
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                isAboveBoard = y + piece['y'] + adjY < 0
                if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                    continue
                if not self.isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                    return False
                if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                    return False
        return True

    def isCompleteLine(self, board, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(BOARDWIDTH):
            if board[x][y] == BLANK:
                return False
        return True


    def removeCompleteLines(self, board):
        # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
        numLinesRemoved = 0
        y = BOARDHEIGHT - 1# start y at the bottom of the board
        while y >= 0:
            if self.isCompleteLine(board, y):
                # Remove the line and pull boxes down by one line.
                for pullDownY in range(y, 0, -1):
                    for x in range(BOARDWIDTH):
                        board[x][pullDownY] = board[x][pullDownY-1]
                # Set very top line to blank.
                for x in range(BOARDWIDTH):
                    board[x][0] = BLANK
                numLinesRemoved += 1
                # Note on the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also complete, it will be removed.
            else:
                y -= 1 # move on to check next row up
        return numLinesRemoved


    def convertToPixelCoords(self, boxx, boxy):
        # Convert the given xy coordinates of the board to xy
        # coordinates of the location on the screen.
        return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


    def drawBox(self, boxx, boxy, color, pixelx=None, pixely=None):
        # draw a single box (each tetris piece has four boxes)
        # at xy coordinates on the board. Or, if pixelx & pixely
        # are specified, draw to the pixel coordinates stored in
        # pixelx & pixely (this is used for the "Next" piece).
        if color == BLANK:
            return
        if pixelx == None and pixely == None:
            pixelx, pixely = self.convertToPixelCoords(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
        # pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


    def drawBoard(self, board):
        # draw the border around the board
        pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

        # fill the background of the board
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
        # draw the individual boxes on the board
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                self.drawBox(x, y, board[x][y])


    def drawStatus(self, score, level):
        # draw the score text
        scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 150, 20)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        # draw the level text
        levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (WINDOWWIDTH - 150, 50)
        DISPLAYSURF.blit(levelSurf, levelRect)


    def drawPiece(self, piece, pixelx=None, pixely=None):
        shapeToDraw = PIECES[piece['shape']][piece['rotation']]
        if pixelx == None and pixely == None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx, pixely = self.convertToPixelCoords(piece['x'], piece['y'])

        # draw each of the boxes that make up the piece
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shapeToDraw[y][x] != BLANK:
                    self.drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


    def drawNextPiece(self, piece):
        # draw the "next" text
        nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (WINDOWWIDTH - 120, 80)
        DISPLAYSURF.blit(nextSurf, nextRect)
        # draw the "next" piece
        self.drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


if __name__ == '__main__':
    App = TetrisApp()
    App.main()