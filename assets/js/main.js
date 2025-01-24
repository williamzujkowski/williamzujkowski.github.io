document.addEventListener("DOMContentLoaded", function () {
  initNavFooter();
  initPizzaCalculator();
  initCoffeeCalculator();
  initBlogLogic();
  initSecretToggles();
});

function initNavFooter() {
  const nav = document.getElementById("dynamic-nav");
  const footer = document.getElementById("dynamic-footer");

  nav.innerHTML = `
  <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="pizza.html">Pizza Calculator</a></li>
      <li><a href="coffee.html">Coffee Calculator</a></li>
      <li><a href="blog.html">Blog</a></li>
  </ul>
  `;

  footer.innerHTML = `
  <p>&copy; 2025 William Zujkowski</p>
  `;
}