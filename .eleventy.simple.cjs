module.exports = function(eleventyConfig) {
  // Just a simple passthrough config for GitHub Actions
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy({ "assets/icons/favicon.ico": "favicon.ico" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/icon.svg": "icon.svg" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/apple-touch-icon.png": "apple-touch-icon.png" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/android-chrome-192x192.png": "android-chrome-192x192.png" });
  eleventyConfig.addPassthroughCopy({ "assets/icons/android-chrome-512x512.png": "android-chrome-512x512.png" });
  eleventyConfig.addPassthroughCopy(".nojekyll");
  
  // Add shortcodes
  eleventyConfig.addShortcode("year", () => new Date().getFullYear());
  
  // Add breadcrumb shortcode
  eleventyConfig.addShortcode("breadcrumbs", function(page) {
    if (!page || !page.url) return "";
    
    const parts = page.url.split('/').filter(part => part);
    let breadcrumbs = '<nav aria-label="Breadcrumb" class="breadcrumbs"><div class="breadcrumbs-list">';
    
    // Add home
    breadcrumbs += '<span class="breadcrumbs-item"><a href="/" class="breadcrumbs-link">Home</a></span>';
    
    // Build the breadcrumb path
    let path = "";
    parts.forEach((part, i) => {
      path += `/${part}`;
      
      // Add separator
      breadcrumbs += '<span class="breadcrumbs-separator">&gt;</span>';
      
      // Last item (current page)
      if (i === parts.length - 1) {
        const label = page.title || part.replace(/-/g, ' ');
        breadcrumbs += `<span class="breadcrumbs-item current">${label}</span>`;
      } else {
        // Get proper title if available
        const segment = part.replace(/-/g, ' ');
        const title = segment.charAt(0).toUpperCase() + segment.slice(1);
        
        breadcrumbs += `<span class="breadcrumbs-item">
          <a href="${path}/" class="breadcrumbs-link">${title}</a>
        </span>`;
      }
    });
    
    breadcrumbs += '</div></nav>';
    return breadcrumbs;
  });
  
  // Add image shortcode
  eleventyConfig.addShortcode("image", function(src, alt, sizes = "100vw") {
    if (!src) {
      throw new Error(`Missing image source`);
    }
    if (!alt) {
      throw new Error(`Missing alt text for image: ${src}`);
    }
    
    // Simple image tag for GitHub Actions build
    return `<img src="${src}" alt="${alt}" class="w-full h-auto object-cover" loading="lazy" decoding="async">`;
  });
  
  // Site structure
  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts"
    }
  };
};