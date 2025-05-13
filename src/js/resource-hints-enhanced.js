/**
 * Enhanced resource hints for optimized loading performance
 *
 * This module provides advanced resource hint management with:
 * - Dynamic hint prioritization based on user connection
 * - Fetch priority signals
 * - Module/nomodule handling
 * - Intersection Observer for lazy resources
 * - HTTP/2 server push hints
 */

// Configuration
const CONFIG = {
  // Critical resources needed for initial render
  criticalResources: {
    fonts: [
      {
        url: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        type: "style",
      },
    ],
    styles: [{ url: "/css/optimized/critical.css", type: "style" }],
    scripts: [{ url: "/js/core.[hash].js", type: "script", module: true }],
  },

  // Resources needed soon after initial render
  earlyResources: {
    fonts: [],
    styles: [{ url: "/css/optimized/components.css", type: "style" }],
    scripts: [
      { url: "/js/components/theme-toggle.[hash].js", type: "script", module: true },
    ],
  },

  // Page-specific resources
  pageResources: {
    blog: {
      styles: [{ url: "/css/optimized/blog.css", type: "style" }],
      scripts: [
        { url: "/js/pages/blog.[hash].js", type: "script", module: true },
        {
          url: "/js/components/code-highlight.[hash].js",
          type: "script",
          module: true,
          lazy: true,
        },
      ],
    },
    home: {
      styles: [],
      scripts: [],
    },
  },

  // External domains to preconnect to
  connections: ["https://fonts.googleapis.com", "https://fonts.gstatic.com"],
};

/**
 * Get the current page type
 * @returns {string} Page type (blog, home, etc.)
 */
function getPageType() {
  const path = window.location.pathname;

  if (path.includes("/blog/")) {
    return "blog";
  } else if (path === "/" || path === "/index.html") {
    return "home";
  }

  return "other";
}

/**
 * Get the user's connection type if available
 * @returns {string} Connection type (4g, 3g, 2g, slow-2g, or unknown)
 */
function getConnectionType() {
  if (navigator.connection && navigator.connection.effectiveType) {
    return navigator.connection.effectiveType;
  }

  return "unknown";
}

/**
 * Add preconnect hints for external domains
 * @param {string[]} domains - Array of domains to preconnect to
 */
function addPreconnect(domains) {
  domains.forEach((domain) => {
    // Check if preconnect already exists
    if (document.querySelector(`link[rel="preconnect"][href="${domain}"]`)) {
      return;
    }

    const link = document.createElement("link");
    link.rel = "preconnect";
    link.href = domain;
    link.crossOrigin = "anonymous";
    document.head.appendChild(link);

    // Also add DNS-prefetch as fallback for browsers that don't support preconnect
    const dnsPrefetch = document.createElement("link");
    dnsPrefetch.rel = "dns-prefetch";
    dnsPrefetch.href = domain;
    document.head.appendChild(dnsPrefetch);
  });
}

/**
 * Add a resource hint
 * @param {Object} resource - Resource object with url, type, and options
 * @param {string} hintType - Type of hint (preload, prefetch, prerender)
 * @param {boolean} isHighPriority - Whether this is a high priority resource
 */
function addResourceHint(resource, hintType = "preload", isHighPriority = false) {
  const { url, type, module = false, lazy = false } = resource;

  // Skip if hint already exists
  const selector = `link[rel="${hintType}"][href="${url}"]`;
  if (document.querySelector(selector)) {
    return;
  }

  const link = document.createElement("link");
  link.rel = hintType;
  link.href = url;

  // Set correct as attribute
  if (type === "script") {
    link.as = "script";
    if (module) {
      link.crossOrigin = "anonymous";
    }
  } else if (type === "style") {
    link.as = "style";
  } else if (type === "font") {
    link.as = "font";
    link.crossOrigin = "anonymous";
    // Font display optimization
    link.type = "font/woff2";
  } else if (type === "image") {
    link.as = "image";
    // Use fetchpriority for images
    if (isHighPriority) {
      link.setAttribute("fetchpriority", "high");
    } else {
      link.setAttribute("fetchpriority", "low");
    }
  }

  // Set priority for browsers that support it
  if ("fetchpriority" in HTMLLinkElement.prototype) {
    link.fetchpriority = isHighPriority ? "high" : "low";
  }

  // For lazy resources, use IntersectionObserver
  if (lazy && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            document.head.appendChild(link);
            observer.disconnect();
          }
        });
      },
      { rootMargin: "200px" }
    );

    // Observe the document body to load when user scrolls
    observer.observe(document.body);
  } else {
    document.head.appendChild(link);
  }

  return link;
}

/**
 * Add HTTP/2 server push hints
 * This uses Link headers for server push
 */
function addServerPushHints() {
  const pageType = getPageType();
  const resources = [];

  // Add critical resources
  CONFIG.criticalResources.styles.forEach((resource) => {
    resources.push(`<${resource.url}>; rel=preload; as=style`);
  });

  CONFIG.criticalResources.scripts.forEach((resource) => {
    resources.push(
      `<${resource.url}>; rel=preload; as=script${resource.module ? "; crossorigin" : ""}`
    );
  });

  // Add page-specific resources
  if (pageType in CONFIG.pageResources) {
    CONFIG.pageResources[pageType].styles.forEach((resource) => {
      if (!resource.lazy) {
        resources.push(`<${resource.url}>; rel=preload; as=style`);
      }
    });

    CONFIG.pageResources[pageType].scripts.forEach((resource) => {
      if (!resource.lazy) {
        resources.push(
          `<${resource.url}>; rel=preload; as=script${resource.module ? "; crossorigin" : ""}`
        );
      }
    });
  }

  // Create a meta tag with the HTTP/2 push hints
  // The server can read this and convert it to HTTP Link headers
  const meta = document.createElement("meta");
  meta.name = "http2-push";
  meta.content = resources.join(", ");
  document.head.appendChild(meta);
}

/**
 * Initialize all resource hints
 */
export function initEnhancedResourceHints() {
  try {
    console.time("Resource hints");

    // Get page type and connection info
    const pageType = getPageType();
    const connectionType = getConnectionType();
    const isFastConnection = connectionType === "4g" || connectionType === "unknown";

    // 1. Add preconnect for external domains
    addPreconnect(CONFIG.connections);

    // 2. Preload critical resources first
    CONFIG.criticalResources.fonts.forEach((resource) => {
      addResourceHint(resource, "preload", true);
    });

    CONFIG.criticalResources.styles.forEach((resource) => {
      addResourceHint(resource, "preload", true);
    });

    CONFIG.criticalResources.scripts.forEach((resource) => {
      addResourceHint(resource, "preload", true);
    });

    // 3. Add page-specific resources
    if (pageType in CONFIG.pageResources) {
      CONFIG.pageResources[pageType].styles.forEach((resource) => {
        const hintType = resource.lazy ? "prefetch" : "preload";
        addResourceHint(resource, hintType, !resource.lazy);
      });

      CONFIG.pageResources[pageType].scripts.forEach((resource) => {
        const hintType = resource.lazy ? "prefetch" : "preload";
        addResourceHint(resource, hintType, !resource.lazy);
      });
    }

    // 4. For fast connections, add early resources as prefetch
    if (isFastConnection) {
      CONFIG.earlyResources.styles.forEach((resource) => {
        addResourceHint(resource, "prefetch", false);
      });

      CONFIG.earlyResources.scripts.forEach((resource) => {
        addResourceHint(resource, "prefetch", false);
      });

      // Add HTTP/2 server push hints
      addServerPushHints();
    }

    console.timeEnd("Resource hints");
    return true;
  } catch (error) {
    console.error("Error initializing resource hints:", error);
    return false;
  }
}

/**
 * Dynamically load a script
 * @param {string} src - Script URL
 * @param {boolean} isModule - Whether this is a module script
 * @param {boolean} async - Whether to load asynchronously
 * @returns {Promise} Promise that resolves when script is loaded
 */
export function loadScript(src, isModule = true, async = true) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    if (isModule) {
      script.type = "module";
    }
    script.async = async;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

/**
 * Dynamically load a stylesheet
 * @param {string} href - Stylesheet URL
 * @returns {Promise} Promise that resolves when stylesheet is loaded
 */
export function loadStylesheet(href) {
  return new Promise((resolve, reject) => {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    link.onload = resolve;
    link.onerror = reject;
    document.head.appendChild(link);
  });
}

// Export all functions
export default {
  initEnhancedResourceHints,
  loadScript,
  loadStylesheet,
  getPageType,
  getConnectionType,
};
