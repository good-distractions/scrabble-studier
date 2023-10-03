var flashcardEl = document.getElementById("flashcards");
var mainEl = document.createElement("main");
var mainTitleEl = document.createElement("h1");
mainTitleEl.id = "main-title";
// var wordList = JSON.parse({{my_data|safe}});
var timeBetween = 2;




// initialize page function
var initializePage = function () {
    // reset word array and word num
    wordList = [];
    wordNum = 0;
    // load questions in question array
    generateWordArray();
    // initialize interval todo: based user input
    // initialize instructions and start flashcards elements
    var introEl = document.createElement("div");
    introEl.id = "intro-content";
    mainTitleEl.textContent = "Scrabble Flashcards";
    var introInstructionsEl = document.createElement("p");
    introInstructionsEl.id = "instructions";
    introInstructionsEl.textContent =
      "You will be shown the words from the selected dictionary. Each word will remain on screen for 3 seconds";
    var startFlashcardsEl = document.createElement("button");
    startFlashcardsEl.id = "start-flashcards";
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

// load cards function
var generateWordArray = function (){
    // wordList.push('hello','world','goodbye','again')
}

// start cards function

var startFlashcardsHandler = function (){
    // remove instructions text & start flashcards button
    document.querySelector("#instructions").remove();
    document.querySelector("#start-flashcards").remove();
    // call display first word
    displayWords();
}

// https://www.geeksforgeeks.org/how-to-delay-a-loop-in-javascript-using-async-await-with-promise/
function intervalLoop(millisec) {
  return new Promise(resolve => {
      setTimeout(() => { resolve('') }, millisec);
  })
}

async function displayWords() {
  for (var i = wordNum; i < wordList.length; i++){
      await intervalLoop(timeBetween*1000);
      var currentWord = wordList[i];
      mainTitleEl.textContent = currentWord;
  }
}


// pause cards function

// resume cards function

// end cards function
// var endFlashcards = function () {
//     initializePage()
//   };


// initialize page
initializePage();