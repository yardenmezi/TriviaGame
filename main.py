import logging

import yaml
import messages
from game import GameHandler
import formatter


if __name__ == '__main__':
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        formatter = formatter.Formatter(config["FORMATTING"]["CATEGORIES_IN_LINE"])
        game_handler = GameHandler(formatter, config["GAME"]["QUESTIONS_API"])

        score = game_handler.run_trivia()
        print(f"your score is {score}")
    except RuntimeError or OSError as e:
        logging.error(f'An error occurred: {e}.')
        print(messages.TRIVIA_UNAVAILABLE)

