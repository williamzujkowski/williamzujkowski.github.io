/**
 * joke-generator.js - Programming joke generator component
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

  // Function to fetch a new joke
  function fetchJoke() {
    // Show loading on desktop view if elements exist
    if (jokeSetup) showLoading();
    // Show loading on mobile view if elements exist
    if (mobileJokeSetup) showMobileLoading();

    fetch(
      "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
    )
      .then((response) => response.json())
      .then((data) => {
        // Update desktop view if elements exist
        if (jokeContainer) {
          jokeContainer.classList.remove("opacity-50");

          if (data.type === "twopart") {
            jokeSetup.textContent = data.setup;
            jokeDelivery.textContent = data.delivery;
            jokeSingle.textContent = "";
          } else {
            jokeSetup.textContent = "";
            jokeDelivery.textContent = "";
            jokeSingle.textContent = data.joke;
          }
        }

        // Update mobile view if elements exist
        if (mobileJokeContainer) {
          mobileJokeContainer.classList.remove("opacity-50");

          if (data.type === "twopart") {
            mobileJokeSetup.textContent = data.setup;
            mobileJokeDelivery.textContent = data.delivery;
            mobileJokeSingle.textContent = "";
          } else {
            mobileJokeSetup.textContent = "";
            mobileJokeDelivery.textContent = "";
            mobileJokeSingle.textContent = data.joke;
          }
        }
      })
      .catch((error) => {
        // Handle errors for desktop view
        if (jokeContainer) {
          jokeContainer.classList.remove("opacity-50");
          jokeSetup.textContent = "Error loading joke";
          jokeDelivery.textContent = "";
          jokeSingle.textContent = "Please try again";
        }

        // Handle errors for mobile view
        if (mobileJokeContainer) {
          mobileJokeContainer.classList.remove("opacity-50");
          mobileJokeSetup.textContent = "Error loading joke";
          mobileJokeDelivery.textContent = "";
          mobileJokeSingle.textContent = "Please try again";
        }

        console.error("Error fetching joke:", error);
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
