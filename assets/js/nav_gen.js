document.addEventListener("DOMContentLoaded", function () {
    const navContainer = document.getElementById("dynamic-nav");
    if (!navContainer) {
        console.error("No element with id 'dynamic-nav' found.");
        return;
    }

    // Load nav markup from absolute path
    fetch("/includes/nav.html")
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.text();
        })
        .then(html => {
            navContainer.innerHTML = html;
            console.log("Navigation loaded successfully.");

            const navToggle = navContainer.querySelector(".nav-toggle");
            const navPanel = navContainer.querySelector(".nav-panel");

            if (!navToggle || !navPanel) {
                console.error("Required nav elements not found in nav.html");
                return;
            }

            // Toggle the off-canvas panel when the toggle button is clicked
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

            // Listen for window resize and auto-close the off-canvas panel if on desktop
            window.addEventListener("resize", function () {
                if (window.innerWidth >= 769 && navPanel.classList.contains("active")) {
                    navPanel.classList.remove("active");
                    navToggle.setAttribute("aria-expanded", "false");
                    console.log("Window resized to desktop; closing nav panel.");
                }
            });
        })
        .catch(err => console.error("Error loading nav:", err));
});
