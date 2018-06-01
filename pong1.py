import pygame
import colors
import math
import random
width = 800
height = 400

pygame.init()#init pygame
infoObject = pygame.display.Info() # get monitor size (infoObject.current_w, infoObject.current_h) width and heigth
gameDisplay = pygame.display.set_mode((width, height)) #init window for display --> flag pygame.FULLSCREEN  create a fullscreen display
#icon = pygame.image.load('snake.jpg')#load image onto surface

#pygame.display.set_icon(icon)#set icon for window
pygame.display.set_caption('pong')#set window title

gameExit = False
numberOfPlayers = 2
paddleWidth = 10
paddleHeight = 60
ballWidth = paddleWidth
netWidth = paddleWidth//2
netHeight = paddleWidth


direction = 0  #1 is up, -1 is down
smallFont = pygame.font.SysFont('Arial Black', 25)
mediumFont = pygame.font.SysFont('Arial Black', 40)
largeFont = pygame.font.SysFont('Arial Black', 60)

clock = pygame.time.Clock()  # initialise clock

def message_to_screen(msg, color, y_displacement=0, size=mediumFont):
    textsurface = size.render(msg, True, color)  # render message with antialiasing and color
    # print surface text onto display centered -> get_height()
    gameDisplay.blit(textsurface, (width // 2 - textsurface.get_width()//2, height // 2-textsurface.get_height()//2+y_displacement))
def drawNet():
    i = 0
    while i < height:
        pygame.draw.rect(gameDisplay, colors.white, (width // 2-netHeight//2, i, netWidth, netHeight))  #draw net
        i += netHeight + netHeight // 2
def drawScore(leftPaddleScore, rightPaddleScore):
    leftScore = mediumFont.render(str(leftPaddleScore), False, colors.white)
    rightScore = mediumFont.render(str(rightPaddleScore), False, colors.white)
    gameDisplay.blit(leftScore, (width // 2 - leftScore.get_width() // 2 - 50, height // 20))  # print score
    gameDisplay.blit(rightScore, (width // 2 - rightScore.get_width() // 2 + 50, height // 20))  # print score
def draw(xL,yL,xR,yR,ballX,ballY,leftPaddleScore, rightPaddleScore):
    drawScore(leftPaddleScore, rightPaddleScore)
    drawNet()

    pygame.draw.rect(gameDisplay, colors.white, (xL, yL, paddleWidth, paddleHeight))  # draw left paddle
    pygame.draw.rect(gameDisplay, colors.white, (xR, yR, paddleWidth, paddleHeight))  # draw right paddle

    #draw ball
    pygame.draw.rect(gameDisplay, colors.white, (ballX, ballY, ballWidth, ballWidth))  # draw right paddle
def pause():
    paused = True
    message_to_screen('Paused', colors.white, -100, size=largeFont)
    message_to_screen('Press P to continue, Q to quit', colors.white, 0, size=mediumFont)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # restart game
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)

def gameIntro():
    intro = True
    while intro:
        gameDisplay.fill(colors.black)  # fill surface with color optional contained to a specific area
        message_to_screen('Welcome to Pong', colors.white, -120, size=largeFont)
        message_to_screen('Press 1 for single player or 2 for 2 player game,', colors.white, 30, size=smallFont)
        message_to_screen('P to pause or Q to QUIT', colors.white, 60, size=smallFont)
        message_to_screen('Controls: Player 1: "w" for up and "s" for down', colors.white, 90, size=smallFont)
        message_to_screen('              Player 2: arrow up and arrow down', colors.white, 120, size=smallFont)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # when pressed change direction
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    intro = False
                    global numberOfPlayers
                    numberOfPlayers = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    intro = False


                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(15)
def gameLoop():
    xL = paddleWidth
    yL = height / 2
    xR = width - 2*paddleWidth
    yR = height / 2
    ballX = width//2 + 20
    ballY = height//2
    ballSpeed = 10
    stepSize = 10
    rand= random.uniform(0, math.pi * 5 / 12)
    ballX_change = ballSpeed * math.cos(rand)
    ballY_change = ballSpeed * -math.sin(rand)
    yL_change = 0
    yR_change = 0
    leftPaddleScore = 0
    rightPaddleScore = 0
    gameExit = False
    gameOver = False
    frames=60
    bounce_sound = pygame.mixer.Sound('ping-pong-ball-hit.wav')
    while not gameExit:
        while gameOver == True:
            # check if someone won the game and has score==11
            if leftPaddleScore == 11:  # left player wins
                message_to_screen("Player 1 wins!", colors.white, y_displacement=0, size=smallFont)
                gameOver = True
                leftPaddleScore = 0
                rightPaddleScore = 0
            elif rightPaddleScore == 11:  # right player wins
                message_to_screen("Player 2 wins!", colors.white, y_displacement=0, size=smallFont)
                gameOver = True
                leftPaddleScore = 0
                rightPaddleScore = 0
            message_to_screen('Press R to restart, Q to quit', colors.white, 50, size=smallFont)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # restart game
                        gameOver = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:#when pressed change direction
                if event.key == pygame.K_w:
                    yL_change = -stepSize
                    direction = 1
                if event.key == pygame.K_s:
                    yL_change = stepSize
                    direction = -1
                if event.key == pygame.K_UP:
                    yR_change = -stepSize
                    direction = 1
                if event.key == pygame.K_DOWN:
                    yR_change = stepSize
                    direction = -1
                elif event.key == pygame.K_p:  # run game in more frames
                    pause()
                elif event.key == pygame.K_KP8:# run ball faster
                    ballSpeed += 2
                elif event.key == pygame.K_KP2:# run ball slower
                    ballSpeed -= 2
                elif event.key == pygame.K_KP_PLUS:# run game in more frames
                    frames += 2
                elif event.key == pygame.K_KP_MINUS:# run game in less frames
                    frames -= 2
                    if frames <= 0:
                        frames = 1
            if event.type == pygame.KEYUP:  # when key is released stop paddle
                if event.key == pygame.K_s and direction == -1:
                    yL_change = 0
                    direction = 0
                if event.key == pygame.K_w and direction == 1:
                    yL_change = 0
                    direction = 0
                if event.key == pygame.K_DOWN and direction == -1:
                    yR_change = 0
                    direction = 0
                if event.key == pygame.K_UP and direction == 1:
                    yR_change = 0
                    direction = 0
        if numberOfPlayers==1:
            if ballY >= yL+paddleHeight+20 and ballX<width//2 and ballX_change<0:
                yL_change = stepSize
            elif ballY+ballWidth < yL-20 and ballX<width//2 and ballX_change<0:
                yL_change = -stepSize
        #update paddle locations
        yL += yL_change
        yR += yR_change


        # check if paddles are in range of the screen
        if yL>height-paddleHeight:
            yL=height-paddleHeight
            yL_change=0
        if yL<0:
            yL=0
            yL_change = 0
        if yR>height-paddleHeight:
            yR=height-paddleHeight
            yR_change=0
        if yR<0:
            yR=0
            yR_change = 0

        #check for ball colision with edgeof screen
        if ballX>=width-ballWidth:
            leftPaddleScore+=1
            ballX=width//2 + 20
            ballY = random.randint(20,height-20)
            rand=random.uniform(0, math.pi*5/12)
            ballX_change = ballSpeed * math.cos(rand)
            ballY_change = ballSpeed * -math.sin(rand)
        if ballX<=0:
            rightPaddleScore+=1
            ballX = width//2 + 20
            ballY = random.randint(20,height-20)
            rand = random.uniform(0, math.pi * 5 / 12)
            ballX_change = -ballSpeed * math.cos(rand)
            ballY_change = ballSpeed * -math.sin(rand)
        #check for paddle collision
        if ballX<=xL+paddleWidth and ballX>=xL and ballY+ballWidth>yL and ballY<yL+paddleHeight and ballX_change<0:
            relativeIntersectY = (yL + (paddleHeight / 2)) - ballY
            normalizedRelativeIntersectionY = (relativeIntersectY / (paddleHeight / 2))
            bounceAngle = normalizedRelativeIntersectionY * (math.pi*5/16)
            ballX_change = ballSpeed * math.cos(bounceAngle)
            ballY_change = ballSpeed * -math.sin(bounceAngle)
            bounce_sound.play()
            if numberOfPlayers == 1:
                yL_change=0
        elif ballX+ballWidth>=xR and ballX+ballWidth<=xR+paddleWidth and ballY+ballWidth>yR and ballY<yR+paddleHeight and ballX_change>0:
            relativeIntersectY = (yR + (paddleHeight / 2)) - ballY
            normalizedRelativeIntersectionY = (relativeIntersectY / (paddleHeight / 2))
            bounceAngle = normalizedRelativeIntersectionY * (math.pi*5/16)
            ballX_change = -ballSpeed * math.cos(bounceAngle)
            ballY_change = ballSpeed * -math.sin(bounceAngle)
            bounce_sound.play()
        if ballY <= 0:
            ballY_change = -ballY_change
        if ballY >= height-ballWidth:
            ballY_change = -ballY_change

        #change ball position
        ballX+=ballX_change
        ballY+=ballY_change
        if leftPaddleScore == 11:  # left player wins
            gameOver = True
        elif rightPaddleScore == 11:  # right player wins
            gameOver = True
        gameDisplay.fill(colors.black)  # fill surface with color optional contained to a specific area
        draw(xL,yL,xR,yR,ballX,ballY,leftPaddleScore, rightPaddleScore)

        pygame.display.update()
        clock.tick(frames) # frames per second
    pygame.quit() #pygame quit
    quit()
gameIntro()
gameLoop()