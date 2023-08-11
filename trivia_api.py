import requests
import random
from dataclasses import dataclass
from trivia_components import TriviaQuestion

BASE_OPENTB_URL = 'https://opentdb.com'
API_REQUESTS_URL = f'{BASE_OPENTB_URL}/api.php'
CATEGORY_URL = f'{BASE_OPENTB_URL}/api_category.php'


@dataclass
class OpenTDBParams:
    amount: int
    type: str
    category: int


def _extract_response(url, params=''):
    response = requests.get(url, params=params)
    if response.ok:
        response = response.json()
        # response_code is a parameter received by some of the requests. It is used to check the the response
        # For more information, see opentb documentation: https://opentdb.com/api_config.php
        if "response_code" not in response.keys() or response["response_code"] == 0:
            return response
        raise requests.RequestException(
            f'Failed to get data from {API_REQUESTS_URL}. response code: {response["response_code"]}')
    else:
        raise requests.RequestException(
            f'Failed to get data from {API_REQUESTS_URL}. Status code: {response.status_code}. Reason: {response.reason}')


def get_trivia_question(category_number):
    params = vars(OpenTDBParams(1, 'multiple', category_number))
    response = _extract_response(API_REQUESTS_URL, params)
    return [TriviaQuestion(result) for result in response['results']][0]


def get_trivia_categories(categories_number):
    all_possible_categories = _extract_response(CATEGORY_URL)["trivia_categories"]
    chosen_indices = random.sample(range(min(len(all_possible_categories), categories_number)), categories_number)
    categories = [all_possible_categories[i] for i in chosen_indices]
    return categories
