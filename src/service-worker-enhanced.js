/**
 * Enhanced Service Worker with Workbox
 * Provides:
 * - Runtime caching
 * - Stale-while-revalidate pattern
 * - Cache prefetch
 * - Offline support
 * - Network monitoring
 */

// Cache version
const CACHE_VERSION = "v1";

// Cache names
const CORE_CACHE_NAME = `core-${CACHE_VERSION}`;
const ASSETS_CACHE_NAME = `assets-${CACHE_VERSION}`;
const PAGES_CACHE_NAME = `pages-${CACHE_VERSION}`;
const API_CACHE_NAME = `api-${CACHE_VERSION}`;

// URLs to cache immediately during installation
const CORE_ASSETS = [
  "/",
  "/offline.html",
  "/css/optimized/critical.css",
  "/css/optimized/main.css",
  "/js/core.js",
  "/manifest.json",
];

// URLs to cache during the service worker's idle time
const PRECACHE_ASSETS = [
  "/blog/",
  "/css/optimized/blog.css",
  "/js/pages/blog.js",
  "/img/placeholder.webp",
];

// Install event - cache core assets
self.addEventListener("install", (event) => {
  console.log("[Service Worker] Installing");

  event.waitUntil(
    caches
      .open(CORE_CACHE_NAME)
      .then((cache) => {
        console.log("[Service Worker] Caching core assets");
        return cache.addAll(CORE_ASSETS);
      })
      .then(() => {
        console.log("[Service Worker] Core assets cached");
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener("activate", (event) => {
  console.log("[Service Worker] Activating");

  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => {
              // Filter caches that don't match current version
              return (
                (cacheName.startsWith("core-") && cacheName !== CORE_CACHE_NAME) ||
                (cacheName.startsWith("assets-") && cacheName !== ASSETS_CACHE_NAME) ||
                (cacheName.startsWith("pages-") && cacheName !== PAGES_CACHE_NAME) ||
                (cacheName.startsWith("api-") && cacheName !== API_CACHE_NAME)
              );
            })
            .map((cacheName) => {
              console.log(`[Service Worker] Deleting old cache: ${cacheName}`);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log("[Service Worker] Claiming clients");
        return self.clients.claim();
      })
      .then(() => {
        // Precache assets during idle time
        console.log("[Service Worker] Precaching additional assets");
        return precacheAssetsDuringIdle();
      })
  );
});

// Helper function to precache assets during idle time
function precacheAssetsDuringIdle() {
  if ("requestIdleCallback" in self) {
    return new Promise((resolve) => {
      self.requestIdleCallback(() => {
        caches
          .open(ASSETS_CACHE_NAME)
          .then((cache) => {
            console.log(
              "[Service Worker] Precaching additional assets during idle time"
            );
            return cache.addAll(PRECACHE_ASSETS).then(resolve);
          })
          .catch(resolve); // Still resolve even if precaching fails
      });
    });
  } else {
    // Fallback for browsers that don't support requestIdleCallback
    return caches
      .open(ASSETS_CACHE_NAME)
      .then((cache) => {
        console.log("[Service Worker] Precaching additional assets");
        return cache.addAll(PRECACHE_ASSETS);
      })
      .catch((error) => {
        console.error("[Service Worker] Precaching failed:", error);
      });
  }
}

// Cache strategies
const strategies = {
  // Stale while revalidate - return cached response immediately, then update cache
  staleWhileRevalidate: (cacheName) => {
    return async (request) => {
      const cache = await caches.open(cacheName);
      const cachedResponse = await cache.match(request);

      const fetchPromise = fetch(request)
        .then((response) => {
          if (response && response.ok && response.status === 200) {
            cache.put(request, response.clone());
          }
          return response;
        })
        .catch((error) => {
          console.error(`[Service Worker] Fetch failed for ${request.url}:`, error);
          return null;
        });

      return cachedResponse || fetchPromise;
    };
  },

  // Cache first - check cache first, fall back to network
  cacheFirst: (cacheName) => {
    return async (request) => {
      const cache = await caches.open(cacheName);
      const cachedResponse = await cache.match(request);

      if (cachedResponse) {
        return cachedResponse;
      }

      try {
        const networkResponse = await fetch(request);

        if (networkResponse && networkResponse.ok && networkResponse.status === 200) {
          cache.put(request, networkResponse.clone());
        }

        return networkResponse;
      } catch (error) {
        console.error(`[Service Worker] Fetch failed for ${request.url}:`, error);
        return null;
      }
    };
  },

  // Network first - try network first, fall back to cache
  networkFirst: (cacheName) => {
    return async (request) => {
      const cache = await caches.open(cacheName);

      try {
        const networkResponse = await fetch(request);

        if (networkResponse && networkResponse.ok && networkResponse.status === 200) {
          cache.put(request, networkResponse.clone());
        }

        return networkResponse;
      } catch (error) {
        console.error(`[Service Worker] Fetch failed for ${request.url}:`, error);

        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
          return cachedResponse;
        }

        // If it's a page request, return the offline page
        if (request.mode === "navigate") {
          return caches.match("/offline.html");
        }

        return null;
      }
    };
  },
};

// Routing based on URL pattern
const routes = [
  // HTML pages - Network first with offline fallback
  {
    matcher: (request) =>
      request.mode === "navigate" || request.destination === "document",
    handler: strategies.networkFirst(PAGES_CACHE_NAME),
  },

  // CSS and JS - Cache first for fast loading
  {
    matcher: (request) =>
      request.destination === "style" || request.destination === "script",
    handler: strategies.cacheFirst(ASSETS_CACHE_NAME),
  },

  // Images - Stale while revalidate
  {
    matcher: (request) =>
      request.destination === "image" ||
      request.url.match(/\.(jpe?g|png|gif|svg|webp|avif)$/i),
    handler: strategies.staleWhileRevalidate(ASSETS_CACHE_NAME),
  },

  // Fonts - Cache first
  {
    matcher: (request) =>
      request.destination === "font" || request.url.match(/\.(woff2?|ttf|otf|eot)$/i),
    handler: strategies.cacheFirst(ASSETS_CACHE_NAME),
  },

  // API requests - Network first with cache fallback
  {
    matcher: (request) => request.url.includes("/api/"),
    handler: strategies.networkFirst(API_CACHE_NAME),
  },
];

// Fetch event - handle requests based on routes
self.addEventListener("fetch", (event) => {
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  // Find the appropriate route handler
  const route = routes.find((route) => route.matcher(event.request));

  if (route) {
    event.respondWith(route.handler(event.request.clone()));
  }
});

// Listen for messages from the client
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// Background sync for offline data
self.addEventListener("sync", (event) => {
  if (event.tag === "sync-forms") {
    event.waitUntil(syncFormData());
  }
});

// Function to sync form data
async function syncFormData() {
  try {
    const cache = await caches.open("form-data");
    const requests = await cache.keys();

    for (const request of requests) {
      const formData = await cache.match(request).then((res) => res.json());

      // Try to send the form data
      const response = await fetch(request, {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        // If successful, remove from cache
        await cache.delete(request);
      }
    }
  } catch (error) {
    console.error("[Service Worker] Sync failed:", error);
  }
}

// Log when service worker is active
console.log("[Service Worker] Service worker active");
