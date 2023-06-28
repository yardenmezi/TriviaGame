import logging
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

        score = game.run_trivia()
        print(f"your score is {score}")
    except RuntimeError or OSError as e:
        logging.error(f'An error occurred: {e}.')
        print(messages.TRIVIA_UNAVAILABLE)
