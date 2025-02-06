let round = 1, score1 = 0, score2 = 0, choices = { player1: null, player2: null };

function getRandomChoice() {
    return ['✊', '✋', '✌'][Math.floor(Math.random() * 3)];
}

function playRound(player) {
    choices[player] = getRandomChoice();
    const choiceElement = document.getElementById(player === "player1" ? "choice1" : "choice2");
    choiceElement.textContent = choices[player];
    choiceElement.classList.add('animated');

    setTimeout(() => choiceElement.classList.remove('animated'), 500);

    if (choices.player1 && choices.player2) {
        setTimeout(determineRoundWinner, 1000);
    }
}

function determineRoundWinner() {
    const [p1, p2] = [choices.player1, choices.player2];
    let result = "It's a tie!";
    
    if ((p1 === '✊' && p2 === '✌') || (p1 === '✋' && p2 === '✊') || (p1 === '✌' && p2 === '✋')) {
        result = "{{ player1 }} wins this round!";
        score1++;
    } else if (p1 !== p2) {
        result = "{{ player2 }} wins this round!";
        score2++;
    }

    updateScores();
    showRoundWinner(result);

    if (++round > 5) {
        setTimeout(showFinalWinner, 2000); // Show final winner after a delay
    } else {
        setTimeout(resetRound, 1000); // Continue to next round
    }
}

function showRoundWinner(message) {
    document.getElementById("resultText").textContent = message;
    document.getElementById("overlay").style.display = "block";
    document.getElementById("resultModal").style.display = "block";

    setTimeout(() => {
        document.getElementById("overlay").style.display = "none";
        document.getElementById("resultModal").style.display = "none";
    }, 1000);
}

function updateScores() {
    document.getElementById('score1').textContent = score1;
    document.getElementById('score2').textContent = score2;
    document.getElementById('round').textContent = round;
}

function resetRound() {
    choices = { player1: null, player2: null };
    document.getElementById("choice1").textContent = "❔";
    document.getElementById("choice2").textContent = "❔";
}

function showFinalWinner() {
    let winnerMsg = score1 === score2 ? "It's a tie!" : (score1 > score2 ? "{{ player1 }} Wins the Game!" : "{{ player2 }} Wins the Game!");
    document.getElementById("winnerText").textContent = winnerMsg;
    document.getElementById("overlay").style.display = "block";
    document.getElementById("winnerModal").style.display = "block";

    // Auto-restart the game after 5 seconds
    setTimeout(restartGame, 5000);
}

function restartGame() {
    location.reload();
}