from flask import request

def paginate_questions(request, selection, qPerPage):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * qPerPage
    end = start + qPerPage

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions