import pygame
import random
import NEAT_network
import math

WIDTH, HEIGHT, SIZE = 320, 240, 10
# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#board
rows = int(HEIGHT / SIZE)
cols = int(WIDTH / SIZE)
"""
def updateInputs(snake, board, snake_dir, food_row, food_col, hunger):
    # 0-3: dist above,below,left, and right of food, 
    #4-7: snake_dir NESW
    #8-11: nearest obstacles NESW 
    #12: MD to food, 
    #13: snake length, 
    #14: hunger,
    inputs = [0] * 15
    head = snake[0]
    #how far above the snake's head is the food (if at all)
    inputs[0] = max(0, (head[0] - food_row)/rows)
    #how far to the right of the snake's head is the food (if at all)
    inputs[1] - max(0, (food_col - head[1])/cols)
    #how far below the snake's head is the food (if at all)
    inputs[2] = max(0, (food_row - head[0])/rows)
    #how far to the left of the snake's head is the food (if at all)
    inputs[3] = max(0, (head[1] - food_col)/cols)
    
    #directions
    #up
    if snake_dir == (-1, 0):
        inputs[4] = 1
    #right
    elif snake_dir == (0, 1):
        inputs[5] = 1
    #down
    elif snake_dir == (1, 0):
        inputs[6] = 1
    #left
    elif snake_dir == (0, -1):
        inputs[7] = 1 
        
    #check collisions dist
    #up
    for i in range(head[0] - 1, -1, -1):
        if board[i][head[1]] == 1:
            inputs[8] = i/rows
            break
        inputs[8] = head[0]/rows
    #right
    for i in range(head[1] + 1, cols):
        if board[head[0]][i] == 1:
            inputs[9] = i/cols
            break
        inputs[9] = (cols - head[1])/cols
    #down
    for i in range(head[0] + 1, rows):
        if board[i][head[1]] == 1:
            inputs[10] = i/rows
            break
        inputs[10] = (rows - head[0])/rows
    #left
    for i in range(head[1] - 1, -1, -1):
        if board[head[0]][i] == 1:
            inputs[11] = i/cols
            break
        inputs[11] = head[1]/cols
        
    #calculate MD to food from head
    inputs[12] = abs(snake[0][0] - food_row)/rows + abs(snake[0][1] - food_col)/cols
    #calculate length of snake
    inputs[13] = len(snake)/100
    #add hunger
    inputs[14] = hunger/100

    return inputs
"""
def updateInputs(snake, board, snake_dir, food_row, food_col, turns):
    # 0-1: dist above/below and left/right of food, 
    #2-9: nearest obstacles (N, NE, E, SE, S, SW, W, NW) 
    #10: MD to food, 
    #11: snake length, 
    #12: hunger,
    inputs = [0] * 15
    head = snake[0]
    #how far above/below the snake's head is the food (if at all)
    inputs[0] = (food_row - head[0])/rows
    #how far to the right/left the snake's head is the food (if at all)
    inputs[1] = (food_col - head[1])/cols
    #update head direction inputs and nearest collisions
    #up
    for i in range(1, head[0]):
        if board[head[0] - i][head[1]] == 1:
            inputs[2] = i/rows
            break
        inputs[2] = head[0]/rows
    #top-right
    for i in range(1, min(cols - head[1], head[0])):
        if board[head[0] - i][head[1] + i] == 1:
            inputs[3] = (2 * i)/(rows + cols)
            break
        inputs[3] = (2 * i)/(rows + cols)
    #right
    for i in range(1, cols - head[1]):
        if board[head[0]][head[1] + i] == 1:
            inputs[4] = i/cols
            break
        inputs[4] = (cols - head[1])/cols
    #bottom-right
    for i in range(1, min(cols - head[1], rows - head[0])):
        if board[head[0] + i][head[1] + i] == 1:
            inputs[5] = (2 * i)/(rows + cols)
            break
        inputs[5] = (2 * i)/(rows + cols)
    #down
    for i in range(1, rows - head[0]):
        if board[head[0] + i][head[1]] == 1:
            inputs[6] = i/rows
            break
        inputs[6] = (rows - head[0])/rows
    #bottom-left
    for i in range(1, min(head[1], rows - head[0])):
        if board[head[0] + i][head[1] - i] == 1:
            inputs[7] = (2 * i)/(rows + cols)
            break
        inputs[7] = (2 * i)/(rows + cols)
    #left
    for i in range(1, head[1]):
        if board[head[0]][head[1] - i] == 1:
            inputs[8] = i/cols
            break
        inputs[8] = head[1]/cols
    #top-left
    for i in range(1, min(head[1], head[0])):
        if board[head[0] - i][head[1] - i] == 1:
            inputs[9] = (2 * i)/(rows + cols)
            break
        inputs[9] = (2 * i)/(rows + cols)
    #calculate MD to food from head
    inputs[10] = abs(snake[0][0] - food_row)/rows + abs(snake[0][1] - food_col)/cols
    #calculate length of snake
    inputs[11] = len(snake)
    
    inputs[12] = turns/75
    
    inputs[13] = snake_dir[0]
    inputs[14] = snake_dir[1]

    return inputs
# Initialize pygame

#renders snake body segments



def play(genome):
    
    pygame.init()

    #state space is represented by a 2D list: 0 = empty, 1 = occupied snake body segment, 2 = occupied by food
    board = [[0 for i in range(cols)] for j in range(rows)]
    
    # Set up display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Snake and food
    snake = [(int(math.floor(rows/2)), int(math.floor(cols/2)))]
    board[snake[0][0]][snake[0][1]] = 1
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    snake_dir = (0, 1)#random.choice(dirs)    
    food_row = random.randint(0, rows - 1)
    food_col = random.randint(0, cols - 1)
    food = (food_row, food_col)
    board[food_row][food_col] = 2

    # Main game loop
    clock = pygame.time.Clock()
    clock_speed = 50
    running = True
    score = 0
    survival = 0
    turnNum = 0
    
    #game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    clock_speed += 5
                elif event.key == pygame.K_DOWN:
                    clock_speed -= 5
                print(clock_speed)
        
        
        #if AI spends too much time not collecting food, end sim
        if turnNum >= 50:
            score -= 3
            running = False
            continue
        
        inputs = updateInputs(snake, board, snake_dir, food[0], food[1], turnNum)
        #print(inputs)
        new_dir, turn = genome.predict(inputs, snake_dir)
        turnNum += turn
        #snake can't switch directions 180 degrees
        if ((snake_dir == (-1, 0) and new_dir == (1, 0)) or 
            (snake_dir == (1, 0) and new_dir == (-1, 0)) or
            (snake_dir == (0, 1) and new_dir == (0, -1)) or
            (snake_dir == (0, -1) and new_dir == (0, 1))):
            new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        else:
            new_head = (snake[0][0] + new_dir[0], snake[0][1] + new_dir[1])
            snake_dir = new_dir


        # Check collision with walls or snake's body
        if (
            new_head[0] < 0
            or new_head[0] >= rows
            or new_head[1] < 0
            or new_head[1] >= cols
            or new_head in snake
        ):
            running = False
            score -= 0.25
            continue

        #insert new_head into the front of snake
        board[new_head[0]][new_head[1]] = 1
        snake.insert(0, new_head)

        # Check collision with food
        if snake[0] == food:
            turnNum = 0
            board[food[0]][food[1]] = 1
            food_row = random.randint(0, rows - 1)
            food_col = random.randint(0, cols - 1)
            #check that food isn't spawned on top of the snake
            while True:
                if board[food_row][food_col] == 1:
                    food_row = random.randint(0, rows - 1)
                    food_col = random.randint(0, cols - 1)
                else:
                    break
            food = (food_row, food_col)
            board[food[0]][food[1]] = 2
            #score += 1
        else:
            #remove the tail from the snake during game iterations without eating the food
            tail = snake.pop()
            board[tail[0]][tail[1]] = 0

        # Draw everything
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[1] * SIZE, segment[0] * SIZE, SIZE, SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food[1] * SIZE, food[0] * SIZE, SIZE, SIZE))
        pygame.display.flip()
        clock.tick(clock_speed)
        survival += 0.01

    pygame.quit()
    return max(0, len(snake) - (turnNum * 0.01) + survival)
    #return score + survival
    #return max(0, score + survival - 0.5 * math.log(abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1]) + 1))
    #return max(0, score + survival - 0.1 * math.log(len(genome.connectionGenes) + 1) - 0.1 * math.log(len(genome.hiddenNodes) + 1)) 


def play_silent(genome):
    #state space is represented by a 2D list: 0 = empty, 1 = occupied snake body segment, 2 = occupied by food
    board = [[0 for i in range(cols)] for j in range(rows)]
    # Snake and food
    snake = [(int(math.floor(rows/2)), int(math.floor(cols/2)))]
    board[snake[0][0]][snake[0][1]] = 1
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    snake_dir = (0, 1)#random.choice(dirs)
    food_row = random.randint(0, rows - 1)
    food_col = random.randint(0, cols - 1)
    food = (food_row, food_col)
    board[food_row][food_col] = 3

    survival = 0
    score = 0
    turnNum = 0
    
    #loop through game
    while True:
        if turnNum > 50:
            score -= 2
            break
        inputs = updateInputs(snake, board, snake_dir, food[0], food[1], turnNum)
        #print((food, snake[0]))
        #print(inputs)
        new_dir, turn = genome.predict(inputs, snake_dir)
        turnNum += turn
        #snake can't switch directions 180 degrees
        if ((snake_dir == (-1, 0) and new_dir == (1, 0)) or 
            (snake_dir == (1, 0) and new_dir == (-1, 0)) or
            (snake_dir == (0, 1) and new_dir == (0, -1)) or
            (snake_dir == (0, -1) and new_dir == (0, 1))):
            new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        else:
            new_head = (snake[0][0] + new_dir[0], snake[0][1] + new_dir[1])
            snake_dir = new_dir

        # Check collision with walls or snake's body
        if (
            new_head[0] < 0
            or new_head[0] >= rows
            or new_head[1] < 0
            or new_head[1] >= cols
            or new_head in snake
        ):
            score -= 0.25
            break

        #insert new_head into the front of snake
        board[new_head[0]][new_head[1]] = 1
        snake.insert(0, new_head)

        # Check collision with food
        if snake[0] == food:
            turnNum = 0
            board[food[0]][food[1]] = 1
            food_row = random.randint(0, rows - 1)
            food_col = random.randint(0, cols - 1)
            #check that food isn't spawned on top of the snake
            while True:
                if board[food_row][food_col] == 1:
                    food_row = random.randint(0, rows - 1)
                    food_col = random.randint(0, cols - 1)
                else:
                    break
            food = (food_row, food_col)
            board[food[0]][food[1]] = 2
            #score += 1
        else:
            #remove the tail from the snake during game iterations without eating the food
            tail = snake.pop()
            board[tail[0]][tail[1]] = 0
        survival += 0.01
    #print(turnNum)
    return max(0, len(snake) - (turnNum * 0.01) + survival)
    #return max(0, score + survival - 0.5 * math.log(abs(snake[0][0] - food[0]) + abs(snake[0][1] - food[1]) + 1))
    #return max(0, score + survival - 0.1 * math.log(len(genome.connectionGenes) + 1) - 0.1 * math.log(len(genome.hiddenNodes) + 1)) 

