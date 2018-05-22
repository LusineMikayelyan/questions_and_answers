from django.contrib.auth.decorators import login_required

from django.shortcuts import render, HttpResponse
from django.views.generic import View

from . import forms
from . import helpers

import operator


@login_required
def index(request, *args, **kwargs):
    """
    Return the question, the right answers and the score
    :param request: The request object
    :param args:
    :param kwargs: Kwargs may contain arguments from other redirected views
    :return: render to Questions and Answers dashboard
    """
    db_empty = kwargs.get('db_empty', False)

    if db_empty:
        return HttpResponse("No records yet! Please contact with administration.")

    q_next = kwargs.get('q_next', False)
    msg = kwargs.get('msg', False)
    correct_answers = kwargs.get('correct', False)
    finish = kwargs.get('finish', False)
    question_form = False
    answers = False

    if not finish:
        curr_username = request.user.username
        session_obj = helpers.get_pickle('/task/session' + curr_username + '.pkl')
        q_id = helpers.get_pickle('/task/question_id' + curr_username + '.pkl')

        question_form = forms.QuestionForm(initial={'question_field': session_obj[q_id]['question']})
        answers = [answer['answer'] for answer in session_obj[q_id]['answers']]

    return render(request, 'qanda_app/dashboard.html', {'question_form': question_form,
                                                        'answers': answers,
                                                        'q_next': q_next,
                                                        'msg': msg,
                                                        'finish': finish,
                                                        'correct_answers': correct_answers})


def start_questionnaire(request, *args, **kwargs):
    """
    Load pickle files, check if DB is not empty, redirect to index
    :param request:
    :param args:
    :param kwargs:
    :return: redirect to index view
    """
    session_obj = helpers.create_sassion_obj()
    question_keys = list(session_obj.keys())
    db_empty = True

    if question_keys:
        db_empty = False
        curr_username = request.user.username
        helpers.save_as_a_pickle(session_obj, '/task/session' + curr_username + '.pkl')
        helpers.save_as_a_pickle(question_keys[0], '/task/question_id' + curr_username + '.pkl')
        helpers.save_as_a_pickle(0, '/task/score' + curr_username + '.pkl')

    kwargs = {'db_empty': db_empty}
    return index(request, **kwargs)


def next_question(request, *args, **kwargs):
    """
    Load pickle files, get next question, on finish- update score for that user, redirect to index
    :param request:
    :param args:
    :param kwargs:
    :return: redirect to the index
    """
    curr_username = request.user.username
    session_obj = helpers.get_pickle('/task/session' + curr_username + '.pkl')
    q_id = helpers.get_pickle('/task/question_id' + curr_username + '.pkl')
    score = helpers.get_pickle('/task/score' + curr_username + '.pkl')
    users_results = helpers.get_pickle('/task/users_results.pkl')
    questions = list(session_obj.keys())

    if questions.index(q_id) == len(questions) - 1:
        msg = "Congratulations!! You have finished your questionnaire and your score is: " + \
              str(score)

        user_in_pickle = users_results.get(curr_username, None)

        if not user_in_pickle:
            users_results[curr_username] = score
        else:
            if score > users_results[curr_username]:
                users_results[curr_username] = score

        helpers.save_as_a_pickle(users_results, '/task/users_results.pkl')
        helpers.remove_files('/task/session' + curr_username + '.pkl',
                             '/task/question_id' + curr_username + '.pkl',
                             '/task/score' + curr_username + '.pkl')

        kwargs = {'msg': msg, 'finish': True}
        return index(request, **kwargs)

    q_id = questions.index(q_id) + 1
    helpers.save_as_a_pickle(questions[q_id], '/task/question_id' + curr_username + '.pkl')
    return index(request)


def check_answer(request, *args, **kwargs):
    """
    Load pickle files, check answer, update current score, redirect to index
    :param request:
    :param args:
    :param kwargs:
    :return: redirect to the index
    """
    curr_username = request.user.username
    req = kwargs.get('req')
    session_obj = helpers.get_pickle('/task/session' + curr_username + '.pkl')
    q_id = helpers.get_pickle('/task/question_id' + curr_username + '.pkl')
    score = helpers.get_pickle('/task/score' + curr_username + '.pkl')
    db_answers = session_obj[q_id]['answers']

    i = 0
    correct_answers = []

    if not req.getlist('checks'):
        msg = "Please select at least one answer"
        kwargs = {"msg": msg}

    else:

        for answer in req.getlist('checks'):      # user's selected answers
            for db_answer_obj in db_answers:
                if answer == db_answer_obj['answer'] and db_answer_obj['correct']:
                    i += 1

                # We need to collect correct answers as well
                if db_answer_obj['correct'] and db_answer_obj['answer'] not in correct_answers:
                    correct_answers.append(db_answer_obj['answer'])

        if i == len(correct_answers):
            score += session_obj[q_id]['complexity']
            msg = "You are correct. Go Ahead!"
            helpers.save_as_a_pickle(score, '/task/score' + curr_username + '.pkl')
            kwargs = {'msg': msg, 'q_next': True}
        else:
            msg = "Sorry. You are incorrect! Please see below the correct ones"
            kwargs = {'msg': msg, 'q_next': True, 'correct': correct_answers}

    return index(request, **kwargs)


class ActionView(View):
    """
    Simple view to redirect
    """
    def post(self, request, *args, **kwargs):
        kwargs = {'req': request.POST}

        if 'check' in request.POST:
            return check_answer(request, **kwargs)

        elif 'next' in request.POST:
            return next_question(request, **kwargs)

        return HttpResponse("Sorry! Bad query")


@login_required
def best_results(request, *args, **kwargs):
    """
    Load user_results pickle, render to the Best Results page
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    users_results = helpers.get_pickle('/task/users_results.pkl')
    result = sorted(users_results.items(), key=operator.itemgetter(1))

    return render(request, 'qanda_app/best_results_dashboard.html', {'result': result[:10]})
