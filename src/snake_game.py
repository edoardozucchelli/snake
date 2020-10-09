import pygame
import random
from src import snake_config as c


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.display = pygame.display
        self.screen = self.display.set_mode((self.width, self.height))

        pygame.display.set_caption('Snake')


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.snake_body = [(x, y)]

    def turn(self, key):
        if key == pygame.K_LEFT:
            self.x = self.x - c.BLOCK
        elif key == pygame.K_RIGHT:
            self.x = self.x + c.BLOCK
        elif key == pygame.K_UP:
            self.y = self.y - c.BLOCK
        elif key == pygame.K_DOWN:
            self.y = self.y + c.BLOCK

    def step(self):
        self.snake_body.append((self.x, self.y))
        self.snake_body.pop(0)

    def grow(self):
        self.snake_body.append((self.x, self.y))

    def draw(self, screen):
        for x in self.snake_body:
            pygame.draw.rect(screen, c.SNAKE_COLOUR, [x[0], x[1], c.BLOCK, c.BLOCK])


class Food:
    def __init__(self, snake_body):
        self.excluding_list = snake_body
        self.x = random_excluding_values(0, c.SCREEN_WIDTH, extract(self.excluding_list, 0))
        self.y = random_excluding_values(0, c.SCREEN_HEIGHT, extract(self.excluding_list, 1))

    def respawn(self):
        return self.__init__(self.excluding_list)

    def draw(self, display):
        pygame.draw.rect(display, c.FOOD_COLOUR, [self.x, self.y, c.BLOCK, c.BLOCK])


def extract(lst, i):
    return [item[i] for item in lst]


def random_excluding_values(_min, _max, excluded_values):
    all_nums = {num for num in range(_min, _max - c.BLOCK, c.BLOCK)}
    exclude_set = set(excluded_values)
    valid_choices = all_nums - exclude_set

    return random.sample(valid_choices, 1)[0]


class Game:
    high_score = 0

    def __init__(self):
        self.game_quit = False
        self.score = 0
        self.latest_key = pygame.K_RIGHT

        self.screen = Screen(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self.snake = Snake(c.SNAKE_X, c.SNAKE_Y)
        self.food = Food(self.snake.snake_body)

    def restart(self):
        return self.__init__()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_quit = True
            if event.type == pygame.KEYDOWN:
                self.latest_key = event.key

    def is_eaten(self):
        if (self.snake.x, self.snake.y) == (self.food.x, self.food.y):
            self.snake.grow()
            self.food.respawn()
            self.score = self.score + 1
        else:
            self.snake.step()

    def draw_objects(self):
        self.snake.draw(self.screen.screen)
        self.food.draw(self.screen.screen)

    def is_new_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            print(f"New high score is {self.high_score}!!!")

    def is_game_over(self):
        if any(
            [
             (self.snake.x, self.snake.y) in self.snake.snake_body[:-1],
             self.snake.x in {-c.BLOCK, self.screen.width},
             self.snake.y in {-c.BLOCK, self.screen.height}
             ]
        ):
            self.is_new_high_score()
            self.restart()

    def game_loop(self):
        self.screen.screen.fill(c.SCREEN_COLOUR)
        self.event_loop()
        self.snake.turn(self.latest_key)
        self.is_eaten()
        self.is_game_over()
        self.draw_objects()


def main():
    pygame.init()
    clock = pygame.time.Clock()

    game = Game()
    while not game.game_quit:
        game.game_loop()
        pygame.display.update()
        clock.tick(c.SNAKE_SPEED)

    pygame.quit()


if __name__ == '__main__':
    main()
