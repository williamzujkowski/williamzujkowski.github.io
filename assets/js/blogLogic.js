// assets/js/blogLogic.js

export function initBlogLogic() {
    const path = window.location.pathname.split('/').pop() || 'index.html';

    if (path === 'index.html') {
        // Fetch and render recent blog posts
        fetchRecentBlogPosts();
    } else if (path === 'blog.html') {
        // Fetch and render all blog posts
        fetchAllBlogPosts();
    }
}

// Fetch recent blog posts for the index page
async function fetchRecentBlogPosts() {
    try {
        const resp = await fetch('blog_data.html');
        if (!resp.ok) throw new Error('Failed to fetch blog_data.html');
        const textData = await resp.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(textData, 'text/html');
        const articles = Array.from(doc.querySelectorAll('article'));
        if (!articles.length) {
            console.error("No posts found in blog_data.html");
            return;
        }
        // Sort descending by date
        articles.sort((a, b) => {
            const dateA = new Date(a.getAttribute('data-date'));
            const dateB = new Date(b.getAttribute('data-date'));
            return dateB - dateA;
        });
        // Display them
        const blogListDiv = document.getElementById('recent-blog-list');
        if (!blogListDiv) return;

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
        blogListDiv.innerHTML = html;
    } catch (err) {
        console.error("Error fetching recent blog posts:", err);
    }
}

// Fetch all blog posts for the blog page
async function fetchAllBlogPosts() {
    try {
        const resp = await fetch('blog_data.html');
        if (!resp.ok) throw new Error('Failed to fetch blog_data.html');
        const textData = await resp.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(textData, 'text/html');
        window.allArticles = Array.from(doc.querySelectorAll('article'));
        if (!window.allArticles.length) {
            console.error("No posts found in blog_data.html");
            return;
        }
        // Sort by date descending
        window.allArticles.sort((a, b) => {
            const dateA = new Date(a.getAttribute('data-date'));
            const dateB = new Date(b.getAttribute('data-date'));
            return dateB - dateA;
        });
        renderArticles(window.allArticles);
    } catch (err) {
        console.error("Error fetching blog data:", err);
    }
}

function renderArticles(articles) {
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
          <div><strong>${postTitle}</strong> <span>(${dateAttr})</span></div>
          <details style="margin: 0.5rem 0;">
            <summary>Read More</summary>
            <div>${articleContent}</div>
          </details>
        </article>
      `;
        archiveSection.insertAdjacentHTML('beforeend', detailsHtml);
    });

    autoExpandPostFromHash();
    window.addEventListener('hashchange', autoExpandPostFromHash);
}

function autoExpandPostFromHash() {
    if (!window.location.hash) return;
    const slug = window.location.hash.slice(1);
    if (!slug) return;
    const articleEl = document.getElementById(slug);
    if (!articleEl) return;

    const details = articleEl.querySelector('details');
    if (details) {
        details.open = true;
        articleEl.scrollIntoView({ behavior: 'smooth' });
    }
}

// Filter logic
let debounceTimer;
window.filterBlogPosts = function () {
    const searchInput = document.getElementById('blogSearch');
    if (!searchInput || !window.allArticles) return;

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
