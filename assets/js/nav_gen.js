document.addEventListener("DOMContentLoaded", function () {
    const navContainer = document.getElementById("dynamic-nav");
    if (!navContainer) {
        console.error("No element with id 'dynamic-nav' found.");
        return;
    }

    fetch("/includes/nav.html")
        .then(response => response.text())
        .then(html => {
            navContainer.innerHTML = html;

            // Attach event listener to the hamburger toggle button.
            const navToggle = navContainer.querySelector(".nav-toggle");
            if (navToggle) {
                navToggle.addEventListener("click", function () {
                    const siteNav = this.closest(".site-nav");
                    siteNav.classList.toggle("active");
                    const expanded = siteNav.classList.contains("active");
                    this.setAttribute("aria-expanded", expanded ? "true" : "false");
                });
            } else {
                console.error("No .nav-toggle button found within dynamic-nav.");
            }

            // Close the mobile menu when any nav link is clicked.
            const navLinks = navContainer.querySelectorAll(".nav-menu a");
            navLinks.forEach(link => {
                link.addEventListener("click", function () {
                    const siteNav = this.closest(".site-nav");
                    if (siteNav && siteNav.classList.contains("active")) {
                        siteNav.classList.remove("active");
                        const toggle = siteNav.querySelector(".nav-toggle");
                        if (toggle) toggle.setAttribute("aria-expanded", "false");
                    }
                });
            });
        })
        .catch(err => console.error("Error loading nav:", err));
});
