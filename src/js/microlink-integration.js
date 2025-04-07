/**
 * Microlink integration for link and content enrichment
 * This version uses pre-generated data during build time
 * and falls back to the API for validation
 */

document.addEventListener('DOMContentLoaded', () => {
  // Load pre-generated link preview data
  let linkPreviewData = null;
  let dataLoaded = false;

  // Function to fetch pre-generated data
  async function loadLinkPreviewData() {
    try {
      const response = await fetch('/assets/data/link-previews.json');
      if (response.ok) {
        linkPreviewData = await response.json();
        dataLoaded = true;
        return true;
      } else {
        console.error('Failed to load link preview data:', response.status);
        return false;
      }
    } catch (error) {
      console.error('Error loading link preview data:', error);
      return false;
    }
  }

  // Function to get pre-generated data for a URL
  function getPreviewData(url) {
    if (!dataLoaded || !linkPreviewData) return null;
    
    return linkPreviewData.find(item => 
      item.url === url || 
      url.replace(/\/$/, '') === item.url || 
      url === item.url.replace(/\/$/, '')
    );
  }

  // Fallback: Function to fetch metadata for a specific URL
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

  // The main function to enhance link cards using pre-generated data
  async function enhanceLinkCards() {
    // Load pre-generated data first
    const dataLoaded = await loadLinkPreviewData();
    
    // Get all link cards from the links page
    const linkCards = document.querySelectorAll('.link-card');
    if (!linkCards.length) return;
    
    // Add style for link metadata and loading state
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
      
      .microlink-card-error {
        border-color: rgba(255, 0, 0, 0.3);
      }
      
      .link-header .preview-date {
        position: absolute;
        bottom: 8px;
        right: 8px;
        font-size: 10px;
        color: white;
        background: rgba(0, 0, 0, 0.5);
        padding: 2px 6px;
        border-radius: 3px;
        z-index: 1;
      }
    `;
    document.head.appendChild(style);
    
    // Process each card
    for (const card of linkCards) {
      // Skip if already enhanced
      if (card.classList.contains('microlink-enhanced')) continue;
      
      const linkUrl = card.querySelector('a[data-url]')?.dataset.url;
      const imageContainer = card.querySelector('.link-header');
      
      if (linkUrl && imageContainer) {
        // Mark as processing
        card.classList.add('microlink-enhanced');
        card.classList.add('microlink-loading');
        
        // Try to get pre-generated data
        const previewData = getPreviewData(linkUrl);
        
        if (previewData && previewData.screenshot) {
          // Use pre-generated screenshot
          imageContainer.innerHTML = `
            <div class="absolute inset-0">
              <img src="${previewData.screenshot}" alt="Preview of ${previewData.name}" class="w-full h-full object-cover" loading="lazy">
              <div class="absolute inset-0 bg-gradient-to-b from-transparent to-surface/80"></div>
              <div class="preview-date">Last checked: ${new Date(previewData.last_checked).toLocaleDateString()}</div>
            </div>
          `;
          
          // Add metadata if available
          const metadataContainer = card.querySelector('.link-metadata');
          if (metadataContainer && previewData.metadata?.status === 'success') {
            let metadataHtml = '';
            
            if (previewData.metadata.publisher) {
              metadataHtml += `<div class="text-xs text-text-secondary mt-1">Published by: ${previewData.metadata.publisher}</div>`;
            }
            
            if (previewData.metadata.author) {
              metadataHtml += `<div class="text-xs text-text-secondary mt-1">Author: ${previewData.metadata.author}</div>`;
            }
            
            metadataContainer.innerHTML = metadataHtml;
          }
        } else if (!dataLoaded) {
          // Fall back to API if data couldn't be loaded
          try {
            // Fetch metadata and screenshot in parallel
            const [metadata, screenshotResponse] = await Promise.all([
              fetchMicrolinkMetadata(linkUrl),
              fetch(`https://api.microlink.io/?url=${encodeURIComponent(linkUrl)}&screenshot=true`)
            ]);
            
            const screenshotData = await screenshotResponse.json();
            
            if (screenshotData.status === 'success' && screenshotData.data.screenshot) {
              // Replace default icon with screenshot
              imageContainer.innerHTML = `
                <div class="absolute inset-0">
                  <img src="${screenshotData.data.screenshot.url}" alt="Preview of ${linkUrl}" class="w-full h-full object-cover" loading="lazy">
                  <div class="absolute inset-0 bg-gradient-to-b from-transparent to-surface/80"></div>
                </div>
              `;
              
              // Add metadata if available
              const metadataContainer = card.querySelector('.link-metadata');
              if (metadataContainer && metadata) {
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
          } catch (error) {
            console.error('Error fetching preview for', linkUrl, error);
            card.classList.add('microlink-card-error');
          }
        } else if (previewData && previewData.metadata?.status === 'error') {
          // Mark card with error if metadata fetch previously failed
          card.classList.add('microlink-card-error');
        }
        
        // Remove loading state
        card.classList.remove('microlink-loading');
      }
    }
    
    // Load Microlink SDK for interactive previews on hover
    // Only if we're on a page with external-preview links
    if (document.querySelector('.external-preview')) {
      const microlinkScript = document.createElement('script');
      microlinkScript.src = 'https://cdn.jsdelivr.net/npm/@microlink/vanilla/dist/microlink.min.js';
      microlinkScript.async = true;
      microlinkScript.onload = function() {
        if (window.microlink) {
          microlink('.external-preview', {
            size: 'large',
            media: ['screenshot', 'image', 'logo'],
            controls: true
          });
        }
      };
      document.head.appendChild(microlinkScript);
    }
  }

  // Run the enhancement on specific pages
  if (window.location.pathname.includes('/links/')) {
    enhanceLinkCards();
  }
});