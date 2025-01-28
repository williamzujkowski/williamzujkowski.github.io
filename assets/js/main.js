/*****************************************************
 * main.js - Consolidated Script for grenlan.com
 *
 * Features:
 *  - Navigation & Footer injection (nav spans full width)
 *  - Konami Code Easter Egg
 *  - Blog Logic (TOC, short excerpt, partial snippet on index)
 *  - Pizza Calculator & Coffee Calculator with progress animations
 *  - Active nav link highlight
 *  - Floating 'Back to Top' button
 *****************************************************/

document.addEventListener('DOMContentLoaded', () => {
  buildNavigation();
  buildFooter();

  // Blog page check
  if (document.querySelector('#blog-archive')) {
    loadBlogPosts().then(() => {
      buildTableOfContents();
    });
  }

  // Index page: load recent posts
  if (document.querySelector('#recent-blog-list')) {
    loadRecentPosts();
  }

  activateKonamiCode();
  handleActiveNavLink();
  setupBackToTop();
});

/* ============== NAV & FOOTER ============== */
const navLinks = [
  { title: 'Home', url: 'index.html' },
  { title: 'About', url: 'about.html' },
  { title: 'Blog', url: 'blog.html' },
  { title: 'Pizza Calc', url: 'pizza.html' },
  { title: 'Coffee Calc', url: 'coffee.html' }
];

function buildNavigation() {
  const navContainer = document.getElementById('dynamic-nav');
  if (!navContainer) return;

  navLinks.forEach(link => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = link.url;
    a.textContent = link.title;
    li.appendChild(a);
    navContainer.appendChild(li);
  });
}

function buildFooter() {
  const footerContainer = document.getElementById('dynamic-footer');
  if (!footerContainer) return;

  const currentYear = new Date().getFullYear();
  footerContainer.innerHTML = `<p>&copy; ${currentYear} William Zujkowski. All rights reserved.</p>`;
}

function handleActiveNavLink() {
  const currentPage = window.location.pathname.split('/').pop(); // e.g. 'index.html', 'blog.html'
  const navContainer = document.getElementById('dynamic-nav');
  if (!navContainer) return;

  const navItems = navContainer.querySelectorAll('a');
  navItems.forEach(link => {
    const linkPage = link.getAttribute('href');
    if (linkPage === currentPage) {
      link.classList.add('active');
    }
  });
}

/* ============== KONAMI CODE EASTER EGG ============== */
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

/* ============== BLOG LOGIC ============== */
async function loadBlogPosts() {
  try {
    const response = await fetch('blog_data.html');
    const data = await response.text();
    const tempContainer = document.createElement('div');
    tempContainer.innerHTML = data;

    const articles = tempContainer.querySelectorAll('article');
    const archiveContainer = document.querySelector('#blog-archive');

    articles.forEach(article => {
      const cloned = article.cloneNode(true);
      const articleSlug = cloned.getAttribute('data-slug') || '';

      const wrapper = document.createElement('div');
      wrapper.classList.add('blog-article-wrapper');
      wrapper.id = articleSlug; // anchor ID

      // Excerpt logic
      const fullText = cloned.innerHTML.trim();
      const textOnly = cloned.textContent.trim();
      const words = textOnly.split(/\s+/);
      const excerptWords = words.slice(0, 80).join(' ');
      const excerpt = excerptWords + (words.length > 80 ? '...' : '');

      // Title
      const headerDiv = document.createElement('div');
      headerDiv.classList.add('blog-article-header');
      const h2 = cloned.querySelector('h2') ? cloned.querySelector('h2').cloneNode(true) : document.createElement('h2');
      headerDiv.appendChild(h2);

      // Excerpt paragraph
      const excerptP = document.createElement('p');
      excerptP.classList.add('blog-excerpt');
      excerptP.textContent = excerpt;

      // Show More button
      const showMoreBtn = document.createElement('button');
      showMoreBtn.textContent = 'Show More';
      showMoreBtn.classList.add('show-more-button');

      // Full text div
      const fullTextDiv = document.createElement('div');
      fullTextDiv.classList.add('blog-full-text');
      fullTextDiv.innerHTML = fullText;

      // Toggling
      let expanded = false;
      showMoreBtn.addEventListener('click', () => {
        expanded = !expanded;
        if (expanded) {
          fullTextDiv.style.display = 'block';
          showMoreBtn.textContent = 'Show Less';
        } else {
          fullTextDiv.style.display = 'none';
          showMoreBtn.textContent = 'Show More';
        }
      });

      wrapper.appendChild(headerDiv);
      wrapper.appendChild(excerptP);
      if (words.length > 80) {
        wrapper.appendChild(showMoreBtn);
      }
      wrapper.appendChild(fullTextDiv);

      archiveContainer.appendChild(wrapper);
    });
  } catch (err) {
    console.error('Error fetching blog data:', err);
  }
}

function buildTableOfContents() {
  const tocList = document.getElementById('toc-list');
  if (!tocList) return;

  const articleWrappers = document.querySelectorAll('#blog-archive .blog-article-wrapper');
  articleWrappers.forEach(wrapper => {
    const slug = wrapper.id;
    const h2 = wrapper.querySelector('h2');
    if (!h2) return;

    const titleText = h2.textContent || 'Untitled';
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = `#${slug}`;
    a.textContent = titleText;
    li.appendChild(a);
    tocList.appendChild(li);
  });
}

async function loadRecentPosts() {
  try {
    const response = await fetch('blog_data.html');
    const data = await response.text();

    const tempContainer = document.createElement('div');
    tempContainer.innerHTML = data;

    let articles = Array.from(tempContainer.querySelectorAll('article'));
    // sort by data-date descending
    articles.sort((a, b) => {
      const dateA = new Date(a.getAttribute('data-date'));
      const dateB = new Date(b.getAttribute('data-date'));
      return dateB - dateA;
    });

    const latestThree = articles.slice(0, 3);
    const recentList = document.getElementById('recent-blog-list');

    latestThree.forEach(article => {
      const slug = article.getAttribute('data-slug') || '';
      const titleEl = article.querySelector('h2');
      const title = titleEl ? titleEl.innerText : 'No Title';
      const dateAttr = article.getAttribute('data-date') || '';
      const textOnly = article.textContent.trim();
      const words = textOnly.split(/\s+/);
      const snippetWords = words.slice(0, 30).join(' ');
      const shortSnippet = snippetWords + (words.length > 30 ? '...' : '');

      const containerDiv = document.createElement('div');
      containerDiv.innerHTML = `
        <h3>${title}</h3>
        <p><em>${dateAttr}</em></p>
        <p>${shortSnippet}</p>
        <p><a href="blog.html#${slug}">Read more...</a></p>
      `;
      recentList.appendChild(containerDiv);
    });
  } catch (err) {
    console.error('Error fetching recent blog posts:', err);
  }
}

window.filterBlogPosts = function () {
  const searchInput = document.getElementById('blogSearch').value.toLowerCase().trim();
  const allArticles = document.querySelectorAll('#blog-archive .blog-article-wrapper');

  allArticles.forEach(wrapper => {
    const textContent = wrapper.textContent.toLowerCase();
    wrapper.style.display = (textContent.indexOf(searchInput) > -1) ? 'block' : 'none';
  });
};

window.resetBlogFilter = function () {
  document.getElementById('blogSearch').value = '';
  const allArticles = document.querySelectorAll('#blog-archive .blog-article-wrapper');
  allArticles.forEach(wrapper => {
    wrapper.style.display = 'block';
  });
};

/* ============== PIZZA CALCULATOR ============== */
window.calculatePizzas = function () {
  const attendees = parseInt(document.getElementById('attendees').value, 10) || 0;
  const pizzaType = document.getElementById('pizzaType').value;
  const slicesPerPerson = parseInt(document.getElementById('slicesPerPerson').value, 10) || 1;
  const hoursDebugging = parseInt(document.getElementById('hoursDebugging').value, 10) || 0;

  let typeMultiplier = 1;
  if (pizzaType === 'cloud') {
    typeMultiplier = 0.8;
  } else {
    typeMultiplier = parseFloat(pizzaType) || 1;
  }

  const baseSlices = attendees * slicesPerPerson;
  const debugBonus = hoursDebugging;
  const totalSlices = (baseSlices + attendees * debugBonus) * typeMultiplier;
  const slicesPerPizza = 8;
  const totalPizzas = Math.ceil(totalSlices / slicesPerPizza);

  animateProgressBar('progressBar', 'progressLabel', () => {
    displayPizzaResult(totalPizzas);
  });
};

function displayPizzaResult(totalPizzas) {
  const resultDiv = document.getElementById('result');
  if (!resultDiv) return;

  if (totalPizzas > 0) {
    let message = `You’ll need about <strong>${totalPizzas}</strong> pizzas.`;
    if (totalPizzas >= 42) {
      message += ` <br>That’s a lot of pizza! Please enter your email to talk about an “enterprise” pizza plan.`;
      document.getElementById('emailPromptSection').hidden = false;
    } else {
      document.getElementById('emailPromptSection').hidden = true;
    }
    resultDiv.innerHTML = message;
  } else {
    resultDiv.innerHTML = `Looks like you don’t need pizza... or maybe check your inputs.`;
  }
}

window.submitEmail = function () {
  const emailInput = document.getElementById('emailInput');
  if (!emailInput.value) {
    showToast('Please enter a valid email for enterprise pizza inquiries!');
    return;
  }
  showToast(`Thanks, ${emailInput.value}! We’ll reach out about your massive pizza order soon.`);
};

window.downloadReport = function () {
  const resultText = document.getElementById('result')?.innerText || 'No result yet.';
  const blob = new Blob([`Pizza Calculation Report\n\n${resultText}`], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);

  const hiddenLink = document.createElement('a');
  hiddenLink.href = url;
  hiddenLink.download = 'Pizza_Calculation_Report.txt';
  document.body.appendChild(hiddenLink);
  hiddenLink.click();
  document.body.removeChild(hiddenLink);
};

/* ============== COFFEE CALCULATOR ============== */
window.calculateCoffee = function () {
  const devCount = parseInt(document.getElementById('javaAttendees').value, 10) || 0;
  const strength = parseInt(document.getElementById('coffeeStrength').value, 10) || 1;
  const hours = parseInt(document.getElementById('hoursCoding').value, 10) || 0;
  const fails = parseInt(document.getElementById('timesBuildFailed').value, 10) || 0;

  const baseCups = devCount * hours;
  const failBonus = fails * 0.5;
  const totalCups = Math.ceil(baseCups * strength + failBonus);

  animateProgressBar('progressBar', 'progressLabel', () => {
    displayCoffeeResult(totalCups);
  });
};

function displayCoffeeResult(totalCups) {
  const coffeeResult = document.getElementById('coffeeResult');
  if (!coffeeResult) return;

  if (totalCups <= 0) {
    coffeeResult.innerHTML = `No coffee needed. Are you sure you’re coding?`;
    return;
  }

  let msg = `You might want <strong>${totalCups}</strong> cups of coffee in total. `;
  if (totalCups > 20) {
    msg += `Take care—your team might start vibrating if they drink that much!`;
  }
  coffeeResult.innerHTML = msg;
}

window.downloadCoffeeReport = function () {
  const resultText = document.getElementById('coffeeResult')?.innerText || 'No coffee calculation yet.';
  const blob = new Blob([`Coffee Calculation Report\n\n${resultText}`], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);

  const downloadLink = document.getElementById('downloadCoffeeLink');
  downloadLink.href = url;
  downloadLink.download = 'Coffee_Calculation_Report.txt';
  downloadLink.hidden = false;
  downloadLink.click();
  downloadLink.hidden = true;
  URL.revokeObjectURL(url);
};

window.shareCoffeeReport = function () {
  showToast('Sharing coffee calc is not yet implemented, but thanks for your enthusiasm!');
};

/* ============== HELPER FUNCTIONS ============== */
function animateProgressBar(progressId, labelId, onComplete) {
  const progressBar = document.getElementById(progressId);
  const label = document.getElementById(labelId);
  if (!progressBar || !label) {
    onComplete();
    return;
  }

  let width = 0;
  label.innerText = 'Calculating...';
  progressBar.value = 0;

  const interval = setInterval(() => {
    width += 5;
    progressBar.value = width;
    if (width >= 100) {
      clearInterval(interval);
      label.innerText = '';
      progressBar.value = 0;
      onComplete();
    }
  }, 100);
}

function showToast(message) {
  const toastEl = document.getElementById('toast');
  if (!toastEl) return;

  toastEl.innerText = message;
  toastEl.style.display = 'block';
  setTimeout(() => {
    toastEl.style.display = 'none';
  }, 3000);
}

/* ============== BACK TO TOP BUTTON ============== */
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

window.scrollToTop = function () {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
