document.addEventListener("DOMContentLoaded", function () {
  loadComponent("includes/header.html", "header-placeholder");
  loadComponent("includes/nav.html", "nav-placeholder");
  loadComponent("includes/footer.html", "footer-placeholder");
  loadRecentBlogPosts();
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

function loadRecentBlogPosts() {
  fetch("blog_data.html")
    .then(response => response.text())
    .then(data => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, "text/html");
      let articles = Array.from(doc.querySelectorAll("article"));
      // Sort articles by date (newest first)
      articles.sort((a, b) => new Date(b.getAttribute("data-date")) - new Date(a.getAttribute("data-date")));
      const recent = articles.slice(0, 3);
      const listDiv = document.getElementById("recent-blog-list");
      if (listDiv) {
        recent.forEach(article => {
          const titleElement = article.querySelector("h2");
          if (!titleElement) return;
          const title = titleElement.innerText;
          const date = article.getAttribute("data-date");
          const slug = article.getAttribute("data-slug") || "";
          const link = document.createElement("a");
          // Link to the blog page with the corresponding slug
          link.href = "blog.html#" + slug;
          link.innerText = `${title} (${date})`;
          const p = document.createElement("p");
          p.appendChild(link);
          listDiv.appendChild(p);
        });
      }
    })
    .catch(error => {
      console.error("Error loading recent blog posts:", error);
    });
}
