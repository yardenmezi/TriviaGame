from enum import Enum


class Color(Enum):
    YELLOW = '\033[1;34m'
    BLUE = '\033[1;33m'
    UNAVAILABLE = '\033[47m'
    RESET = '\033[0m'


class Formatter:
    apply_color = lambda color, question_box: [color + string + Color.RESET.value for string in question_box]
    QUESTION_BOX = ['╔' + '═' * 45, '║' + ' ' * 45, None, '╚' + '═' * 45]

    def __init__(self, config: dict):
        self.categories_in_line = config["CATEGORIES_IN_LINE"]

    def display_game_table(self, categories: list, available_categories: set):
        if len(categories) == 0:
            raise RuntimeError("No trivia categories to show")
        categories_table = self._build_categories_table(categories, available_categories)
        self._print_categories(categories_table)

    @staticmethod
    def _build_question_box(question_number: int, category: str) -> list:
        formatted_question_box = []
        category_line = f'║ {question_number + 1}) {category}' + ' ' * (41 - len(category))
        for line in Formatter.QUESTION_BOX:
            if line:
                formatted_question_box.append(line)
            else:
                formatted_question_box.append(category_line)
        return formatted_question_box

    def _build_categories_table(self, categories: list, available_categories: set) -> list:
        categories_table = []
        for question_idx, category in enumerate(categories):
            color = Color.YELLOW.value if question_idx % 2 else Color.BLUE.value
            question_cell = self._build_question_box(question_idx, category["name"])
            if question_idx not in available_categories:
                question_cell = Formatter.apply_color(Color.UNAVAILABLE.value, question_cell)
            categories_table.append(Formatter.apply_color(color, question_cell))
        return categories_table

    def _print_categories(self, categories_table):
        table_rows = len(categories_table) // self.categories_in_line

        for row in range(table_rows):
            for box_line_number in range(len(Formatter.QUESTION_BOX)):
                for col in range(self.categories_in_line):
                    question_number = (row * self.categories_in_line) + col
                    print(categories_table[question_number][box_line_number], end='')
                print('')
            print('')
