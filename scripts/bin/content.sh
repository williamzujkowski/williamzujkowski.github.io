#!/bin/bash

# Content management utilities for the site
# Provides a command-line interface to content management tasks

# Color constants
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to the root directory of the project
cd "$(dirname "$0")/../.."

# Display help message
function show_help {
    echo -e "${BLUE}Content Management Utilities${NC}"
    echo "============================"
    echo -e "Usage: ${YELLOW}./scripts/bin/content.sh ${GREEN}[command] [options]${NC}"
    echo ""
    echo -e "Commands:"
    echo -e "  ${GREEN}blog:process${NC}      Process new blog posts"
    echo -e "  ${GREEN}blog:enhanced${NC}     Enhanced blog post processing (interactive)"
    echo -e "  ${GREEN}blog:batch${NC}        Process blog posts in batch mode"
    echo -e "  ${GREEN}blog:fix${NC}          Fix blog post formatting issues"
    echo -e "  ${GREEN}links:check${NC}       Check for missing link previews"
    echo -e "  ${GREEN}links:update${NC}      Update link previews"
    echo -e "  ${GREEN}links:update-all${NC}  Force update all link previews"
    echo -e "  ${GREEN}screenshots${NC}       Generate screenshots for links"
    echo -e "  ${GREEN}help${NC}              Show this help message"
    echo ""
    echo -e "Examples:"
    echo -e "  ${YELLOW}./scripts/bin/content.sh blog:process${NC}      # Process new blog posts"
    echo -e "  ${YELLOW}./scripts/bin/content.sh links:update${NC}      # Update link previews"
}

# Handle different commands
case "$1" in
    "blog:process")
        echo -e "${GREEN}Processing new blog posts...${NC}"
        npm run process:posts
        ;;
        
    "blog:enhanced")
        echo -e "${GREEN}Running enhanced blog post processing (interactive)...${NC}"
        npm run process:posts:enhanced
        ;;
        
    "blog:batch")
        echo -e "${GREEN}Processing blog posts in batch mode...${NC}"
        npm run process:posts:batch
        ;;
        
    "blog:fix")
        echo -e "${GREEN}Fixing blog post formatting issues...${NC}"
        npm run standardize:frontmatter
        ;;
        
    "links:check")
        echo -e "${GREEN}Checking for missing link previews...${NC}"
        npm run check:links
        ;;
        
    "links:update")
        echo -e "${GREEN}Updating link previews...${NC}"
        npm run update:links
        ;;
        
    "links:update-all")
        echo -e "${GREEN}Force updating all link previews...${NC}"
        npm run update:links:all
        ;;
        
    "screenshots")
        echo -e "${GREEN}Generating screenshots for links...${NC}"
        npm run screenshots
        ;;
        
    "help" | *)
        show_help
        ;;
esac