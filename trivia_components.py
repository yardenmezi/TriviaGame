import html
import random

NUMBER_OF_ANSWERS = 4


class TriviaQuestion:
    _category: str
    _question: str
    _answers: list
    _correct_answer_idx: int

    def __init__(self, result):
        self._category = result['category']
        self._question = html.unescape(result['question'])
        self._set_answers(result['incorrect_answers'], result['correct_answer'])

    def get_answer_index(self):
        return self._correct_answer_idx

    def get_answer(self):
        return self._answers[self._correct_answer_idx]

    def get_category(self):
        return self._category

    def _set_answers(self, wrong_answers, correct_answer):
        self._answers = wrong_answers
        self._correct_answer_idx = random.randrange(NUMBER_OF_ANSWERS)
        self._answers.insert(self._correct_answer_idx, correct_answer)

    def __str__(self):
        question = f"Category: {self._category}\nQuestion: {self._question}\n"
        for i, answer in enumerate(self._answers):
            question += f"{i + 1}) {answer}     "
        question += "\n"
        return question
