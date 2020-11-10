from flask import request
import random

def paginate_questions(request, selection, qPerPage):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * qPerPage
    end = start + qPerPage

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def random_Qs(questions):
    return questions[random.randrange(0, len(questions), 1)]

def detect_isUsed(question, prev): 
    isUsed = False

    for pq in prev:
        if pq == question.id:
            isUsed = True
    return isUsed
