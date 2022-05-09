import random
import pygame
from pygame.locals import *
from pygame import mixer
pygame.init()
surface = pygame.display.set_mode((600, 400))

font_style = pygame.font.SysFont(None, 50)
dis_width = 800
dis_height = 800
snake_block = 40
purple = (210, 155, 192)
white = (255, 255, 255)
black = (0, 0, 0)
orange = (255, 202, 111) #orange
red = (245, 108, 96)
green = (0, 255, 0)
gray = (20, 20, 20)
dark_gray = (15, 15, 15)
snack_speed = 30
clock = pygame.time.Clock()
winning_score = 400


def draw_surface():
    dis.fill(dark_gray)

def draw_grid():
    for i in range(0, dis_width, snake_block):
        pygame.draw.line(dis, gray, (i, 0), (i, dis_height))
        pygame.draw.line(dis, gray, (0, i), (dis_width, i))

def draw_path(paths, goal, start):
    actual_path = []
    curr = tuple(goal)
    while curr != tuple(start):
        if curr in paths.keys():
            if len(paths[curr]):
                pygame.draw.rect(dis, green, [paths[curr][0], paths[curr][1], snake_block, snake_block])
                actual_path.append(paths[curr])
                curr = tuple(paths[curr])
            else:
                return []

    actual_path = actual_path[:-1]
    actual_path.reverse()
    actual_path.append(goal)
    print(actual_path)

    return actual_path

def bfs(snake_list, start, goal, obstacles):
    visited = []
    queue = []
    paths = {}
    print("masi bfs")

    dvs = [[snake_block, 0], [0, snake_block], [-snake_block, 0], [0, -snake_block]]

    visited.append(start)
    queue.append(start)

    while queue:
        node = queue.pop(0)
        if node == goal:
            break

        for dv in dvs:
            newnode = [node[0] + dv[0], node[1] + dv[1]]
            if newnode not in obstacles and newnode not in snake_list and newnode not in visited and not hit_boundaries(newnode):
                queue.append([node[0] + dv[0], node[1] + dv[1]])
                visited.append([node[0] + dv[0], node[1] + dv[1]])
                paths[tuple(newnode)] = node

    actual_path = draw_path(paths, goal, start)

    return actual_path

def get_direction(closest_path, snake_head):
    if len(closest_path):
        dx = closest_path[0] - snake_head[0]
        dy = closest_path[1] - snake_head[1]

        print([dx, dy])
        return [dx, dy]

def get_path_to_food(snake_list, food, obstacles):
    return bfs(snake_list, snake_list[-1], food, obstacles)

def get_path_to_tail(snake_list, obstacles):
    return bfs(snake_list, snake_list[-1], snake_list[0], obstacles)

def random_move(dv, snakelist, flag):
    rand = random.randrange(0, 4)
    print("masi random")
    if rand not in flag:
        if rand == 0: ##kanan
            head = [snakelist[-1][0] + snake_block, snakelist[-1][1]]
            if dv != [-snake_block, 0] and head not in snakelist and not hit_boundaries(head) and not hit_obstacle(head):
                return [snake_block, 0]
        elif rand == 1: ##kiri
            head = [snakelist[-1][0] - snake_block, snakelist[-1][1]]
            if dv != [snake_block, 0] and head not in snakelist and not hit_boundaries(head) and not hit_obstacle(head):
                return [-snake_block, 0]
        elif rand == 2: ##baawah
            head = [snakelist[-1][0], snakelist[-1][1] + snake_block]
            if dv != [0, -snake_block] and head not in snakelist and not hit_boundaries(head) and not hit_obstacle(head):
                return [0, snake_block]
        elif rand == 3: ##atas
            head = [snakelist[-1][0], snakelist[-1][1] - snake_block]
            if dv != [0, snake_block] and head not in snakelist and not hit_boundaries(head) and not hit_obstacle(head) :
                return [0, -snake_block]

        flag.update(rand)
    elif len(flag) < 4:
        return random_move(dv, snakelist, flag)
    else:
        return []


def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(dis, purple, [pos[0], pos[1], snake_block-1, snake_block-1])

def hit_self(head, snake):
    for body in snake[:-2]:
        if body == head:
            return True

def hit_boundaries(head):
    if head[0] > dis_width - snake_block or head[0] < 0 or head[1] > dis_height - snake_block or head[1] < 0:
        return True

def hit_obstacle(head, obstacles):
    for obstacle in obstacles:
        if head[0] == obstacle[0] and head[1] == obstacle[1]:
            return True

def message(msg, color, pos):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [pos[0], pos[1]])

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(dis, red, [obstacle[0], obstacle[1], snake_block-1, snake_block-1])

def draw_score(score):
    str = "Score: " + score.__str__()
    message(str, red, [30, 30])

def draw_level(level):
    str = "Level: " + level.__str__()
    message(str, red, [dis_width - 150, 30])

def generate_food(snake_list, obstacles):
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    if [foodx, foody] not in snake_list and [foodx, foody] not in obstacles:
        return [foodx, foody]
    else:
        return generate_food(snake_list, obstacles)

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.update()
pygame.display.set_caption("Snake Solver")

click = False

def button_rect():
    button_1 = pygame.Rect(300,300,200,50)
    button_2 = pygame.Rect(300,400,200,50)
    pygame.draw.rect(surface,(red), button_1)
    pygame.draw.rect(surface,(red), button_2)

def menuLoop():
    goto_gameplay = False
    exit_game = False

    while not exit_game:
        if goto_gameplay:
            gameLoop(0)

        message("WELCOME", red, [310 , 200])
        mx,my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(300,300,200,50)
        button_2 = pygame.Rect(300,400,200,50)
        button_rect()
        message("Play", white, [365 , 307])
        message("Quit", white, [365 , 407])
        if button_1.collidepoint((mx,my)):
            if click:
                goto_gameplay = True
        if button_2.collidepoint((mx,my)):
            if click:
                exit_game = True
        pygame.display.update()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game = True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
def gameLoop(level):
    game_over = False
    game_close = False
    goto_nextlevel = False

    x1 = dis_width/2
    y1 = dis_width/2
    dv = [0, 0]
    curr_score = 0

    snake_list = []
    obstacles = []
    length_of_snake = 1

    food = generate_food(snake_list, obstacles)
    for i in range(0, level*10):
        x = random.randrange(0, dis_width, snake_block)
        y = random.randrange(0, dis_height, snake_block)
        obstacles.append([x, y])

    curr_path = []

    while not game_over:

        while goto_nextlevel:
            dis.fill(dark_gray)
            message("Next level!", red, [dis_width / 3 + 60, dis_width / 5])
            message("Press N to go to the next level!", red, [dis_width / 3 - 50, dis_width / 5 + 100])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        level += 1
                        gameLoop(level)

        while game_close:
            dis.fill(dark_gray)
            message("You lost!", red, [dis_width/3 + 60, dis_width/5])
            message("Press Q-Quit or C-Play Again", red, [dis_width/4 - 20, dis_width/4])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                        exit()
                    if event.key == pygame.K_c:
                        mixer.music.load("res/y2mate.com - Wii Music  Gaming Background Music HD.mp3")
                        mixer.music.play()
                        gameLoop(0)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         game_over = True
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT and dx == 0:
        #             dx = -snake_block
        #             dy = 0
        #         elif event.key == pygame.K_RIGHT and dx == 0:
        #             dx = snake_block
        #             dy = 0
        #         elif event.key == pygame.K_UP and dy == 0:
        #             dx = 0
        #             dy = -snake_block
        #         elif event.key == pygame.K_DOWN and dy == 0:
        #             dx = 0
        #             dy = snake_block
        # if dv == [0, 0]:
        #     continue

        if curr_score == winning_score:
            goto_nextlevel = True

        x1 += dv[0]
        y1 += dv[1]
        dis.fill(white)

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if x1 == food[0] and y1 == food[1]:
            food = generate_food(snake_list, obstacles)
            length_of_snake += 1
            curr_score += 1

        curr_path = get_path_to_food(snake_list, food, obstacles)

        if len(curr_path) == 0:
            curr_path = get_path_to_tail(snake_list, obstacles)
        if len(curr_path) == 0:
            curr_path = random_move(dv, snake_list, {})
        if len(curr_path) == 0:
            game_close = True

        dv = get_direction(curr_path[0], snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        if hit_self(snake_head, snake_list):
            game_close = True

        if hit_obstacle(snake_head, obstacles):
            game_close = True

        if hit_boundaries(snake_head):
            game_close = True

        #draw surface
        draw_surface()

        #draw grid
        draw_grid()

        #draw obstacles
        draw_obstacles(obstacles)

        #draw food
        rect = pygame.Rect(food[0], food[1], snake_block-1, snake_block-1)
        pygame.draw.rect(dis, orange, rect)

        #draw snake
        draw_snake(snake_list)

        #draw score
        draw_score(curr_score)

        #draw level
        draw_level(level)

        pygame.display.update()

        clock.tick(snack_speed)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

mixer.init()
mixer.music.load("res/y2mate.com - Game Show Tv Theme Music.mp3")
mixer.music.play()
menuLoop()

pygame.quit()
quit()
