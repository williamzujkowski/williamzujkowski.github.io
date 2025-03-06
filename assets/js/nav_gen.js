document.addEventListener("DOMContentLoaded", function () {
    const navContainer = document.getElementById("dynamic-nav");
    if (!navContainer) {
        console.error("No element with id 'dynamic-nav' found.");
        return;
    }

    // Load the navigation markup from an absolute path
    fetch("/includes/nav.html")
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.text();
        })
        .then(html => {
            navContainer.innerHTML = html;
            console.log("Navigation loaded successfully.");

            // Retrieve the main nav container and toggle button
            const siteNav = navContainer.querySelector(".site-nav");
            const navToggle = navContainer.querySelector(".nav-toggle");
            const navPanel = navContainer.querySelector(".nav-panel");

            if (!siteNav || !navToggle || !navPanel) {
                console.error("Required nav elements not found in nav.html");
                return;
            }

            // Toggle the off-canvas panel when the toggle button is clicked
            navToggle.addEventListener("click", function () {
                siteNav.classList.toggle("active");
                const expanded = siteNav.classList.contains("active");
                navToggle.setAttribute("aria-expanded", expanded ? "true" : "false");
                console.log("Nav toggle clicked. Expanded =", expanded);
            });

            // Close the panel when any nav link is clicked
            const navLinks = siteNav.querySelectorAll(".nav-menu a");
            navLinks.forEach(link => {
                link.addEventListener("click", function () {
                    if (siteNav.classList.contains("active")) {
                        siteNav.classList.remove("active");
                        navToggle.setAttribute("aria-expanded", "false");
                        console.log("Nav link clicked; closing panel.");
                    }
                });
            });

            // Listen for window resize to auto-close the mobile nav on desktop
            window.addEventListener("resize", function () {
                if (window.innerWidth >= 769 && siteNav.classList.contains("active")) {
                    siteNav.classList.remove("active");
                    navToggle.setAttribute("aria-expanded", "false");
                    console.log("Window resized to desktop; closing nav panel.");
                }
            });
        })
        .catch(err => console.error("Error loading nav:", err));
});
