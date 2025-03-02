document.addEventListener("DOMContentLoaded", function() {
    loadComponent("includes/header.html", "header-placeholder");
    loadComponent("includes/nav.html", "nav-placeholder");
    loadComponent("includes/footer.html", "footer-placeholder");
  });
  
  function loadComponent(url, elementId) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        document.getElementById(elementId).innerHTML = html;
      })
      .catch(error => {
        console.error("Error loading component: " + url, error);
      });
  }
  