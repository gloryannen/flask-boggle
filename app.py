from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)

BOGGLE = Boggle()
scores = []


@app.route('/')
def home():
    """Boggle Game page"""

    board = BOGGLE.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    return render_template('boggle_board.html', board=board, highscore=highscore, nplays=nplays)


@app.route('/word-check')
def word_check():
    """Validate if word is in dictionary"""

    word = request.args['word']
    word = word.lower()
    board = session['board']
    response = BOGGLE.check_valid_word(board, word)

    return jsonify(result=response)


@app.route('/post-score', methods=['POST'])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
