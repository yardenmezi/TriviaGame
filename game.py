import logging
from typing import List
import requests
import cli_formatting as formatting
from trivia_components import TriviaQuestion

# TODO: CONFIG FILE
CATEGORIES_IN_LINE = 3
QUESTIONS_NUMBER = 9
TRIVIA_URL = 'https://opentdb.com/api.php'
trivia_params = {
    'amount': QUESTIONS_NUMBER,
    'type': 'multiple'
}


class GameHandler:
    def __init__(self):
        self._score = 0
        try:
            self.trivia_questions = self.get_trivia_questions()
        except RuntimeError as e:
            logging.error(f'An error occurred: {e}')
            print("Sorry, trivia is not currently available")
            return None
        self.answered_questions = set()
        self.category_table = formatting.QuestionsTable(self.trivia_questions, CATEGORIES_IN_LINE)

    # todo: where to put it?
    def get_trivia_questions(self):
        response = requests.get(TRIVIA_URL, params=trivia_params)
        if response.ok:
            return [TriviaQuestion(result) for result in response.json()['results']]

        raise RuntimeError(
            f'Failed to get data from {TRIVIA_URL}. Status code: {response.status_code}. Reason: {response.reason}')

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
            print("Input is not valid")
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


    def handle_question_choosing(self) -> int:
        _answer = self.get_valid_user_input([1, len(self.trivia_questions)], 'please choose question')
        question_number: int = int(_answer) - 1
        self.category_table.mark_answered_question(question_number)

        if question_number in self.answered_questions:
            print('You already chose this question')
        else:
            self.answered_questions.add(question_number)
            self.ask_trivia_question(self.trivia_questions[question_number])
            # if self.ask_trivia_question(self.trivia_questions[question_number]):
                # return 1
        # return 0

    def is_game_over(self) -> bool:
        return len(self.answered_questions) == len(self.trivia_questions)

    def run_trivia(self) -> int:
        while not self.is_game_over():
            self.category_table.print_categories()
            self.handle_question_choosing()
        print("Game over")
        return self._score
