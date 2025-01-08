// assets/js/blogLogic.js

export function initBlogLogic() {
    const path = window.location.pathname.split('/').pop() || 'index.html';

    if (path === 'index.html') {
        // Fetch and render recent blog posts
        fetchRecentBlogPosts();
    } else if (path === 'blog.html') {
        // Fetch and render all blog posts with pagination
        fetchAllBlogPosts();
    }
}

// Pagination Variables
let currentPage = 1;
const postsPerPage = 5;
let totalPages = 1;
let allArticles = [];

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
        articles.slice(0, 5).forEach(article => { // Show latest 5 posts
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

// Fetch all blog posts for the blog page with pagination
async function fetchAllBlogPosts() {
    try {
        const resp = await fetch('blog_data.html');
        if (!resp.ok) throw new Error('Failed to fetch blog_data.html');
        const textData = await resp.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(textData, 'text/html');
        allArticles = Array.from(doc.querySelectorAll('article'));
        if (!allArticles.length) {
            console.error("No posts found in blog_data.html");
            return;
        }
        // Sort by date descending
        allArticles.sort((a, b) => {
            const dateA = new Date(a.getAttribute('data-date'));
            const dateB = new Date(b.getAttribute('data-date'));
            return dateB - dateA;
        });
        totalPages = Math.ceil(allArticles.length / postsPerPage);
        renderArticles();
        updatePaginationButtons();
    } catch (err) {
        console.error("Error fetching blog data:", err);
    }
}

function renderArticles(filteredArticles = null) {
    const archiveSection = document.getElementById('blog-archive');
    if (!archiveSection) return;
    archiveSection.innerHTML = '';

    const articlesToRender = filteredArticles || allArticles;
    const start = (currentPage - 1) * postsPerPage;
    const end = start + postsPerPage;
    const paginatedArticles = articlesToRender.slice(start, end);

    paginatedArticles.forEach(article => {
        const dateAttr = article.getAttribute('data-date');
        const slug = article.getAttribute('data-slug') || '';
        const titleEl = article.querySelector('h2');
        const postTitle = titleEl ? titleEl.textContent.trim() : '(Untitled)';
        const articleContent = article.innerHTML;

        const detailsHtml = `
        <article id="${slug}" class="blog-card">
          <h2>${postTitle}</h2>
          <p><em>${dateAttr}</em></p>
          <details>
            <summary>Read More</summary>
            <div>${articleContent}</div>
          </details>
        </article>
      `;
        archiveSection.insertAdjacentHTML('beforeend', detailsHtml);
    });
}

function updatePaginationButtons(filtered = false) {
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');

    if (!prevBtn || !nextBtn) return;

    if (currentPage <= 1) {
        prevBtn.disabled = true;
    } else {
        prevBtn.disabled = false;
    }

    if (currentPage >= totalPages) {
        nextBtn.disabled = true;
    } else {
        nextBtn.disabled = false;
    }
}

window.prevPage = function () {
    if (currentPage > 1) {
        currentPage--;
        renderArticles();
        updatePaginationButtons();
        window.scrollTo(0, 0);
    }
};

window.nextPage = function () {
    if (currentPage < totalPages) {
        currentPage++;
        renderArticles();
        updatePaginationButtons();
        window.scrollTo(0, 0);
    }
};

// Filter logic
let debounceTimer;
window.filterBlogPosts = function () {
    const searchInput = document.getElementById('blogSearch');
    if (!searchInput || !allArticles.length) return;

    const searchValue = searchInput.value.toLowerCase().trim();
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        if (!searchValue) {
            currentPage = 1;
            renderArticles();
            updatePaginationButtons();
            return;
        }
        const filtered = allArticles.filter(article => {
            const text = article.textContent.toLowerCase();
            return text.includes(searchValue);
        });
        currentPage = 1;
        renderArticles(filtered);
        totalPages = Math.ceil(filtered.length / postsPerPage);
        updatePaginationButtons();
    }, 250);
};

window.resetBlogFilter = function () {
    const searchInput = document.getElementById('blogSearch');
    if (searchInput) {
        searchInput.value = '';
    }
    if (allArticles.length) {
        currentPage = 1;
        renderArticles();
        totalPages = Math.ceil(allArticles.length / postsPerPage);
        updatePaginationButtons();
    }
};
