let secretNumber = 0;
let attempts = 0;

const messageEl = document.getElementById('message');
const attemptsEl = document.getElementById('attempts');
const formEl = document.getElementById('guess-form');
const inputEl = document.getElementById('guess-input');
const restartBtn = document.getElementById('restart-btn');

function startGame() {
  secretNumber = Math.floor(Math.random() * 100) + 1;
  attempts = 0;
  attemptsEl.textContent = attempts;
  messageEl.textContent = '새 게임이 시작되었습니다. 숫자를 입력해 주세요.';
  inputEl.value = '';
  inputEl.focus();
}

function checkGuess(guess) {
  attempts += 1;
  attemptsEl.textContent = attempts;

  if (guess < secretNumber) {
    messageEl.textContent = '업! 더 큰 숫자입니다.';
  } else if (guess > secretNumber) {
    messageEl.textContent = '다운! 더 작은 숫자입니다.';
  } else {
    messageEl.textContent = `정답입니다! ${attempts}번 만에 맞추셨습니다.`;
    inputEl.disabled = true;
    inputEl.blur();
  }
}

formEl.addEventListener('submit', (event) => {
  event.preventDefault();

  const guess = Number(inputEl.value);
  if (!Number.isInteger(guess) || guess < 1 || guess > 100) {
    messageEl.textContent = '1부터 100 사이의 숫자를 입력해 주세요.';
    return;
  }

  checkGuess(guess);
  inputEl.value = '';
});

restartBtn.addEventListener('click', () => {
  inputEl.disabled = false;
  startGame();
});

startGame();
