/**
 * joke-generator.js - Programming joke generator component
 *
 * Enhanced with debug logging and more robust fallback mechanism
 */

import { $ } from "../utils/dom.js";

export function initJokeGenerator() {
  // Add debug message to verify component is being loaded
  console.log("Joke Generator initialized at:", new Date().toISOString());

  const jokeSetup = $("#joke-setup");
  const jokeDelivery = $("#joke-delivery");
  const jokeSingle = $("#joke-single");
  const jokeContainer = $("#joke-container");
  const newJokeBtn = $("#new-joke-btn");

  // For mobile view
  const mobileJokeSetup = $("#mobile-joke-setup");
  const mobileJokeDelivery = $("#mobile-joke-delivery");
  const mobileJokeSingle = $("#mobile-joke-single");
  const mobileJokeContainer = $("#mobile-joke-container");
  const mobileNewJokeBtn = $("#mobile-new-joke-btn");

  // Log which DOM elements were found
  console.log("DOM Elements found:", {
    "Desktop container": !!jokeContainer,
    "Desktop setup": !!jokeSetup,
    "Desktop delivery": !!jokeDelivery,
    "Desktop single": !!jokeSingle,
    "Desktop button": !!newJokeBtn,
    "Mobile container": !!mobileJokeContainer,
    "Mobile setup": !!mobileJokeSetup,
    "Mobile delivery": !!mobileJokeDelivery,
    "Mobile single": !!mobileJokeSingle,
    "Mobile button": !!mobileNewJokeBtn,
  });

  // Fallback jokes in case the API is unavailable
  const fallbackJokes = [
    {
      type: "twopart",
      setup: "Why do programmers prefer dark mode?",
      delivery: "Because light attracts bugs!",
    },
    {
      type: "twopart",
      setup: "Why do Java developers wear glasses?",
      delivery: "Because they can't C#!",
    },
    {
      type: "single",
      joke: "There are 10 types of people in this world: those who understand binary and those who don't.",
    },
    {
      type: "twopart",
      setup: "How many programmers does it take to change a light bulb?",
      delivery: "None, that's a hardware problem.",
    },
    {
      type: "single",
      joke: "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
    },
    {
      type: "twopart",
      setup: "Why did the developer go broke?",
      delivery: "Because they used up all their cache!",
    },
    {
      type: "single",
      joke: "Debugging is like being the detective in a crime movie where you're also the murderer.",
    },
    {
      type: "twopart",
      setup: "Why was the JavaScript developer sad?",
      delivery: "Because they didn't Node how to Express themselves!",
    },
  ];

  // Function to show loading state - desktop
  function showLoading() {
    if (!jokeSetup) return;

    jokeSetup.textContent = "Loading joke...";
    jokeDelivery.textContent = "";
    jokeSingle.textContent = "";
    jokeContainer.classList.add("opacity-50");
  }

  // Function to show loading state - mobile
  function showMobileLoading() {
    if (!mobileJokeSetup) return;

    mobileJokeSetup.textContent = "Loading joke...";
    mobileJokeDelivery.textContent = "";
    mobileJokeSingle.textContent = "";
    mobileJokeContainer.classList.add("opacity-50");
  }

  // Function to display a joke - desktop
  function displayDesktopJoke(joke) {
    if (!jokeContainer) return;

    console.log("Displaying desktop joke:", joke);
    jokeContainer.classList.remove("opacity-50");

    if (joke.type === "twopart") {
      jokeSetup.textContent = joke.setup;
      jokeDelivery.textContent = joke.delivery;
      jokeSingle.textContent = "";
    } else {
      jokeSetup.textContent = "";
      jokeDelivery.textContent = "";
      jokeSingle.textContent = joke.joke;
    }
  }

  // Function to display a joke - mobile
  function displayMobileJoke(joke) {
    if (!mobileJokeContainer) return;

    console.log("Displaying mobile joke:", joke);
    mobileJokeContainer.classList.remove("opacity-50");

    if (joke.type === "twopart") {
      mobileJokeSetup.textContent = joke.setup;
      mobileJokeDelivery.textContent = joke.delivery;
      mobileJokeSingle.textContent = "";
    } else {
      mobileJokeSetup.textContent = "";
      mobileJokeDelivery.textContent = "";
      mobileJokeSingle.textContent = joke.joke;
    }
  }

  // Function to get a random fallback joke
  function getRandomFallbackJoke() {
    const randomIndex = Math.floor(Math.random() * fallbackJokes.length);
    return fallbackJokes[randomIndex];
  }

  // Function to fetch a new joke
  function fetchJoke() {
    console.log("Fetching joke at:", new Date().toISOString());

    // Show loading on desktop view if elements exist
    if (jokeSetup) showLoading();
    // Show loading on mobile view if elements exist
    if (mobileJokeSetup) showMobileLoading();

    // Try the API to get a dynamic joke (will replace fallback if successful)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 second timeout

    fetch(
      "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit",
      { signal: controller.signal }
    )
      .then((response) => {
        clearTimeout(timeoutId);
        console.log("API Response status:", response.status);
        if (!response.ok) {
          throw new Error("API response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("API Response data:", data);

        // Display the joke from the API
        displayDesktopJoke(data);
        displayMobileJoke(data);
      })
      .catch((error) => {
        console.warn("API error, using fallback joke:", error.message);

        // Use fallback joke if API fails
        const fallbackJoke = getRandomFallbackJoke();
        displayDesktopJoke(fallbackJoke);
        displayMobileJoke(fallbackJoke);
      });
  }

  // Initialize the component
  function init() {
    console.log("Initializing joke component");

    // Initial joke fetch
    fetchJoke();

    // Event listeners for desktop view
    if (newJokeBtn) {
      console.log("Adding desktop button click listener");
      newJokeBtn.addEventListener("click", fetchJoke);
    }

    // Event listeners for mobile view
    if (mobileNewJokeBtn) {
      console.log("Adding mobile button click listener");
      mobileNewJokeBtn.addEventListener("click", fetchJoke);
    }
  }

  // Only initialize if at least one of the containers exists
  if (jokeContainer || mobileJokeContainer) {
    console.log("At least one container found, initializing...");
    init();
  } else {
    console.warn("No joke containers found on page");
  }
}

// Call initJokeGenerator directly to ensure it runs
// This is in addition to the dynamic import in main.js
if (typeof window !== "undefined") {
  console.log("Self-initializing joke generator");
  // Use setTimeout to ensure DOM is ready
  setTimeout(() => {
    initJokeGenerator();
  }, 1000);

  // Expose fetchJoke to window for page refresh
  window.fetchJokeRefresh = fetchJoke;
}
