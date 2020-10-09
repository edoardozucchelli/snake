import pytest
from src import snake_config as c
from src.snake_game import (
    Screen, Snake, Food, Game, extract, random_excluding_values
)


dict_key = {
    'left': 1073741904,
    'right': 1073741903,
    'up': 1073741906,
    'down': 1073741905
}


@pytest.fixture
def screen():
    screen = Screen(c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
    return screen


@pytest.fixture
def snake():
    snake = Snake(c.SNAKE_X, c.SNAKE_Y)
    return snake


@pytest.fixture
def food():
    food = Food([])
    return food


@pytest.fixture
def game():
    game = Game()
    return game


class TestScreen:
    def test_screen(self, screen):
        assert screen is not None
        assert screen.width == c.SCREEN_WIDTH
        assert screen.height == c.SCREEN_HEIGHT
        assert screen.screen.get_width() == c.SCREEN_WIDTH
        assert screen.screen.get_height() == c.SCREEN_HEIGHT
        assert screen.display.get_caption() == ('Snake', 'Snake')


class TestSnake:
    def test_snake(self, snake):
        assert snake is not None
        assert (snake.x, snake.y) == (c.SNAKE_X, c.SNAKE_Y)
        assert snake.snake_body == [(c.SNAKE_X, c.SNAKE_Y)]

    def test_turn_left(self, snake):
        snake.turn(dict_key['left'])
        assert (snake.x, snake.y) == (c.SNAKE_X - c.BLOCK, c.SNAKE_Y)

    def test_turn_right(self, snake):
        snake.turn(dict_key['right'])
        assert (snake.x, snake.y) == (c.SNAKE_X + c.BLOCK, c.SNAKE_Y)

    def test_turn_down(self, snake):
        snake.turn(dict_key['down'])
        assert (snake.x, snake.y) == (c.SNAKE_X, c.SNAKE_Y + c.BLOCK)

    def test_turn_up(self, snake):
        snake.turn(dict_key['up'])
        assert (snake.x, snake.y) == (c.SNAKE_X, c.SNAKE_Y - c.BLOCK)

    def test_step(self, snake):
        snake.x, snake.y = (c.SNAKE_X + c.BLOCK, c.SNAKE_Y)
        snake.step()
        assert snake.snake_body == [(c.SNAKE_X + c.BLOCK, c.SNAKE_Y)]

    def test_grow(self, snake):
        snake.x, snake.y = (c.SNAKE_X + c.BLOCK, c.SNAKE_Y)
        snake.grow()
        assert snake.snake_body == [(c.SNAKE_X, c.SNAKE_Y), (c.SNAKE_X + c.BLOCK, c.SNAKE_Y)]


class TestFood:
    def test_food(self, food):
        assert food is not None
        assert food.excluding_list == []
        assert food.x is not None
        assert food.y is not None

    def test_respawn_food(self, food):
        food_1 = (food.x, food.y)
        food.respawn()
        food_2 = (food.x, food.y)
        assert food_1 != food_2


def test_extract():
    lst = [(0, 1), (2, 3)]
    lst_x = extract(lst, 0)
    lst_y = extract(lst, 1)
    assert lst_x == [0, 2]
    assert lst_y == [1, 3]


def test_random_excluding_values():
    excluded_values = [10]
    rand_n = random_excluding_values(_min=0, _max=20, excluded_values=excluded_values)
    assert rand_n == 0


class TestGame:
    def test_game(self, game):
        assert game is not None
        assert game.high_score == 0
        assert game.game_quit is False
        assert game.score == 0
        assert game.latest_key is not None

        assert game.screen is not None
        assert game.snake is not None
        assert game.food is not None

    def test_restart(self, game):
        game.score = 1
        game.restart()
        self.test_game(game)

    def test_is_eaten(self, game):
        game.food.x, game.food.y = game.snake.x + c.BLOCK, game.snake.y
        game.snake.x = game.snake.x + c.BLOCK
        game.is_eaten()
        assert len(game.snake.snake_body) == 2
        assert game.score == 1

    def test_is_new_high_score(self, game):
        game.score = 2
        game.is_new_high_score()
        assert game.high_score == 2
        game.score = 1
        assert game.high_score != 1
        game.restart()
        assert game.high_score == 2
