import pygame
import colors
import random

width = 800
height = 600

pygame.init()  # init pygame
infoObject = pygame.display.Info()  # get monitor size (infoObject.current_w, infoObject.current_h) width and heigth
gameDisplay = pygame.display.set_mode(
    (width, height))  # init window for display --> flag pygame.FULLSCREEN  create a fullscreen display
icon = pygame.image.load('apple_transparent.png')  # load image onto surface


pygame.display.set_icon(icon)  # set icon for window
pygame.display.set_caption('Snake')  # set window title
highScore = 0
snakeWidth = 20
appleThickness = 30
blockSize = 20
smallFont = pygame.font.SysFont('Arial Black', 25)
mediumFont = pygame.font.SysFont('Arial Black', 40)
largeFont = pygame.font.SysFont('Arial Black', 60)

head_sprite = pygame.image.load('snake_head_transparent.png')
tail_sprite = pygame.image.load('snake_tail_transparent.png')
apple_sprite = pygame.image.load('apple_transparent.png')

clock = pygame.time.Clock()  # initialise clock


def message_to_screen(msg, color, y_displacement=0, size=mediumFont):
    textsurface = size.render(msg, True, color)  # render message with antialiasing and color
    # print surface text onto display centered -> get_height()
    gameDisplay.blit(textsurface, (width // 2 - textsurface.get_width()//2, height // 2-textsurface.get_height()//2+y_displacement))


def drawSnake(snakeList, direction):
    if direction == 8:#up
        head = head_sprite
    elif direction ==2:#down
        head = pygame.transform.rotate(head_sprite, 180)
    elif direction ==4:#left
        head = pygame.transform.rotate(head_sprite, 90)
    elif direction ==6:#right
        head = pygame.transform.rotate(head_sprite, 270)
    gameDisplay.blit(head, (snakeList[0][0],snakeList[0][1]))
    if snakeList[-2][1]<snakeList[-1][1]:
        tail = tail_sprite
    elif snakeList[-2][1]>snakeList[-1][1]:
        tail = pygame.transform.rotate(tail_sprite, 180)
    elif snakeList[-2][0]>snakeList[-1][0]:
        tail = pygame.transform.rotate(tail_sprite, 270)
    elif snakeList[-2][0]<snakeList[-1][0]:
        tail = pygame.transform.rotate(tail_sprite, 90)
    gameDisplay.blit(tail, (snakeList[-1][0], snakeList[-1][1]))
    for (x, y) in snakeList[1:-1]:
        pygame.draw.rect(gameDisplay, colors.green,
                         (x, y, snakeWidth, snakeWidth))  # surface, color, (x,y,width, height)


def drawApple(x, y):
    gameDisplay.blit(apple_sprite, (x,y))
    #pygame.draw.rect(gameDisplay, colors.red,(x, y, appleThickness, appleThickness))  # surface, color, (x,y,width, height)


def randAppleLocation():
    randAppleX = random.randrange(0,
                                  width - appleThickness)  # , blockSize)  # calculate random apple location in step size=10
    randAppleY = random.randrange(0, height - appleThickness)  # , blockSize)

    return randAppleX, randAppleY
def pause():
    paused = True
    message_to_screen('Paused', colors.black, -100, size=largeFont)
    message_to_screen('Press P to continue, Q to quit', colors.black, 0, size=mediumFont)
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

def initSnake():
    x = height // 2
    y = height // 2
    x_change = 0
    y_change = 0
    snakeLength = 0
    frames = 15
    snakeList = [(x, y), (x, y - blockSize), (x, y - 2 * blockSize), (x, y - 3 * blockSize), (x, y - 4 * blockSize),
                 (x, y - 5 * blockSize)]  # initialise snake with 6 elements
    return (x, y, x_change, y_change, snakeLength, snakeList, frames)

def gameIntro():
    intro = True
    while intro:
        gameDisplay.fill(colors.white)  # fill surface with color optional contained to a specific area
        message_to_screen('Welcome to Snake', colors.green, -120, size=largeFont)
        message_to_screen('The objective of the game is to eat red apples', colors.black, -30, size=smallFont)
        message_to_screen('The more apples you eat, the longer you get,', colors.black, 0, size=smallFont)
        message_to_screen('   and the faster the snake is.', colors.black, 30, size=smallFont)
        message_to_screen('If you run into the edges or into yourself, you die!', colors.black, 60, size=smallFont)
        message_to_screen('Press SPACE to play, P to pause or Q to QUIT', colors.black, 180, size=smallFont)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # when pressed change direction
                if event.key == pygame.K_SPACE:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(15)
def gameLoop():
    (x, y, x_change, y_change, snakeLength, snakeList, frames) = initSnake()
    gameExit = False
    gameOver = False
    direction = 2

    randAppleX, randAppleY = randAppleLocation()

    while not gameExit:
        while gameOver == True:
            message_to_screen('Game Over', colors.red, -50, size=largeFont)
            message_to_screen('Press R to restart or Q to quit', colors.black, 50, size=mediumFont)
            highscoreFile = open("highscore.txt", "r")  # highscore file
            highScore = highscoreFile.read()
            highscoreFile.close()

            scoreText = smallFont.render("High score: " + str(highScore), False, colors.black)
            gameDisplay.blit(scoreText, (width // 2 - scoreText.get_width()//2, height // 4))  # print current highscore

            if snakeLength >= int(highScore):  # if player beats old highscore update it
                highScore = snakeLength
                highscoreFile = open("highscore.txt", "w")
                highscoreFile.write(str(highScore))
                scoreText = mediumFont.render("New highscore: " + str(snakeLength), False, colors.green)
                gameDisplay.blit(scoreText, (width // 2 - scoreText.get_width()//2, height // 20))  # print new highscore
                highscoreFile.close()
            else:
                scoreText = mediumFont.render("Score: ", False, colors.black)
                gameDisplay.blit(scoreText, (width // 2 - scoreText.get_width()*1.1, height // 20))  # print current score
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # restart game
                        gameOver = False
                        (x, y, x_change, y_change, snakeLength, snakeList,
                         frames) = initSnake()  # reinitialise variables
                        direction=2
                    elif event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:  # when pressed change direction
                if event.key == pygame.K_UP and y_change != blockSize and x_change != 0:
                    y_change = -blockSize
                    x_change = 0
                    direction = 8  #up
                elif event.key == pygame.K_DOWN and y_change != -blockSize:
                    y_change = blockSize
                    x_change = 0
                    direction = 2  #down
                elif event.key == pygame.K_LEFT and x_change != blockSize:
                    x_change = -blockSize
                    y_change = 0
                    direction = 4  #left
                elif event.key == pygame.K_RIGHT and x_change != -blockSize:
                    x_change = blockSize
                    y_change = 0
                    direction = 6  #right
                elif event.key == pygame.K_p:  # run game in more frames
                    pause()
                elif event.key == pygame.K_KP_PLUS:  # run game in more frames
                    frames += 15
                elif event.key == pygame.K_KP_MINUS:  # run game in less frames
                    frames -= 15
                    if (frames <= 0): frames = 1
                elif event.key == pygame.K_KP8:  # run game in more frames
                    frames += 2
                elif event.key == pygame.K_KP2:  # run game in less frames
                    frames -= 2
                    if (frames <= 0):  # min number of frames is one
                        frames = 1
        if x_change != 0 or y_change != 0:  # if there is change in snake head location update snakeList
            x += x_change
            y += y_change
            snakeList.insert(0, (x, y))  # add new head
            snakeList.pop()  # remove last part
        if x + 10 > width or x < 0 or y + 10 > height or y < 0:  # if snake runs out of screen game over
            gameOver = True
            # message_to_screen('Game Over',colors.red)
            # print("Game Over")
        if len(snakeList) > 6 and snakeList.count(
                (x, y)) > 1:  # if there are two same elements in snakeList you have crashed into yourself
            gameOver = True
        gameDisplay.fill(colors.white)  # fill surface with color optional contained to a specific area
        drawApple(randAppleX, randAppleY)
        drawSnake(snakeList,direction)

        if randAppleX + appleThickness > x and randAppleX < x + snakeWidth \
                and randAppleY + appleThickness > y and randAppleY < y + snakeWidth:  # if snake ate the apple
            snakeLength += 1
            frames += 2  # everytime player eats apple speed up the snake
            snakeList.append((x, y))
            randAppleX, randAppleY = randAppleLocation()
            drawSnake(snakeList,direction)
        highscoreFile = open("highscore.txt", "r")  # highscore file
        highScore = highscoreFile.read()  # read highscore all time
        highscoreFile.close()
        if snakeLength >= int(highScore):
            scoreText = mediumFont.render(str(snakeLength), False,
                                          colors.gold)  # display gold score so that player knows he achieved highscore
            gameDisplay.blit(scoreText, (width // 2 - scoreText.get_width()//2, height // 20))  # print score
        else:
            scoreText = mediumFont.render(str(snakeLength), False, colors.black)  # if not new highscore score is black
            gameDisplay.blit(scoreText, (width // 2 - scoreText.get_width()//2, height // 20))  # print score
        pygame.display.update()
        clock.tick(frames)  # frames per second
    pygame.quit()  # pygame quit
    quit()

gameIntro()
gameLoop()
