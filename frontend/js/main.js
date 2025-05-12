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
    const author = document.getElementById('article-author').value;

    const newArticle = {
        id: Date.now(),
        title: title,
        slug: title.toLowerCase().replace(/ /g, '-').replace(/[^a-z0-9-]/g, ''),
        content: content,
        author: author || "Автор 1",
        date: new Date().toISOString().split('T')[0]
    };

    fetch('/api/articles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newArticle)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Стаття додана:', data);
            alert('Ваша стаття успішно додана! Вона з\'явиться для перегляду незабаром.');
            document.getElementById('article-form').reset();
        })
        .catch(error => {
            console.error('Помилка при додаванні статті:', error);
            alert('Виникла помилка при додаванні статті. Спробуйте ще раз або зверніться до адміністратора.');
        });
});

const createFile = async () => {
    const response = await fetch('/api/github/create-file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            repo: 'Olexandr43/miniproject-blog',
            path: 'backend/db.json',
            content: 'Оновлений вміст бази даних'
        })
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data.message);
    } else {
        const error = await response.json();
        console.error('Error:', error);
    }
};
