"""
Project Name: Jeopardy Python Game
Project Author(s): Joseph Lefkovitz (github.com/lefkovitz), Santiago Rached Alvarez (https://github.com/Tw0S41nt)
Last Modified: 7/24/2025

File Purpose: Data manipulation and processing utilities for the application.
"""

import csv

def get_all_category_entries(data_source):
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
            if jeopardy_question_data[3] not in jeopardy_categories and int(jeopardy_question_data[0]) != 3:
                jeopardy_categories.append(jeopardy_question_data[3])
    return jeopardy_categories, len(jeopardy_categories)
        
def get_all_question_entries(data_source):
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
            if int(jeopardy_question_data[0]) !=3:
                question = jeopardy_question_data[5]
                points = jeopardy_question_data[1] 
                answer = jeopardy_question_data[6]
                category = jeopardy_question_data[3]
                question_dict = {"question": question, "answer": answer, "points": points, "category": category}
                jeopardy_questions.append(question_dict)
    return jeopardy_questions, len(jeopardy_questions)
