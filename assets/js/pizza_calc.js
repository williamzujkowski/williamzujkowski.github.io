/*****************************************************
 * pizza_calc.js - Pizza Calculator Logic
 *
 * Handles pizza calculations, humorous progress,
 * reporting, and related actions.
 *****************************************************/

window.calculatePizzas = function () {
    const attendees = Number(document.getElementById("attendees").value) || 0;
    const pizzaType = document.getElementById("pizzaType").value;
    const slicesPerPerson = Number(document.getElementById("slicesPerPerson").value) || 0;
    const hoursDebugging = Number(document.getElementById("hoursDebugging").value) || 0;

    const resultDiv = document.getElementById("result");
    const progressBar = document.getElementById("progressBar");
    const progressLabel = document.getElementById("progressLabel");

    resultDiv.innerHTML = "";
    progressBar.style.width = "0%";
    progressLabel.textContent = "";

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
    function updatePizzaProgress() {
        if (stepIndex < loadingSteps.length) {
            let computed = ((stepIndex + 1) * (110 / loadingSteps.length));
            if (computed > 89 && stepIndex < loadingSteps.length - 1) {
                computed = 89;
            }
            progressBar.style.width = computed + "%";
            progressLabel.textContent = loadingSteps[stepIndex];
            stepIndex++;
            let delay = (computed === 89) ? 1500 : 500;
            setTimeout(updatePizzaProgress, delay);
        } else {
            progressBar.style.width = "110%";
            progressLabel.textContent = "Pizza deployment exceeded expectations. You're 110% ready to eat! 🍕🎉";
            completePizzaCalculation();
        }
    }
    updatePizzaProgress();

    function completePizzaCalculation() {
        const debuggingExtraSlices = hoursDebugging * 2;
        const totalSlicesNeeded = (attendees * slicesPerPerson) + debuggingExtraSlices;
        let pizzasRequired;
        let sliceEquivalency = 1;
        const type = pizzaType;
        if (type === "3") {
            pizzasRequired = attendees * hoursDebugging;
            finalizePizzaResult(pizzasRequired, type, slicesPerPerson, hoursDebugging, attendees, "Hot Pockets: quick, regrettable!");
            return;
        } else if (type === "cloud") {
            finalizePizzaResult(Infinity, type, slicesPerPerson, hoursDebugging, attendees, "Cloud pizza infinite cost!");
            return;
        } else if (type === "pineapple") {
            resultDiv.innerHTML = `<blockquote>WiFi Pineapple Pizza is an acquired taste. It's capturing your taste buds even as we speak. 🍍📡🍕</blockquote>`;
            return;
        }
        switch (type) {
            case "1":
                sliceEquivalency = 1;
                break;
            case "0.5":
                sliceEquivalency = 1.5;
                break;
            case "0.6":
                sliceEquivalency = 1.7;
                break;
            case "2":
                sliceEquivalency = 0.75;
                break;
            case "100":
                sliceEquivalency = (Math.random() > 0.5) ? 0.1 : 2;
                break;
            default:
                sliceEquivalency = 1;
        }
        const adjustedSlicesPerPizza = 8 * sliceEquivalency;
        pizzasRequired = Math.ceil(totalSlicesNeeded / adjustedSlicesPerPizza);
        if (type === "100") {
            finalizePizzaResult(pizzasRequired, type, slicesPerPerson, hoursDebugging, attendees, "Blockchain madness!");
            return;
        }
        const humor = getPizzaHumorMessage(pizzasRequired);
        finalizePizzaResult(pizzasRequired, type, slicesPerPerson, hoursDebugging, attendees, humor);
    }

    function finalizePizzaResult(pizzasRequired, type, slicesPerPerson, hoursDebugging, attendees, humor) {
        let displayMessage = "";
        if (type === "3") {
            displayMessage = `<blockquote>You need <strong>${pizzasRequired}</strong> Hot Pocket(s) to feed <strong>${attendees}</strong> attendees for <strong>${hoursDebugging}</strong> hours of debugging. ${humor}</blockquote>`;
        } else if (type === "cloud") {
            displayMessage = `<blockquote>Cloud Pizza can feed any number of attendees, but watch out for that infinite billing! ☁️🍕</blockquote>`;
        } else if (type === "100") {
            displayMessage = `<blockquote>You need <strong>${pizzasRequired}</strong> Blockchain Pizza(s) for <strong>${attendees}</strong> devs. ${humor} 🍕💸</blockquote>`;
        } else {
            displayMessage = `<blockquote>You need <strong>${pizzasRequired}</strong> pizza(s) for <strong>${attendees}</strong> attendees, factoring in <strong>${hoursDebugging} hours</strong> of debugging. Using style: ${document.getElementById("pizzaType").options[document.getElementById("pizzaType").selectedIndex].text}.<br><br>${humor}</blockquote>`;
        }
        resultDiv.innerHTML = displayMessage;
        const report =
            `Pizza Calculation Report\n\n` +
            `Number of Attendees: ${attendees}\n` +
            `Selected Pizza Style: ${document.getElementById("pizzaType").options[document.getElementById("pizzaType").selectedIndex].text}\n` +
            `Slices Per Person: ${slicesPerPerson}\n` +
            `Hours Debugging: ${hoursDebugging}\n` +
            `Total Pizzas Required: ${pizzasRequired}\n\n` +
            humor;
        const pre = document.createElement("pre");
        pre.textContent = report;
        resultDiv.appendChild(pre);
        performFunnyTests("Pizza");
        checkEnterpriseEmail(pizzasRequired);
    }
};

function getPizzaHumorMessage(pizzasRequired) {
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

function performFunnyTests(calculatorName) {
    console.log(`\n--- ${calculatorName} Additional Testing Suite Initiated ---`);
    console.log("[Load Test] Simulating thousands of hungry devs hitting the server for calculations...");
    console.log("[Unit Test] Checking if slices per person is not negative or infinite... Looks good!");
    console.log("[UX Test] Asking random dev if they prefer pineapple on pizza. 50% meltdown rate detected!");
    console.log(`[All Tests Passed] The ${calculatorName} Calculator is stable...ish.\n`);
}

function checkEnterpriseEmail(pizzasRequired) {
    const emailSection = document.getElementById("emailPromptSection");
    if (pizzasRequired >= 42) {
        emailSection.hidden = false;
    } else {
        emailSection.hidden = true;
    }
}

window.downloadReport = function () {
    const resultText = document.getElementById("result")?.innerText || "No result yet.";
    const report = "Pizza Calculation Report\n\n" + resultText;
    const blob = new Blob([report], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Pizza_Calculation_Report.txt";
    a.click();
};

window.submitEmail = function () {
    const email = document.getElementById("emailInput").value;
    if (!email) {
        showToast("Please enter a valid email!");
        return;
    }
    console.log(`Enterprise pizza inquiry from: ${email}`);
    showToast("Thanks! Our Enterprise Pizza Sales Team will contact you soon.");
};
