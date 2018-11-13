import numpy as np
import random as rand
from collections import deque


class Snake:
    """Encapsulates the Snake. It turns, moves and grows!

    Attributes:
        body (deque): Container of the coordinates for all of the Snake's bits
        velocity (np.array): Vector representing movement in the (y, x) plane
    """

    TURN_CW = np.array([[0, 1], [-1, 0]])  # 2-D clockwise rotation matrix
    TURN_CCW = np.array([[0, -1], [1, 0]])  # 2-D counter-clockwise r-matx

    def __init__(self, head: tuple):
        """Snake class initilizer

        Args:
            head (tuple): Head coordinates. What's a snake without a head?
        """
        self.body = deque()
        self.body.appendleft(head)
        self.velocity = np.array([0, 1])

    def __turn(self, turn_direction: int):
        """Rotates the velocity vector given a direction

        Args:
            turn_direction (int): -1->CCW, 1->CW, Anything Else->No Turn

        Notes:
            Leading underscores (__) designates this as a private method
        """
        if turn_direction == -1:
            print('TURN CCW')
            self.velocity = np.matmul(self.TURN_CCW, self.velocity)
            # print(self.velocity)
        elif turn_direction == 1:
            print('TURN CW')
            self.velocity = np.matmul(self.TURN_CW, self.velocity)
            # print(self.velocity)

    def move(self, turn_direction: int) -> tuple:
        """Moves the snake given a direction

        Args:
            turn_direction (int): Passed into __turn() and handled

        Returns:
            (y,x) coordinates to location moved off of or from
        """
        self.__turn(turn_direction)
        self.body.appendleft(np.add(self.body[0], self.velocity))
        return self.body.pop()

    def grow(self, place: tuple):
        """Makes the snake one bit bigger

        Args:
            place (tuple): (y,x) coordinates to where the snake grows

        Notes:
            It's a bit gross to pass coordinates for growth back into
           the snake. Seems like something the Snake class should know
           on its own. At some point it may annoy me enough to force my
           hand into some refactoring
        """
        print('GROW')
        self.body.append(np.array(place))
        print('Appended: ', self.body[-1])


class Game:
    """Encapsulates the game state and the actions possibly placed upon that state.

    Attributes:
        board_width (int): The width of the game board
        board_height (int): The height of the game board
        board (np.array): The state of the game board
        snake (Snake): Contains and mantains snake coordinates
    """

    def __init__(self, board_width: int = 8, board_height: int = 8):
        """Game class initializer. Creates board, generates snake, places apple

        Args:
            board_width(int): User defined width parameter
            board_height(int): User defined height parameter
        """
        self.board_width = board_width
        self.board_height = board_height

        self.board = np.zeros((board_width, board_height))
        self.board[1][1] = 1

        self.snake = Snake(np.array([1, 1]))

        self.place_apple()

        self.print_board()

    def refresh_game_state(self, instruction: int):
        """Performs action on game given an instruction. Changes state

        Args:
            instruction(int): Encoded instruction passed into snake.move()
        """
        (rem_h, rem_w) = self.snake.move(instruction)
        (new_h, new_w) = self.snake.body[0]
        if self.board[new_h][new_w] == 2:
            self.snake.grow((rem_h, rem_w))
            self.board[new_h][new_w] = 1
            self.place_apple()
        else:
            self.board[new_h][new_w] = 1
            self.board[rem_h][rem_w] = 0
        # if np.any(self.snake.body[-1] != (rem_h, rem_w)):
        self.print_board()

    def place_apple(self):
        """Places Apple on the on the board

        Notes:
            This is a suboptimal method implemented for haste. Needs to
           change for optimal runtime when the snake is long
        """
        (rand_h, rand_w) = self.snake.body[0]
        print(self.board[rand_h][rand_w])
        while self.board[rand_h][rand_w] == 1:
            rand_h = rand.randint(0, self.board_height-1)
            rand_w = rand.randint(0, self.board_width-1)
        self.board[rand_h][rand_w] = 2
        print('Apple Placed: ', rand_h, rand_w)

    def print_board(self):
        """Simply Prints the board for debugging purposes"""
        print(self.board)
        print('\n---------------------------------------------------\n')


def cli_player(game: Game):
    """Simple Command-Line interface for human control of the game

    Args:
        game (Game): The game we want to play!
    """
    while True:
        text = input()
        game.refresh_game_state(int(text))


if __name__ == '__main__':
    # print(TURN_CCW)
    # print(TURN_CW)
    cli_player(Game())
