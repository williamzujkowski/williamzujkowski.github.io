#!/bin/bash
# Main build script for the site

cd "$(dirname "$0")/../.."

# Colors for better output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to show help
function show_help {
  echo -e "${BLUE}Site Build Tool${NC}"
  echo "===================="
  echo "Usage: ./scripts/bin/build.sh [option]"
  echo ""
  echo "Options:"
  echo "  all       - Build everything (data, site, CSS)"
  echo "  data      - Build only data files"
  echo "  site      - Build only the site"
  echo "  css       - Build only CSS"
  echo "  dev       - Start development server"
  echo "  help      - Show this help message"
  echo ""
  echo "Examples:"
  echo "  ./scripts/bin/build.sh all"
  echo "  ./scripts/bin/build.sh data"
  echo "  ./scripts/bin/build.sh dev"
}

# Check for parameter
if [ $# -eq 0 ]; then
  show_help
  exit 1
fi

# Process build options
case "$1" in
  "all")
    echo -e "${GREEN}Building everything (data, site, CSS)...${NC}"
    npm run build
    ;;

  "data")
    echo -e "${GREEN}Building data files...${NC}"
    npm run build:data
    ;;

  "site")
    echo -e "${GREEN}Building site...${NC}"
    npx @11ty/eleventy --config=config/.eleventy.simple.cjs
    ;;

  "css")
    echo -e "${GREEN}Building CSS...${NC}"
    npm run build:css
    ;;

  "dev")
    echo -e "${GREEN}Starting development server...${NC}"
    npm run dev
    ;;

  "help")
    show_help
    ;;

  *)
    echo -e "${RED}Unknown option: $1${NC}"
    show_help
    exit 1
    ;;
esac
