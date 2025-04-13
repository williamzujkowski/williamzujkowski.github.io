/**
 * Microlink integration for link and content enrichment
 * This version uses pre-generated data during build time
 * and falls back to the API for validation
 */

document.addEventListener('DOMContentLoaded', () => {
  // Load pre-generated link preview data
  let linkPreviewIndex = null;
  let linkPreviewDataCache = {};
  let dataLoaded = false;
  let categoriesLoaded = false;
  
  // Function to fetch categorized link preview data
  async function loadLinkPreviewData() {
    try {
      // First, try to load the index file which contains category information
      const indexResponse = await fetch('/assets/data/link-previews-index.json');
      
      if (indexResponse.ok) {
        // We have categorized data
        linkPreviewIndex = await indexResponse.json();
        categoriesLoaded = true;
        console.log(`Loaded link preview index with ${linkPreviewIndex.length} categories`);
        
        // Pre-load the most common categories for faster initial rendering
        // This limits the initial payload size while still getting most links quickly
        const commonCategories = ['technology_innovation', 'art_culture_exploration', 'fun_curiosities', 'social'];
        
        await Promise.all(commonCategories.map(async (category) => {
          const categoryFile = linkPreviewIndex.find(c => c.category === category)?.file;
          if (categoryFile) {
            await loadCategoryData(category);
          }
        }));
        
        dataLoaded = true;
        return true;
      } else {
        console.log('No categorized data index found, falling back to single file');
        // Fall back to the legacy single file approach
        const response = await fetch('/assets/data/link-previews.json');
        if (response.ok) {
          linkPreviewDataCache['all'] = await response.json();
          dataLoaded = true;
          return true;
        } else {
          console.error('Failed to load link preview data:', response.status);
          return false;
        }
      }
    } catch (error) {
      console.error('Error loading link preview data:', error);
      return false;
    }
  }
  
  // Load a specific category of link preview data
  async function loadCategoryData(category) {
    if (linkPreviewDataCache[category]) {
      return linkPreviewDataCache[category];
    }
    
    try {
      const response = await fetch(`/assets/data/link-previews-${category}.json`);
      if (response.ok) {
        const data = await response.json();
        linkPreviewDataCache[category] = data;
        return data;
      }
    } catch (error) {
      console.error(`Error loading category data for ${category}:`, error);
    }
    
    return null;
  }

  // Function to get pre-generated data for a URL
  async function getPreviewData(url) {
    if (!dataLoaded) return null;
    
    // If we're using the categorized approach
    if (categoriesLoaded) {
      // Search in already loaded categories first
      for (const category of Object.keys(linkPreviewDataCache)) {
        const data = linkPreviewDataCache[category];
        const match = data.find(item => 
          item.url === url || 
          url.replace(/\/$/, '') === item.url || 
          url === item.url.replace(/\/$/, '')
        );
        
        if (match) return match;
      }
      
      // If not found in loaded categories, we need to check other categories
      if (linkPreviewIndex) {
        for (const indexItem of linkPreviewIndex) {
          // Skip categories we've already checked
          if (linkPreviewDataCache[indexItem.category]) continue;
          
          // Load this category and check it
          const categoryData = await loadCategoryData(indexItem.category);
          if (categoryData) {
            const match = categoryData.find(item => 
              item.url === url || 
              url.replace(/\/$/, '') === item.url || 
              url === item.url.replace(/\/$/, '')
            );
            
            if (match) return match;
          }
        }
      }
      
      return null;
    } else {
      // Legacy single file approach
      return linkPreviewDataCache['all']?.find(item => 
        item.url === url || 
        url.replace(/\/$/, '') === item.url || 
        url === item.url.replace(/\/$/, '')
      );
    }
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
    const dataLoadedSuccess = await loadLinkPreviewData();
    
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

      .link-header .preview-cat {
        position: absolute;
        bottom: 8px;
        left: 8px;
        font-size: 10px;
        color: white;
        background: rgba(0, 0, 0, 0.5);
        padding: 2px 6px;
        border-radius: 3px;
        z-index: 1;
      }
    `;
    document.head.appendChild(style);
    
    // Process cards in batches to avoid freezing the UI
    const BATCH_SIZE = 6;
    const cardArray = Array.from(linkCards);
    
    for (let i = 0; i < cardArray.length; i += BATCH_SIZE) {
      const batch = cardArray.slice(i, i + BATCH_SIZE);
      
      // Process each batch with a small delay to keep UI responsive
      await new Promise(resolve => {
        setTimeout(async () => {
          await Promise.all(batch.map(processCard));
          resolve();
        }, i === 0 ? 0 : 100); // No delay for first batch
      });
    }
    
    // Process a single card
    async function processCard(card) {
      // Skip if already enhanced
      if (card.classList.contains('microlink-enhanced')) return;
      
      const linkUrl = card.closest('a[data-url]')?.dataset.url || card.querySelector('a[data-url]')?.dataset.url;
      const imageContainer = card.querySelector('.link-header');
      
      if (linkUrl && imageContainer) {
        // Mark as processing
        card.classList.add('microlink-enhanced');
        card.classList.add('microlink-loading');
        
        try {
          // Try to get pre-generated data - this is now async
          const previewData = await getPreviewData(linkUrl);
          
          if (previewData && previewData.screenshot) {
            // Use pre-generated screenshot
            imageContainer.innerHTML = `
              <div class="absolute inset-0">
                <img src="${previewData.screenshot}" alt="Preview of ${previewData.name}" class="w-full h-full object-cover" loading="lazy">
                <div class="absolute inset-0 bg-gradient-to-b from-transparent to-surface/80"></div>
                <div class="preview-date">Last checked: ${new Date(previewData.last_checked).toLocaleDateString()}</div>
                ${previewData.group ? `<div class="preview-cat">${previewData.group}</div>` : ''}
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
          } else if (!dataLoadedSuccess) {
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
        } catch (error) {
          console.error('Error processing card for', linkUrl, error);
          card.classList.add('microlink-card-error');
        } finally {
          // Always remove loading state
          card.classList.remove('microlink-loading');
        }
      }
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