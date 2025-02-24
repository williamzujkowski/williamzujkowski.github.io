# William Zujkowski’s Personal Website

Welcome to the repository for my personal website! This refactored version uses semantic HTML with a minimal, responsive CSS style (powered by OKLCH–based colors) and modular JavaScript. Core site functions (navigation, footer, Konami code, back-to-top, etc.) are in `assets/js/main.js` while the interactive Coffee and Pizza calculators are in `assets/js/coffee_calc.js` and `assets/js/pizza_calc.js` respectively.

## Key Features

- **Modular JavaScript:**  
  Core site logic is in `assets/js/main.js` and the calculators have their own modules.
  
- **Modern OKLCH Colors:**  
  The CSS uses OKLCH color values for a perceptually uniform color palette across the site.
  
- **Consistent, Responsive Design:**  
  All pages use the shared stylesheet (`assets/css/styles.css`).

- **Interactive Calculators:**  
  Both calculators feature humorous progress animations that mimic your old site’s behavior (progress bar hangs at 89% and then jumps to 110%), along with detailed reports and witty messages.

- **Easter Egg:**  
  Enter the Konami code (↑ ↑ ↓ ↓ ← → ← → B A) on any page to reveal a secret!

## How It Works

- **Core Logic:**  
  `main.js` handles navigation, footer injection, the Konami code Easter egg, and the back-to-top button.

- **Calculators:**  
  `coffee_calc.js` and `pizza_calc.js` contain the interactive logic. They use a progress update function that calculates a computed percentage for each step; if the computed percentage is above 89% (but not the final step), it is forced to 89%, then after a delay the final step jumps the progress bar to 110%.

Enjoy exploring, coding, and indulging in some pizza and coffee!