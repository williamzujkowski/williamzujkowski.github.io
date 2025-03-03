document.addEventListener("DOMContentLoaded", function () {
  loadComponent("includes/header.html", "header-placeholder");
  loadComponent("includes/nav.html", "nav-placeholder");
  loadComponent("includes/footer.html", "footer-placeholder");
  loadRecentBlogPosts();
});

function loadComponent(url, elementId) {
  fetch(url)
    .then(response => response.text())
    .then(html => {
      document.getElementById(elementId).innerHTML = html;
    })
    .catch(error => {
      console.error("Error loading component: " + url, error);
    });
}

// NEW: Dynamically load recent blog posts from blog_data.html
function loadRecentBlogPosts() {
  fetch("blog_data.html")
    .then(response => response.text())
    .then(data => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, "text/html");
      let articles = Array.from(doc.querySelectorAll("article"));
      // Sort articles by data-date (most recent first)
      articles.sort((a, b) => new Date(b.getAttribute("data-date")) - new Date(a.getAttribute("data-date")));
      // Take the top three posts
      const recent = articles.slice(0, 3);
      const listDiv = document.getElementById("recent-blog-list");
      if (listDiv) {
        recent.forEach(article => {
          const titleElement = article.querySelector("h2");
          if (!titleElement) return;
          const title = titleElement.innerText;
          const date = article.getAttribute("data-date");
          const slug = article.getAttribute("data-slug") || "";
          const link = document.createElement("a");
          // Assuming blog posts are linked via blog.html#slug
          link.href = "blog.html#" + slug;
          link.innerText = `${title} (${date})`;
          const p = document.createElement("p");
          p.appendChild(link);
          listDiv.appendChild(p);
        });
      }
    })
    .catch(error => {
      console.error("Error loading recent blog posts:", error);
    });
}

// Coffee Calculator Logic with IT Humor
function calculateCoffee() {
  try {
    const devs = parseInt(document.getElementById("javaAttendees").value) || 0;
    const strength = parseFloat(document.getElementById("coffeeStrength").value) || 1;
    const hours = parseFloat(document.getElementById("hoursCoding").value) || 0;
    const failures = parseInt(document.getElementById("timesBuildFailed").value) || 0;

    if (devs <= 0 || hours <= 0) {
      document.getElementById("coffeeResult").innerText =
        "Please enter valid numbers for devs and coding hours. Even a toaster can code, but not without coffee!";
      return;
    }

    // Base need is proportional to dev count and hours, with an extra cup per build failure
    const baseNeed = devs * hours;
    const penalty = failures; // each failure adds one cup for the team
    // Higher coffee strength means fewer cups needed per dev
    const totalCups = Math.ceil((baseNeed + penalty) / strength);

    let message = "";
    if (totalCups < devs) {
      message = "Your coffee is so strong, it might just refactor your code for you!";
    } else if (totalCups === devs) {
      message = "Just enough coffee for each dev to stay awake, but not enough to start debugging themselves!";
    } else {
      message = "Warning: Your coffee requirements exceed available supply. Time to refactor your caffeine dependencies!";
    }
    document.getElementById("coffeeResult").innerText =
      `Estimated cups of coffee needed: ${totalCups}\n${message}`;
  } catch (e) {
    console.error("Error in calculateCoffee:", e);
    document.getElementById("coffeeResult").innerText =
      "An error occurred while calculating coffee. Please try again.";
  }
}

function downloadCoffeeReport() {
  try {
    const devs = document.getElementById("javaAttendees").value;
    const strength = document.getElementById("coffeeStrength").value;
    const hours = document.getElementById("hoursCoding").value;
    const failures = document.getElementById("timesBuildFailed").value;
    const resultText = document.getElementById("coffeeResult").innerText;
    const report = `Coffee Calculator Report
---------------------------
Number of Devs: ${devs}
Coffee Strength: ${strength}
Hours Coding: ${hours}
Times Build Failed: ${failures}

Result:
${resultText}

Remember: Strong coffee means fewer cups per person, because it's like debugging with a superpower!`;
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.getElementById("downloadCoffeeLink");
    link.href = url;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (e) {
    console.error("Error in downloadCoffeeReport:", e);
    alert("Error generating coffee report. Please try again.");
  }
}

function shareCoffeeReport() {
  try {
    const devs = document.getElementById("javaAttendees").value;
    const strength = document.getElementById("coffeeStrength").value;
    const hours = document.getElementById("hoursCoding").value;
    const failures = document.getElementById("timesBuildFailed").value;
    const resultText = document.getElementById("coffeeResult").innerText;
    const report = `Coffee Calculator Report
---------------------------
Number of Devs: ${devs}
Coffee Strength: ${strength}
Hours Coding: ${hours}
Times Build Failed: ${failures}

Result:
${resultText}

Enjoy your brew!`;
    navigator.clipboard.writeText(report).then(() => {
      alert("Coffee report copied to clipboard! Now go share the caffeine love.");
    }).catch(err => {
      alert("Failed to copy report: " + err);
    });
  } catch (e) {
    console.error("Error in shareCoffeeReport:", e);
    alert("Error sharing coffee report. Please try again.");
  }
}

// Pizza Calculator Logic with IT Humor
function calculatePizzas() {
  try {
    const attendees = parseInt(document.getElementById("attendees").value) || 0;
    const pizzaTypeValue = document.getElementById("pizzaType").value;
    const slicesPerPerson = parseFloat(document.getElementById("slicesPerPerson").value) || 1;
    const hoursDebugging = parseFloat(document.getElementById("hoursDebugging").value) || 0;

    if (attendees <= 0) {
      document.getElementById("result").innerText =
        "No attendees? Even a lone coder deserves a slice!";
      return;
    }
    if (isNaN(slicesPerPerson) || slicesPerPerson <= 0) {
      document.getElementById("result").innerText =
        "Please enter a valid number for slices per person.";
      return;
    }

    // Handle special "Cloud Pizza" option
    if (pizzaTypeValue === "cloud") {
      document.getElementById("result").innerText =
        "Cloud Pizza detected: It might vanish before you order it. Please select a real pizza type.";
      return;
    }

    const pizzaFactor = parseFloat(pizzaTypeValue);
    if (isNaN(pizzaFactor) || pizzaFactor <= 0) {
      document.getElementById("result").innerText =
        "Invalid pizza type factor. Please try again.";
      return;
    }

    // Assume a standard NY pizza has 8 slices; adjust by the selected pizza factor
    const baseSlices = 8 * pizzaFactor;
    // Total required slices include a bonus for debugging frustration (0.5 slice per dev per debugging hour)
    const totalSlices = (attendees * slicesPerPerson) + (attendees * hoursDebugging * 0.5);
    const pizzasNeeded = Math.ceil(totalSlices / baseSlices);

    let message = "";
    if (pizzasNeeded < attendees) {
      message = "Your pizza order is so optimized, it's like your code got refactored by a DevOps ninja!";
    } else if (pizzasNeeded === attendees) {
      message = "One pizza per dev? Just enough to keep the bug reports at bay... or maybe not!";
    } else {
      message = "Warning: Your pizza requirement might cause a fork() in the system! Better double-check your dependencies.";
    }

    document.getElementById("result").innerText =
      `Estimated number of pizzas needed: ${pizzasNeeded}\n${message}`;

    // If the order is massive (42 pizzas or more), show the email prompt for enterprise orders
    const emailPromptSection = document.getElementById("emailPromptSection");
    if (pizzasNeeded >= 42) {
      emailPromptSection.hidden = false;
    } else {
      emailPromptSection.hidden = true;
    }
  } catch (e) {
    console.error("Error in calculatePizzas:", e);
    document.getElementById("result").innerText =
      "An error occurred while calculating pizzas. Please try again.";
  }
}

function downloadReport() {
  try {
    const attendees = document.getElementById("attendees").value;
    const pizzaType = document.getElementById("pizzaType").value;
    const slicesPerPerson = document.getElementById("slicesPerPerson").value;
    const hoursDebugging = document.getElementById("hoursDebugging").value;
    const resultText = document.getElementById("result").innerText;
    const report = `Pizza Calculator Report
---------------------------
Number of Attendees: ${attendees}
Pizza Type Factor: ${pizzaType}
Average Slices per Person: ${slicesPerPerson}
Hours Spent Debugging: ${hoursDebugging}

Result:
${resultText}

Remember: Even in the code of life, never hardcode your pizza orders!`;
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const tempLink = document.createElement("a");
    tempLink.href = url;
    tempLink.download = "Pizza_Calculation_Report.txt";
    document.body.appendChild(tempLink);
    tempLink.click();
    document.body.removeChild(tempLink);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (e) {
    console.error("Error in downloadReport:", e);
    alert("Error generating pizza report. Please try again.");
  }
}

function submitEmail() {
  try {
    const email = document.getElementById("emailInput").value;
    if (email.trim() === "") {
      alert("Please enter a valid email address.");
      return;
    }
    alert(`Email ${email} submitted. Our Enterprise Pizza Sales Team will contact you shortly about your massive order.`);
    document.getElementById("emailPromptSection").hidden = true;
  } catch (e) {
    console.error("Error in submitEmail:", e);
    alert("Error submitting email. Please try again.");
  }
}
