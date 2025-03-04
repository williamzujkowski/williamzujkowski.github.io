document.addEventListener("DOMContentLoaded", function () {
    fetch("includes/nav.html")
        .then(response => response.text())
        .then(html => {
            document.getElementById("dynamic-nav").innerHTML = html;
            // Add event listener for the hamburger toggle
            const navToggle = document.getElementById("dynamic-nav").querySelector(".nav-toggle");
            if (navToggle) {
                navToggle.addEventListener("click", function () {
                    this.closest(".site-nav").classList.toggle("active");
                });
            }
        })
        .catch(err => console.error("Error loading nav:", err));
});
