/*****************************************************
 * coffee_calc.js - Coffee Calculator Logic
 *
 * Handles coffee calculations, humorous progress,
 * reporting, and related actions.
 *****************************************************/

window.calculateCoffee = function () {
    const devs = Number(document.getElementById("javaAttendees").value) || 0;
    const strength = Number(document.getElementById("coffeeStrength").value) || 1;
    const hours = Number(document.getElementById("hoursCoding").value) || 0;
    const fails = Number(document.getElementById("timesBuildFailed").value) || 0;

    const coffeeResult = document.getElementById("coffeeResult");
    const progressBar = document.getElementById("progressBar");
    const progressLabel = document.getElementById("progressLabel");

    // Reset displays
    progressBar.style.width = "0%";
    progressLabel.textContent = "";
    coffeeResult.innerHTML = "";

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
    function updateCoffeeProgress() {
        if (stepIndex < coffeeSteps.length) {
            // Compute percentage based on steps; final step should jump to 110%
            let computed = ((stepIndex + 1) * (110 / coffeeSteps.length));
            // If not final step and computed percentage is between 89 and 110, force it to 89%
            if (computed > 89 && stepIndex < coffeeSteps.length - 1) {
                computed = 89;
            }
            progressBar.style.width = computed + "%";
            progressLabel.textContent = coffeeSteps[stepIndex];
            stepIndex++;
            // Use a longer delay if we forced the hang at 89%
            let delay = (computed === 89) ? 1500 : 500;
            setTimeout(updateCoffeeProgress, delay);
        } else {
            progressBar.style.width = "110%";
            progressLabel.textContent = "Coffee is brewed to perfection. ☕🎉";
            finalizeCoffeeCalc();
        }
    }
    updateCoffeeProgress();

    function finalizeCoffeeCalc() {
        const baseCups = (devs * hours) / strength;
        const additionalCups = fails * 2;
        const totalCups = Math.ceil(baseCups + additionalCups);
        const message = getCoffeeMessage(totalCups, devs, strength, hours, fails);
        coffeeResult.innerHTML = message;
        const report =
            `Coffee Calculation Report\n\n` +
            `Number of Devs: ${devs}\n` +
            `Coffee Strength Factor: ${strength}\n` +
            `Hours of Coding: ${hours}\n` +
            `Times Build Failed: ${fails}\n` +
            `Total Cups Recommended: ${totalCups}\n\n` +
            `Stay caffeinated and code on!`;
        const pre = document.createElement("pre");
        pre.textContent = report;
        coffeeResult.appendChild(pre);
        performFunnyCoffeeTests();
    }
};

function getCoffeeMessage(totalCups, devs, strength, hours, fails) {
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
    return `<blockquote>You need approximately <strong>${totalCups}</strong> cup(s) of coffee to sustain <strong>${devs}</strong> dev(s) for <strong>${hours}</strong> hour(s). Coffee strength factor: <strong>${strength}</strong>, plus <strong>${fails * 2}</strong> extra cups for <strong>${fails}</strong> build failures.<br><br>${humor}</blockquote>`;
}

function performFunnyCoffeeTests() {
    console.log("\n--- Coffee Additional Testing Suite Initiated ---");
    console.log("[Load Test] Simulating the entire dev team brewing coffee at 2 AM simultaneously...");
    console.log("[Unit Test] Verifying that coffee cups do not exceed OSHA safe levels of caffeine...");
    console.log("[UX Test] Observing devs shaking from caffeine overload while rewriting code in 15 languages...");
    console.log("[Security Test] Attempting to stash contraband donuts in the coffee filter. Denied!");
    console.log("[All Tests Passed] The Coffee Calculator is dangerously effective.\n");
}

window.downloadCoffeeReport = function () {
    const coffeeResultText = document.getElementById("coffeeResult").innerText;
    const report = "Coffee Calculation Report\n\n" + coffeeResultText;
    const blob = new Blob([report], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Coffee_Calculation_Report.txt";
    a.click();
    URL.revokeObjectURL(url);
};

window.shareCoffeeReport = function () {
    console.log("Shared coffee report with the world!");
    showToast("Shared the coffee report with your teammates!");
};
