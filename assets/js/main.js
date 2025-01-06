// assets/js/main.js
// Our aggregator module that imports everything and sets it up.

import { initNavFooter } from './navFooter.js';
import { initPizzaCalculator } from './pizzaCalc.js';
import { initCoffeeCalculator } from './coffeeCalc.js';
import { initBlogLogic } from './blogLogic.js';
import { initSecretToggles } from './secretToggles.js';

document.addEventListener('DOMContentLoaded', () => {
  // Initialize nav + footer
  initNavFooter();

  // Initialize pizza calc if on pizza.html
  initPizzaCalculator();

  // Initialize coffee calc if on coffee.html
  initCoffeeCalculator();

  // Initialize blog logic for index + blog.html
  initBlogLogic();

  // Initialize Easter eggs
  initSecretToggles();

  // Friendly console greeting
  console.log(
    "%c\n" +
    " grenlan.com is loading...                \n" +
    "\nHello there, console explorer! Keep up the curiosity!\n",
    "color: green; font-family: monospace;"
  );
});
