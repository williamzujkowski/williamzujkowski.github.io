#!/bin/bash

# media.sh - Script for handling media-related operations
# Usage: ./media.sh [command]

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Commands
function optimize_images() {
  echo "Optimizing images..."
  node "$PROJECT_ROOT/scripts/content/media/optimize-images.js"
}

function optimize_blog_images() {
  echo "Optimizing blog images..."
  node -e "
    import('$PROJECT_ROOT/scripts/content/media/optimize-images.js')
      .then(module => {
        module.initMetadata();
        module.processDirectory('$PROJECT_ROOT/assets/images/blog')
          .then(() => module.saveMetadata())
          .catch(console.error);
      })
      .catch(console.error);
  "
}

function optimize_specific_image() {
  if [ -z "$1" ]; then
    echo "Error: No image path provided"
    echo "Usage: ./media.sh optimize-image <path-to-image>"
    exit 1
  fi
  
  IMAGE_PATH="$1"
  
  if [ ! -f "$IMAGE_PATH" ]; then
    echo "Error: Image file not found: $IMAGE_PATH"
    exit 1
  fi
  
  echo "Optimizing specific image: $IMAGE_PATH"
  node -e "
    import('$PROJECT_ROOT/scripts/content/media/optimize-images.js')
      .then(module => {
        module.initMetadata();
        module.optimizeImage('$IMAGE_PATH')
          .then(() => module.saveMetadata())
          .catch(console.error);
      })
      .catch(console.error);
  "
}

# Command parsing
case "$1" in
  optimize|optimize-all)
    optimize_images
    ;;
  optimize-blog)
    optimize_blog_images
    ;;
  optimize-image)
    optimize_specific_image "$2"
    ;;
  *)
    echo "Usage: $0 [command]"
    echo ""
    echo "Available commands:"
    echo "  optimize, optimize-all   Optimize all images"
    echo "  optimize-blog            Optimize only blog images"
    echo "  optimize-image <path>    Optimize a specific image"
    exit 1
    ;;
esac