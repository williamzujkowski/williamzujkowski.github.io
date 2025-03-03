document.addEventListener("DOMContentLoaded", function () {
    fetch("includes/nav.html")
        .then(response => response.text())
        .then(html => {
            document.getElementById("dynamic-nav").innerHTML = html;
        })
        .catch(err => console.error("Error loading nav:", err));
});
