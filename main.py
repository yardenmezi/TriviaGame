import logging
import requests
import yaml
import messages
from game import Game
import formatter


if __name__ == '__main__':
    try:
        with open("config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)

        formatter = formatter.Formatter(config=config["FORMATTING"])
        game = Game(formatter, game_config=config["GAME"])

        score = game.start()
        print(f"your score is {score}")

    except requests.exceptions.ConnectionError as exception:
        logging.error(f'Failed to connect: {exception}.')
        print(f"{messages.TRIVIA_UNAVAILABLE} {messages.CONNECTION_ERROR}")
    except Exception as exception:
        logging.error(f'An error occurred: {exception}.')
        print(messages.TRIVIA_UNAVAILABLE)
