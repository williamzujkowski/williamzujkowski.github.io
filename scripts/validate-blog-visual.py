#!/usr/bin/env python3
"""
Validate blog posts visual appearance using Playwright
Checks for proper rendering of Mermaid diagrams and overall layout
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess
import time

class BlogVisualValidator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.issues_found = []
        
    async def start_dev_server(self):
        """Start the Eleventy dev server"""
        print("🚀 Starting development server...")
        # Start server in background
        process = subprocess.Popen(
            ['npm', 'run', 'serve'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.base_path
        )
        
        # Wait for server to start
        await asyncio.sleep(5)
        return process
    
    async def validate_post(self, browser, post_slug: str, post_title: str):
        """Validate a single blog post"""
        page = await browser.new_page()
        url = f"http://localhost:8080/posts/{post_slug}/"
        
        try:
            print(f"\n📝 Checking: {post_title[:50]}...")
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Check if page loaded
            title = await page.title()
            if "404" in title or "Not Found" in title:
                self.issues_found.append(f"❌ 404 Error: {post_slug}")
                return
            
            # Check for Mermaid diagrams
            mermaid_elements = await page.query_selector_all('.mermaid, pre code.language-mermaid')
            if mermaid_elements:
                print(f"  ✅ Found {len(mermaid_elements)} Mermaid diagram(s)")
                
                # Check if diagrams rendered (should have SVG)
                for i, element in enumerate(mermaid_elements):
                    # Wait a bit for rendering
                    await asyncio.sleep(1)
                    
                    # Check if it contains SVG (rendered) or still has text (not rendered)
                    inner_html = await element.inner_html()
                    if '<svg' in inner_html:
                        print(f"    ✅ Diagram {i+1} rendered successfully")
                    elif 'graph' in inner_html or 'flowchart' in inner_html:
                        print(f"    ⚠️ Diagram {i+1} may not be rendered (still shows source)")
                        self.issues_found.append(f"Unrendered diagram in {post_slug}")
            
            # Check for code blocks
            code_blocks = await page.query_selector_all('pre code')
            if code_blocks:
                print(f"  📊 Found {len(code_blocks)} code blocks")
                
                # Check if any are too long
                for i, block in enumerate(code_blocks):
                    text = await block.inner_text()
                    lines = text.strip().split('\n')
                    if len(lines) > 30:
                        print(f"    ⚠️ Code block {i+1} has {len(lines)} lines (consider reducing)")
                        self.issues_found.append(f"Long code block ({len(lines)} lines) in {post_slug}")
            
            # Check for images
            images = await page.query_selector_all('article img')
            if images:
                print(f"  🖼️ Found {len(images)} images")
                for img in images:
                    alt = await img.get_attribute('alt')
                    src = await img.get_attribute('src')
                    if not alt:
                        print(f"    ⚠️ Image missing alt text: {src}")
                        self.issues_found.append(f"Missing alt text in {post_slug}: {src}")
            
            # Check page performance
            # Get content metrics
            content_height = await page.evaluate('document.body.scrollHeight')
            viewport_height = await page.evaluate('window.innerHeight')
            
            if content_height > viewport_height * 10:
                print(f"  ⚠️ Very long page ({content_height}px)")
                self.issues_found.append(f"Very long page in {post_slug}")
            
            # Take screenshot for manual review
            screenshot_dir = self.base_path / "validation_screenshots"
            screenshot_dir.mkdir(exist_ok=True)
            screenshot_path = screenshot_dir / f"{post_slug}.png"
            await page.screenshot(path=str(screenshot_path), full_page=False)
            print(f"  📸 Screenshot saved: {screenshot_path.name}")
            
        except Exception as e:
            print(f"  ❌ Error validating {post_slug}: {e}")
            self.issues_found.append(f"Validation error in {post_slug}: {str(e)}")
        finally:
            await page.close()
    
    async def validate_all_posts(self):
        """Validate all blog posts"""
        # Posts to validate (high-priority ones with new diagrams)
        posts_to_check = [
            ('2025-08-07-supercharging-development-claude-flow', 'Supercharging Development with Claude-Flow'),
            ('2025-07-15-vulnerability-management-scale-open-source', 'Vulnerability Management at Scale'),
            ('2025-07-01-ebpf-security-monitoring-practical-guide', 'eBPF for Security Monitoring'),
            ('2025-02-10-automating-home-network-security', 'Automating Home Network Security'),
            ('2025-03-10-raspberry-pi-security-projects', 'Raspberry Pi Security Projects'),
            ('2025-06-25-local-llm-deployment-privacy-first', 'Local LLM Deployment'),
        ]
        
        # Start dev server
        server_process = await self.start_dev_server()
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                
                print("\n" + "=" * 60)
                print("🔍 Visual Validation Starting...")
                print("=" * 60)
                
                for slug, title in posts_to_check:
                    await self.validate_post(browser, slug, title)
                    await asyncio.sleep(1)  # Rate limiting
                
                await browser.close()
                
                # Print summary
                print("\n" + "=" * 60)
                print("📊 Validation Summary")
                print("=" * 60)
                
                if self.issues_found:
                    print(f"\n⚠️ Found {len(self.issues_found)} issues:\n")
                    for issue in self.issues_found:
                        print(f"  • {issue}")
                else:
                    print("\n✅ All posts validated successfully!")
                
                print("\n📸 Screenshots saved in: validation_screenshots/")
                print("   Review them to ensure visual quality")
                
        finally:
            # Stop dev server
            server_process.terminate()
            await asyncio.sleep(1)
            server_process.kill()

async def main():
    validator = BlogVisualValidator()
    await validator.validate_all_posts()

if __name__ == "__main__":
    print("🎨 Blog Visual Validation Tool")
    print("This will check blog posts for:")
    print("  • Proper Mermaid diagram rendering")
    print("  • Code block length")
    print("  • Image alt text")
    print("  • Overall layout issues\n")
    
    asyncio.run(main())