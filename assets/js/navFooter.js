// assets/js/navFooter.js

export function initNavFooter() {
    // Build Navigation
    const navContainer = document.querySelector('#nav-container #dynamic-nav');
    if (navContainer) {
        navContainer.appendChild(createNav());
    }

    // Build Footer
    const footerContainer = document.querySelector('#footer-container #dynamic-footer');
    if (footerContainer) {
        footerContainer.appendChild(createFooter());
    }

    // Color Scheme
    const storedColorScheme = localStorage.getItem('colorScheme');
    if (storedColorScheme) {
        document.documentElement.setAttribute('data-color-scheme', storedColorScheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-color-scheme', 'dark');
    }
}

function createNav() {
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Main navigation');

    const pages = [
        { href: 'index.html', label: 'Home' },
        { href: 'about.html', label: 'About Me' },
        { href: 'pizza.html', label: 'Pizza Calculator' },
        { href: 'coffee.html', label: 'Coffee Calculator' },
        { href: 'blog.html', label: 'Blog' }
    ];

    const ul = document.createElement('ul');
    ul.classList.add('block', 'lg:flex', 'flex-wrap', 'gap-0.5');

    const currentPage = (window.location.pathname.split('/').pop() || 'index.html');
    pages.forEach(({ href, label }) => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = href;
        a.textContent = label;
        a.classList.add('p-0.5', 'px-1');

        if (href === currentPage) {
            a.setAttribute('aria-current', 'page');
            a.classList.add('active');
        }
        li.appendChild(a);
        ul.appendChild(li);
    });

    // Add dark mode toggle
    const darkModeToggleLi = document.createElement('li');
    darkModeToggleLi.appendChild(createDarkModeToggle());
    ul.appendChild(darkModeToggleLi);

    nav.appendChild(ul);
    return nav;
}

function createFooter() {
    const footer = document.createElement('footer');
    footer.innerHTML = `
        <small class="p-1">
         © 2024 William Zujkowski. Powered by 
         <a href="assets/mizu/client.js" target="_blank" rel="noopener noreferrer">mizu.js</a> & 
         <a href="assets/mizu/matcha.css" target="_blank" rel="noopener noreferrer">matcha.css</a>
         <br>
         <a href="https://github.com/williamzujkowski" target="_blank">GitHub</a> |
         <a href="https://www.linkedin.com/in/williamzujkowski/" target="_blank">LinkedIn</a> |
         <a href="https://steamcommunity.com/id/grenlan/" target="_blank">Steam</a>
        </small>
    `;
    return footer;
}

function createDarkModeToggle() {
    const toggleButton = document.createElement('button');
    toggleButton.id = 'darkModeToggle';
    toggleButton.classList.add('p-0.5', 'px-1');
    toggleButton.textContent = 'Toggle Dark Mode';
    toggleButton.addEventListener('click', () => {
        const currentMode = document.documentElement.getAttribute('data-color-scheme');
        const newMode = currentMode === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-color-scheme', newMode);
        localStorage.setItem('colorScheme', newMode);
    });
    return toggleButton;
}
