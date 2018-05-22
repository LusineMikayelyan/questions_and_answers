from . import models

import random


def get_questions(limit=5):
    """
    Get random, unique records from Question model database
    :param limit: The count of result records
    :return: result_set
    """
    count = models.Question.objects.all().count()
    result_set = set()

    if count < limit:   # there are not enough records
        return result_set

    try:
        while len(result_set) != limit:
            random_id = random.sample(range(0, count), 1)  # generate random id

            if models.Question.objects.filter(pk=random_id[0]).exists():  # check is there question object with that id
                result_set.add(models.Question.objects.get(pk=random_id[0]))

        return result_set

    except ValueError:
        return []


def get_answers_related_to_question(quesion_obj):
    return quesion_obj.answer_set.all()

