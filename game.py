from typing import List
import requests
import messages
from trivia_components import TriviaQuestion


class GameHandler:
    def __init__(self, formatter, questions_api_config):
        self._score = 0
        self.formatter = formatter
        self._questions_api_config = questions_api_config
        self.trivia_questions = None
        self.answered_questions = set()

        self.init_new_game()

    def init_new_game(self):
        self._score = 0
        self.answered_questions = set()
        self.trivia_questions = self.get_trivia_questions(self._questions_api_config)
        self.formatter.set_questions(self.trivia_questions)

    @staticmethod
    def get_trivia_questions(questions_api_config):
        response = requests.get(questions_api_config["URL"], params=questions_api_config["PARAMS"])
        if response.ok:
            return [TriviaQuestion(result) for result in response.json()['results']]

        raise RuntimeError(
            f'Failed to get data from {questions_api_config["URL"]}. Status code: {response.status_code}. Reason: {response.reason}')

    @staticmethod
    def is_valid_user_input(user_input: str, valid_range):
        if user_input.isnumeric() and valid_range[0] <= int(user_input) <= valid_range[1]:
            return True
        else:
            return False

    def get_valid_user_input(self, valid_answers_range: List[int], instruction_msg: str):
        print(instruction_msg)
        _answer = input()
        while not self.is_valid_user_input(_answer, valid_answers_range):
            print(messages.USER_INPUT_INVALID)
            print(instruction_msg)
            _answer = input()
        return _answer

    def ask_trivia_question(self, chosen_question: TriviaQuestion):
        _answer = self.get_valid_user_input([1, 4], chosen_question)
        if int(_answer) == chosen_question.get_answer_index():
            self._score += 1
            print("Correct!")
        else:
            print(f"Wrong answer. Answer was: {chosen_question.get_answer()}")

    def handle_question_choosing(self):
        _answer = self.get_valid_user_input([1, len(self.trivia_questions)], 'please choose question')
        question_number: int = int(_answer) - 1
        self.formatter.mark_answered_question(question_number)

        if question_number in self.answered_questions:
            print(messages.QUESTION_CHOSEN)
        else:
            self.answered_questions.add(question_number)
            self.ask_trivia_question(self.trivia_questions[question_number])

    def is_game_over(self) -> bool:
        return len(self.answered_questions) == len(self.trivia_questions)

    def run_trivia(self) -> int:
        self.formatter.set_questions(self.trivia_questions)
        while not self.is_game_over():
            self.formatter.show_categories()
            self.handle_question_choosing()
