// Charger les citations depuis le fichier JSON
async function fetchQuotes() {
    const response = await fetch('../quotes.json'); // Charger le fichier JSON
    const data = await response.json(); // Convertir en JSON
    return data;
}

async function displayRandomQuote() {
    const quotesData = await fetchQuotes();
    
    // Récupérer toutes les citations indépendamment des catégories
    let allQuotes = [];
    quotesData.forEach(category => {
        allQuotes = allQuotes.concat(category.entries);
    });

    // Choisir une citation au hasard
    const randomIndex = Math.floor(Math.random() * allQuotes.length);
    const randomQuote = allQuotes[randomIndex];

    // Sélectionner l'élément et y insérer la citation
    document.querySelector('blockquote').innerHTML = `
        <p class="quote" style="font-style: italic;">${randomQuote.text}</p>
        <p class="source"><strong>Source :</strong> ${randomQuote.source}</p>
    `;
}

// Afficher une citation au chargement de la page
displayRandomQuote();
