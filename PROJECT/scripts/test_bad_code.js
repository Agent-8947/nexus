/**
 * TEST FILE: bad_code.js
 * Purpose: Validate the Adversarial Reviewer's new JS rules.
 */

var globalData = []; // SMELL: var usage

function processItems(items) {
  let i; // SMELL: single letter loop variable
  for (i = 0; i < items.length; i++) {
    console.log("Processing: " + items[i]); // SMELL: console.log leak
    globalData.push(items[i]); // SMELL: side effect on global
  }

  // SMELL: Promise.then instead of async/await
  fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => {
      console.log(data);
    });
}

processItems(['A', 'B', 'C']);
