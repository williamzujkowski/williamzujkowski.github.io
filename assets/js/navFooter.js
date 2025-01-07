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

    // Color Scheme
    const storedColorScheme = localStorage.getItem('colorScheme');
    if (storedColorScheme) {
        document.documentElement.setAttribute('data-color-scheme', storedColorScheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-color-scheme', 'dark');
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

    // Dark mode toggle
    const liToggle = document.createElement('li');
    const toggleBtn = document.createElement('button');
    toggleBtn.textContent = 'Toggle Dark Mode';
    toggleBtn.addEventListener('click', () => {
        const currentMode = document.documentElement.getAttribute('data-color-scheme');
        const newMode = currentMode === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-color-scheme', newMode);
        localStorage.setItem('colorScheme', newMode);
    });
    liToggle.appendChild(toggleBtn);
    navUL.appendChild(liToggle);
}

function createFooterContent() {
    return `
      <small>
        © 2024 William Zujkowski. All rights reserved.
        <br>
        <a href="https://github.com/williamzujkowski" target="_blank">GitHub</a> |
        <a href="https://www.linkedin.com/in/williamzujkowski/" target="_blank">LinkedIn</a> |
        <a href="https://steamcommunity.com/id/grenlan/" target="_blank">Steam</a>
      </small>
    `;
}
