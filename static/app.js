class Boggle {
  constructor (boardId, seconds = 60) {
    this.board = $('#' + boardId);
    this.words = new Set();
    this.score = 0;
    this.seconds = seconds;
    this.timer = setInterval(this.tick.bind(this), 1000);
    this.guesses = []

    $('.submit-word').on('submit', this.handleSubmit.bind(this));
  }

  /* Display word in board */
  displayWord (word) {
    $('.words', this.board).append($('<li>', { text: word }).addClass('list-group-item'));

  }

  /* show a status message */

  displayMsg (msg) {
    $('.msg', this.board).text(msg)
  }

  displayScore (word) {
    let scored = word.length
    this.score += scored
    $('.score', this.board).text(this.score);
  }

  async handleSubmit (e) {
    e.preventDefault();

    const $word = $('.word', this.board);
    let word = $word.val().toLowerCase();

    if (!word) return;

    if (this.guesses.includes(word)) {
      this.displayMsg(`${word} already exist, please try another.`);
      return;
    }

    const resp = await axios.get('/word-check', { params: { word: word } });

    if (resp.data.result === 'not-word') {
      this.displayMsg(`${word} is not valid`);
    } else if (resp.data.result === 'not-on-board') {
      this.displayMsg(`${word} is not on this board`);
    } else {
      this.guesses.push(word);
      this.displayWord(word);
      this.displayMsg(`Added: ${word}`);
      this.displayScore(word);
    }
    $word.val('');
  }

  displayTimer () {
    $('.timer', this.board).text(this.seconds);
  }

  /* Tick: handle a second passing in board */

  async tick () {
    this.seconds -= 1;
    this.displayTimer();

    if (this.seconds === 0) {
      clearInterval(this.timer);
      await this.scoreboard();
    }
  }

  /* end of board: score and update message. */

  async scoreboard () {
    $('.submit-word', this.board).hide();
    const resp = await axios.post('/post-score', { score: this.score });
    if (resp.data.brokeRecord) {
      this.displayMsg(`New record: ${this.score}`, 'ok');
    } else {
      this.displayMsg(`Final score: ${this.score}`, 'ok');
    }
  }

}

