/**
 * joke-generator.bundle.js - Bundled Programming joke generator component
 */

(function () {
  /**
   * joke-generator.js - Programming joke generator component
   *
   * Enhanced with debug logging and more robust fallback mechanism
   */

  // Use a more robust selector for compatibility
  function $(selector) {
    return document.querySelector(selector);
  }

  function initJokeGenerator() {
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
        category: "Programming",
      },
      {
        type: "twopart",
        setup: "Why do Java developers wear glasses?",
        delivery: "Because they can't C#!",
        category: "Programming",
      },
      {
        type: "single",
        joke: "There are 10 types of people in this world: those who understand binary and those who don't.",
        category: "Programming",
      },
      {
        type: "twopart",
        setup: "How many programmers does it take to change a light bulb?",
        delivery: "None, that's a hardware problem.",
        category: "Programming",
      },
      {
        type: "single",
        joke: "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
        category: "Programming",
      },
      {
        type: "twopart",
        setup: "Why did the developer go broke?",
        delivery: "Because they used up all their cache!",
        category: "Programming",
      },
      {
        type: "single",
        joke: "Debugging is like being the detective in a crime movie where you're also the murderer.",
        category: "Programming",
      },
      {
        type: "twopart",
        setup: "Why was the JavaScript developer sad?",
        delivery: "Because they didn't Node how to Express themselves!",
        category: "Programming",
      },
      {
        type: "twopart",
        setup: "Why is C# always so polite?",
        delivery: "Because it never forgets to say 'please' with its LINQ.",
        category: "Programming",
      },
      {
        type: "twopart",
        setup: "What's a web developer's favorite tea?",
        delivery: "URL Grey.",
        category: "Programming",
      },
      {
        type: "twopart",
        setup: "Why did the functions stop calling each other?",
        delivery: "They had too many arguments.",
        category: "Programming",
      },
      {
        type: "single",
        joke: "The generation of random numbers is too important to be left to chance.",
        category: "Programming",
      },
      {
        type: "twopart",
        setup: "Why do frontend developers eat lunch alone?",
        delivery: "Because they don't know how to join tables.",
        category: "Programming",
      },
    ];

    // Function to show loading state - desktop (simplified, minimal animation)
    function showLoading() {
      if (!jokeSetup) return;

      jokeSetup.textContent = "Loading joke...";
      jokeDelivery.textContent = "";
      jokeSingle.textContent = "";
      jokeContainer.classList.add("opacity-50");
    }

    // Function to show loading state - mobile (simplified, minimal animation)
    function showMobileLoading() {
      if (!mobileJokeSetup) return;

      mobileJokeSetup.textContent = "Loading joke...";
      mobileJokeDelivery.textContent = "";
      mobileJokeSingle.textContent = "";
      mobileJokeContainer.classList.add("opacity-50");
    }

    // Function to display a joke - desktop (simplified, no animations)
    function displayDesktopJoke(joke) {
      if (!jokeContainer) return;

      console.log("Displaying desktop joke:", joke);
      jokeContainer.classList.remove("opacity-50");

      // Direct display without animations or staggered timing
      if (joke.type === "twopart") {
        jokeSetup.textContent = joke.setup;
        jokeDelivery.textContent = joke.delivery;
        jokeSingle.textContent = "";
      } else {
        jokeSetup.textContent = "";
        jokeDelivery.textContent = "";
        jokeSingle.textContent = joke.joke;
      }

      // Update the category display if available
      const categorySpan = document.querySelector("#joke-category");
      if (categorySpan && joke.category) {
        categorySpan.textContent = joke.category + " Jokes";
      }
    }

    // Function to display a joke - mobile (simplified, no animations)
    function displayMobileJoke(joke) {
      if (!mobileJokeContainer) return;

      console.log("Displaying mobile joke:", joke);
      mobileJokeContainer.classList.remove("opacity-50");

      // Direct display without animations or staggered timing
      if (joke.type === "twopart") {
        mobileJokeSetup.textContent = joke.setup;
        mobileJokeDelivery.textContent = joke.delivery;
        mobileJokeSingle.textContent = "";
      } else {
        mobileJokeSetup.textContent = "";
        mobileJokeDelivery.textContent = "";
        mobileJokeSingle.textContent = joke.joke;
      }

      // Update the category display if available
      const categorySpan = document.querySelector("#mobile-joke-category");
      if (categorySpan && joke.category) {
        categorySpan.textContent = joke.category + " Jokes";
      }
    }

    // Keep track of seen jokes to avoid repetition
    const seenJokes = new Set();

    // Function to track joke to avoid repetition
    function trackJoke(joke) {
      let jokeId;
      if (joke.id) {
        jokeId = `api-${joke.id}`;
      } else if (joke.type === "twopart") {
        jokeId = `local-${joke.setup.substring(0, 20)}`;
      } else {
        jokeId = `local-${joke.joke.substring(0, 20)}`;
      }
      seenJokes.add(jokeId);

      // Only keep track of the last 10 jokes
      if (seenJokes.size > 10) {
        seenJokes.delete(seenJokes.values().next().value);
      }
      return jokeId;
    }

    // Check if we've seen this joke recently
    function isJokeSeen(joke) {
      let jokeId;
      if (joke.id) {
        jokeId = `api-${joke.id}`;
      } else if (joke.type === "twopart") {
        jokeId = `local-${joke.setup.substring(0, 20)}`;
      } else {
        jokeId = `local-${joke.joke.substring(0, 20)}`;
      }
      return seenJokes.has(jokeId);
    }

    // Function to get a random fallback joke
    function getRandomFallbackJoke() {
      const randomIndex = Math.floor(Math.random() * fallbackJokes.length);
      return fallbackJokes[randomIndex];
    }

    // Function to fetch a new joke
    function fetchJoke() {
      // Make this function globally available for page refreshes
      if (typeof window !== "undefined") {
        window.fetchJokeRefresh = fetchJoke;
      }
      console.log("Fetching joke at:", new Date().toISOString());

      // Show loading on desktop view if elements exist
      if (jokeSetup) showLoading();
      // Show loading on mobile view if elements exist
      if (mobileJokeSetup) showMobileLoading();

      // Try different categories occasionally
      const categories = ["Programming", "Miscellaneous", "Pun"];
      const categoryIndex = Math.random() > 0.8 ? Math.floor(Math.random() * 3) : 0; // 80% chance for Programming
      const category = categories[categoryIndex];

      // Try the API to get a dynamic joke (will replace fallback if successful)
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 second timeout

      fetch(
        `https://v2.jokeapi.dev/joke/${category}?blacklistFlags=nsfw,religious,political,racist,sexist,explicit`,
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

          // Add category if not present
          if (!data.category) {
            data.category = category;
          }

          // Check if we've seen this joke recently
          if (isJokeSeen(data)) {
            console.log("Joke has been seen recently, getting a new one");
            // 50% chance to try a new API joke or use fallback
            if (Math.random() > 0.5) {
              fetchJoke(); // Try again
              return;
            } else {
              // Find an unseen fallback joke
              let fallbackJoke = getRandomFallbackJoke();
              let attempts = 0;
              while (isJokeSeen(fallbackJoke) && attempts < 5) {
                fallbackJoke = getRandomFallbackJoke();
                attempts++;
              }
              trackJoke(fallbackJoke);
              displayDesktopJoke(fallbackJoke);
              displayMobileJoke(fallbackJoke);
              return;
            }
          }

          // Track this joke to avoid repetition
          trackJoke(data);

          // Display the joke from the API
          displayDesktopJoke(data);
          displayMobileJoke(data);
        })
        .catch((error) => {
          console.warn("API error, using fallback joke:", error.message);

          // Use fallback joke if API fails
          let fallbackJoke = getRandomFallbackJoke();

          // Try to find an unseen joke
          let attempts = 0;
          while (isJokeSeen(fallbackJoke) && attempts < 5) {
            fallbackJoke = getRandomFallbackJoke();
            attempts++;
          }

          // Track this joke
          trackJoke(fallbackJoke);

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

  // Expose the function for external use
  window.initJokeGenerator = initJokeGenerator;

  // Call initJokeGenerator directly to ensure it runs
  if (typeof document !== "undefined" && document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initJokeGenerator);
  } else if (typeof document !== "undefined") {
    // Use setTimeout to ensure DOM is ready
    setTimeout(initJokeGenerator, 100);
  }
})();
