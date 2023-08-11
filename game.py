from typing import List
import messages
import trivia_api
from trivia_components import TriviaQuestion, NUMBER_OF_ANSWERS


def get_valid_user_input(valid_answers_range: List[int] or set, instruction_msg: str):
    print(instruction_msg)
    user_input = input()
    while not user_input.isnumeric() or not Game.offset_user_input(int(user_input)) in valid_answers_range:
        print(messages.USER_INPUT_INVALID)
        print(instruction_msg)
        user_input = input()
    return Game.offset_user_input(int(user_input))


class Game:
    def __init__(self, formatter, game_config: dict):
        self._score = 0
        self._formatter = formatter
        # todo: handle empty list - should raise an error
        self._trivia_categories: list = trivia_api.get_trivia_categories(game_config["QUESTIONS_NUMBER"])

    offset_user_input = lambda x: x - 1

    def start(self) -> int:
        while not self._is_game_over():
            self._manage_round_flow()
        return self._score

    def _get_available_indexes(self):
        available_indexes = []
        for idx, category in enumerate(self._trivia_categories):
            if "is_available" not in category or category["is_available"]:
                available_indexes.append(idx)
        return available_indexes

    def _is_game_over(self) -> bool:
        return len(self._get_available_indexes()) == 0

    def _handle_question_asking_flow(self, question_idx):
        question: TriviaQuestion = trivia_api.get_trivia_question(self._trivia_categories[question_idx]["id"])
        self._trivia_categories[question_idx]["is_available"] = False

        user_response = get_valid_user_input([i for i in range(NUMBER_OF_ANSWERS)], question)

        if int(user_response) == question.get_answer_index():
            self._score += 1
            msg = "Correct!"
        else:
            msg = f"Wrong answer. Answer was: {question.get_answer()}"
        print(msg)

    def _manage_round_flow(self):
        self._formatter.display_game_table(self._trivia_categories)
        available_indexes = self._get_available_indexes()
        print(available_indexes)
        _question_idx = get_valid_user_input(available_indexes, messages.CHOOSING_QUESTION)
        self._handle_question_asking_flow(_question_idx)