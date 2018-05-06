document.getElementById("btnAnswer").addEventListener("click", checkAnswer);
function checkAnswer() {
    var userGuesses = document.getElementById("answer").value;

    document.getElementById("answer").value = "";//resets the answer for further answers
    document.getElementById("incorrectA").style.color = 'red';
    var myNotice = "<strong>Wrong Guesses:</strong>";
    var points;

    if (!compareAnswers(userGuesses, document.getElementById("user_received_answer").value)) {
        myNotice = "<strong>Correct!</strong>:<br />";
        document.getElementById("incorrectA").style.color = 'green';
        document.getElementById("incorrectA").innerHTML = myNotice;
        // document.getElementById("formAnswers").submit()
        points = parseInt(document.getElementById("points").innerHTML, 10);
        autoLogIn((points));

    } else {
        var attempts = parseInt(document.getElementById("attempts").value, 10);
        attempts += 1;
        document.getElementById("answerAttempts").innerHTML = "Answer Attempts: " + attempts;
        document.getElementById("attempts").value = attempts;        
        document.getElementById("incorrectA").innerHTML = myNotice;
        appendGuesses(userGuesses);
        document.getElementById("pointsMes").innerHTML = "POINTS LEFT:";
        points = parseInt(document.getElementById("points").innerHTML, 10);
        document.getElementById("points").innerHTML = (points - 1);
        if((attempts) == 8){
            window.location.reload();
        }
    }
    
}

function compareAnswers(userAnswer, gameAnswer) {
    // Used to compare the user answer and the game answer;
    return userAnswer.toLowerCase().localeCompare(gameAnswer.toLowerCase());
}
function appendGuesses(guess) {
    var node = document.createElement("LI");
    var textnode = document.createTextNode(guess);
    node.appendChild(textnode);
    document.getElementById("guessed").appendChild(node);
}

function autoLogIn(points) {
    var form = document.createElement("form");
    var userName = document.createElement("input");
    var questionId = document.createElement("input");
    var pointsReceived = document.createElement("input");
    var team_name = document.createElement("input");
    var players = document.createElement("input");
    var noPlayers = document.createElement("input");
    var reg_players = document.createElement("input");
    
    form.method = "POST";
    form.action = "/index/";

    questionId.setAttribute("type", "hidden");
    questionId.value = document.getElementById("user_received_question").value;
    questionId.name = "questionId";
    form.appendChild(questionId);


    noPlayers.setAttribute("type", "hidden");
    noPlayers.name = "noPlayers";
    noPlayers.value = document.getElementById("noPlayers").value;
    form.appendChild(noPlayers);
    
    userName.setAttribute("type", "hidden");
    userName.name = "userName";
    userName.value = document.getElementById("this_user").value;
    form.appendChild(userName);
    
    players.setAttribute("type", "hidden");
    players.name = "players";
    players.value = document.getElementById("players").value;
    form.appendChild(players);
    
    reg_players.setAttribute("type", "hidden");
    reg_players.name = "reg_players";
    reg_players.value = document.getElementById("reg_players").value;
    form.appendChild(reg_players);    
    

    team_name.setAttribute("type", "hidden");
    team_name.name = "team_name";
    team_name.value = document.getElementById("team_name").value;
    form.appendChild(team_name);    
 
    pointsReceived.setAttribute("type", "hidden");
    pointsReceived.name = "pointsReceived";
    pointsReceived.value = points;
    form.appendChild(pointsReceived);

    document.body.appendChild(form);
    form.submit();

}

document.getElementById("endSession").addEventListener("click", submitEndSessionRequest);
function submitEndSessionRequest(){
    var form = document.createElement("form");
    var userName = document.createElement("input");
    var team_name = document.createElement("input");
    
    form.method = "POST";
    form.action = "/end_session";

    team_name.setAttribute("type", "hidden");
    team_name.name = "team_name";
    team_name.value = document.getElementById("team_name").value;
    form.appendChild(team_name);   

    userName.setAttribute("type", "hidden");
    userName.name = "userName";
    userName.value = document.getElementById("this_user").value;
    form.appendChild(userName);
    
    document.getElementById("endSession").style.color = "red";

    document.body.appendChild(form);
    form.submit();  
}
window.onload = function() {
  document.getElementById("answer").focus();
};