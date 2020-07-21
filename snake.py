import pygame
from pygame import gfxdraw
import sys
import random


clock = pygame.time.Clock()
# Define Constants
BOARD_SIZE = 20  # Size of the board, in block
BLOCK_SIZE = 20  # Size of 1 block, in pixel
GAME_SPEED = 8  # Game speed (Normal = 10), The bigger, the faster
window = pygame.display.set_mode((BOARD_SIZE * BLOCK_SIZE, BOARD_SIZE * BLOCK_SIZE))
pygame.display.set_caption("window")
score = 0

class Snake():
    def __init__(self):
        self.start()


    def start(self):
        self.head = [int(BOARD_SIZE / 4), int(BOARD_SIZE / 4)]
        self.body = [[self.head[0], self.head[1]],
                     [self.head[0] - 1, self.head[1]],
                     [self.head[0] - 2, self.head[1]]
                     ]
        self.direction = "RIGHT"


    def change_direction_to(self, dir):
        if dir == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if dir == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if dir == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if dir == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    def move(self, food_pos):
        ''' Move the snake to the desired direction by adding the head to that direction
            and remove the tail if the snake does not eat food
        '''
        if self.direction == "RIGHT":
            self.head[0] += 1
        if self.direction == "LEFT":
            self.head[0] -= 1
        if self.direction == "UP":
            self.head[1] -= 1
        if self.direction == "DOWN":
            self.head[1] += 1

        self.body.insert(0, list(self.head))
        if self.head == food_pos:
            return 1
        else:
            "If do not eat... same size"
            self.body.pop()
            return 0

    def check_collision(self):
        # Check if the head collides with the edges of the board
        # if 1 => GAME OVER

        conditions = (
        self.head[0] >= 20 or self.head[0] < 0,
        self.head[1] > 20 or self.head[1] < 0,
        [x for x in self.body[1:] if self.head == x]
        )
        if any(conditions):
            return 1
        else:
            return 0


class FoodSpawner():
    def __init__(self):
        self.head = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
        self.is_food_on_screen = True

    def spawn_food(self):
        if self.is_food_on_screen == False:
            self.head = [random.randrange(1, BOARD_SIZE), random.randrange(1, BOARD_SIZE)]
            self.is_food_on_screen = True
        return self.head

    def set_food_on_screen(self, bool_value):
        self.is_food_on_screen = bool_value


#                         2 main objects
snake = Snake()
food_spawner = FoodSpawner()



def draw_head(pos):
    pygame.draw.rect(
        window,
        (0, 255, 0),
        pygame.Rect(
            pos[0] * BLOCK_SIZE,
            pos[1] * BLOCK_SIZE,
            BLOCK_SIZE,
            BLOCK_SIZE))

def blit_head(pos):
    "Use a surface, instead"
    window.blit(head, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE,))

def blit_blacktail(pos):
    "Use a surface, instead"
    window.blit(head, (pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE,))

def draw_body(pos):
    pygame.draw.rect(window, (0, 128, 0), pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def delete_tail(pos):
    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(snake.body[-1][0] * BLOCK_SIZE, snake.body[-1][1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def delete_fruit(pos, food_pos):
    x = food_pos[0] * BLOCK_SIZE + 10
    y = food_pos[1] * BLOCK_SIZE + 10
    r = 9
    gfxdraw.filled_circle(window, x, y, r, (0, 0, 0))


def draw_fruit(pos, food_pos):
    gfxdraw.filled_circle(window, food_pos[0] * BLOCK_SIZE + 10, food_pos[1] * BLOCK_SIZE + 10, 9, (255, 0, 0))


pygame.init()


def write(text_to_show, x=0, y=0, middle=0):
    font = pygame.font.SysFont(text_to_show, 24)
    text = font.render(text_to_show, 1, pygame.Color("Coral"))
    w = h = BOARD_SIZE * BLOCK_SIZE
    if middle:
        text_rect = text.get_rect(center=((w // 2, h // 2)))
        window.blit(text, text_rect)
    else:
        window.blit(text, (x, y))
    pygame.display.update()


def restart():
    global GAME_SPEED


    GAME_SPEED = 8
    window.fill((0, 0, 0))
    snake.start()
    start()


def press_to_start():
    global loop
    write("Press any s to start", middle=1)
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            loop = 0
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = 0
                break
            if event.key == pygame.K_s:
                restart()
                break
    pygame.quit()



def start():
    global GAME_SPEED, score, loop

    food_pos = food_spawner.spawn_food()
    loop = 1
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction_to("RIGHT")
                elif event.key == pygame.K_UP:
                    snake.change_direction_to("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction_to("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction_to("LEFT")
        if snake.move(food_pos) == 1:
            delete_fruit(pos, food_pos)
            score += 1
            food_spawner.set_food_on_screen(False)
            GAME_SPEED += 1
            food_pos = food_spawner.spawn_food()


        # window.fill(pygame.Color(225, 225, 225))
        # Draw snake
        head = 1
        for pos in snake.body:
            if head == 1:
                draw_head(pos)
                head = 0
            else:
                draw_body(pos)
        delete_tail(pos)
        draw_fruit(pos,food_pos)

        if snake.check_collision() == 1:
            loop = 0
            press_to_start()
        pygame.display.update()
        clock.tick(GAME_SPEED)

    pygame.quit()

press_to_start()
