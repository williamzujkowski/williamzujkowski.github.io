#!/usr/bin/env python3
"""
Validate all Mermaid diagrams on the live website using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
from pathlib import Path

class MermaidValidator:
    def __init__(self):
        self.base_url = "https://williamzujkowski.github.io"
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "posts_checked": 0,
            "posts_with_mermaid": 0,
            "posts_with_errors": 0,
            "errors": []
        }
    
    async def get_all_post_urls(self, page):
        """Get all blog post URLs from the posts page."""
        await page.goto(f"{self.base_url}/posts/", wait_until="networkidle")
        
        # Get all post links
        post_links = await page.evaluate("""() => {
            const links = document.querySelectorAll('article a[href*="/posts/"]');
            return Array.from(links).map(link => link.href).filter(href => !href.includes('#'));
        }""")
        
        # Remove duplicates
        unique_links = list(set(post_links))
        print(f"Found {len(unique_links)} blog posts to check")
        
        return unique_links
    
    async def check_mermaid_diagram(self, page, post_url):
        """Check a single post for Mermaid diagram errors."""
        try:
            await page.goto(post_url, wait_until="networkidle", timeout=30000)
            
            # Wait a bit for Mermaid to render
            await page.wait_for_timeout(2000)
            
            # Check for Mermaid diagrams
            mermaid_elements = await page.query_selector_all('.mermaid')
            
            if not mermaid_elements:
                return None
            
            # Check for syntax errors
            errors = await page.evaluate("""() => {
                const errorElements = document.querySelectorAll('.mermaid');
                const errors = [];
                
                errorElements.forEach((element, index) => {
                    const text = element.textContent || element.innerText || '';
                    if (text.includes('Syntax error') || text.includes('Parse error')) {
                        errors.push({
                            index: index + 1,
                            error: text.substring(0, 200)
                        });
                    }
                });
                
                return errors;
            }""")
            
            # Check console for Mermaid errors
            console_errors = []
            
            # Set up console listener
            def handle_console(msg):
                if 'mermaid' in msg.text.lower() and ('error' in msg.text.lower() or 'fail' in msg.text.lower()):
                    console_errors.append(msg.text)
            
            page.on("console", handle_console)
            
            # Reload to catch console errors
            await page.reload()
            await page.wait_for_timeout(2000)
            
            result = {
                "url": post_url,
                "title": await page.title(),
                "mermaid_count": len(mermaid_elements),
                "syntax_errors": errors,
                "console_errors": console_errors,
                "has_errors": len(errors) > 0 or len(console_errors) > 0
            }
            
            return result
            
        except Exception as e:
            return {
                "url": post_url,
                "error": str(e),
                "has_errors": True
            }
    
    async def validate_all_posts(self):
        """Validate Mermaid diagrams on all blog posts."""
        print("="*60)
        print("VALIDATING MERMAID DIAGRAMS ON LIVE WEBSITE")
        print("="*60)
        print(f"URL: {self.base_url}\n")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Get all post URLs
            post_urls = await self.get_all_post_urls(page)
            self.validation_results["posts_checked"] = len(post_urls)
            
            print(f"\n🔍 Checking {len(post_urls)} posts for Mermaid diagrams...\n")
            
            # Check each post
            for i, url in enumerate(post_urls, 1):
                post_name = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
                print(f"[{i}/{len(post_urls)}] Checking: {post_name}...", end=" ")
                
                result = await self.check_mermaid_diagram(page, url)
                
                if result:
                    if result.get("mermaid_count", 0) > 0:
                        self.validation_results["posts_with_mermaid"] += 1
                        
                        if result.get("has_errors"):
                            self.validation_results["posts_with_errors"] += 1
                            self.validation_results["errors"].append(result)
                            print(f"❌ ERRORS FOUND")
                            if result.get("syntax_errors"):
                                for err in result["syntax_errors"]:
                                    print(f"    - Diagram {err['index']}: Syntax error")
                        else:
                            print(f"✅ {result['mermaid_count']} diagrams OK")
                    else:
                        print("⚪ No Mermaid diagrams")
                else:
                    print("⚪ Skipped")
                
                # Be respectful to the server
                await page.wait_for_timeout(500)
            
            await browser.close()
        
        # Print summary
        self.print_summary()
        
        # Save results
        self.save_results()
        
        return self.validation_results
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        print(f"Total posts checked: {self.validation_results['posts_checked']}")
        print(f"Posts with Mermaid diagrams: {self.validation_results['posts_with_mermaid']}")
        print(f"Posts with errors: {self.validation_results['posts_with_errors']}")
        
        if self.validation_results["errors"]:
            print("\n❌ POSTS WITH ERRORS:")
            for error in self.validation_results["errors"]:
                post_name = error["url"].split('/')[-2] if error["url"].endswith('/') else error["url"].split('/')[-1]
                print(f"\n  📄 {post_name}")
                print(f"     URL: {error['url']}")
                if error.get("syntax_errors"):
                    for err in error["syntax_errors"]:
                        print(f"     - Diagram {err['index']}: Syntax error")
                if error.get("console_errors"):
                    for err in error["console_errors"]:
                        print(f"     - Console: {err[:100]}")
        else:
            print("\n✅ All Mermaid diagrams are rendering correctly!")
    
    def save_results(self):
        """Save validation results to file."""
        output_path = Path("docs/mermaid-validation-results.json")
        
        with open(output_path, 'w') as f:
            json.dump(self.validation_results, f, indent=2, default=str)
        
        print(f"\nResults saved to: {output_path}")

async def main():
    validator = MermaidValidator()
    results = await validator.validate_all_posts()
    
    # Return success/failure
    return results["posts_with_errors"] == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)