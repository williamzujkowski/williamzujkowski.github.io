#!/bin/bash
# Run the optimized screenshot generator with common options

cd "$(dirname "$0")/.."

# Colors for better output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Display help
function show_help {
  echo -e "${BLUE}Fast Screenshot Generator${NC}"
  echo "============================="
  echo "Usage: ./tools/fast-screenshots.sh [option]"
  echo ""
  echo "Options:"
  echo "  all       - Generate screenshots for all links without screenshots"
  echo "  update    - Update all existing screenshots"
  echo "  batch N M - Process M links starting at index N"
  echo "  missing   - Only generate screenshots for links without them"
  echo "  help      - Show this help message"
  echo ""
  echo "Examples:"
  echo "  ./tools/fast-screenshots.sh all"
  echo "  ./tools/fast-screenshots.sh batch 50 10"
  echo "  ./tools/fast-screenshots.sh update"
}

# Check for parameter
if [ $# -eq 0 ]; then
  show_help
  exit 1
fi

# Process options
case "$1" in
  "all")
    echo -e "${GREEN}Generating screenshots for all links without screenshots${NC}"
    node tools/fast-screenshot-generator.js 0 1000 
    ;;
    
  "update")
    echo -e "${GREEN}Updating all existing screenshots${NC}"
    node tools/fast-screenshot-generator.js 0 1000 --update-all --force-refresh
    ;;
    
  "batch")
    if [ $# -lt 3 ]; then
      echo -e "${YELLOW}Missing parameters for batch processing${NC}"
      echo "Usage: ./tools/fast-screenshots.sh batch START_INDEX COUNT"
      exit 1
    fi
    echo -e "${GREEN}Processing batch starting at index $2 with count $3${NC}"
    node tools/fast-screenshot-generator.js $2 $3
    ;;
    
  "missing")
    echo -e "${GREEN}Generating screenshots for links without them${NC}"
    node tools/fast-screenshot-generator.js 0 1000
    ;;
    
  "help")
    show_help
    ;;
    
  *)
    echo -e "${YELLOW}Unknown option: $1${NC}"
    show_help
    exit 1
    ;;
esac