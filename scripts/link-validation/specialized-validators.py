#!/usr/bin/env -S uv run python3
"""
SCRIPT: specialized-validators.py
PURPOSE: Specialized Link Validators
CATEGORY: utilities
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Specialized Link Validators. This script is part of the utilities
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/specialized-validators.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/specialized-validators.py

    # With verbose output
    python scripts/specialized-validators.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in utilities category]

MANIFEST_REGISTRY: scripts/specialized-validators.py
"""

import re
import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import hashlib

@dataclass
class SpecializedValidation:
    """Result from specialized validator"""
    url: str
    link_type: str
    is_valid: bool
    status_code: Optional[int]
    issues: List[str]
    metadata: Dict
    suggestions: List[str]
    timestamp: str

class GitHubValidator:
    """Validates GitHub links and checks repository/file status"""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.api_base = "https://api.github.com"

    async def validate(self, url: str) -> SpecializedValidation:
        """Validate GitHub URL"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')

        if len(path_parts) < 2:
            return self._create_result(url, False, ["Invalid GitHub URL format"], {})

        owner = path_parts[0]
        repo = path_parts[1]

        # Check repository exists
        api_url = f"{self.api_base}/repos/{owner}/{repo}"
        issues = []
        metadata = {}
        suggestions = []

        try:
            async with self.session.get(api_url) as response:
                if response.status == 404:
                    issues.append("Repository not found or private")
                    suggestions.append(f"Check if repo moved or was renamed")
                elif response.status == 200:
                    data = await response.json()
                    metadata['stars'] = data.get('stargazers_count', 0)
                    metadata['archived'] = data.get('archived', False)
                    metadata['fork'] = data.get('fork', False)

                    if metadata['archived']:
                        issues.append("Repository is archived")
                        suggestions.append("Consider finding active alternative")

                    # Check specific file if present
                    if len(path_parts) > 3 and path_parts[2] in ['blob', 'tree']:
                        branch = path_parts[3]
                        file_path = '/'.join(path_parts[4:])
                        if file_path:
                            file_url = f"{self.api_base}/repos/{owner}/{repo}/contents/{file_path}"
                            async with self.session.get(file_url) as file_response:
                                if file_response.status == 404:
                                    issues.append(f"File '{file_path}' not found")
                                    suggestions.append("File may have been moved or deleted")

                status_code = response.status

        except Exception as e:
            issues.append(f"Validation error: {str(e)}")
            status_code = None

        return self._create_result(url, len(issues) == 0, issues, metadata,
                                  suggestions, status_code)

    def _create_result(self, url: str, is_valid: bool, issues: List[str],
                      metadata: Dict, suggestions: List[str] = [],
                      status_code: Optional[int] = None) -> SpecializedValidation:
        return SpecializedValidation(
            url=url,
            link_type="github",
            is_valid=is_valid,
            status_code=status_code,
            issues=issues,
            metadata=metadata,
            suggestions=suggestions,
            timestamp=datetime.now().isoformat()
        )

class YouTubeValidator:
    """Validates YouTube links and checks video availability"""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def validate(self, url: str) -> SpecializedValidation:
        """Validate YouTube URL"""
        parsed = urlparse(url)
        issues = []
        metadata = {}
        suggestions = []

        # Extract video ID
        video_id = None
        if 'youtube.com' in parsed.netloc:
            if parsed.path == '/watch':
                query = parse_qs(parsed.query)
                video_id = query.get('v', [None])[0]
            elif '/embed/' in parsed.path:
                video_id = parsed.path.split('/embed/')[1].split('?')[0]
        elif 'youtu.be' in parsed.netloc:
            video_id = parsed.path.strip('/')

        if not video_id:
            return self._create_result(url, False, ["Invalid YouTube URL format"], {})

        # Check video availability using oembed
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}"

        try:
            async with self.session.get(oembed_url) as response:
                if response.status == 404:
                    issues.append("Video not found or private")
                    suggestions.append("Video may have been removed or made private")
                elif response.status == 200:
                    data = await response.json()
                    metadata['title'] = data.get('title', '')
                    metadata['author'] = data.get('author_name', '')

                status_code = response.status

        except Exception as e:
            issues.append(f"Validation error: {str(e)}")
            status_code = None

        return self._create_result(url, len(issues) == 0, issues, metadata,
                                  suggestions, status_code)

    def _create_result(self, url: str, is_valid: bool, issues: List[str],
                      metadata: Dict, suggestions: List[str] = [],
                      status_code: Optional[int] = None) -> SpecializedValidation:
        return SpecializedValidation(
            url=url,
            link_type="youtube",
            is_valid=is_valid,
            status_code=status_code,
            issues=issues,
            metadata=metadata,
            suggestions=suggestions,
            timestamp=datetime.now().isoformat()
        )

class DocumentationValidator:
    """Validates documentation links and checks version currency"""

    KNOWN_DOCS = {
        'docs.python.org': {'latest': '3.12', 'pattern': r'/(\d+\.\d+)/'},
        'docs.djangoproject.com': {'latest': '5.0', 'pattern': r'/(\d+\.\d+)/'},
        'docs.docker.com': {'versioned': False},
        'kubernetes.io': {'versioned': False},
        'docs.aws.amazon.com': {'versioned': False},
        'cloud.google.com': {'versioned': False},
        'docs.microsoft.com': {'versioned': False},
        'developer.mozilla.org': {'versioned': False}
    }

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def validate(self, url: str) -> SpecializedValidation:
        """Validate documentation URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        issues = []
        metadata = {}
        suggestions = []

        # Check if known documentation site
        doc_config = self.KNOWN_DOCS.get(domain)
        if doc_config and doc_config.get('versioned', True):
            pattern = doc_config.get('pattern')
            if pattern:
                import re
                match = re.search(pattern, parsed.path)
                if match:
                    version = match.group(1)
                    latest = doc_config.get('latest')
                    metadata['version'] = version
                    metadata['latest_version'] = latest

                    if latest and version != latest:
                        from packaging import version as pkg_version
                        try:
                            if pkg_version.parse(version) < pkg_version.parse(latest):
                                issues.append(f"Documentation for old version {version}")
                                suggestions.append(f"Update to latest version {latest}")
                                new_url = url.replace(f"/{version}/", f"/{latest}/")
                                suggestions.append(f"Try: {new_url}")
                        except:
                            pass

        # Check basic availability
        try:
            async with self.session.get(url, timeout=10) as response:
                status_code = response.status
                if status_code == 404:
                    issues.append("Documentation page not found")
                    suggestions.append("Page may have moved in recent docs restructuring")
                elif status_code >= 500:
                    issues.append(f"Documentation site error: {status_code}")

        except asyncio.TimeoutError:
            issues.append("Documentation site timeout")
            status_code = None
        except Exception as e:
            issues.append(f"Validation error: {str(e)}")
            status_code = None

        return SpecializedValidation(
            url=url,
            link_type="documentation",
            is_valid=len(issues) == 0,
            status_code=status_code,
            issues=issues,
            metadata=metadata,
            suggestions=suggestions,
            timestamp=datetime.now().isoformat()
        )

class SocialMediaValidator:
    """Validates social media links (Twitter/X, LinkedIn, etc.)"""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def validate(self, url: str) -> SpecializedValidation:
        """Validate social media URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        issues = []
        metadata = {}
        suggestions = []

        # Handle Twitter/X transition
        if domain in ['twitter.com', 'x.com']:
            metadata['platform'] = 'twitter/x'
            # Check if old twitter.com URL
            if domain == 'twitter.com':
                suggestions.append("Consider updating to x.com URL")
                new_url = url.replace('twitter.com', 'x.com')
                suggestions.append(f"New URL: {new_url}")

        elif 'linkedin.com' in domain:
            metadata['platform'] = 'linkedin'
        elif 'reddit.com' in domain:
            metadata['platform'] = 'reddit'
        else:
            metadata['platform'] = domain

        # Basic availability check
        try:
            async with self.session.get(url, timeout=10, allow_redirects=True) as response:
                status_code = response.status
                final_url = str(response.url)

                if status_code == 404:
                    issues.append("Profile or content not found")
                    suggestions.append("User may have deleted account or content")
                elif final_url != url:
                    metadata['redirected_to'] = final_url
                    if 'twitter.com' in url and 'x.com' in final_url:
                        suggestions.append(f"Update to new URL: {final_url}")

        except Exception as e:
            issues.append(f"Validation error: {str(e)}")
            status_code = None

        return SpecializedValidation(
            url=url,
            link_type="social_media",
            is_valid=len(issues) == 0,
            status_code=status_code,
            issues=issues,
            metadata=metadata,
            suggestions=suggestions,
            timestamp=datetime.now().isoformat()
        )

class ImageValidator:
    """Validates image links and checks availability"""

    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico']

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def validate(self, url: str) -> SpecializedValidation:
        """Validate image URL"""
        parsed = urlparse(url)
        path_lower = parsed.path.lower()
        issues = []
        metadata = {}
        suggestions = []

        # Check if likely an image
        is_image = any(path_lower.endswith(ext) for ext in self.IMAGE_EXTENSIONS)
        if not is_image and 'image' not in path_lower:
            metadata['likely_image'] = False

        try:
            async with self.session.head(url, timeout=10) as response:
                status_code = response.status
                content_type = response.headers.get('Content-Type', '')
                content_length = response.headers.get('Content-Length')

                metadata['content_type'] = content_type
                if content_length:
                    size_mb = int(content_length) / (1024 * 1024)
                    metadata['size_mb'] = round(size_mb, 2)
                    if size_mb > 5:
                        issues.append(f"Large image size: {size_mb:.2f} MB")
                        suggestions.append("Consider optimizing or using smaller image")

                if status_code == 404:
                    issues.append("Image not found")
                    suggestions.append("Image may have been moved or deleted")
                elif not content_type.startswith('image/'):
                    issues.append(f"Not an image: {content_type}")

        except Exception as e:
            issues.append(f"Validation error: {str(e)}")
            status_code = None

        return SpecializedValidation(
            url=url,
            link_type="image",
            is_valid=len(issues) == 0,
            status_code=status_code,
            issues=issues,
            metadata=metadata,
            suggestions=suggestions,
            timestamp=datetime.now().isoformat()
        )

class SpecializedValidatorOrchestrator:
    """Orchestrates specialized validators based on URL patterns"""

    def __init__(self):
        self.session = None
        self.validators = {}

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        self.validators = {
            'github': GitHubValidator(self.session),
            'youtube': YouTubeValidator(self.session),
            'documentation': DocumentationValidator(self.session),
            'social_media': SocialMediaValidator(self.session),
            'image': ImageValidator(self.session)
        }
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def detect_link_type(self, url: str) -> str:
        """Detect the type of link"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        # GitHub
        if 'github.com' in domain or 'githubusercontent.com' in domain:
            return 'github'

        # YouTube
        if 'youtube.com' in domain or 'youtu.be' in domain:
            return 'youtube'

        # Documentation sites
        doc_domains = ['docs.', 'developer.', 'kubernetes.io', 'cloud.google.com',
                      'docs.microsoft.com', 'docs.aws.amazon.com']
        if any(d in domain for d in doc_domains):
            return 'documentation'

        # Social media
        social_domains = ['twitter.com', 'x.com', 'linkedin.com', 'reddit.com',
                         'facebook.com', 'instagram.com']
        if any(d in domain for d in social_domains):
            return 'social_media'

        # Images
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        if any(path.endswith(ext) for ext in image_extensions):
            return 'image'

        return 'generic'

    async def validate(self, url: str) -> Optional[SpecializedValidation]:
        """Validate URL with appropriate specialized validator"""
        link_type = self.detect_link_type(url)

        if link_type in self.validators:
            return await self.validators[link_type].validate(url)

        return None

    async def validate_batch(self, urls: List[str]) -> List[SpecializedValidation]:
        """Validate multiple URLs concurrently"""
        tasks = [self.validate(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

async def main():
    """Test specialized validators"""
    test_urls = [
        "https://github.com/anthropics/claude-flow",
        "https://github.com/fake-owner/fake-repo",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://docs.python.org/3.8/library/asyncio.html",
        "https://twitter.com/anthropicai",
        "https://images.unsplash.com/photo-123456789"
    ]

    async with SpecializedValidatorOrchestrator() as orchestrator:
        results = await orchestrator.validate_batch(test_urls)

        for result in results:
            print(f"\n{result.link_type.upper()}: {result.url}")
            print(f"  Valid: {result.is_valid}")
            if result.issues:
                print(f"  Issues: {', '.join(result.issues)}")
            if result.suggestions:
                print(f"  Suggestions: {', '.join(result.suggestions)}")
            if result.metadata:
                print(f"  Metadata: {result.metadata}")

if __name__ == "__main__":
    asyncio.run(main())