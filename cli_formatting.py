from enum import Enum
# todo: add here the messages


class Color(Enum):
    YELLOW = '\033[1;34m'
    BLUE = '\033[1;33m'
    UNAVAILABLE = '\033[47m'
    RESET = '\033[0m'


color_string = lambda color, question_box: [color + string + Color.RESET.value for string in question_box]
QUESTION_BOX = ['╔' + '═' * 45, '║' + ' ' * 45, None, '╚' + '═' * 45]


def build_question_box_str(question_number, category) -> str:
    formatted_question_box = []
    category_line = f'║ {question_number + 1}) {category}' + ' ' * (41 - len(category))
    for line in QUESTION_BOX:
        if line:
            formatted_question_box.append(line)
        else:
            formatted_question_box.append(category_line)
    return formatted_question_box
