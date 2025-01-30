import * as data from '../quotes.json';
const quotes = data;

function displayRandomQuote() {
    // Combine all entries into a single array
    const allQuotes = quotes.flatMap(category => category.entries);
  
    // Select a random quote
    const randomQuote = allQuotes[Math.floor(Math.random() * allQuotes.length)];
  
    // Update the HTML content
    const quoteElement = document.querySelector(".quote");
    quoteElement.innerHTML = `<p>"${randomQuote.text}"</p><p><em>${randomQuote.source}</em></p>`;
}



document.addEventListener("DOMContentLoaded", () => {
    displayRandomQuote();
});