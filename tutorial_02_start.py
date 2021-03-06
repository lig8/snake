import pygame
from random import randrange

class Snake(pygame.sprite.Sprite):
    """docstring for Snake"""
    head = pygame.image.load("imgs/head.png")
    skin = pygame.image.load("imgs/skin.png")
    tail = pygame.Surface((5, 5))
    tail.fill((0, 0, 0))

    def __init__(self):
        self.direction = "right"
        self.x = 5 * 20
        self.y = 5 * 20
        self.body = [
            [Snake.head, [self.x, self.y]],
            [Snake.skin, [self.x - 5, self.y]],
            [Snake.skin, [self.x - 10, self.y]]
        ]


snake = Snake()
class Game:
    "Starts the game"
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 24)
    WIDTH: int = 600
    HEIGHT: int = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 16)
    display = pygame.Surface((WIDTH // 4, HEIGHT // 4))
    clock = pygame.time.Clock()
    # used by Game.move()
    next_step = {
        "right": 1,
        "left": -1,
        "K_UP": -1,
        "down": 1}

    def menu() -> None:
        "PRESS S TO START"
        Game.write('Snake', 0, 0, middle="")
        Game.write("Press s to start", 0, 20, middle="")
        # Wait the user to press 's' or to quit / escape
        while True:
            event = pygame.event.wait()
            if pygame.event.get(pygame.QUIT):
                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                break
            if keys[pygame.K_s]:
                print("Start")
                Game.start()
                # break
        pygame.quit()


    def write(t, x: int = 0, y: int = 0, middle: str = "both", color="Coral") -> pygame.Surface:
        "RENDERS AND BLIT THE TEXT ====================\
        Examples to display text on the screen:  \
        - Write in the middle:           \
        Game.write('Game over')         \
        - write everywhere:          \
        Game.write('Snake', 0, 0, middle='')"
        text = Game.font.render(t, 1, pygame.Color(color))
        if middle == "both":
            rect_middle = text.get_rect(center=((Game.WIDTH // 2, Game.HEIGHT //2)))
            Game.display.blit(text, rect_middle)
        else:
            Game.display.blit(text, (x, y))
        Game.screen.blit(pygame.transform.scale(Game.display, (400, 400)), (0,0))
        pygame.display.update()
        return text


    def start():

        go = "RIGHT"
        row = randrange(1, 20)
        col = randrange(1, 20)
        # a random posizion multiple of 20
        pos_food = [row * 20, col * 20]
        loop = 1
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loop = 0
                    # You cannot move backwards
                    elif event.key == pygame.K_RIGHT:
                        go = "right"
                    elif event.key == pygame.K_UP:
                        go = "K_UP"
                    elif event.key == pygame.K_DOWN:
                        go = "down"
                    elif event.key == pygame.K_LEFT:
                        go = "left"
                    Game.not_back(go)
                    Game.move()
                    Game.blit_all()
            Game.screen.blit(pygame.transform.scale(Game.display, (400, 400)), (0,0))
            pygame.display.update()
            Game.clock.tick(60)
        pygame.quit()

    def not_back(wanna_go):
        "Avoid going backwards and moves"
        if wanna_go in "LEFT RIGHT":
            if snake.direction in "UP DOWN":
                snake.direction = wanna_go
        # IF YOU GO LEFT OR RIGHT YOU CAN GO UP OR DOWN
        elif snake.goes_to in "LEFT RIGHT":
            snake.direction = wanna_go
        # ========= goes to the next step =====

    def move():
        if snake.direction in "RIGHT LEFT":
            snake.x += Game.next_step[snake.direction]
        else:
            snake.y += Game.next_step[snake.direction]
        snake.body.insert(0, [snake.x, snake.y])

    def blit_all():
        "Blits all the sprites and surfaces"
        Game.display.blits(blit_sequence=Game.build_snake())

    def build_snake():
        "Creates the sequence to be blitted"
        seq_snake = []
        for n in snake.body:
            seq_snake.append((n[0], (n[1][0], n[1][1])))
        return seq_snake

Game.menu()
