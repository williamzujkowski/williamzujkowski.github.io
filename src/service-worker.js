/**
 * Service Worker for caching and offline support
 * Part of Phase 4 performance optimization
 */

// Cache name includes a version for easy updates
const CACHE_NAME = "site-cache-v1";

// Assets to cache immediately on install
const CORE_ASSETS = [
  "/",
  "/index.html",
  "/css/main.css",
  "/js/main.bundle.js",
  "/js/utils.bundle.js",
  "/js/components/theme-toggle.bundle.js",
  "/assets/icons/favicon.ico",
  "/assets/icons/icon.svg",
  "/offline.html", // Fallback page for offline use
];

// Additional assets to cache on first use
const CACHE_ON_USE = [
  "/js/blog.bundle.js",
  "/js/search.bundle.js",
  "/js/components/code-highlight.bundle.js",
  "/css/blog-enhanced.css",
];

// Install event - cache core assets
self.addEventListener("install", (event) => {
  console.log("[Service Worker] Installing...");

  // Pre-cache core assets
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => {
        console.log("[Service Worker] Pre-caching assets");
        return cache.addAll(CORE_ASSETS);
      })
      .then(() => {
        // Activate immediately without waiting for existing tabs to close
        return self.skipWaiting();
      })
  );
});

// Activate event - cleanup old caches
self.addEventListener("activate", (event) => {
  console.log("[Service Worker] Activating...");

  // Remove old cache versions
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME) {
              console.log("[Service Worker] Deleting old cache:", cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        // Take control of all clients immediately
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache or network
self.addEventListener("fetch", (event) => {
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  // Skip non-GET requests
  if (event.request.method !== "GET") {
    return;
  }

  // For HTML pages - network-first strategy
  if (event.request.headers.get("Accept").includes("text/html")) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Cache the latest version
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
          return response;
        })
        .catch(() => {
          // Fallback to cache or offline page
          return caches.match(event.request).then((cachedResponse) => {
            return cachedResponse || caches.match("/offline.html");
          });
        })
    );
    return;
  }

  // For JavaScript, CSS, and images - cache-first strategy
  if (event.request.url.match(/\.(js|css|png|jpg|jpeg|svg|webp|gif|ico)$/)) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        // Return cached response or fetch from network
        const fetchPromise = fetch(event.request).then((networkResponse) => {
          // Cache the new response
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, networkResponse.clone());
          });
          return networkResponse;
        });

        return cachedResponse || fetchPromise;
      })
    );
    return;
  }

  // For everything else - network-first strategy
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Cache items that are in CACHE_ON_USE list
        if (CACHE_ON_USE.some((asset) => event.request.url.includes(asset))) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Fallback to cache
        return caches.match(event.request);
      })
  );
});

// Background sync for offline form submissions (if applicable)
self.addEventListener("sync", (event) => {
  if (event.tag === "sync-forms") {
    event.waitUntil(syncForms());
  }
});

// Periodic cache cleanup (every 24 hours)
self.addEventListener("periodicsync", (event) => {
  if (event.tag === "cleanup-caches") {
    event.waitUntil(cleanupCaches());
  }
});

/**
 * Clean up old cached items (not used in last 30 days)
 */
async function cleanupCaches() {
  const cache = await caches.open(CACHE_NAME);
  const requests = await cache.keys();
  const now = Date.now();
  const maxAge = 30 * 24 * 60 * 60 * 1000; // 30 days in milliseconds

  for (const request of requests) {
    // Skip core assets
    if (CORE_ASSETS.includes(new URL(request.url).pathname)) {
      continue;
    }

    // Get cache entry timestamp from cache headers
    const response = await cache.match(request);
    const headers = response.headers;

    // Get the date from headers or use fallback
    let timestamp;
    if (headers.has("date")) {
      timestamp = new Date(headers.get("date")).getTime();
    } else {
      // Skip if we can't determine age
      continue;
    }

    // Remove if older than max age
    if (now - timestamp > maxAge) {
      await cache.delete(request);
    }
  }
}

/**
 * Sync form submissions that occurred offline
 */
async function syncForms() {
  // Implementation would go here if the site has forms
  // For now, this is just a placeholder
  console.log("[Service Worker] Form sync not implemented");
}

// Log activation
console.log("[Service Worker] Service worker registered and active");
