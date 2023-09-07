import pygame
import random
import NEAT_network

WIDTH, HEIGHT, SIZE = 320, 240, 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#board
rows = int(HEIGHT / SIZE)
cols = int(WIDTH / SIZE)

def updateInputs(snake, board, snake_dir, food_row, food_col, hunger):
    # 0-3: NESW dirs, 4-6: left, forward, right (rel. to dir) 7: MD to food, 8: snake length
    width_tiles = int(WIDTH/SIZE)
    height_tiles = int(HEIGHT/SIZE)
    inputs = [0] * 8
    head = snake[0]
    #how far above/below the snake's head is the food (if at all)
    inputs[0] = abs(head[0] - food_row)/height_tiles
    #how far to the right/left the snake's head is the food (if at all)
    inputs[1] = abs(head[1] - food_col)/width_tiles
    #update head direction inputs and nearest collisions
    #moving up
    if snake_dir == (-1, 0):
        #check left (left)
        for i in range(head[1] - 1, -1, -1):
            if board[head[0]][i] == 1:
                inputs[2] = i/width_tiles
                break
        #check forward (up)
        for i in range(head[0] - 1, -1, -1):
            if board[i][head[1]] == 1:
                inputs[3] = i/height_tiles
                break
        #check right (right)
        for i in range(head[1] + 1, width_tiles):
            if board[head[0]][i] == 1:
                inputs[4] = i/width_tiles
                break
    #moving right
    elif snake_dir == (0, 1):        
        #check left (up)
        for i in range(head[0] - 1, -1, -1):
            if board[i][head[1]] == 1:
                inputs[2] = i/height_tiles
                break
        #check forward (right)
        for i in range(head[1] + 1, width_tiles):
            if board[head[0]][i] == 1:
                inputs[3] = i/width_tiles
                break
        #check right (down)
        for i in range(head[0] + 1, height_tiles):
            if board[i][head[1]] == 1:
                inputs[4] = i/height_tiles
                break
    #moving down
    elif snake_dir == (1, 0):
        #check left (right)
        for i in range(head[1] + 1, width_tiles):
            if board[head[0]][i] == 1:
                inputs[2] = i/width_tiles
                break
        #check forward (down)
        for i in range(head[0] + 1, height_tiles):
            if board[i][head[1]] == 1:
                print(head[0] + i)
                inputs[3] = i/height_tiles
                break
        #check right (left)
        for i in range(head[1] - 1, 0, -1):
            if board[head[0]][i] == 1:
                print(head[1] + i)
                inputs[4] = i/width_tiles
                break
    #moving left
    elif snake_dir == (0, -1):
        #check left (down)
        for i in range(head[0] + 1, height_tiles):
            if board[i][head[1]] == 1:
                inputs[2] = i/height_tiles
                break
        #check forward (left)
        for i in range(head[1] - 1, 0, -1):
            if board[head[0]][i] == 1:
                inputs[3] = i/width_tiles
                break
        #check right (up)
        for i in range(head[0] - 1, -1, - 1):
            if board[i][head[1]] == 1:
                inputs[4] = i/height_tiles
                break
    #calculate MD to food from head
    inputs[5] = abs(snake[0][0] - food_row)/height_tiles + abs(snake[0][1] - food_col)/width_tiles
    #calculate length of snake
    inputs[6] = len(snake)
    #add hunger
    inputs[7] = hunger/100
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
    snake = [(10, 10)]
    board[snake[0][0]][snake[0][1]] = 1
    snake_dir = (1, 0)
    food_row = random.randint(0, rows - 1)
    food_col = random.randint(0, cols - 1)
    food = (food_row, food_col)
    board[food_row][food_col] = 2

    # Main game loop
    clock = pygame.time.Clock()
    clock_speed = 50
    running = True
    score = 0
    hunger = 100
    survival = 0
    
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
        if hunger <= 0:
            running = False
            continue
        
        inputs = updateInputs(snake, board, snake_dir, food[0], food[1], hunger)
        new_dir = genome.predict(inputs, snake_dir)
        snake_dir = new_dir
        new_head = (snake[0][0] + new_dir[0], snake[0][1] + new_dir[1])

        # Check collision with walls or snake's body
        if (
            new_head[0] < 0
            or new_head[0] >= rows
            or new_head[1] < 0
            or new_head[1] >= cols
            or new_head in snake
        ):
            running = False
            continue

        #insert new_head into the front of snake
        board[new_head[0]][new_head[1]] = 1
        snake.insert(0, new_head)

        # Check collision with food
        if snake[0] == food:
            hunger = 100
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
            score += 3
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
        hunger -= 2
        survival += 0.1

    pygame.quit()
    return score + survival


def play_silent(genome):
    #state space is represented by a 2D list: 0 = empty, 1 = occupied snake body segment, 2 = occupied by food
    board = [[0 for i in range(cols)] for j in range(rows)]
    # Snake and food
    snake = [(10, 10)]
    board[snake[0][0]][snake[0][1]] = 1
    snake_dir = (1, 0)
    food_row = random.randint(0, rows - 1)
    food_col = random.randint(0, cols - 1)
    food = (food_row, food_col)
    board[food_row][food_col] = 2

    hunger = 100
    survival = 0
    score = 0
    #loop through game
    while hunger >= 0:
        inputs = updateInputs(snake, board, snake_dir, food[0], food[1], hunger)
        new_dir = genome.predict(inputs, snake_dir)
        snake_dir = new_dir
        new_head = (snake[0][0] + new_dir[0], snake[0][1] + new_dir[1])

        # Check collision with walls or snake's body
        if (
            new_head[0] < 0
            or new_head[0] >= rows
            or new_head[1] < 0
            or new_head[1] >= cols
            or new_head in snake
        ):
            break

        #insert new_head into the front of snake
        board[new_head[0]][new_head[1]] = 1
        snake.insert(0, new_head)

        # Check collision with food
        if snake[0] == food:
            hunger = 100
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
            score += 3
        else:
            #remove the tail from the snake during game iterations without eating the food
            tail = snake.pop()
            board[tail[0]][tail[1]] = 0
        hunger -= 2
        survival += 0.1
    return score + survival

