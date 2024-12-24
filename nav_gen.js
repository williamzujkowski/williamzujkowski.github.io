// nav_gen.js
(function() {
    const pages = [
      { href: 'index.html', label: 'Home' },
      { href: 'pizza.html', label: 'Pizza Calculator' },
      { href: 'coffee.html', label: 'Coffee Calculator' },
      { href: 'blog.html', label: 'Blog' },
    ];
  
    function createNav(currentPage) {
      const nav = document.createElement('nav');
      nav.setAttribute('aria-label', 'Main navigation');
  
      const ul = document.createElement('ul');
      ul.style.display = 'flex';
      ul.style.gap = '1rem';
      ul.style.listStyle = 'none';
  
      pages.forEach(({ href, label }) => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = href;
        a.textContent = label;
        if (href === currentPage) {
          a.setAttribute('aria-current', 'page');
        }
        li.appendChild(a);
        ul.appendChild(li);
      });
  
      nav.appendChild(ul);
      return nav;
    }
  
    document.addEventListener('DOMContentLoaded', () => {
      const container = document.getElementById('dynamic-nav');
      if (container) {
        const path = window.location.pathname;
        const currentPage = path.substring(path.lastIndexOf('/') + 1) || 'index.html';
        const navEl = createNav(currentPage);
        container.appendChild(navEl);
      }
    });
  })();
  