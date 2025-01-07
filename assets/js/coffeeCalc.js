// assets/js/coffeeCalc.js

export function initCoffeeCalculator() {
    if (!document.getElementById('coffeeForm')) {
        return;
    }

    let coffeeCalculationCompleted = false;
    let coffeeReport = "";

    async function loadCoffeeDefaults() {
        const storedDevs = await localStorage.getItem('coffeeDevs');
        const storedStrength = await localStorage.getItem('coffeeStrength');
        const storedHours = await localStorage.getItem('coffeeHours');
        const storedFails = await localStorage.getItem('coffeeFails');

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
        if (progressBar) progressBar.value = 0;
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
                let percentage = (stepIndex + 1) * (100 / coffeeSteps.length);
                if (progressBar) progressBar.value = percentage;
                if (progressLabel) progressLabel.textContent = coffeeSteps[stepIndex];
                stepIndex++;
                if (percentage === 75) {
                    setTimeout(updateProgress, 1500);
                } else {
                    setTimeout(updateProgress, 500);
                }
            } else {
                if (progressBar) progressBar.value = 100;
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
            humor = "You have a decent coffee setup. Ensure your brew pipeline has no single points of failure!";
        } else if (totalCups > 5) {
            humor = "Enough coffee to keep the devs awake—at least until the next all-nighter!";
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

        const downloadCoffeeLink = document.createElement('a');
        downloadCoffeeLink.id = 'downloadCoffeeLink';
        downloadCoffeeLink.href = url;
        downloadCoffeeLink.download = 'Coffee_Calculation_Report.txt';
        document.body.appendChild(downloadCoffeeLink);
        downloadCoffeeLink.click();
        document.body.removeChild(downloadCoffeeLink);
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

    window.showToast = function (message) {
        const toast = document.getElementById('toast');
        if (!toast) return;
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    };
}
