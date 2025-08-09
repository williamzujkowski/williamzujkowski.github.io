#!/usr/bin/env python3
"""
Validate Mermaid diagrams and images on the live website
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import json

class LiveSiteValidator:
    def __init__(self):
        self.base_url = "https://williamzujkowski.github.io"
        self.issues = []
        self.results = {}
        
    async def check_post(self, browser, slug: str, title: str):
        """Check a single blog post for Mermaid and images"""
        page = await browser.new_page()
        url = f"{self.base_url}/posts/{slug}/"
        
        try:
            print(f"\n🔍 Checking: {title[:50]}...")
            print(f"   URL: {url}")
            
            # Navigate to the page
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Check page title to ensure it loaded
            actual_title = await page.title()
            if "404" in actual_title:
                self.issues.append(f"❌ 404 Error: {slug}")
                return {"error": "404"}
            
            result = {
                "url": url,
                "title": title,
                "mermaid_diagrams": 0,
                "rendered_diagrams": 0,
                "images": 0,
                "hero_images": 0,
                "issues": []
            }
            
            # Check for Mermaid diagram elements
            # Look for both pre>code.language-mermaid (unrendered) and svg (rendered)
            mermaid_code_blocks = await page.query_selector_all('pre code.language-mermaid')
            mermaid_divs = await page.query_selector_all('div.mermaid')
            svg_diagrams = await page.query_selector_all('svg[id*="mermaid"], svg.mermaid-svg')
            
            print(f"   📊 Mermaid code blocks found: {len(mermaid_code_blocks)}")
            print(f"   📊 Mermaid divs found: {len(mermaid_divs)}")
            print(f"   📊 SVG diagrams found: {len(svg_diagrams)}")
            
            result["mermaid_diagrams"] = len(mermaid_code_blocks) + len(mermaid_divs)
            
            # Check if Mermaid actually rendered (should see SVGs)
            if len(mermaid_code_blocks) > 0 and len(svg_diagrams) == 0:
                print(f"   ⚠️ Mermaid blocks found but NOT rendered!")
                result["issues"].append("Mermaid not rendering")
                self.issues.append(f"Mermaid not rendering in {slug}")
                
                # Check if Mermaid script is loaded
                mermaid_loaded = await page.evaluate("typeof window.mermaid !== 'undefined'")
                print(f"   📦 Mermaid library loaded: {mermaid_loaded}")
                
                if not mermaid_loaded:
                    result["issues"].append("Mermaid library not loaded")
            else:
                result["rendered_diagrams"] = len(svg_diagrams)
                if len(svg_diagrams) > 0:
                    print(f"   ✅ {len(svg_diagrams)} Mermaid diagrams rendered successfully!")
            
            # Check for images
            all_images = await page.query_selector_all('article img')
            hero_images = await page.query_selector_all('article img[src*="hero"], article img[src*="stock"]')
            
            print(f"   🖼️ Total images: {len(all_images)}")
            print(f"   🎨 Hero/stock images: {len(hero_images)}")
            
            result["images"] = len(all_images)
            result["hero_images"] = len(hero_images)
            
            if len(all_images) == 0:
                print(f"   ⚠️ No images found in article")
                result["issues"].append("No images")
            
            # Check for broken images
            for img in all_images:
                src = await img.get_attribute('src')
                # Check if image loaded
                is_broken = await img.evaluate("(img) => img.naturalWidth === 0")
                if is_broken:
                    print(f"   ❌ Broken image: {src}")
                    result["issues"].append(f"Broken image: {src}")
                    self.issues.append(f"Broken image in {slug}: {src}")
            
            # Take a screenshot for manual review
            screenshot_dir = Path("live_site_screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            screenshot_path = screenshot_dir / f"{slug}.png"
            await page.screenshot(path=str(screenshot_path), full_page=False)
            print(f"   📸 Screenshot saved: {screenshot_path.name}")
            
            self.results[slug] = result
            
        except Exception as e:
            print(f"   ❌ Error checking {slug}: {e}")
            self.issues.append(f"Error checking {slug}: {str(e)}")
            result["error"] = str(e)
            self.results[slug] = result
        finally:
            await page.close()
        
        return result
    
    async def validate_all_posts(self):
        """Validate key blog posts on the live site"""
        
        # Posts that should have Mermaid diagrams (using actual live URLs)
        posts_to_check = [
            ("supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering", "Supercharging Development with Claude-Flow"),
            ("vulnerability-management-at-scale-with-open-source-tools", "Vulnerability Management at Scale"),
            ("ebpf-for-security-monitoring-a-practical-guide", "eBPF for Security Monitoring"),
            ("implementing-zero-trust-security-never-trust-always-verify", "Zero Trust Security"),
            ("building-a-security-mindset-lessons-from-the-field", "Building Security Mindset"),
            ("local-llm-deployment-privacy-first-approach", "Local LLM Deployment"),
        ]
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            print("=" * 70)
            print("🌐 Live Site Validation - williamzujkowski.github.io")
            print("=" * 70)
            
            for slug, title in posts_to_check:
                await self.check_post(browser, slug, title)
                await asyncio.sleep(2)  # Be nice to the server
            
            await browser.close()
            
            # Print summary
            print("\n" + "=" * 70)
            print("📊 Validation Summary")
            print("=" * 70)
            
            total_mermaid = sum(r.get("mermaid_diagrams", 0) for r in self.results.values())
            total_rendered = sum(r.get("rendered_diagrams", 0) for r in self.results.values())
            total_images = sum(r.get("images", 0) for r in self.results.values())
            total_hero = sum(r.get("hero_images", 0) for r in self.results.values())
            
            print(f"\n📈 Overall Statistics:")
            print(f"   Posts checked: {len(self.results)}")
            print(f"   Mermaid diagrams found: {total_mermaid}")
            print(f"   Mermaid diagrams rendered: {total_rendered}")
            print(f"   Total images: {total_images}")
            print(f"   Hero/stock images: {total_hero}")
            
            if self.issues:
                print(f"\n⚠️ Issues Found ({len(self.issues)}):")
                for issue in self.issues:
                    print(f"   • {issue}")
            else:
                print("\n✅ No issues found!")
            
            # Save detailed results
            with open("live_site_validation.json", "w") as f:
                json.dump(self.results, f, indent=2)
            print(f"\n📁 Detailed results saved to: live_site_validation.json")
            
            return self.results

async def main():
    validator = LiveSiteValidator()
    results = await validator.validate_all_posts()
    
    # Return exit code based on issues
    if validator.issues:
        return 1
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)