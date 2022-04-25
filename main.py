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
snack_speed = 30
clock = pygame.time.Clock()

def draw_snake(snake):
    for pos in snake:
        pygame.draw.rect(dis, black, [pos[0], pos[1], snake_block, snake_block])

def hit_boundaries(x, y):
    if x == dis_width + snake_block or x == -snake_block or y == dis_height + snake_block or y == -snake_block:
        return True

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/3, dis_height/3])

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
                if event.key == pygame.K_LEFT:
                    dx = -10
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = 10
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -10
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = 10

        x1 += dx
        y1 += dy
        dis.fill(white)

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if hit_boundaries(x1 + dx, y1 + dy):
            game_close = True

        if len(snake_list) > length_of_snake:
            del snake_list[0]

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