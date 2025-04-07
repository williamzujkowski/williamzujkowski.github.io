/**
 * Microlink integration for link and content enrichment
 */

document.addEventListener('DOMContentLoaded', () => {
  // Function to fetch metadata for a specific URL
  async function fetchMicrolinkMetadata(url) {
    try {
      const response = await fetch(`https://api.microlink.io/?url=${encodeURIComponent(url)}`);
      const data = await response.json();
      
      if (data.status === 'success') {
        return data.data;
      } else {
        console.error('Error fetching data for', url, data);
        return null;
      }
    } catch (error) {
      console.error('Failed to fetch metadata for', url, error);
      return null;
    }
  }

  // Function to fetch a screenshot for a URL
  async function fetchMicrolinkScreenshot(url) {
    try {
      const response = await fetch(`https://api.microlink.io/?url=${encodeURIComponent(url)}&screenshot=true`);
      const data = await response.json();
      
      if (data.status === 'success' && data.data.screenshot) {
        return data.data.screenshot.url;
      } else {
        console.error('Error fetching screenshot for', url, data);
        return null;
      }
    } catch (error) {
      console.error('Failed to fetch screenshot for', url, error);
      return null;
    }
  }

  // The main function to enhance link cards by replacing default icons with screenshots
  async function enhanceLinkCards() {
    // Only process a limited number to stay within free tier limits
    const maxEnhancedLinks = 10;
    let enhancedCount = 0;
    
    // Get all link cards from the links page
    const linkCards = document.querySelectorAll('.link-card');
    
    for (const card of linkCards) {
      // Exit if we've reached our limit
      if (enhancedCount >= maxEnhancedLinks) break;
      
      // Skip if already enhanced
      if (card.classList.contains('microlink-enhanced')) continue;
      
      const linkUrl = card.querySelector('a[data-url]')?.dataset.url;
      const imageContainer = card.querySelector('.link-header');
      
      if (linkUrl && imageContainer) {
        // Mark as processing to avoid double-enhancement
        card.classList.add('microlink-enhanced');
        card.classList.add('microlink-loading');
        
        // Fetch screenshot
        const screenshotUrl = await fetchMicrolinkScreenshot(linkUrl);
        
        if (screenshotUrl) {
          // Replace default icon with screenshot
          imageContainer.innerHTML = `
            <div class="absolute inset-0">
              <img src="${screenshotUrl}" alt="Preview of ${linkUrl}" class="w-full h-full object-cover" loading="lazy">
              <div class="absolute inset-0 bg-gradient-to-b from-transparent to-surface/80"></div>
            </div>
          `;
          
          // Update metadata if needed from the same API call
          const metadata = await fetchMicrolinkMetadata(linkUrl);
          if (metadata) {
            // Add additional metadata if available
            const metadataContainer = card.querySelector('.link-metadata');
            if (metadataContainer) {
              let metadataHtml = '';
              
              if (metadata.publisher) {
                metadataHtml += `<div class="text-xs text-text-secondary mt-1">Published by: ${metadata.publisher}</div>`;
              }
              
              if (metadata.author) {
                metadataHtml += `<div class="text-xs text-text-secondary mt-1">Author: ${metadata.author}</div>`;
              }
              
              metadataContainer.innerHTML = metadataHtml;
            }
          }
          
          enhancedCount++;
        }
        
        // Remove loading state
        card.classList.remove('microlink-loading');
      }
    }
    
    // Add Microlink SDK for all external links
    // This is within the rate limit since it doesn't fetch many links at once
    if (window.microlink) {
      microlink('.external-preview', {
        size: 'large',
        media: ['screenshot', 'image', 'logo'],
        controls: true
      });
    }
  }

  // Only run on the links page
  if (window.location.pathname.includes('/links/')) {
    // Load Microlink scripts
    const microlinkScript = document.createElement('script');
    microlinkScript.src = 'https://cdn.jsdelivr.net/npm/@microlink/vanilla/dist/microlink.min.js';
    microlinkScript.async = true;
    microlinkScript.onload = enhanceLinkCards;
    document.head.appendChild(microlinkScript);
    
    // Add some needed styles
    const style = document.createElement('style');
    style.textContent = `
      .microlink-loading .link-header::after {
        content: "Loading...";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        background: rgba(0, 0, 0, 0.5);
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
      }
      
      .link-metadata {
        margin-top: 8px;
        font-style: italic;
      }
    `;
    document.head.appendChild(style);
  }
});