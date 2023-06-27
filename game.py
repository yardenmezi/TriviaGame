from typing import List
import messages
import trivia_api
from trivia_components import TriviaQuestion


def get_valid_user_input(valid_answers_range: List[int] or set, instruction_msg: str):
    print(instruction_msg)
    user_input = input()
    while user_input.isnumeric() == False or not Game.offset_user_input(int(user_input)) in valid_answers_range:
        print(messages.USER_INPUT_INVALID)
        print(instruction_msg)
        user_input = input()
    return Game.offset_user_input(int(user_input))


class Game:
    def __init__(self, formatter, game_config: dict):

        self._score = 0
        self._formatter = formatter
        self._trivia_categories: list = trivia_api.get_trivia_categories(game_config["QUESTIONS_NUMBER"])
        self._available_category_indices: set = {i for i in range(0, len(self._trivia_categories))}

    offset_user_input = lambda x: x - 1

    def _is_game_over(self) -> bool:
        return len(self._available_category_indices) == 0

    def _handle_question_asking_flow(self, question_idx):
        question: TriviaQuestion = trivia_api.get_trivia_question(self._trivia_categories[question_idx]["id"])
        self._available_category_indices.remove(question_idx)
        user_response = get_valid_user_input([i for i in range(4)], question)
        if int(user_response) == question.get_answer_index():
            self._score += 1
            msg = "Correct!"
        else:
            msg = f"Wrong answer. Answer was: {question.get_answer()}"
        print(msg)

    def _manage_round_flow(self):
        self._formatter.display_game_table(self._trivia_categories, self._available_category_indices)
        _question_idx = get_valid_user_input(self._available_category_indices, messages.CHOOSING_QUESTION)
        self._handle_question_asking_flow(_question_idx)

    def start(self) -> int:
        while not self._is_game_over():
            self._manage_round_flow()
        return self._score
