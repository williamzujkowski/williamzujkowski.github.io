# Blog Post Broken Links Fix Report

## Executive Summary
Successfully identified and fixed all broken links on williamzujkowski.github.io blog posts. The issue was caused by improper URL slug generation that converted apostrophes to HTML entities (`&#39;`).

## Problem Identified
- **Total broken links found**: 5 blog posts with apostrophes in titles
- **Root cause**: The Eleventy static site generator was converting apostrophes in titles to HTML entities when generating URL slugs
- **Impact**: 404 errors for all blog posts containing apostrophes in their titles

## Affected Blog Posts
1. **Quantum Computing's Leap Forward**
   - Broken URL: `/posts/quantum-computing&#39;s-leap-forward/`
   - Fixed URL: `/posts/quantum-computings-leap-forward/`

2. **Sustainable Computing: Strategies for Reducing IT's Carbon Footprint**
   - Broken URL: `/posts/sustainable-computing:-strategies-for-reducing-it&#39;s-carbon-footprint/`
   - Fixed URL: `/posts/sustainable-computing-strategies-for-reducing-its-carbon-footprint/`

3. **Quantum Computing and Defense: The Double-Edged Sword of Tomorrow's Technology**
   - Broken URL: `/posts/quantum-computing-and-defense:-the-double-edged-sword-of-tomorrow&#39;s-technology/`
   - Fixed URL: `/posts/quantum-computing-and-defense-the-double-edged-sword-of-tomorrows-technology/`

4. **Demystifying Cryptography: A Beginner's Guide to Encryption, Hashing, and Digital Signatures**
   - Broken URL: `/posts/demystifying-cryptography:-a-beginner&#39;s-guide-to-encryption-hashing-and-digital-signatures/`
   - Fixed URL: `/posts/demystifying-cryptography-a-beginners-guide-to-encryption-hashing-and-digital-signatures/`

5. **Writing Secure Code: A Developer's Guide to Thwarting Security Exploits**
   - Broken URL: `/posts/writing-secure-code:-a-developer&#39;s-guide-to-thwarting-security-exploits/`
   - Fixed URL: `/posts/writing-secure-code-a-developers-guide-to-thwarting-security-exploits/`

## Solution Implemented
Modified `.eleventy.js` configuration file to add a custom `slug` filter that properly handles apostrophes:

```javascript
// Override the built-in slug filter to properly handle apostrophes
eleventyConfig.addFilter("slug", (str) => {
  if (!str) return "";
  return str.toString().toLowerCase()
    .replace(/['′'']/g, '')        // Remove apostrophes and smart quotes
    .replace(/\s+/g, '-')           // Replace spaces with -
    .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
    .replace(/\-\-+/g, '-')         // Replace multiple - with single -
    .replace(/^-+/, '')             // Trim - from start of text
    .replace(/-+$/, '');            // Trim - from end of text
});
```

## Testing & Validation
1. Rebuilt the site using `npm run build`
2. Started local server on port 8080
3. Successfully navigated to all previously broken URLs
4. Confirmed all posts are now accessible with properly formatted URLs

## Recommendations
1. **Deploy the fix**: Push the changes to the main branch to fix the production site
2. **Add URL validation**: Consider adding automated tests to catch URL issues during build
3. **Monitor 404s**: Set up monitoring to alert on future 404 errors
4. **Document the fix**: This report serves as documentation for future reference

## Conclusion
The broken link issue has been successfully resolved by implementing a custom slug filter that properly handles apostrophes and other special characters in blog post titles. All affected URLs are now working correctly in the local build and ready for deployment.

---
*Report generated: January 8, 2025*
*Fixed by: Hive Mind Collective Intelligence System*