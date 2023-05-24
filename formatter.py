from enum import Enum


class Color(Enum):
    YELLOW = '\033[1;34m'
    BLUE = '\033[1;33m'
    UNAVAILABLE = '\033[47m'
    RESET = '\033[0m'


apply_color = lambda color, question_box: [color + string + Color.RESET.value for string in question_box]
QUESTION_BOX = ['╔' + '═' * 45, '║' + ' ' * 45, None, '╚' + '═' * 45]


class Formatter:
    def __init__(self, categories_in_line: int):
        self.categories_in_line = categories_in_line
        self.trivia_questions = []
        self.categories_lst = []

    def set_questions(self, trivia_questions):
        self.trivia_questions = trivia_questions
        self.categories_lst = self._build_categories_table()

    @staticmethod
    def _build_question_box(question_number: int, category: str) -> str:
        formatted_question_box = []
        category_line = f'║ {question_number + 1}) {category}' + ' ' * (41 - len(category))
        for line in QUESTION_BOX:
            if line:
                formatted_question_box.append(line)
            else:
                formatted_question_box.append(category_line)
        return formatted_question_box

    def _build_categories_table(self) -> list:
        categories_table = []

        categories = [question.get_category() for question in self.trivia_questions]
        for question_idx, category_name in enumerate(categories):
            color = Color.YELLOW.value if question_idx % 2 else Color.BLUE.value
            question_cell = self._build_question_box(question_idx, category_name)
            categories_table.append(apply_color(color, question_cell))
        return categories_table

    def show_categories(self):
        if len(self.categories_lst):
            #todo: handle
            print("No trivia questions to show")
        table_rows = len(self.categories_lst) // self.categories_in_line
        for row in range(table_rows):
            for box_line_number in range(len(QUESTION_BOX)):
                for col in range(self.categories_in_line):
                    question_number = (row * self.categories_in_line) + col
                    print(self.categories_lst[question_number][box_line_number], end='')
                print('')
            print('')

    def mark_answered_question(self, answered_question: int):
        if answered_question < len(self.categories_lst):
            self.categories_lst[answered_question] = apply_color(Color.UNAVAILABLE.value,
                                                                 self.categories_lst[answered_question])
        # todo: raise exception else.
