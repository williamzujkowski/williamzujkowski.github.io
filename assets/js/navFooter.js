// assets/js/navFooter.js

export function initNavFooter() {
    // Build Nav
    const navUL = document.querySelector('#nav-container ul#dynamic-nav');
    if (navUL) {
        createNavLinks(navUL);
    }

    // Build Footer
    const footerDiv = document.getElementById('dynamic-footer');
    if (footerDiv) {
        footerDiv.innerHTML = createFooterContent();
    }
}

function createNavLinks(navUL) {
    const pages = [
        { href: 'index.html', label: 'Home' },
        { href: 'about.html', label: 'About Me' },
        { href: 'pizza.html', label: 'Pizza Calculator' },
        { href: 'coffee.html', label: 'Coffee Calculator' },
        { href: 'blog.html', label: 'Blog' }
    ];

    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    pages.forEach(page => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = page.href;
        a.textContent = page.label;

        if (page.href === currentPage) {
            a.classList.add('active');
        }
        li.appendChild(a);
        navUL.appendChild(li);
    });
}

function createFooterContent() {
    return `
      <small>
        © 2024 William Zujkowski. All rights reserved.
        <br>
        <a href="https://github.com/williamzujkowski" target="_blank" rel="noopener noreferrer">GitHub</a> |
        <a href="https://www.linkedin.com/in/williamzujkowski/" target="_blank" rel="noopener noreferrer">LinkedIn</a> |
        <a href="https://steamcommunity.com/id/grenlan/" target="_blank" rel="noopener noreferrer">Steam</a>
      </small>
    `;
}
