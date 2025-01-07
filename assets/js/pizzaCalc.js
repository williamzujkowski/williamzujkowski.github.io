// assets/js/pizzaCalc.js

export function initPizzaCalculator() {
    if (!document.getElementById('pizzaForm')) {
        return;
    }

    let calculationCompleted = false;
    let pizzaReport = "";

    async function loadPizzaDefaults() {
        const storedAttendees = await localStorage.getItem('pizzaAttendees');
        const storedSlicesPerPerson = await localStorage.getItem('pizzaSlicesPerPerson');
        const storedHoursDebugging = await localStorage.getItem('pizzaHoursDebugging');
        const storedPizzaType = await localStorage.getItem('pizzaType');

        if (storedAttendees) document.getElementById('attendees').value = storedAttendees;
        if (storedSlicesPerPerson) document.getElementById('slicesPerPerson').value = storedSlicesPerPerson;
        if (storedHoursDebugging) document.getElementById('hoursDebugging').value = storedHoursDebugging;
        if (storedPizzaType) document.getElementById('pizzaType').value = storedPizzaType;
    }
    loadPizzaDefaults();

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

    // Add extra buttons to form
    (function initPizzaButtons() {
        const formFieldset = document.querySelector('#pizzaForm fieldset');
        if (!formFieldset) return;

        const aiBtn = document.createElement('button');
        aiBtn.type = 'button';
        aiBtn.textContent = 'Generate AI Toppings';
        aiBtn.style.marginRight = '0.5rem';
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

    window.calculatePizzas = function () {
        calculationCompleted = false;
        pizzaReport = "";

        const attendeesInput = document.getElementById('attendees');
        const pizzaTypeInput = document.getElementById('pizzaType');
        const hoursDebuggingInput = document.getElementById('hoursDebugging');
        const slicesPerPersonInput = document.getElementById('slicesPerPerson');

        const resultDiv = document.getElementById('result');
        const progressBar = document.getElementById('progressBar');
        const progressLabel = document.getElementById('progressLabel');

        localStorage.setItem('pizzaAttendees', attendeesInput.value);
        localStorage.setItem('pizzaType', pizzaTypeInput.value);
        localStorage.setItem('pizzaSlicesPerPerson', slicesPerPersonInput.value);
        localStorage.setItem('pizzaHoursDebugging', hoursDebuggingInput.value);

        if (resultDiv) resultDiv.innerHTML = '';
        if (progressBar) progressBar.value = 0;
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
                let percentage = (stepIndex + 1) * (100 / loadingSteps.length);
                if (progressBar) progressBar.value = percentage;
                if (progressLabel) progressLabel.textContent = loadingSteps[stepIndex];
                stepIndex++;
                setTimeout(updateProgress, 500);
            } else {
                if (progressBar) progressBar.value = 100;
                if (progressLabel) {
                    progressLabel.textContent =
                        "Pizza deployment exceeded expectations. You're 110% ready to eat! 🍕🎉";
                }
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
                    finalizeResult(pizzasRequired, pizzaType, slicesPerPerson, hoursDebugging, attendees,
                        "Hot Pockets: quick, regrettable!");
                    return;
                case "100": // Blockchain
                    sliceEquivalency = Math.random() > 0.5 ? 0.1 : 2;
                    break;
                case "cloud":
                    finalizeResult(Infinity, pizzaType, slicesPerPerson, hoursDebugging, attendees,
                        "Cloud pizza infinite cost!");
                    return;
                default:
                    break;
            }

            const adjustedSlicesPerPizza = slicesPerPizza * sliceEquivalency;
            pizzasRequired = Math.ceil(totalSlicesNeeded / adjustedSlicesPerPizza);

            if (pizzaType === "100") {
                finalizeResult(pizzasRequired, pizzaType, slicesPerPerson, hoursDebugging, attendees,
                    "Blockchain madness!");
                return;
            }
            finalizeResult(pizzasRequired, pizzaType, slicesPerPerson, hoursDebugging, attendees,
                getHumorMessage(pizzasRequired));
        }
    };

    function finalizeResult(pizzasRequired, pizzaType, slicesPerPerson, hoursDebugging, attendees, humor) {
        const resultDiv = document.getElementById('result');
        calculationCompleted = true;
        let displayMessage = "";

        if (pizzaType === "3") {
            displayMessage = `<blockquote>You need <strong>${pizzasRequired}</strong> Hot Pocket(s)
                to feed <strong>${attendees}</strong> attendees for <strong>${hoursDebugging}</strong> hours
                of debugging. ${humor}</blockquote>`;
        } else if (pizzaType === "cloud") {
            displayMessage = `<blockquote>Cloud Pizza can feed any number of attendees,
                but watch out for that infinite billing! ☁️🍕</blockquote>`;
        } else if (pizzaType === "100") {
            displayMessage = `<blockquote>You need <strong>${pizzasRequired}</strong> Blockchain Pizza(s)
                for <strong>${attendees}</strong> devs. ${humor} 🍕💸</blockquote>`;
        } else {
            const styleText = document.getElementById('pizzaType').options[
                document.getElementById('pizzaType').selectedIndex
            ].text;
            displayMessage = `<blockquote>You need <strong>${pizzasRequired}</strong> pizza(s) for
                <strong>${attendees}</strong> attendees, factoring in <strong>${hoursDebugging} hours</strong>.
                Using <strong>${styleText}</strong> style.<br><br>${humor}</blockquote>`;
        }

        if (resultDiv) resultDiv.innerHTML = displayMessage;
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
        if (resultDiv) resultDiv.appendChild(preElement);

        performFunnyTests("Pizza");
    }

    function checkEnterpriseEmail(pizzasRequired) {
        const emailPromptSection = document.getElementById('emailPromptSection');
        if (!emailPromptSection) return;
        if (pizzasRequired >= 42) {
            emailPromptSection.hidden = false;
        } else {
            emailPromptSection.hidden = true;
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
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    };

    window.downloadReport = function () {
        if (!calculationCompleted || !pizzaReport) {
            showToast("Please perform a calculation first!");
            return;
        }
        const blob = new Blob([pizzaReport], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);

        const downloadLink = document.createElement('a');
        downloadLink.href = url;
        downloadLink.download = 'Pizza_Calculation_Report.txt';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);

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
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            showToast("Invalid email format!");
            return;
        }

        console.log(`Enterprise pizza inquiry from: ${email}`);
        showToast("Thanks! Our Enterprise Pizza Sales Team will contact you soon.");

        emailInput.value = '';
        const emailPromptSection = document.getElementById('emailPromptSection');
        if (emailPromptSection) emailPromptSection.hidden = true;
    };
}
