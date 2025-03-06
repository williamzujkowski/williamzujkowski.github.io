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
            const navToggle = navContainer.querySelector(".nav-toggle");
            const navPanel = navContainer.querySelector(".nav-panel");

            if (navToggle && navPanel) {
                // Toggle off-canvas panel on click
                navToggle.addEventListener("click", function () {
                    navPanel.classList.toggle("active");
                    const expanded = navPanel.classList.contains("active");
                    this.setAttribute("aria-expanded", expanded ? "true" : "false");
                });

                // Close panel when any nav link is clicked
                const navLinks = navPanel.querySelectorAll(".nav-menu a");
                navLinks.forEach(link => {
                    link.addEventListener("click", function () {
                        navPanel.classList.remove("active");
                        navToggle.setAttribute("aria-expanded", "false");
                    });
                });
            } else {
                console.error("Required nav elements not found.");
            }
        })
        .catch(err => console.error("Error loading nav:", err));
});
