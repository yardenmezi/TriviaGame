# Trivia Game

A simple trivia game in the terminal where you can choose the question number by category and get the question and answer it.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)
- [Acknowledgments](#Acknowledgments)


## Description

This is a simple trivia game that runs in the terminal. You can select a category and choose which question you want to answer by its number. 

The game will retrieve questions from the Open Trivia Database API and display them on the screen. After choosing a question, you will see the question and options for answers. You can select the correct answer by typing its number. The game will display whether your answer is correct or incorrect.

Please note that the categories are randomly selected, so it's possible to have the same category appear more than once during a game session.

##Installation
To use this project and play the trivia game, make sure you have Python version 3.7 or above installed on your machine. 
you can check your Python version by running: ```python --version ```

To get started, clone this project to your local machine, then navigate to the project directory and run the following command to install the required modules:
```pip install -r requirements.txt```

That's it! You should now have everything you need to run this project on your machine.

## Usage

To start the game, run the following command in your terminal:
python main.py
Follow the prompts to select the number of questions you want to answer and the category of the questions.

## Credits

This game uses questions from the [Open Trivia Database API](https://opentdb.com/), which is created and maintained by [PixelTail Games](https://www.pixeltailgames.com/). The questions are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).


## License

This project is licensed under the [MIT License](LICENSE), but please note that the trivia questions used in this game are sourced from the [Open Trivia Database API](https://opentdb.com/), which is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

This means that if you use the trivia questions in your own projects, you must also license your work under the CC BY-SA 4.0 license and give appropriate credit to the Open Trivia Database API as the source of the questions. 

The rest of the code in this project is licensed under the MIT License.

## Acknowledgments

- Thanks to ChatGPT for helping me write this README.md file!
