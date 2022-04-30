import random
import pygame
import time
pygame.init()

font_style = pygame.font.SysFont(None, 50)
dis_width = 400
dis_height = 400
snake_block = 20
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
gray = (20, 20, 20)
dark_gray = (15, 15, 15)
snack_speed = 15
clock = pygame.time.Clock()


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
        pygame.draw.rect(dis, green, [paths[curr][0], paths[curr][1], snake_block, snake_block])
        actual_path.append(paths[curr])
        curr = tuple(paths[curr])

    actual_path = actual_path[:-1]
    actual_path.reverse()
    actual_path.append(goal)

    return actual_path

def bfs(snake_list, start, goal, obstacles):
    visited = []
    queue = []
    paths = {}

    dvs = [[snake_block, 0], [0, snake_block], [-snake_block, 0], [0, -snake_block]]

    visited.append(start)
    queue.append(start)

    while queue:
        node = queue.pop(0)
        if node == goal:
            break

        for dv in dvs:
            newnode = [node[0] + dv[0], node[1] + dv[1]]
            if newnode not in obstacles and newnode not in snake_list and newnode not in visited:
                queue.append([node[0] + dv[0], node[1] + dv[1]])
                visited.append([node[0] + dv[0], node[1] + dv[1]])
                paths[tuple(newnode)] = node

    actual_path = draw_path(paths, goal, start)

    return actual_path

def get_direction(closest_path, snake_head):
    if len(closest_path) and len(snake_head):
        dx = closest_path[0] - snake_head[0]
        dy = closest_path[1] - snake_head[1]

        return [dx, dy]

    return [0, 0]

def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(dis, white, [pos[0], pos[1], snake_block, snake_block])

def hit_self(head, snake):
    for body in snake[:-2]:
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

def generate_food(snake_list, obstacles):
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    if [foodx, foody] not in snake_list and [foodx, foody] not in obstacles:
        return [foodx, foody]
    else:
        generate_food(snake_list, obstacles)

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.update()
pygame.display.set_caption("Snake Solver")

def gameLoop(level):
    game_over = False
    game_close = False

    x1 = dis_width/2
    y1 = dis_width/2
    dv = [0, 0]
    dx = 0
    dy = 0

    snake_list = []
    obstacles = []
    length_of_snake = 1

    food = generate_food(snake_list, obstacles)
    for i in range(0, level*10):
        x = random.randrange(0, dis_width, snake_block)
        y = random.randrange(0, dis_height, snake_block)
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
                        gameLoop(level)

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


        x1 += dv[0]
        y1 += dv[1]
        print(dv)
        dis.fill(white)

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        curr_path = bfs(snake_list, snake_head, food, obstacles)
        print("current path: ", curr_path, "snake_list: ", snake_list, "food: ", food)
        dv = get_direction(curr_path[0], snake_head)

        if hit_self(snake_head, snake_list):
            print(snake_head, snake_list)
            print("tabrak sendiri bos")
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
        pygame.draw.rect(dis, red, [food[0], food[1], snake_block, snake_block])

        #draw paths
        curr_path = bfs(snake_list, snake_head, food, obstacles)
        print("current path: ", curr_path, "snake_list: ", snake_list, "food: ", food)
        dv = get_direction(curr_path[0], snake_head)

        #draw snake
        draw_snake(snake_list)

        pygame.display.update()

        if x1 == food[0] and y1 == food[1]:
            food = generate_food(snake_list, obstacles)
            length_of_snake += 1

        clock.tick(snack_speed)

gameLoop(1)

pygame.quit()
quit()
