from flask import request
import random

def paginate_questions(request, selection, qPerPage):
    page = request.args.get('page', type=int)

    start = (page - 1) * qPerPage
    end = start + qPerPage

    questions = []

    for question in selection:
        questions.append(question.format())
        
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
