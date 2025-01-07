// assets/js/main.js

import { initNavFooter } from './navFooter.js';
import { initPizzaCalculator } from './pizzaCalc.js';
import { initCoffeeCalculator } from './coffeeCalc.js';
import { initBlogLogic } from './blogLogic.js';
import { initSecretToggles } from './secretToggles.js';

document.addEventListener('DOMContentLoaded', () => {
  initNavFooter();
  initPizzaCalculator();
  initCoffeeCalculator();
  initBlogLogic();
  initSecretToggles();

  console.log(
    "%c\n" +
    " grenlan.com is loading...                \n" +
    "\nHello there, console explorer! Keep up the curiosity!\n",
    "color: green; font-family: monospace;"
  );
});
