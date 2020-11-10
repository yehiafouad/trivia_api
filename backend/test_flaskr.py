import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # A sample new question for testing
        self.newQuestion = {
            'question': "what's your favorite author?",
            'answer': "Shakespear",
            'difficulty': 3,
            'category': 3
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Test get questions
    def test_get_questions(self):
        # Get questions response
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # Check the response data
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])

    # Test delete question
    def test_delete_question(self):
        # Create a new question for testing
        newQ = Question(
            question=self.newQuestion['question'],
            answer=self.newQuestion['answer'],
            category=self.newQuestion['category'], 
            difficulty=self.newQuestion['difficulty']
            )

        # Insert question
        newQ.insert()

        # Delete question response
        res = self.client().delete(f'/questions/{newQ.id}')
        data = json.loads(res.data)

        # check response data
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deletedQ'], newQ.id)

    # Test create new question
    def test_create_new_question(self):
        # Create question response
        res = self.client().post('/questions', json=self.newQuestion)
        data = json.loads(res.data)

        # Check response data
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Test search questions
    def test_search_questions(self):
        # search field response
        response = self.client().post('/searchQuestions', json={'searchTerm': 'title'})
        data = json.loads(response.data)

        # Check response data
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

<<<<<<< HEAD
=======
    def test_get_quizzes(self):
        res = self.client().post('/quizes', json={'previous_question': [16, 17], 'quiz_category': {'type': 'Geography', 'id': '3'}})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

>>>>>>> fb8f3040269a891bfff630340bad0e446f69fa89





    

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()