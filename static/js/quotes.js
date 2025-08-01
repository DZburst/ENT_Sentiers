async function fetchQuotes() {
    const response = await fetch('/static/resources/quotes.json');
    const data = await response.json();
    return data;
}

async function displayRandomQuote() {
    const quotesData = await fetchQuotes();
    
    let allQuotes = [];
    quotesData.forEach(category => {
        allQuotes = allQuotes.concat(category.entries);
    });

    const randomIndex = Math.floor(Math.random() * allQuotes.length);
    const randomQuote = allQuotes[randomIndex];

    const quoteBlock = document.querySelector('#quote-block');
    if (quoteBlock) {
        quoteBlock.innerHTML = `
            <p class="quote" style="font-style: italic;">${randomQuote.text}</p>
            <p class="source"><strong>Source :</strong> ${randomQuote.source}</p>
        `;
    }
}

document.addEventListener('DOMContentLoaded', displayRandomQuote);