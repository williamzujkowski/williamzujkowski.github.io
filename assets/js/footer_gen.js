document.addEventListener("DOMContentLoaded", function () {
    fetch("includes/footer.html")
        .then(response => response.text())
        .then(html => {
            document.getElementById("dynamic-footer").innerHTML = html;
        })
        .catch(err => console.error("Error loading footer:", err));
});
