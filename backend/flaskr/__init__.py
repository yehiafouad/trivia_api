import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
from functions import paginate_questions, random_Qs, detect_isUsed

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app, resources={r'/*': {'origins': '*'}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      response.headers.add('Access-Control-Allow-Origin', '*')
      return response

  @app.route('/categories')
  def get_categories():
    try:
      # get all categories
      categories = Category.query.all()
      categoriesData = {}
      for category in categories:
          categoriesData[category.id] = category.type

      # If no categories, return error
      if (len(categoriesData) == 0):
        return jsonify({'error': True, 'message': 'There are no catergories'})

      # return jsonify data
      return jsonify({
          'success': True,
          'categories': categoriesData
      })
    except:
      abort(404)

  @app.route('/questions')
  def get_questions():
    try:
      # get all questions
      questions = Question.query.all()

      # Calculate the total of questions
      totalQ = len(questions)

      paginateQuestions = paginate_questions(request, questions, QUESTIONS_PER_PAGE)

      # get all categories
      categories = Category.query.all()

      # Empty object for categories and add the type only for each category.
      categoriesData = {}
      for category in categories:
        categoriesData[category.id] = category.type

      # Send error for empty questions
      if (len(paginateQuestions) == 0):
        return jsonify({'error': True, 'message': 'There are no questions found'})

      # return the data as response object
      return jsonify({
            'success': True,
            'questions': paginateQuestions,
            'total_questions': totalQ,
            'categories': categoriesData
      })
    except:
      abort(404)

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      # Get the selected question
      deletedQ = Question.query.filter_by(id=id).one_or_none()

      # Return error is there is not question found with this ID
      if deletedQ is None:
        return jsonify({'error': True, 'message': 'Selected question not found'})

      # Delete the question
      deletedQ.delete()

      # Return success
      return jsonify({'success': True, 'deletedQ': id})
    except:
      # Abort function if there is an error while deleting
      abort(422)

  @app.route('/questions', methods=['POST'])
  def create_new_question():

    # Get the requested fields
    newQuestion = request.get_json().get('question')
    newAnswer = request.get_json().get('answer')
    newDifficulty = request.get_json().get('difficulty')
    newCategory = request.get_json().get('category')

    # Validate all fields
    if (newQuestion is None) or (newAnswer is None) or (newDifficulty is None) or (newCategory is None):
      return jsonify({'error': True, 'message':'Fill the empty fields'})

    print(newQuestion, newAnswer, newDifficulty, newCategory)
    try:
      # Create the new question
      newQ = Question(question=newQuestion, answer=newAnswer, difficulty=newDifficulty, category=newCategory)
      newQ.insert()

      # return the data as response object
      return jsonify({'success': True, 'new_question': newQ.id})
    except:
      abort(422)

  @app.route('/searchQuestions', methods=['POST'])
  def search_questions():
    # Get the search field value
    searchField = request.get_json().get('searchTerm')

    try:
      # Filter questions inside the database as per the search field value
      questions = Question.query.filter(Question.question.ilike(f'%{searchField}%')).all()

      # Check if no questions match
      if (len(questions) == 0):
        return jsonify({'error': True, 'message': 'No results'})
    
      # paginate the results
      paginateQ = paginate_questions(request, questions, QUESTIONS_PER_PAGE)

      # return results
      return jsonify({
        'success': True,
        'questions': paginateQ,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)

  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    try:

      # get the category data by id
      categoryData = Category.query.filter_by(id=id).one()

      # return error if catergory isn't found
      if (categoryData is None):
        return jsonify({'error': True, 'message': 'There is no category found'})

      # get all questions for this category
      questions = Question.query.filter_by(category=str(categoryData.id)).all()

      # paginate questions
      paginateQ = paginate_questions(request, questions, QUESTIONS_PER_PAGE)

      # return results
      return jsonify({
        'success': True,
        'questions': paginateQ,
        'total_questions': len(Question.query.all()),
        'current_category': categoryData.type
      })
    except:
      abort(404)

  @app.route('/quizzes', methods=['POST'])
  def get_quizzes():
    # Get the body fields
    body = request.get_json()
    prev = body.get('previous_questions')
    categoryId = body.get('quiz_category')

    # Return error if previous questions or categories are None
    if (prev is None) or (categoryId is None):
      return jsonify({'error': True, 'message': 'There is no categories or questions found!'})
      
    try:
      # Get all questions for all categories or for selected category
      if categoryId['id'] == 0:
        questions = Question.query.all()
      else:
        questions = Question.query.filter_by(category=str(categoryId['id'])).all()

        # Return random questions
        question = random_Qs(questions)

        # Detect the used questions from previous questions 
        while (detect_isUsed(question, prev)):
          question = random_Qs(questions)

          # Check if previous questions length are equal questions length
          if (len(prev) == len(questions)):
            return jsonify({'success': True})

        return jsonify({'success': True, 'question': question.format()})
    except:
      abort(422)
        
  @app.errorhandler(404)
  def not_found(error):
        return jsonify({'success': False, 'code': 404, 'message': 'resource not found'}), 404

  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({'success': False, 'code': 422, 'message': 'unprocessable'}), 422
  
  return app

    
