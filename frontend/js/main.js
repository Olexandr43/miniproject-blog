document.addEventListener('DOMContentLoaded', () => {
    const articlesList = document.getElementById('articles-list');
    const apiUrl = '/api/articles';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(articles => {
            if (articles.length === 0) {
                articlesList.innerHTML = '<p>Наразі статей немає.</p>';
                return;
            }
            articlesList.innerHTML = '';
            articles.forEach(article => {
                const articleElement = document.createElement('div');
                articleElement.classList.add('article-item');
                articleElement.innerHTML = `
                    <h3><a href="article.html?slug=${article.slug}">${article.title}</a></h3>
                    <p>Автор: ${article.author} | Дата: ${article.date}</p>
                `;
                articlesList.appendChild(articleElement);
            });
        })
        .catch(error => {
            console.error('Помилка завантаження статей:', error);
            articlesList.innerHTML = `<p>Не вдалося завантажити статті. Перевірте консоль для деталей. ${error.message}</p>`;
        });
});

document.getElementById('article-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const title = document.getElementById('article-title').value;
    const content = document.getElementById('article-content').value;

    const newArticle = {
        id: Date.now(),  // Генерація ID на основі часу
        title: title,
        slug: title.toLowerCase().replace(/ /g, '-'),  // Генерація slug
        content: content,
        author: "Автор 1",  // Можна змінити на реального автора
        date: new Date().toISOString().split('T')[0]  // Сьогоднішня дата
    };

    fetch('/api/articles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newArticle)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Стаття додана:', data);
            // Оновіть список статей або виконайте інші дії
        })
        .catch(error => {
            console.error('Помилка:', error);
        });
});
