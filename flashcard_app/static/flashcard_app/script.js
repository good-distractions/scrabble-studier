var flashcardEl = document.getElementById("flashcards");
var mainEl = document.createElement("main");
var mainTitleEl = document.createElement("h1");
mainTitleEl.id = "main-title";
var isPaused = false;
var endCards = true;
var wordNum = 0;

// initialize page function
var initializePage = function () {
  isPaused = false;
  endCards = true;
  wordNum = 0;
  // initialize interval todo: based user input
  // initialize instructions and start flashcards elements
  var introEl = document.createElement("div");
  introEl.id = "intro-content";
  mainTitleEl.textContent = "";
  var introInstructionsEl = document.createElement("p");
  introInstructionsEl.id = "instructions";
  introInstructionsEl.textContent =
    "You will be shown the words from the selected dictionary. Each word will remain on screen for 3 seconds.";
  var startFlashcardsEl = document.createElement("button");
  startFlashcardsEl.id = "start-flashcards";
  startFlashcardsEl.className = "btn";
  startFlashcardsEl.textContent = "Start Flashcards";
  startFlashcardsEl.addEventListener("click", startFlashcardsHandler);
  // append instructions, start quiz and title to main
  introEl.append(mainTitleEl);
  introEl.append(introInstructionsEl);
  introEl.append(startFlashcardsEl);
  // append intro elements to main
  mainEl.append(introEl);
  // append main to body
  flashcardEl.append(mainEl);
};

// start cards function

var startFlashcardsHandler = function () {
  endCards = false;
  // remove instructions text & start flashcards button
  document.querySelector("#instructions").remove();
  document.querySelector("#start-flashcards").remove();
  var pauseFlashcardsEl = document.createElement("button");
  pauseFlashcardsEl.id = "pause-flashcards";
  pauseFlashcardsEl.className = "btn";
  pauseFlashcardsEl.textContent = "Pause";
  pauseFlashcardsEl.addEventListener("click", pauseFlashcardsHandler);
  mainEl.append(pauseFlashcardsEl);
  // display first word
  mainTitleEl.textContent = wordList[wordNum];
  wordNum++;
  // loop through words
  displayWords();
};

// https://www.geeksforgeeks.org/how-to-delay-a-loop-in-javascript-using-async-await-with-promise/
function intervalLoop(millisec) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("");
    }, millisec);
  });
}

async function displayWords() {
  for (var i = wordNum; (i < wordList.length) & !isPaused & !endCards; i++) {
    var currentWord = wordList[i];
    await intervalLoop(timeBetween * 1000);
    // var currentWord = wordList[i];
    mainTitleEl.textContent = currentWord;
    wordNum++;
  }
  if (document.querySelector("#pause-flashcards")) {
    document.querySelector("#pause-flashcards").remove();
  }

  if (document.querySelector("#end-flashcards")) {
    document.querySelector("#end-flashcards").remove();
  }
  if (wordNum == wordList.length) {
    initializePage();
  }
}

// pause cards function
var pauseFlashcardsHandler = function () {
  isPaused = true;
  document.querySelector("#pause-flashcards").remove();
  var resumeFlashcardsEl = document.createElement("button");
  resumeFlashcardsEl.id = "resume-flashcards";
  resumeFlashcardsEl.textContent = "Resume";
  resumeFlashcardsEl.className = "btn";
  resumeFlashcardsEl.addEventListener("click", resumeFlashcardsHandler);
  mainEl.append(resumeFlashcardsEl);
};

// resume cards function
var resumeFlashcardsHandler = function () {
  document.querySelector("#resume-flashcards").remove();
  isPaused = false;
  var pauseFlashcardsEl = document.createElement("button");
  pauseFlashcardsEl.id = "pause-flashcards";
  pauseFlashcardsEl.textContent = "Pause";
  pauseFlashcardsEl.className = "btn";
  pauseFlashcardsEl.addEventListener("click", pauseFlashcardsHandler);
  mainEl.append(pauseFlashcardsEl);
  displayWords();
};

// end cards function
// update to redirect to dictionary page
var endFlashcardsHandler = function () {
  endCards = true;
  if (document.querySelector("#pause-flashcards")) {
    document.querySelector("#pause-flashcards").remove();
  }
  if (document.querySelector("#resume-flashcards")) {
    document.querySelector("#resume-flashcards").remove();
  }
  if (document.querySelector("#end-flashcards")) {
    document.querySelector("#end-flashcards").remove();
  }

  initializePage();
};

// initialize page
initializePage();
