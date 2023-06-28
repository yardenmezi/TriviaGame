import requests
import random
from dataclasses import dataclass
from trivia_components import TriviaQuestion

BASE_URL = 'https://opentdb.com'
URL = f'{BASE_URL}/api.php'
CATEGORY_URL = f'{BASE_URL}/api_category.php'


@dataclass
class OpenTDBParams:
    amount: int
    type: str
    category: int


def _extract_response(url, extract_func, params=''):
    response = requests.get(url, params=params)
    if response.ok:
        response = response.json()
        if "response_code" not in response.keys() or response["response_code"] == 0:
            return extract_func(response)
        raise requests.RequestException(
            f'Failed to get data from {URL}. response code: {response["response_code"]}')
    else:
        raise requests.RequestException(
            f'Failed to get data from {URL}. Status code: {response.status_code}. Reason: {response.reason}')


def get_trivia_question(category_number) -> TriviaQuestion:
    params = vars(OpenTDBParams(1, 'multiple', category_number))
    get_question = lambda response: [TriviaQuestion(result) for result in response['results']][0]
    return _extract_response(URL, get_question, params)


def get_trivia_categories(categories_number: int) -> list:
    all_possible_categories = _extract_response(CATEGORY_URL, lambda x: x["trivia_categories"])
    chosen_indices = random.sample(range(min(len(all_possible_categories), categories_number)), categories_number)
    categories = [all_possible_categories[i] for i in chosen_indices]
    return categories
