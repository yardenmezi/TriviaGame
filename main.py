import logging
import urllib
import pymongo as pymongo
from typing import List, Set
import requests

from cli_formatting import Color
import cli_formatting
from triviaComponents import TriviaQuestion

CATEGORIES_IN_LINE = 3
QUESTIONS_NUMBER = 9
OPENTDB_URL = 'https://opentdb.com/api.php'


def get_trivia_questions():
    response = requests.get(OPENTDB_URL, params={'amount': QUESTIONS_NUMBER, 'type': 'multiple', 'category': 11})
    if response.ok:
        results = [TriviaQuestion(result) for result in response.json()['results']]
    else:
        raise RuntimeError(
            f'Failed to get data from {OPENTDB_URL}. Status code: {response.status_code}. Reason: {response.reason}')

    return results


def build_categories_table(trivia_questions):
    categories = [question.get_category() for question in trivia_questions]
    categories_rep = []

    for question_number, category_name in enumerate(categories):
        color = Color.YELLOW.value if question_number % 2 else Color.BLUE.value
        categories_rep.append(
            cli_formatting.color_string(color, cli_formatting.format_question_box(question_number, category_name)))
    return categories_rep


def print_categories(category_table: list):
    for row in range(int(len(category_table) / CATEGORIES_IN_LINE)):
        for box_line_number in range(len(cli_formatting.QUESTION_BOX)):
            for col in range(CATEGORIES_IN_LINE):
                question_number = (row * CATEGORIES_IN_LINE) + col
                print(category_table[question_number][box_line_number], end='')
            print('')
        print('')


def mark_answered_question(category_table: list, answered_question: int):
    category_table[answered_question] = cli_formatting.color_string(Color.UNAVAILABLE.value,
                                                                    category_table[answered_question])


def is_valid_user_input(user_input: str, valid_range):
    if user_input.isnumeric() and valid_range[0] <= int(user_input) <= valid_range[1]:
        return True
    else:
        return False

def get_valid_user_input(valid_answers_range: List[int], instruction_msg: str):
    print(instruction_msg)
    _answer = input()

    while not is_valid_user_input(_answer, valid_answers_range):
        print("Input is not valid")
        print(instruction_msg)
        _answer = input()
    return _answer

def ask_trivia_question(chosen_question: TriviaQuestion):
    _answer = get_valid_user_input([1,4], chosen_question)

    _answer = int(_answer)
    if _answer == chosen_question.get_answer_index():
        print("Great!")
    else:
        print("nope.")

    print(f"Answer was: {chosen_question.get_answer()}")


def handle_question_choosing(trivia_questions: List[TriviaQuestion], answered_questions: Set[int], category_table):
    _answer = get_valid_user_input([1, len(trivia_questions) - 1], 'please choose question')
    question_number: int = int(_answer) - 1
    mark_answered_question(category_table, question_number)

    if question_number in answered_questions:
        print('You already chose this question')
    else:
        answered_questions.add(question_number)
        ask_trivia_question(trivia_questions[question_number])


def run_trivia():
    try:
        trivia_questions = get_trivia_questions()
        answered_questions = set()
        category_table = build_categories_table(trivia_questions)

        while len(answered_questions) < len(trivia_questions):
            print_categories(category_table)
            handle_question_choosing(trivia_questions, answered_questions, category_table)
        print("Thank you for playing")
    except RuntimeError as e:
        logging.error('An error occurred: %s', e)
        print("Sorry, trivia is not currently available")


if __name__ == '__main__':
    run_trivia()

