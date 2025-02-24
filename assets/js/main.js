/*****************************************************
 * main.js - Core Script for grenlan.com
 *
 * Features:
 *  - Navigation & Footer injection
 *  - Konami Code Easter Egg activation
 *  - Back-to-top button setup
 *  - Blog Logic (TOC, excerpts, etc.)
 *****************************************************/

document.addEventListener('DOMContentLoaded', () => {
  buildNavigation();
  buildFooter();
  activateKonamiCode();
  setupBackToTop();
  // Additional page-specific initialization can be added here.
});

/* ====== NAVIGATION & FOOTER ====== */
function buildNavigation() {
  const navContainer = document.getElementById('dynamic-nav');
  if (!navContainer) return;
  const navLinks = [
    { title: 'Home', url: 'index.html' },
    { title: 'About', url: 'about.html' },
    { title: 'Blog', url: 'blog.html' },
    { title: 'Pizza Calculator', url: 'pizza.html' },
    { title: 'Coffee Calculator', url: 'coffee.html' }
  ];
  const ul = document.createElement('ul');
  navLinks.forEach(link => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = link.url;
    a.textContent = link.title;
    li.appendChild(a);
    ul.appendChild(li);
  });
  navContainer.appendChild(ul);
}

function buildFooter() {
  const footerContainer = document.getElementById('dynamic-footer');
  if (!footerContainer) return;
  const currentYear = new Date().getFullYear();
  footerContainer.innerHTML = `<p>&copy; ${currentYear} William Zujkowski. All rights reserved.</p>`;
}

/* ====== KONAMI CODE & SECRET CODE ====== */
function activateKonamiCode() {
  const secretCodeSection = document.getElementById('secret-code');
  if (!secretCodeSection) return;
  let keySequence = [];
  const konami = '38,38,40,40,37,39,37,39,66,65';
  window.addEventListener('keyup', (e) => {
    keySequence.push(e.keyCode);
    if (keySequence.toString().indexOf(konami) >= 0) {
      secretCodeSection.style.display = 'block';
      showToast('Secret Unlocked! Enjoy the Easter Egg!');
      keySequence = [];
    }
  });
}

/* ====== BACK TO TOP BUTTON ====== */
function setupBackToTop() {
  const backToTopBtn = document.getElementById('back-to-top');
  if (!backToTopBtn) return;
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      backToTopBtn.style.display = 'block';
    } else {
      backToTopBtn.style.display = 'none';
    }
  });
}

/* ====== TOAST NOTIFICATIONS ====== */
function showToast(message) {
  const toastEl = document.getElementById("toast");
  if (!toastEl) return;
  toastEl.innerText = message;
  toastEl.style.display = "block";
  setTimeout(() => {
    toastEl.style.display = "none";
  }, 3000);
}
