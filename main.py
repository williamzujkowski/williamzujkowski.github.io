#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import tomli
import tomli_w
from rich.logging import RichHandler
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Static
from textual.containers import Container

# Local modules
from pages.home import HomePage
from pages.links import LinksPage
from pages.blog import BlogPage
from pages.placeholder import PlaceholderPage
from utils.builder import StaticSiteBuilder
from utils.navigation import NavigationSidebar

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RichHandler(rich_tracebacks=True),
        logging.FileHandler(log_dir / "app.log"),
    ],
)

logger = logging.getLogger("williamzujkowski.github.io")


class WebsiteApp(App):
    """Main Textual application for William Zujkowski's website."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("h", "show_page('home')", "Home"),
        Binding("l", "show_page('links')", "Links"),
        Binding("b", "show_page('blog')", "Blog"),
    ]

    def __init__(self, config_path: str = "site_config.toml", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_path = config_path
        self.config = self._load_config()
        self.current_page = "home"
        self.pages = {}
        self.env = os.environ.get("SITE_ENV", "development")
        logger.info(f"Starting app in {self.env} environment")

    def _load_config(self) -> Dict:
        """Load configuration from TOML file."""
        try:
            with open(self.config_path, "rb") as f:
                config = tomli.load(f)
                logger.info(f"Loaded configuration from {self.config_path}")
                return config
        except (FileNotFoundError, tomli.TOMLDecodeError) as e:
            logger.error(f"Failed to load configuration: {e}")
            # Return default configuration
            return {
                "site": {
                    "title": "William Zujkowski",
                    "description": "Personal website and blog",
                    "base_url": "https://williamzujkowski.github.io",
                },
                "navigation": [
                    {"name": "Home", "path": "home"},
                    {"name": "Links", "path": "links"},
                    {"name": "Blog", "path": "blog"},
                ],
                "environments": {
                    "development": {
                        "debug": True,
                        "log_level": "DEBUG",
                    },
                    "production": {
                        "debug": False,
                        "log_level": "INFO",
                    },
                },
            }

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        site_title = self.config["site"].get("title", "William Zujkowski")
        yield Header(show_clock=True)

        with Container(id="main-container"):
            yield NavigationSidebar(config=self.config)
            
            # Initialize all pages but only show the home page initially
            self.pages["home"] = HomePage(self.config)
            self.pages["links"] = LinksPage(self.config)
            self.pages["blog"] = BlogPage(self.config)
            self.pages["placeholder"] = PlaceholderPage("Placeholder", self.config)
            
            # Add all pages to the container
            for page_id, page in self.pages.items():
                page.visible = page_id == self.current_page
                yield page

        yield Footer()

    def action_show_page(self, page_id: str) -> None:
        """Switch to a different page."""
        logger.debug(f"Switching to page: {page_id}")

        if page_id not in self.pages:
            logger.error(f"Page not found: {page_id}")
            return

        # Hide all pages and show the selected one
        for pid, page in self.pages.items():
            page.visible = pid == page_id

        self.current_page = page_id


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="William Zujkowski's Textual-based website"
    )
    parser.add_argument(
        "--config",
        default="site_config.toml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build static site for GitHub Pages",
    )
    parser.add_argument(
        "--env",
        choices=["development", "production"],
        default="development",
        help="Environment (development or production)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level",
    )
    return parser.parse_args()


def main():
    """Main entry point for the application."""
    args = parse_args()

    # Set environment variable
    os.environ["SITE_ENV"] = args.env

    # Adjust log level if specified
    if args.log_level:
        logging.getLogger().setLevel(getattr(logging, args.log_level))
        logger.setLevel(getattr(logging, args.log_level))
        logger.info(f"Log level set to {args.log_level}")

    # Load configuration
    try:
        with open(args.config, "rb") as f:
            config = tomli.load(f)
    except (FileNotFoundError, tomli.TOMLDecodeError) as e:
        logger.error(f"Error loading configuration: {e}")
        # Create a default configuration file
        default_config = {
            "site": {
                "title": "William Zujkowski",
                "description": "Personal website and blog",
                "base_url": "https://williamzujkowski.github.io",
            },
            "navigation": [
                {"name": "Home", "path": "home"},
                {"name": "Links", "path": "links"},
                {"name": "Blog", "path": "blog"},
            ],
            "environments": {
                "development": {
                    "debug": True,
                    "log_level": "DEBUG",
                },
                "production": {
                    "debug": False,
                    "log_level": "INFO",
                },
            },
        }
        config_path = Path(args.config)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "wb") as f:
            tomli_w.dump(default_config, f)
        logger.info(f"Created default configuration file at {args.config}")
        config = default_config

    # Apply environment-specific configuration
    env_config = config.get("environments", {}).get(args.env, {})
    log_level = env_config.get("log_level", args.log_level or "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    logger.setLevel(getattr(logging, log_level))

    if args.build:
        logger.info("Building static site for GitHub Pages")
        builder = StaticSiteBuilder(config)
        builder.build()
        logger.info("Static site built successfully")
    else:
        logger.info("Starting interactive app")
        app = WebsiteApp(args.config)
        app.run()


if __name__ == "__main__":
    main()
