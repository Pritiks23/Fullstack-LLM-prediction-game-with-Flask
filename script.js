let words = []
let breakpoints = []
let currentWord = 0
let scoreSum = 0
let currentGuessIndex = 0

let gameStarted = false;
let guessHistory = [];

async function startGame() {
  const res = await fetch("/game")
  const data = await res.json()

  document.getElementById("llm-model").textContent = data.prompt.llm
  document.getElementById("system-prompt").textContent = data.prompt.system_prompt
  document.getElementById("user-question").textContent = data.prompt.user_question

  words = data.words
  breakpoints = data.breakpoints
  showNextWord()
}

function showNextWord() {
  const responseDiv = document.getElementById("response")
  const guessBlock = document.getElementById("guess-block")

  if (currentWord >= words.length) {
    guessBlock.classList.add("hidden")
    document.getElementById("result").classList.remove("hidden")
    document.getElementById("final-score").textContent = scoreSum
    return
  }

  if (breakpoints.includes(currentWord)) {
    guessBlock.classList.remove("hidden")
    document.getElementById("guess-input").value = ""
    return
  }

  const span = document.createElement("span")
  span.textContent = words[currentWord]
  responseDiv.appendChild(span)
  currentWord++
  setTimeout(showNextWord, 600)
}

document.getElementById("submit-guess").addEventListener("click", async () => {
  const guess = document.getElementById("guess-input").value.trim();
  const correct = words[currentWord];

  if (!guess) return;

  const res = await fetch("/submit_guess", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ guess, correct })
  });

  const data = await res.json();
  scoreSum += Math.round(data.score);

  guessHistory.push({ guess, correct, score: data.score });
  updateGuessTable(guess, correct, Math.round(data.score));

  const span = document.createElement("span");
  span.textContent = correct;
  span.style.fontWeight = "bold";
  document.getElementById("response").appendChild(span);

  document.getElementById("guess-block").classList.add("hidden");
  currentWord++;
  setTimeout(showNextWord, 600);
});



function updateGuessTable(guess, correct, score) {
  const table = document.getElementById("guess-table");
  const tbody = table.querySelector("tbody");
  const row = document.createElement("tr");

  const guessCell = document.createElement("td");
  guessCell.textContent = guess;

  const correctCell = document.createElement("td");
  correctCell.textContent = correct;

  const scoreCell = document.createElement("td");
  scoreCell.textContent = score.toString();

  row.appendChild(guessCell);
  row.appendChild(correctCell);
  row.appendChild(scoreCell);

  tbody.appendChild(row);
  table.classList.remove("hidden");
}


document.getElementById("submit-score").addEventListener("click", async () => {
  const name = document.getElementById("name-input").value.trim()
  if (!name) return

  await fetch("/submit_score", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, score: scoreSum })
  })

  const res = await fetch("/leaderboard")
  // TODO: Parse the JSON response to get the leaderboard data
  
  // TODO: Get the score-list element where leaderboard entries will be displayed
  
  // TODO: Clear any existing entries from the list
  
  // TODO: Loop through each score in the data.scores array
  // For each score, create a list item with the player's name and score
  // and append it to the score list
  
  // TODO: Make the leaderboard visible by removing the "hidden" class
})


document.getElementById("start-button").addEventListener("click", () => {
  if (!gameStarted) {
    gameStarted = true;
    document.getElementById("start-block").classList.add("hidden");
    document.getElementById("info").classList.remove("hidden")
    startGame();
  }
});
