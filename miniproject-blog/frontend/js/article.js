document.addEventListener('DOMContentLoaded', () => {
    const articleTitleElement = document.getElementById('article-title');
    const articleContentElement = document.getElementById('article-content');
    const articleAuthorElement = document.getElementById('article-author');
    const articleDateElement = document.getElementById('article-date');

    const params = new URLSearchParams(window.location.search);
    const articleSlug = params.get('slug');

    const apiUrl = `/api/articles/${articleSlug}`;

    if (articleSlug) {
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    if (response.status === 404) {
                        throw new Error('Статтю не знайдено.');
                    }
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(article => {
                document.title = article.title;
                articleTitleElement.textContent = article.title;
                articleContentElement.textContent = article.content;
                articleAuthorElement.textContent = `Автор: ${article.author}`;
                articleDateElement.textContent = `Дата публікації: ${article.date}`;
            })
            .catch(error => {
                console.error('Помилка завантаження статті:', error);
                articleTitleElement.textContent = 'Помилка';
                articleContentElement.innerHTML = `<p>Не вдалося завантажити статтю. ${error.message}</p>`;
            });
    } else {
        articleTitleElement.textContent = 'Стаття не вибрана';
        articleContentElement.innerHTML = '<p>Будь ласка, поверніться на головну та оберіть статтю.</p>';
    }
});
