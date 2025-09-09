"""
Project Name: Jeopardy Python Game
Project Author(s): Joseph Lefkovitz (github.com/lefkovitz), Santiago Rached Alvarez (https://github.com/Tw0S41nt)
Last Modified: 7/24/2025

File Purpose: Data manipulation and processing utilities for the application.
"""

import csv
import random

def get_all_category_entries(data_source, disallowed_rounds=[3]):
    """ Parse the source file and get a list of all unique categories that are not in the Final Jeopardy."""
    # Sanity check.
    assert data_source.endswith(".tsv")

    # Parse the data file of format .tsv. 
    with open(data_source, 'r', encoding="utf-8") as file:
        jeopardy_data = csv.reader(file, delimiter="\t")
        next(jeopardy_data)

        jeopardy_categories = []
        for jeopardy_question_data in jeopardy_data:
            # Select all question categories that are unique and not Final Jeopardy. 
            if jeopardy_question_data[3] not in jeopardy_categories and int(jeopardy_question_data[0]) not in disallowed_rounds:
                jeopardy_categories.append(jeopardy_question_data[3])
    return jeopardy_categories, len(jeopardy_categories)

def get_all_question_entries(data_source, disallowed_rounds=[3]):
    """  Parse the source file and get the questions, points, answers, and categories that are not in the Final Jeopardy."""
    # Sanity check.
    assert data_source.endswith(".tsv")

    # Parse the data file of format .tsv.
    with open(data_source, 'r', encoding="utf-8") as file:
        jeopardy_data = csv.reader(file, delimiter="\t")
        next(jeopardy_data)

        jeopardy_questions = []
        for jeopardy_question_data in jeopardy_data:
            # Select all of the question data for questions not in Final Jeopardy.
            if int(jeopardy_question_data[0]) not in disallowed_rounds:
                question = jeopardy_question_data[5]
                points = jeopardy_question_data[1] 
                answer = jeopardy_question_data[6]
                category = jeopardy_question_data[3]
                round = jeopardy_question_data[0]
                question_dict = {"question": question, "answer": answer, "points": points, "category": category, "round": round}
                jeopardy_questions.append(question_dict)
    return jeopardy_questions, len(jeopardy_questions)

def get_random_game_board(data_source, number_categories=6, disallowed_rounds = [3]):
    """ Build the jeopardy game board with random categories and questions."""

    all_questions, _ = get_all_question_entries(data_source, disallowed_rounds=disallowed_rounds)
    all_categories, _ = get_all_category_entries(data_source, disallowed_rounds=disallowed_rounds)

    board_categories = random.sample(all_categories, number_categories)
    question_list = []

    for category in board_categories:
        question_list.append([])
    for question in all_questions:
        question_category = question["category"]
        if question_category in board_categories:
            category_num = board_categories.index(question_category)
            question_list[category_num].append(question)

    return question_list