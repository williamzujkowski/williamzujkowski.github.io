// assets/js/blogLogic.js

export function initBlogLogic() {

    window.renderIndexBlogHTML = async function (resp) {
        const textData = await resp.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(textData, 'text/html');
        const articles = Array.from(doc.querySelectorAll('article'));

        if (!articles.length) {
            console.error("No posts found in blog_data.html");
            return;
        }

        // Sort descending by data-date
        articles.sort((a, b) => {
            const dateA = new Date(a.getAttribute('data-date'));
            const dateB = new Date(b.getAttribute('data-date'));
            return dateB - dateA;
        });

        // On the homepage, we only show a bulleted list
        const olderEl = document.getElementById('older-posts');
        if (!olderEl) return;

        let html = '<ul>';
        articles.forEach(article => {
            const dateAttr = article.getAttribute('data-date');
            const slug = article.getAttribute('data-slug') || '';
            const h2 = article.querySelector('h2');
            const titleText = h2 ? h2.textContent.trim() : '(Untitled Post)';
            html += `
                <li>
                    <strong>${dateAttr}</strong> -
                    <a href="blog.html#${slug}">${titleText}</a>
                </li>
            `;
        });
        html += '</ul>';
        olderEl.innerHTML = html;
    };

    window.renderBlogPostsHTML = async function (resp) {
        const textData = await resp.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(textData, 'text/html');
        window.allArticles = Array.from(doc.querySelectorAll('article'));

        if (!window.allArticles.length) {
            console.error('No posts found in blog_data.html');
            return;
        }

        // Sort by data-date descending
        window.allArticles.sort((a, b) => {
            const dateA = new Date(a.getAttribute('data-date'));
            const dateB = new Date(b.getAttribute('data-date'));
            return dateB - dateA;
        });

        renderArticles(window.allArticles);
    };

    window.renderArticles = function (articles) {
        const archiveSection = document.getElementById('blog-archive');
        if (!archiveSection) return;
        archiveSection.innerHTML = '';

        articles.forEach(article => {
            const dateAttr = article.getAttribute('data-date');
            const slug = article.getAttribute('data-slug') || '';
            const titleEl = article.querySelector('h2');
            const postTitle = titleEl ? titleEl.textContent.trim() : '(Untitled)';
            const articleContent = article.innerHTML;

            const detailsHtml = `
             <article id="${slug}">
                 <div class="blog-title">${postTitle}</div>
                 <div class="blog-date">${dateAttr}</div>
                 <details class="mt-1">
                     <summary class="p-0.5"><b>${postTitle}</b></summary>
                     <div class="p-1">${articleContent}</div>
                 </details>
             </article>
            `;
            archiveSection.insertAdjacentHTML('beforeend', detailsHtml);
        });
    };

    // Simple text filter for blog.html
    let debounceTimer;
    window.filterBlogPosts = function () {
        const searchInput = document.getElementById('blogSearch');
        if (!searchInput) return;
        const searchValue = searchInput.value.toLowerCase().trim();

        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            if (!searchValue) {
                renderArticles(window.allArticles);
                return;
            }
            const filtered = window.allArticles.filter(article => {
                const text = article.textContent.toLowerCase();
                return text.includes(searchValue);
            });
            renderArticles(filtered);
        }, 250);
    };

    window.resetBlogFilter = function () {
        const searchInput = document.getElementById('blogSearch');
        if (searchInput) {
            searchInput.value = '';
        }
        if (window.allArticles) {
            renderArticles(window.allArticles);
        }
    };
}
