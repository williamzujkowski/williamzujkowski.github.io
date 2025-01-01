// main.js

/********************************************/
/* 1) Dynamic Navigation Generation         */
/********************************************/
(function () {
    const pages = [
        { href: 'index.html', label: 'Home' },
        { href: 'pizza.html', label: 'Pizza Calculator' },
        { href: 'coffee.html', label: 'Coffee Calculator' },
        { href: 'blog.html', label: 'Blog' },
    ];

    function createNav(currentPage) {
        const nav = document.createElement('nav');
        nav.setAttribute('aria-label', 'Main navigation');

        const ul = document.createElement('ul');
        ul.style.display = 'flex';
        ul.style.gap = '1rem';
        ul.style.listStyle = 'none';

        pages.forEach(({ href, label }) => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = href;
            a.textContent = label;
            if (href === currentPage) {
                a.setAttribute('aria-current', 'page');
            }
            li.appendChild(a);
            ul.appendChild(li);
        });

        nav.appendChild(ul);
        return nav;
    }

    function createFooter() {
        const footer = document.createElement('footer');
        footer.innerHTML = `
        <small>
         © 2024 William Zujkowski. Powered by 
         <a href="https://mizu.sh" target="_blank" rel="noopener noreferrer">mizu.js</a> & 
         <a href="https://matcha.mizu.sh" target="_blank" rel="noopener noreferrer">matcha.css</a>
         <br>
         <a href="https://github.com/williamzujkowski" target="_blank">GitHub</a> |
         <a href="https://www.linkedin.com/in/williamzujkowski/" target="_blank">LinkedIn</a> |
         <a href="https://steamcommunity.com/id/grenlan/" target="_blank">Steam</a>
        </small>
     `;
        return footer;
    }

    document.addEventListener('DOMContentLoaded', () => {
        // 1a) Generate Nav
        const navContainer = document.querySelector('nav[\\*mizu] > div#dynamic-nav');
        if (navContainer) {
            const path = window.location.pathname;
            const currentPage = path.substring(path.lastIndexOf('/') + 1) || 'index.html';
            navContainer.appendChild(createNav(currentPage));
        }

        // 1b) Generate Footer
        const footerContainer = document.querySelector('footer[\\*mizu] > div#dynamic-footer');
        if (footerContainer) {
            footerContainer.appendChild(createFooter());
        }
    });
})();

/********************************************/
/* 2) Pizza Calculator Logic               */
/********************************************/
(function () {
    // Only run if #pizzaForm is present
    if (!document.getElementById('pizzaForm')) {
        return;
    }

    let calculationCompleted = false;
    let pizzaReport = "";

    function loadPizzaDefaults() {
        const storedAttendees = localStorage.getItem('pizzaAttendees');
        const storedSlicesPerPerson = localStorage.getItem('pizzaSlicesPerPerson');
        const storedHoursDebugging = localStorage.getItem('pizzaHoursDebugging');
        const storedPizzaType = localStorage.getItem('pizzaType');

        if (storedAttendees) document.getElementById('attendees').value = storedAttendees;
        if (storedSlicesPerPerson) document.getElementById('slicesPerPerson').value = storedSlicesPerPerson;
        if (storedHoursDebugging) document.getElementById('hoursDebugging').value = storedHoursDebugging;
        if (storedPizzaType) document.getElementById('pizzaType').value = storedPizzaType;
    }
    loadPizzaDefaults();

    // FUN: Generate AI Toppings
    function generateAIToppings() {
        const toppingOptions = [
            "Pepperoni++",
            "BBQ Marshmallows",
            "Quantum Pineapple Bits",
            "AI-Generated Olives",
            "Crypto-Sauce",
            "Extra Cheese Layer v2.0",
            "Spicy Jalapeño Clusters",
            "Teriyaki PineappleHate",
            "Bacon-Filled Mushrooms",
            "Elon’s Space Spice"
        ];
        let selected = [];
        for (let i = 0; i < 3; i++) {
            const randIndex = Math.floor(Math.random() * toppingOptions.length);
            selected.push(toppingOptions[randIndex]);
        }
        return selected;
    }

    // Insert additional buttons into the form (AI Toppings, Copy to Clipboard)
    (function initPizzaButtons() {
        const formFieldset = document.querySelector('#pizzaForm fieldset');
        if (!formFieldset) return;

        const aiBtn = document.createElement('button');
        aiBtn.type = 'button';
        aiBtn.textContent = 'Generate AI Toppings';
        aiBtn.classList.add('ai-toppings-button');
        aiBtn.addEventListener('click', function () {
            const resultArea = document.getElementById('result');
            const aiToppings = generateAIToppings();
            const msg = `<p><strong>AI Toppings Suggestion:</strong> ${aiToppings.join(', ')}</p>`;
            resultArea.insertAdjacentHTML('beforeend', msg);
        });
        formFieldset.appendChild(aiBtn);

        const copyBtn = document.createElement('button');
        copyBtn.type = 'button';
        copyBtn.textContent = 'Copy Report to Clipboard';
        copyBtn.classList.add('copy-report-button');
        copyBtn.addEventListener('click', function () {
            if (!calculationCompleted || !pizzaReport) {
                showToast("No pizza report to copy!");
                return;
            }
            navigator.clipboard.writeText(pizzaReport)
                .then(() => {
                    showToast("Pizza report copied to clipboard!");
                })
                .catch(() => {
                    showToast("Failed to copy to clipboard!");
                });
        });
        formFieldset.appendChild(copyBtn);
    })();

    // Expose public functions (like in previous code)
    window.calculatePizzas = function () {
        calculationCompleted = false;
        pizzaReport = "";

        const attendeesInput = document.getElementById('attendees');
        const pizzaTypeInput = document.getElementById('pizzaType');
        const hoursDebuggingInput = document.getElementById('hoursDebugging');
        const slicesPerPersonInput = document.getElementById('slicesPerPerson');

        const resultDiv = document.getElementById('result');
        const emailPromptSection = document.getElementById('emailPromptSection');
        const progressBar = document.getElementById('progressBar');
        const progressLabel = document.getElementById('progressLabel');

        localStorage.setItem('pizzaAttendees', attendeesInput.value);
        localStorage.setItem('pizzaType', pizzaTypeInput.value);
        localStorage.setItem('pizzaSlicesPerPerson', slicesPerPersonInput.value);
        localStorage.setItem('pizzaHoursDebugging', hoursDebuggingInput.value);

        resultDiv.innerHTML = '';
        if (emailPromptSection) emailPromptSection.style.display = 'none';
        if (progressBar) progressBar.style.width = '0%';
        if (progressLabel) progressLabel.textContent = '';

        const loadingSteps = [
            "Analyzing hunger coefficients based on debugging hours...",
            "Contacting Gilfoyle’s pizza orchestration server...",
            "Running middle-out slice allocation algorithm...",
            "Optimizing pizza cluster for maximum throughput...",
            "Spinning up pizza instances on serverless architecture...",
            "Finalizing pizza load balancer configuration...",
            "Pizzas deployed successfully!"
        ];

        let stepIndex = 0;
        function updateProgress() {
            if (stepIndex < loadingSteps.length) {
                let percentage = (stepIndex + 1) * 15;
                if (percentage > 75 && percentage < 100) {
                    percentage = 75;
                }
                if (progressBar) progressBar.style.width = `${percentage}%`;
                if (progressLabel) progressLabel.textContent = loadingSteps[stepIndex];
                stepIndex++;
                if (percentage === 75) {
                    setTimeout(updateProgress, 1500);
                } else {
                    setTimeout(updateProgress, 500);
                }
            } else {
                if (progressBar) progressBar.style.width = '110%';
                if (progressLabel) progressLabel.textContent = "Pizza deployment exceeded expectations. You're 110% ready to eat! 🍕🎉";
                completeCalculation();
            }
        }
        updateProgress();

        function completeCalculation() {
            const hoursDebugging = parseInt(hoursDebuggingInput.value, 10);
            const slicesPerPerson = parseInt(slicesPerPersonInput.value, 10);
            const debuggingExtraSlices = hoursDebugging * 2;
            const attendees = parseInt(attendeesInput.value, 10);

            const totalSlicesNeeded = (attendees * slicesPerPerson) + debuggingExtraSlices;

            let pizzasRequired;
            let sliceEquivalency = 1;
            const pizzaType = pizzaTypeInput.value;
            const slicesPerPizza = 8;

            switch (pizzaType) {
                case "1": // NY
                    sliceEquivalency = 1;
                    break;
                case "0.5": // Detroit
                    sliceEquivalency = 1.5;
                    break;
                case "0.6": // Chicago
                    sliceEquivalency = 1.7;
                    break;
                case "2": // California
                    sliceEquivalency = 0.75;
                    break;
                case "3": // Hot Pockets
                    pizzasRequired = attendees * hoursDebugging;
                    finalizeResult(pizzasRequired, pizzaType, slicesPerPerson, hoursDebugging, attendees, "Hot Pockets: quick, regrettable!");
                    return;
                case "100": // Blockchain
                    sliceEquivalency = Math.random() > 0.5 ? 0.1 : 2;
                    break;
                case "cloud":
                    finalizeResult(Infinity, pizzaType, slicesPerPerson, hoursDebugging, attendees, "Cloud pizza infinite cost!");
                    return;
                case "pineapple":
                    resultDiv.innerHTML = `<blockquote>WiFi Pineapple Pizza is an acquired taste.
                 It's capturing your taste buds even as we speak. 🍍📡🍕</blockquote>`;
                    calculationCompleted = true;
                    return;
            }

            const adjustedSlicesPerPizza = slicesPerPizza * sliceEquivalency;
            pizzasRequired = Math.ceil(totalSlicesNeeded / adjustedSlicesPerPizza);

            if (pizzaType === "100") {
                finalizeResult(pizzasRequired, pizzaType, slicesPerPerson, hoursDebugging, attendees, "Blockchain madness!");
                return;
            }

            finalizeResult(pizzasRequired, pizzaType, slicesPerPerson, hoursDebugging, attendees, getHumorMessage(pizzasRequired));
        }
    };

    function finalizeResult(pizzasRequired, pizzaType, slicesPerPerson, hoursDebugging, attendees, humor) {
        const resultDiv = document.getElementById('result');
        const emailPromptSection = document.getElementById('emailPromptSection');
        calculationCompleted = true;
        let displayMessage = "";

        if (pizzaType === "3") {
            displayMessage = `<blockquote>You need <strong><span class="math-inline">\{pizzasRequired\}</strong\> Hot Pocket\(s\) 
to feed <strong\></span>{attendees}</strong> attendees for <strong>${hoursDebugging}</strong> hours 
                 of debugging. ${humor}</blockquote>`;
        } else if (pizzaType === "cloud") {
            displayMessage = `<blockquote>Cloud Pizza can feed any number of attendees, 
                 but watch out for that infinite billing! ☁️🍕</blockquote>`;
        } else if (pizzaType === "100") {
            displayMessage = `<blockquote>You need <strong><span class="math-inline">\{pizzasRequired\}</strong\> Blockchain Pizza\(s\) 
for <strong\></span>{attendees}</strong> devs. ${humor} 🍕💸</blockquote>`;
        } else if (pizzaType === "pineapple") {
            return;
        } else {
            displayMessage = `<blockquote>You need <strong><span class="math-inline">\{pizzasRequired\}</strong\> pizza\(s\) for 
<strong\></span>{attendees}</strong> attendees, factoring in <strong><span class="math-inline">\{hoursDebugging\} hours</strong\>\. 
Using <strong\></span>{document.getElementById('pizzaType').options[
                    document.getElementById('pizzaType').selectedIndex
                ].text}</strong> style.<br><br>
                 ${humor}</blockquote>`;
        }

        resultDiv.innerHTML = displayMessage;

        checkEnterpriseEmail(pizzasRequired);

        let constructedReport =
            `Pizza Calculation Report\n\n` +
            `Number of Attendees: ${attendees}\n` +
            `Selected Pizza Style: ${document.getElementById('pizzaType').options[
                document.getElementById('pizzaType').selectedIndex
            ].text}\n` +
            `Slices Per Person: ${slicesPerPerson}\n` +
            `Hours Debugging: ${hoursDebugging}\n` +
            `Total Pizzas Required: ${pizzasRequired}\n\n` +
            humor;

        pizzaReport = constructedReport;
        const preElement = document.createElement('pre');
        preElement.textContent = constructedReport;
        resultDiv.appendChild(preElement);

        performFunnyTests("Pizza");
    }

    function checkEnterpriseEmail(pizzasRequired) {
        const emailPromptSection = document.getElementById('emailPromptSection');
        if (emailPromptSection) {
            if (pizzasRequired >= 42) {
                emailPromptSection.style.display = 'block';
            } else {
                emailPromptSection.style.display = 'none';
            }
        }
    }

    function getHumorMessage(pizzasRequired) {
        if (pizzasRequired >= 42) {
            return "You've reached Pied Piper-level scaling. Time for enterprise pizza solutions with distributed toppings and fault-tolerant sauces! 🍕📞";
        } else if (pizzasRequired > 20) {
            return "Caution: Pizza overload detected! Prepare for mass consumption. 🍕🛠️";
        } else if (pizzasRequired > 10) {
            return "That's a hefty pizza cluster! Consider horizontal slice-scaling strategies. ☁️🍕";
        } else if (pizzasRequired > 5) {
            return "A respectable order! Watch for pizza logs to avoid any food comas. 📊🍕";
        } else if (pizzasRequired > 3) {
            return "A moderate batch. Don’t forget to allow burst capacity for last-minute slice demands. 🍕🔄";
        } else if (pizzasRequired === 1) {
            return "A single pizza? That’s like running production on a Raspberry Pi—hope it's enough! 🎛️🍕";
        } else {
            return "Minimal pizza order. For redundancy, might want to double the slices. 📦🍕";
        }
    }

    window.performFunnyTests = function (calculatorName) {
        console.log(`\n--- ${calculatorName} Additional Testing Suite Initiated ---`);
        console.log("[Load Test] Simulating thousands of hungry devs hitting the server for pizza calculations...");
        console.log("[Unit Test] Checking if slices per person is not negative or infinite... Looks good so far!");
        console.log("[UX Test] Asking random dev if they prefer pineapple on pizza. 50% meltdown rate detected!");
        console.log("[Security Test] Attempting to inject 'DROP TABLE Pizza' into debug hours field. Denied!");
        console.log("[All Tests Passed] The Pizza Calculator is stable...ish.\n");
    };

    window.showToast = function (message) {
        const toast = document.getElementById('toast');
        if (!toast) return;
        toast.textContent = message;
        toast.className = "toast show";
        setTimeout(() => {
            toast.className = toast.className.replace("show", "");
        }, 3000);
    };

    window.downloadReport = function () {
        if (!calculationCompleted || !pizzaReport) {
            showToast("Please perform a calculation first!");
            return;
        }
        const blob = new Blob([pizzaReport], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);

        const downloadLink = document.getElementById('downloadLink');
        if (!downloadLink) return;
        downloadLink.href = url;
        downloadLink.click();
        URL.revokeObjectURL(url);
    };

    window.submitEmail = function () {
        const emailInput = document.getElementById('emailInput');
        if (!emailInput) return;

        const email = emailInput.value.trim();
        if (!email) {
            showToast("Please enter a valid email!");
            return;
        }
        console.log(`Enterprise pizza inquiry from: ${email}`);
        showToast("Thanks! Our Enterprise Pizza Sales Team will contact you soon.");
    };
})();

/********************************************/
/* 3) Coffee Calculator Logic               */
/********************************************/
(function () {
    // Only run if #coffeeForm is present
    if (!document.getElementById('coffeeForm')) {
        return;
    }

    let coffeeCalculationCompleted = false;
    let coffeeReport = "";

    function loadCoffeeDefaults() {
        const storedDevs = localStorage.getItem('coffeeDevs');
        const storedStrength = localStorage.getItem('coffeeStrength');
        const storedHours = localStorage.getItem('coffeeHours');
        const storedFails = localStorage.getItem('coffeeFails');

        if (storedDevs) document.getElementById('javaAttendees').value = storedDevs;
        if (storedStrength) document.getElementById('coffeeStrength').value = storedStrength;
        if (storedHours) document.getElementById('hoursCoding').value = storedHours;
        if (storedFails) document.getElementById('timesBuildFailed').value = storedFails;
    }
    loadCoffeeDefaults();

    window.calculateCoffee = function () {
        coffeeCalculationCompleted = false;
        coffeeReport = "";

        const javaAttendeesInput = document.getElementById('javaAttendees');
        const coffeeStrengthInput = document.getElementById('coffeeStrength');
        const hoursCodingInput = document.getElementById('hoursCoding');
        const timesBuildFailedInput = document.getElementById('timesBuildFailed');

        const coffeeResultDiv = document.getElementById('coffeeResult');
        const progressBar = document.getElementById('progressBar');
        const progressLabel = document.getElementById('progressLabel');

        localStorage.setItem('coffeeDevs', javaAttendeesInput.value);
        localStorage.setItem('coffeeStrength', coffeeStrengthInput.value);
        localStorage.setItem('coffeeHours', hoursCodingInput.value);
        localStorage.setItem('coffeeFails', timesBuildFailedInput.value);

        if (coffeeResultDiv) coffeeResultDiv.innerHTML = '';
        if (progressBar) progressBar.style.width = '0%';
        if (progressLabel) progressLabel.textContent = '';

        const coffeeSteps = [
            "Measuring caffeine tolerance thresholds...",
            "Compiling brew instructions...",
            "Checking if we even have filters...",
            "Negotiating with the coffee machine daemon...",
            "Heating water to 'slightly scalding' temperature...",
            "Pouring the glorious liquid code fuel...",
            "Coffee distribution complete!"
        ];

        let stepIndex = 0;

        function updateProgress() {
            if (stepIndex < coffeeSteps.length) {
                let percentage = (stepIndex + 1) * 15;
                if (percentage > 75 && percentage < 100) {
                    percentage = 75;
                }
                if (progressBar) progressBar.style.width = `${percentage}%`;
                if (progressLabel) progressLabel.textContent = coffeeSteps[stepIndex];
                stepIndex++;
                if (percentage === 75) {
                    setTimeout(updateProgress, 1500);
                } else {
                    setTimeout(updateProgress, 500);
                }
            } else {
                if (progressBar) progressBar.style.width = '110%';
                if (progressLabel) progressLabel.textContent = "Coffee is brewed to perfection. ☕🎉";
                finalizeCoffeeCalc();
            }
        }
        updateProgress();

        function finalizeCoffeeCalc() {
            const devs = parseInt(javaAttendeesInput.value, 10);
            const strength = parseInt(coffeeStrengthInput.value, 10);
            const hours = parseInt(hoursCodingInput.value, 10);
            const fails = parseInt(timesBuildFailedInput.value, 10);

            const baseCups = (devs * hours) / strength;
            const additionalCupsForFails = fails * 2;
            const totalCups = Math.ceil(baseCups + additionalCupsForFails);

            const displayedMessage = getCoffeeMessage(totalCups, devs, strength, hours, fails);
            if (coffeeResultDiv) coffeeResultDiv.innerHTML = displayedMessage;
            coffeeCalculationCompleted = true;

            coffeeReport =
                `Coffee Calculation Report\n\n` +
                `Number of Devs: ${devs}\n` +
                `Coffee Strength Factor: ${strength}\n` +
                `Hours of Coding: ${hours}\n` +
                `Times Build Failed: ${fails}\n` +
                `Total Cups Recommended: ${totalCups}\n\n` +
                `Stay caffeinated and code on!`;

            const preElement = document.createElement('pre');
            preElement.textContent = coffeeReport;
            if (coffeeResultDiv) coffeeResultDiv.appendChild(preElement);

            performFunnyCoffeeTests();
        }
    };

    window.performFunnyCoffeeTests = function () {
        console.log("\n--- Coffee Additional Testing Suite Initiated ---");
        console.log("[Load Test] Simulating the entire dev team brewing coffee at 2 AM simultaneously...");
        console.log("[Unit Test] Verifying that coffee cups do not exceed OSHA safe levels of caffeine...");
        console.log("[UX Test] Observing devs shaking from caffeine overload while rewriting code in 15 languages...");
        console.log("[Security Test] Attempting to stash contraband donuts in the coffee filter. Denied!");
        console.log("[All Tests Passed] The Coffee Calculator is dangerously effective.\n");
    };

    window.getCoffeeMessage = function (totalCups, devs, strength, hours, fails) {
        let humor;
        if (totalCups > 100) {
            humor = "Warning: This amount of coffee could fuel a rocket. Seek medical advice or invest in decaf!";
        } else if (totalCups > 40) {
            humor = "Hope you have an industrial coffee machine. That's a giant pot to brew!";
        } else if (totalCups > 20) {
            humor = "You might want to assign a dedicated coffee pourer. That’s a lot of cups!";
        } else if (totalCups > 10) {
            humor = "A decent coffee cluster. Ensure your brew pipeline has no single points of failure!";
        } else if (totalCups > 5) {
            humor = "Enough coffee to keep the devs awake—at least until the next all-nighter!";
        } else if (totalCups > 1) {
            humor = "Modest coffee needs. Make sure the pot doesn’t run dry mid-deploy!";
        } else if (totalCups === 1) {
            humor = "One lonely cup? Must be a slow coding day or everyone else left the building!";
        } else {
            humor = "No coffee needed? Are you sure you're real engineers?";
        }

        return `<blockquote>You need approximately <strong>${totalCups}</strong> cup(s) of coffee 
                 to sustain <strong>${devs}</strong> dev(s) for <strong>${hours}</strong> hour(s). 
                 Coffee strength factor: <strong>${strength}</strong>, 
                 plus <strong>${fails * 2}</strong> extra cups for <strong>${fails}</strong> build failures.<br><br>
                 ${humor}</blockquote>`;
    };

    window.downloadCoffeeReport = function () {
        if (!coffeeCalculationCompleted) {
            showToast("Please perform a coffee calculation first!");
            return;
        }
        const blob = new Blob([coffeeReport], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);

        const downloadCoffeeLink = document.getElementById('downloadCoffeeLink');
        if (!downloadCoffeeLink) return;
        downloadCoffeeLink.href = url;
        downloadCoffeeLink.click();
        URL.revokeObjectURL(url);
    };

    window.shareCoffeeReport = function () {
        if (!coffeeCalculationCompleted) {
            showToast("No coffee report to share!");
            return;
        }
        console.log("Shared coffee report with the world: \n" + coffeeReport);
        showToast("Shared the coffee report with your teammates!");
    };
})();

/********************************************/
/* 4) Blog Logic for blog.html & index.html */
/********************************************/

// For index.html: renderIndexBlogHTML
window.renderIndexBlogHTML = async function (resp) {
    const textData = await resp.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(textData, 'text/html');
    const articles = Array.from(doc.querySelectorAll('article'));

    if (!articles.length) {
        console.error("No posts found in blog_data.html");
        return;
    }

    // Sort descending by data-date
    articles.sort((a, b) => {
        const dateA = new Date(a.getAttribute('data-date'));
        const dateB = new Date(b.getAttribute('data-date'));
        return dateB - dateA;
    });

    const newest = articles[0];
    const older = articles.slice(1);

    const latestEl = document.getElementById('latest-post');
    const olderEl = document.getElementById('older-posts');

    if (!newest) return;
    latestEl.innerHTML = newest.outerHTML;

    if (older.length && olderEl) {
        let html = '<h4>Older Posts:</h4><ul>';
        older.forEach(article => {
            const dateAttr = article.getAttribute('data-date');
            const slug = article.getAttribute('data-slug') || '';
            const h2 = article.querySelector('h2');
            const titleText = h2 ? h2.textContent.trim() : '(Untitled Post)';
            html += `
             <li>
                 <strong>${dateAttr}</strong> -
                 <a href="blog.html#${slug}">${titleText}</a>
             </li>
         `;
        });
        html += '</ul>';
        olderEl.innerHTML = html;
    }
};

// For blog.html: renderBlogPostsHTML
window.renderBlogPostsHTML = async function (resp) {
    const textData = await resp.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(textData, 'text/html');
    window.allArticles = Array.from(doc.querySelectorAll('article'));

    if (!window.allArticles.length) {
        console.error('No posts found in blog_data.html');
        return;
    }

    // Sort by data-date descending
    window.allArticles.sort((a, b) => {
        const dateA = new Date(a.getAttribute('data-date'));
        const dateB = new Date(b.getAttribute('data-date'));
        return dateB - dateA;
    });

    renderArticles(window.allArticles);
};

window.renderArticles = function (articles) {
    const archiveSection = document.getElementById('blog-archive');
    if (!archiveSection) return;
    archiveSection.innerHTML = '';

    articles.forEach(article => {
        const dateAttr = article.getAttribute('data-date');
        const slug = article.getAttribute('data-slug') || '';
        const titleEl = article.querySelector('h2');
        const postTitle = titleEl ? titleEl.textContent.trim() : '(Untitled)';
        const articleContent = article.innerHTML;

        const detailsHtml = `
         <article id="${slug}">
             <div class="blog-title">${postTitle}</div>
             <div class="blog-date">${dateAttr}</div>
             <details>
                 <summary>${postTitle}</summary>
                 <div>${articleContent}</div>
             </details>
         </article>
     `;
        archiveSection.insertAdjacentHTML('beforeend', detailsHtml);
    });
};

// Simple text filter for blog.html
window.filterBlogPosts = function () {
    const searchInput = document.getElementById('blogSearch');
    if (!searchInput) return;
    const searchValue = searchInput.value.toLowerCase().trim();

    if (!searchValue) {
        renderArticles(window.allArticles);
        return;
    }
    const filtered = window.allArticles.filter(article => {
        const text = article.textContent.toLowerCase();
        return text.includes(searchValue);
    });
    renderArticles(filtered);
};

window.resetBlogFilter = function () {
    const searchInput = document.getElementById('blogSearch');
    if (searchInput) {
        searchInput.value = '';
    }
    if (window.allArticles) {
        renderArticles(window.allArticles);
    }
};

/********************************************/
/* 5) Konami Code, Secret Toggles, etc.     */
/********************************************/
(function () {
    // Konami Code
    const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
    let index = 0;
    document.addEventListener('keydown', function (e) {
        if (e.keyCode === konamiCode[index]) {
            index++;
            if (index === konamiCode.length) {
                const secretCodeDiv = document.getElementById('secret-code');
                if (secretCodeDiv) {
                    secretCodeDiv.style.display = 'block';
                }
                alert('You unlocked the secret mode!');
                index = 0;
            }
        } else {
            index = 0;
        }
    });
})();

(function () {
    // Another secret code: "opensesame"
    let input = '';
    const secretCode = 'opensesame';
    document.addEventListener('keypress', function (e) {
        input += e.key.toLowerCase();
        if (input.includes(secretCode)) {
            const secret = document.getElementById('secret-code');
            if (secret) {
                secret.style.display = 'block';
                alert('🔓 Secret content unlocked!');
            }
            input = '';
        }
        if (input.length > secretCode.length) {
            input = input.substr(input.length - secretCode.length);
        }
    });
})();

// Friendly console greeting with updated ASCII referencing grenlan.com
console.log(
    "%c\n" +
    " grenlan.com is loading...                \n" +
    "\nHello there, console explorer! Keep up the curiosity!\n",
    "color: green; font-family: monospace;"
);