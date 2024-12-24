// footer_gen.js
(function () {
    function createFooter() {
        const footer = document.createElement('footer');
        footer.innerHTML = `
        <small>
          © 2024 William Zujkowski. Powered by 
          <a href="https://mizu.sh" target="_blank" rel="noopener noreferrer">mizu.js</a> & 
          <a href="https://matcha.mizu.sh" target="_blank" rel="noopener noreferrer">matcha.css</a>
          <a href="https://github.com/williamzujkowski" target="_blank">GitHub</a> |
          <a href="https://www.linkedin.com/in/williamzujkowski/" target="_blank">LinkedIn</a> |
          <a href="https://steamcommunity.com/id/grenlan/" target="_blank">Steam</a>
          <!-- Hidden message -->
          <span id="secret-message">You found the secret! 🕵️‍♂️</span>
        </small>
      `;
        return footer;
    }

    document.addEventListener('DOMContentLoaded', () => {
        const footerContainer = document.getElementById('dynamic-footer');
        if (footerContainer) {
            footerContainer.appendChild(createFooter());
        }
    });
})();
