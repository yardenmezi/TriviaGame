


# def decorator_example(func):
#     print("I got decorated")
#     func()


# @decorator_example
from game import GameHandler

if __name__ == '__main__':
    game_handler = GameHandler()
    score = game_handler.run_trivia()
    print(f"your score is {score}")


