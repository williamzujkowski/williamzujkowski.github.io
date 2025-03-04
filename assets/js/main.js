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
  // Load recent posts from blog_list.json rather than blog_data.html
  fetch("blog_list.json")
    .then(response => response.json())
    .then(data => {
      // Sort by date (newest first) and slice first 3 posts
      data.sort((a, b) => new Date(b.date) - new Date(a.date));
      const recent = data.slice(0, 3);
      const listDiv = document.getElementById("recent-blog-list");
      if (listDiv) {
        recent.forEach(post => {
          const link = document.createElement("a");
          // Link to the individual blog post file (under /blog/)
          link.href = "blog/" + post.slug + ".html";
          link.innerText = `${post.title} (${post.date})`;
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
