import random
import pygame
import time
pygame.init()

font_style = pygame.font.SysFont(None, 50)
dis_width = 800
dis_height = 600
snake_block = 10
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
snack_speed = 100
clock = pygame.time.Clock()

def draw_path(paths, goal, start):
    curr = tuple(goal)
    while paths[curr] != tuple(start):
        pygame.draw.rect(dis, green, [paths[curr][0], paths[curr][1], snake_block, snake_block])
        print(paths)
        curr = paths[curr]

def bfs(snake_list, start, goal, obstacles):
    visited = []
    queue = []
    paths = {}
    dvs = [[10, 0], [0, 10], [-10, 0], [0, -10]]

    visited.append(start)
    queue.append(start)

    while queue:
        node = queue.pop(0)
        if node == goal:
            break

        for dv in dvs:
            newnode = [node[0] + dv[0], node[1] + dv[1]]
            if newnode not in obstacles and newnode not in snake_list and newnode not in visited and newnode != [dis_width, dis_height]:
                queue.append([node[0] + dv[0], node[1] + dv[1]])
                visited.append([node[0] + dv[0], node[1] + dv[1]])
                paths[tuple(newnode)] = tuple(node)

    draw_path(paths, goal, snake_list[-1])

def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(dis, black, [pos[0], pos[1], snake_block, snake_block])

def hit_self(head, snake):
    for body in snake[:-1]:
        if body == head:
            return True

def hit_boundaries(head):
    if head[0] == dis_width or head[0] == -snake_block or head[1] == dis_height or head[1] == -snake_block:
        return True

def hit_obstacle(head, obstacles):
    for obstacle in obstacles:
        if head[0] == obstacle[0] and head[1] == obstacle[1]:
            return True

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/5, dis_height/5])

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(dis, blue, [obstacle[0], obstacle[1], snake_block, snake_block])

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.update()
pygame.display.set_caption("Snake Solver")

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width/2
    y1 = dis_width/2
    dx = 0
    dy = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10

    snake_list = []
    length_of_snake = 1

    obstacles = []

    for i in range(0, 20):
        x = random.randrange(0, dis_width, 10)
        y = random.randrange(0, dis_height, 10)
        obstacles.append([x, y])

    while not game_over:

        while game_close == True:
            dis.fill(white)
            message("You lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -10
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = 10
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -10
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = 10


        x1 += dx
        y1 += dy
        dis.fill(white)

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        bfs(snake_list, snake_list[-1], [foodx, foody], obstacles)

        print(snake_list)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        if hit_self(snake_head, snake_list):
            game_close = True

        if hit_obstacle(snake_head, obstacles):
            game_close = True

        if hit_boundaries(snake_head):
            game_close = True

        #draw obstacles
        draw_obstacles(obstacles)

        #draw snake
        draw_snake(snake_list)

        #draw food
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10
            length_of_snake += 1
        clock.tick(snack_speed)

gameLoop()

pygame.quit()
quit()
