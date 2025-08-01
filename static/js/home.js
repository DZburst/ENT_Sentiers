document.addEventListener('DOMContentLoaded', () => {
    let currentIndex = 0;
    let newsItems = [];

    // Fetch News from Flask Endpoint
    fetch('/read_news')
        .then(response => response.json())
        .then(news => {
            if (news.length > 0) {
                newsItems = news;
                displayItem(currentIndex);
                generateIndicators();
                setupArrowListeners();
            } else {
                console.log('No news in the database...');
            }
        })
        .catch(error => console.error('Error fetching news:', error));

    // Display News Items
    function displayItem(index) {
        const item = newsItems[index];
        const newsContainer = document.querySelector('.news-items');
        
        newsContainer.innerHTML = `
            <span class="arrow left-arrow">◄</span>
            <div class="news-item">
                <h3>${item._title}</h3>
                <img src="${item._image_url}" alt="${item._title}">
                <p>${item._content || ''}</p>
            </div>
            <span class="arrow right-arrow">►</span>
        `;

        setupArrowListeners();
        updateActiveIndicator();
        setupImageZoom();
    }

    function setupArrowListeners() {
        document.querySelector('.left-arrow').onclick = () => {
            currentIndex = (currentIndex - 1 + newsItems.length) % newsItems.length;
            displayItem(currentIndex);
        };

        document.querySelector('.right-arrow').onclick = () => {
            currentIndex = (currentIndex + 1) % newsItems.length;
            displayItem(currentIndex);
        };
    }

    function generateIndicators() {
        const newsIndicators = document.querySelector('.news-indicators');
        newsIndicators.innerHTML = '';

        newsItems.forEach((_, index) => {
            const indicator = document.createElement('span');
            indicator.classList.add('indicator');
            if (index === currentIndex) {
                indicator.classList.add('active');
            }
            newsIndicators.appendChild(indicator);
        })
    }

    function updateActiveIndicator() {
        const indicators = document.querySelectorAll('.indicator');

        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
        });
    }

    function setupImageZoom() {
        const newsImage = document.querySelector('.news-item img');
        if (newsImage) {
            newsImage.onclick = () => {
                openImageOverlay(newsImage.src);
            }
        }
    }

    function openImageOverlay(src) {
        const overlay = document.getElementById('image-overlay');
        const overlayImg = overlay.querySelector('.overlay-img');
        overlayImg.src = src;
        overlay.style.display = 'flex';
    }

    document.querySelector('.close-btn').onclick = () => {
        document.getElementById('image-overlay').style.display = 'none';
    };

});