from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):
    """Test that most HTML elements are showing correctly"""

    def test_home(self):
        with self.app.test_client() as client:

            resp = self.client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Play Boggle </h1>', html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('nplays'))

    def test_valid_word(self):
        """Test if word is valid (in dictionary and on board) by modifying the board in the session"""

        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [["B", "O", "A", "R", "D"],
                                 ["O", "A", "R", "D", "B"],
                                 ["A", "R", "D", "B", "O"],
                                 ["R", "D", "B", "O", "A"],
                                 ["D", "B", "O", "A", "R"]
                                 ]

        resp = self.client.get('/word-check?word=board')
        self.assertEqual(resp.json['result'], 'ok')

    def test_invalid_word(self):
        """Test for word in dictionary but not on board"""

        with self.app.test_client() as client:

            with client.session_transaction() as sess:
                sess['board'] = [["B", "O", "A", "R", "D"],
                                 ["O", "A", "R", "D", "B"],
                                 ["A", "R", "D", "B", "O"],
                                 ["R", "D", "B", "O", "A"],
                                 ["D", "B", "O", "A", "R"]
                                 ]

            resp = self.client.get('/word-check?word=boarding')
            self.assertEqual(resp.json['result'], 'not-on-board')

    def not_valid_word(self):
        """Test for word not in dictionary"""

        with self.app.test_client() as client:

            self.client.get('/')
            resp = self.client.get('/word-check?word=rdb')
            self.assertEqual(resp.json['result'], 'not-word')
