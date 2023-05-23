import yaml
from game import GameHandler

if __name__ == '__main__':
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    game_handler = GameHandler(config["FORMATTING"], config["GAME"]["QUESTIONS_API"])
    score = game_handler.run_trivia()
    print(f"your score is {score}")


