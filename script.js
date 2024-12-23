let calculationCompleted = false; // Flag to track if calculation is completed

function calculatePizzas() {
    const attendeesInput = document.getElementById('attendees');
    const pizzaTypeInput = document.getElementById('pizzaType');
    const hoursDebuggingInput = document.getElementById('hoursDebugging');
    const slicesPerPersonInput = document.getElementById('slicesPerPerson');
    const resultDiv = document.getElementById('result');
    const emailPromptSection = document.getElementById('emailPromptSection');
    const progressBar = document.getElementById('progressBar');
    const progressLabel = document.getElementById('progressLabel');

    // Reset progress and calculation flag
    progressBar.style.width = '0%';
    progressLabel.innerHTML = '';
    calculationCompleted = false;
    resultDiv.innerHTML = '';
    emailPromptSection.style.display = 'none';

    const loadingSteps = [
        "Analyzing hunger coefficients based on debugging hours...",
        "Contacting Gilfoyle’s pizza orchestration server...",
        "Running middle-out slice allocation algorithm...",
        "Optimizing pizza cluster for maximum throughput...",
        "Spinning up pizza instances on AWS...",
        "Finalizing pizza load balancer configuration...",
        "Pizzas deployed. Load balancer is slicing evenly across all clusters."
    ];

    let stepIndex = 0;

    // Function to update progress bar and show messages
    function updateProgress() {
        if (stepIndex < loadingSteps.length) {
            let percentage = (stepIndex + 1) * 15;
            if (percentage > 75 && percentage < 100) {
                percentage = 75;
            }
            progressBar.style.width = `${percentage}%`;
            progressLabel.innerHTML = loadingSteps[stepIndex];
            stepIndex++;

            if (percentage === 75) {
                setTimeout(updateProgress, 1500); // Delay longer when "stuck" at 75%
            } else {
                setTimeout(updateProgress, 500); // Normal delay between steps
            }
        } else {
            progressBar.style.width = '110%';
            progressLabel.innerHTML = "Pizza deployment exceeded expectations. You are now 110% ready to eat! 🍕🎉";
            completeCalculation();
        }
    }

    updateProgress();

    function completeCalculation() {
        const hoursDebugging = parseInt(hoursDebuggingInput.value);
        const slicesPerPerson = parseInt(slicesPerPersonInput.value);
        const debuggingExtraSlices = hoursDebugging * 2; // Each hour of debugging adds 2 slices to the total
        const attendees = parseInt(attendeesInput.value);

        // Total slices needed considering slices per person plus debugging overhead
        const totalSlicesNeeded = (attendees * slicesPerPerson) + debuggingExtraSlices;

        let pizzasRequired;
        let sliceEquivalency = 1;
        const pizzaType = pizzaTypeInput.value;
        const slicesPerPizza = 8; // Base slices in a standard pizza

        // Switch on pizza type
        switch (pizzaType) {
            case "1": // NY Pizza
                sliceEquivalency = 1;
                break;
            case "0.5": // Detroit Pizza
                sliceEquivalency = 1.5; // Each slice is more filling
                break;
            case "0.6": // Chicago Pizza
                sliceEquivalency = 1.7; // Each slice is even more filling
                break;
            case "2": // California Pizza
                sliceEquivalency = 0.75; // Less filling slices
                break;
            case "100": // Blockchain Pizza
                // Random worth: either almost nothing or a lot
                sliceEquivalency = Math.random() > 0.5 ? 0.1 : 2;
                break;
            case "3": // Hot Pockets
                pizzasRequired = attendees * hoursDebugging;
                resultDiv.innerHTML = `<blockquote><p>You need <strong>${pizzasRequired}</strong> Hot Pocket(s) to feed <strong>${attendees}</strong> attendees for <strong>${hoursDebugging}</strong> hours of debugging. Hot Pockets: like server downtime—unexpected and regrettable. 🥵</p></blockquote>`;
                calculationCompleted = true;
                checkEnterpriseEmail(pizzasRequired);
                return;
            case "cloud": // Cloud Pizza
                resultDiv.innerHTML = `<blockquote><p>Cloud Pizza can feed any number of attendees for any duration. Like the cloud, it auto-scales to feed everyone, but the charges will be just as unpredictable! ☁️🍕</p></blockquote>`;
                calculationCompleted = true;
                // Possibly show enterprise if we consider infinite pizzas? Not doing so by default
                return;
            case "pineapple": // (Not in select but left in code for Easter egg possibility)
                resultDiv.innerHTML = `<blockquote><p>WiFi Pineapple Pizza is highly divisive! Loved by some for its tangy, tropical flavor, but beware—it might just capture all your taste buds without you even realizing it. 🍍📡🍕</p></blockquote>`;
                calculationCompleted = true;
                return;
        }

        const adjustedSlicesPerPizza = slicesPerPizza * sliceEquivalency;
        pizzasRequired = Math.ceil(totalSlicesNeeded / adjustedSlicesPerPizza);

        if (pizzaType === "100") {
            resultDiv.innerHTML = `<blockquote><p>You need <strong>${pizzasRequired}</strong> Blockchain Pizza(s) for <strong>${attendees}</strong> attendees. The value of each slice fluctuates wildly—one slice might change the world, while the next one could just crash your appetite. 🍕💸💥</p></blockquote>`;
            calculationCompleted = true;
            checkEnterpriseEmail(pizzasRequired);
            return;
        }

        let humorMessage = getHumorMessage(pizzasRequired);

        resultDiv.innerHTML = `<blockquote><p>You need <strong>${pizzasRequired}</strong> pizza(s) for <strong>${attendees}</strong> attendees, adjusted for <strong>${hoursDebugging} hours</strong> of debugging. Using <strong>${pizzaTypeInput.options[pizzaTypeInput.selectedIndex].text}</strong>.</p><p>${humorMessage}</p></blockquote>`;

        // Build a text report for "Download Report" function
        window.calculationResult = `Pizza Calculation Report\n\n` +
            `Number of Attendees: ${attendees}\n` +
            `Selected Pizza Style: ${pizzaTypeInput.options[pizzaTypeInput.selectedIndex].text}\n` +
            `Slices Per Person: ${slicesPerPerson}\n` +
            `Hours Debugging: ${hoursDebugging}\n` +
            `Total Pizzas Required: ${pizzasRequired}\n\n` +
            `${humorMessage}`;

        calculationCompleted = true;
        checkEnterpriseEmail(pizzasRequired);
    }
}

function checkEnterpriseEmail(pizzasRequired) {
    const emailPromptSection = document.getElementById('emailPromptSection');
    if (pizzasRequired >= 42) {
        emailPromptSection.style.display = 'block';
    } else {
        emailPromptSection.style.display = 'none';
    }
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = "toast show";
    setTimeout(() => {
        toast.className = toast.className.replace("show", "");
    }, 3000);
}

function downloadReport() {
    if (!calculationCompleted || !window.calculationResult) {
        showToast("Please perform a calculation first!");
        return;
    }

    const blob = new Blob([window.calculationResult], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Pizza_Calculation_Report.txt';
    a.click();
    URL.revokeObjectURL(url);
}

function getHumorMessage(pizzasRequired) {
    if (pizzasRequired >= 42) {
        return "You've reached Pied Piper-level scaling! Contact our Enterprise Pizza Sales Team for multi-cluster pizza solutions, featuring pizza load balancing, distributed slices, and fault-tolerant toppings! 🍕📞";
    } else if (pizzasRequired > 20 && pizzasRequired < 42) {
        return "Caution: Pizza overload detected! You’re approaching the Hooli compression limit. Prepare for mass consumption. Consider upgrading to Pizza++ for enhanced slice delivery and reduced latency. 🍕🛠️";
    } else if (pizzasRequired > 10) {
        return "Wow, that’s a serious pizza cluster! Make sure to optimize your pizza slice distribution or face serious downtime. Remember, you can always offload some slices to the cloud. ☁️🍕";
    } else if (pizzasRequired > 5) {
        return "That’s a respectable amount of pizza. Ensure your horizontal slice scaling strategy is on point, and monitor your pizza logs closely for signs of impending food coma. 📊🍕";
    } else if (pizzasRequired > 3) {
        return "Looks like a solid order, but make sure to account for burst pizza demands during peak debugging times. For high-availability pizza service, consider a multi-zone pizza distribution strategy. 🍕🔄";
    } else if (pizzasRequired === 1) {
        return "Just one pizza? That’s like running a production server on a Raspberry Pi—light, efficient, but might not handle the full load! Consider adding redundancy with a second pizza. 🎛️🍕";
    } else {
        return "Minimal pizza order detected. For proper disaster recovery, consider at least doubling your order to avoid slice shortages during critical phases of debugging. 📦🍕";
    }
}

function submitEmail() {
    const email = document.getElementById('emailInput').value;
    if (email.trim() === "") {
        showToast("Please enter a valid email!");
        return;
    }
    // In a real scenario, you'd send this to a server via AJAX or fetch()
    console.log(`Enterprise pizza inquiry from: ${email}`);
    showToast("Thanks! Our Enterprise Pizza Sales Team will contact you soon.");
}
