#!/bin/bash

# Development utilities for the site
# Provides a command-line interface to development tasks

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
    echo -e "${BLUE}Development Utilities${NC}"
    echo "====================="
    echo -e "Usage: ${YELLOW}./scripts/bin/dev.sh ${GREEN}[command] [options]${NC}"
    echo ""
    echo -e "Commands:"
    echo -e "  ${GREEN}serve${NC}             Start the development server"
    echo -e "  ${GREEN}css${NC}               Watch CSS files for changes"
    echo -e "  ${GREEN}debug${NC}             Run with debug output"
    echo -e "  ${GREEN}lint${NC}              Lint JavaScript files"
    echo -e "  ${GREEN}lint:fix${NC}          Lint and fix JavaScript files"
    echo -e "  ${GREEN}format${NC}            Format files with Prettier"
    echo -e "  ${GREEN}test${NC}              Run tests"
    echo -e "  ${GREEN}help${NC}              Show this help message"
    echo ""
    echo -e "Examples:"
    echo -e "  ${YELLOW}./scripts/bin/dev.sh serve${NC}       # Start development server"
    echo -e "  ${YELLOW}./scripts/bin/dev.sh lint:fix${NC}    # Lint and fix JavaScript files"
}

# Handle different commands
case "$1" in
    "serve")
        echo -e "${GREEN}Starting development server...${NC}"
        npm run serve
        ;;

    "css")
        echo -e "${GREEN}Watching CSS files for changes...${NC}"
        npm run watch:css
        ;;

    "debug")
        echo -e "${GREEN}Running with debug output...${NC}"
        npm run debug
        ;;

    "lint")
        echo -e "${GREEN}Linting JavaScript files...${NC}"
        npm run lint
        ;;

    "lint:fix")
        echo -e "${GREEN}Linting and fixing JavaScript files...${NC}"
        npm run lint:fix
        ;;

    "format")
        echo -e "${GREEN}Formatting files with Prettier...${NC}"
        npm run format
        ;;

    "test")
        echo -e "${GREEN}Running tests...${NC}"
        echo -e "${YELLOW}No tests defined. Add tests in package.json.${NC}"
        ;;

    "help" | *)
        show_help
        ;;
esac
