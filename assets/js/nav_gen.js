document.addEventListener("DOMContentLoaded", function () {
    fetch("/includes/nav.html")
        .then(response => response.text())
        .then(html => {
            document.getElementById("dynamic-nav").innerHTML = html;

            // Add event listener for the hamburger toggle
            const navToggle = document.getElementById("dynamic-nav").querySelector(".nav-toggle");
            if (navToggle) {
                navToggle.addEventListener("click", function () {
                    const siteNav = this.closest(".site-nav");
                    siteNav.classList.toggle("active");
                    const expanded = siteNav.classList.contains("active");
                    this.setAttribute("aria-expanded", expanded);
                });
            }

            // Close mobile menu when a link is clicked
            const navLinks = document.querySelectorAll(".nav-menu a");
            navLinks.forEach(link => {
                link.addEventListener("click", function () {
                    const siteNav = this.closest(".site-nav");
                    if (siteNav.classList.contains("active")) {
                        siteNav.classList.remove("active");
                        const toggle = siteNav.querySelector(".nav-toggle");
                        if (toggle) toggle.setAttribute("aria-expanded", "false");
                    }
                });
            });
        })
        .catch(err => console.error("Error loading nav:", err));
});
