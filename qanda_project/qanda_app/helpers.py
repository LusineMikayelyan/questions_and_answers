from . import access_db

import os
import pickle
from collections import OrderedDict


def create_sassion_obj():
    """
    Get questions , create session object from selected questions and store all information
    :return:
    """
    questions = access_db.get_questions()    # default limit is 5
    session_obj = OrderedDict()

    for question in questions:
        id = question.__dict__['id']   # get the unique id
        session_obj[id] = {'question': question.__dict__['question'],
                           'complexity': question.__dict__['complexity']}

        answers = access_db.get_answers_related_to_question(question)

        answers_obj_list = []
        for answer in answers:
            answer_obj = {'id': answer.__dict__['id'], 'answer': answer.__dict__['answer'],
                          'correct': answer.__dict__['correct']}

            answers_obj_list.append(answer_obj)

        session_obj[id]['answers'] = answers_obj_list

    return session_obj


def save_as_a_pickle(obj, obj_path):
    with open(obj_path, 'wb') as f:
        pickle.dump(obj, f)


def get_pickle(obj_path):
    with open(obj_path, 'rb') as f:
        return pickle.load(f)


def remove_files(*args):
    for file_ in args:
        os.remove(file_)
