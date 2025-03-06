document.addEventListener("DOMContentLoaded", function () {
    const navContainer = document.getElementById("dynamic-nav");
    if (!navContainer) {
        console.error("No element with id 'dynamic-nav' found.");
        return;
    }

    fetch("/includes/nav.html")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text();
        })
        .then(html => {
            navContainer.innerHTML = html;
            console.log("Navigation loaded successfully.");

            // Retrieve the toggle button and off-canvas panel
            const navToggle = navContainer.querySelector(".nav-toggle");
            const navPanel = navContainer.querySelector(".nav-panel");

            if (!navToggle || !navPanel) {
                console.error("Required nav elements not found. Check nav.html structure.");
                return;
            }

            // Toggle the off-canvas panel on click
            navToggle.addEventListener("click", function () {
                navPanel.classList.toggle("active");
                const expanded = navPanel.classList.contains("active");
                navToggle.setAttribute("aria-expanded", expanded ? "true" : "false");
                console.log("Nav toggle clicked. Expanded =", expanded);
            });

            // Close the panel when any nav link is clicked
            const navLinks = navPanel.querySelectorAll(".nav-menu a");
            navLinks.forEach(link => {
                link.addEventListener("click", function () {
                    if (navPanel.classList.contains("active")) {
                        navPanel.classList.remove("active");
                        navToggle.setAttribute("aria-expanded", "false");
                        console.log("Nav link clicked; closing panel.");
                    }
                });
            });
        })
        .catch(err => console.error("Error loading nav:", err));
});
