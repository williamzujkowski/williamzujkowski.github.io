/**
 * joke-generator.js - Programming joke generator component
 *
 * Enhanced with local fallback jokes in case the API is unavailable
 */

import { $ } from "../utils/dom.js";

export function initJokeGenerator() {
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

    jokeSetup.textContent = "Loading...";
    jokeDelivery.textContent = "";
    jokeSingle.textContent = "";
    jokeContainer.classList.add("opacity-50");
  }

  // Function to show loading state - mobile
  function showMobileLoading() {
    if (!mobileJokeSetup) return;

    mobileJokeSetup.textContent = "Loading...";
    mobileJokeDelivery.textContent = "";
    mobileJokeSingle.textContent = "";
    mobileJokeContainer.classList.add("opacity-50");
  }

  // Function to display a joke - desktop
  function displayDesktopJoke(joke) {
    if (!jokeContainer) return;

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
    // Show loading on desktop view if elements exist
    if (jokeSetup) showLoading();
    // Show loading on mobile view if elements exist
    if (mobileJokeSetup) showMobileLoading();

    // Try the API first with a timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 second timeout

    fetch(
      "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit",
      { signal: controller.signal }
    )
      .then((response) => {
        clearTimeout(timeoutId);
        if (!response.ok) {
          throw new Error("API response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Display the joke from the API
        displayDesktopJoke(data);
        displayMobileJoke(data);
      })
      .catch((error) => {
        console.warn("Using fallback joke due to API error:", error.message);

        // Use a fallback joke instead
        const fallbackJoke = getRandomFallbackJoke();
        displayDesktopJoke(fallbackJoke);
        displayMobileJoke(fallbackJoke);
      });
  }

  // Initialize the component
  function init() {
    // Initial joke fetch
    fetchJoke();

    // Event listeners for desktop view
    if (newJokeBtn) {
      newJokeBtn.addEventListener("click", fetchJoke);
    }

    // Event listeners for mobile view
    if (mobileNewJokeBtn) {
      mobileNewJokeBtn.addEventListener("click", fetchJoke);
    }
  }

  // Only initialize if at least one of the containers exists
  if (jokeContainer || mobileJokeContainer) {
    init();
  }
}
