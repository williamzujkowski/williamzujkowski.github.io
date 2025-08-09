#!/usr/bin/env python3
"""
Test live website improvements using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

class LiveSiteTester:
    def __init__(self):
        self.base_url = "https://williamzujkowski.github.io"
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
    
    async def test_homepage_load(self, page):
        """Test homepage loading and structure."""
        print("🔍 Testing homepage...")
        await page.goto(self.base_url)
        
        # Check title
        title = await page.title()
        
        # Check for key sections
        hero = await page.query_selector('.hero')
        posts = await page.query_selector('.post-list')
        
        result = {
            "test": "homepage_load",
            "status": "pass" if hero and posts else "fail",
            "title": title,
            "has_hero": hero is not None,
            "has_posts": posts is not None
        }
        
        self.test_results["tests"].append(result)
        print(f"  ✅ Homepage loaded: {title}")
        return result
    
    async def test_blog_post_citations(self, page):
        """Test that blog posts have academic citations."""
        print("🔍 Testing blog post citations...")
        
        # Test posts we added citations to
        test_posts = [
            "/posts/2024-07-16-sustainable-computing-carbon-footprint/",
            "/posts/2024-07-09-zero-trust-architecture-implementation/",
            "/posts/2025-08-07-supercharging-development-claude-flow/"
        ]
        
        citation_results = []
        
        for post_url in test_posts:
            try:
                await page.goto(self.base_url + post_url, wait_until="networkidle")
                
                # Check for academic research section
                content = await page.content()
                has_academic = "Academic Research" in content or "Research & Industry Resources" in content
                
                # Count citations (look for arxiv, ieee, nist links)
                arxiv_links = await page.query_selector_all('a[href*="arxiv.org"]')
                nist_links = await page.query_selector_all('a[href*="nist.gov"]')
                ieee_links = await page.query_selector_all('a[href*="ieee.org"]')
                
                total_citations = len(arxiv_links) + len(nist_links) + len(ieee_links)
                
                result = {
                    "post": post_url,
                    "has_academic_section": has_academic,
                    "arxiv_citations": len(arxiv_links),
                    "nist_citations": len(nist_links),
                    "ieee_citations": len(ieee_links),
                    "total_citations": total_citations
                }
                
                citation_results.append(result)
                print(f"  ✅ {post_url.split('/')[-2]}: {total_citations} citations found")
                
            except Exception as e:
                print(f"  ❌ Error testing {post_url}: {e}")
                citation_results.append({
                    "post": post_url,
                    "error": str(e)
                })
        
        self.test_results["tests"].append({
            "test": "blog_citations",
            "results": citation_results
        })
        
        return citation_results
    
    async def test_visual_elements(self, page):
        """Test for visual elements like Mermaid diagrams."""
        print("🔍 Testing visual elements...")
        
        # Test AI Edge Computing post which has Mermaid diagram
        await page.goto(self.base_url + "/posts/2024-10-22-ai-edge-computing/", wait_until="networkidle")
        
        # Check for Mermaid diagrams
        mermaid_elements = await page.query_selector_all('.mermaid')
        
        # Check for code blocks
        code_blocks = await page.query_selector_all('pre code')
        
        # Check for images
        images = await page.query_selector_all('article img')
        
        result = {
            "test": "visual_elements",
            "mermaid_diagrams": len(mermaid_elements),
            "code_blocks": len(code_blocks),
            "images": len(images)
        }
        
        self.test_results["tests"].append(result)
        print(f"  ✅ Found {len(mermaid_elements)} Mermaid diagrams, {len(code_blocks)} code blocks, {len(images)} images")
        
        return result
    
    async def test_navigation(self, page):
        """Test site navigation."""
        print("🔍 Testing navigation...")
        
        await page.goto(self.base_url)
        
        # Check navigation links
        nav_links = await page.query_selector_all('nav a')
        
        navigation_results = []
        for link in nav_links[:5]:  # Test first 5 nav links
            href = await link.get_attribute('href')
            text = await link.text_content()
            navigation_results.append({
                "text": text.strip(),
                "href": href
            })
        
        result = {
            "test": "navigation",
            "nav_links_count": len(nav_links),
            "sample_links": navigation_results
        }
        
        self.test_results["tests"].append(result)
        print(f"  ✅ Found {len(nav_links)} navigation links")
        
        return result
    
    async def test_performance_metrics(self, page):
        """Test page performance metrics."""
        print("🔍 Testing performance metrics...")
        
        await page.goto(self.base_url)
        
        # Get performance timing
        performance_timing = await page.evaluate("""() => {
            const timing = performance.timing;
            return {
                domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                loadComplete: timing.loadEventEnd - timing.navigationStart,
                domInteractive: timing.domInteractive - timing.navigationStart
            };
        }""")
        
        result = {
            "test": "performance",
            "metrics": performance_timing,
            "status": "pass" if performance_timing['loadComplete'] < 5000 else "warning"
        }
        
        self.test_results["tests"].append(result)
        print(f"  ✅ Page load time: {performance_timing['loadComplete']}ms")
        
        return result
    
    async def run_all_tests(self):
        """Run all website tests."""
        print("="*60)
        print("TESTING LIVE WEBSITE IMPROVEMENTS")
        print("="*60)
        print(f"URL: {self.base_url}\n")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Run tests
            await self.test_homepage_load(page)
            await self.test_blog_post_citations(page)
            await self.test_visual_elements(page)
            await self.test_navigation(page)
            await self.test_performance_metrics(page)
            
            await browser.close()
        
        # Save results
        with open('docs/live-site-test-results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        # Summarize results
        total_tests = len(self.test_results["tests"])
        passed = sum(1 for t in self.test_results["tests"] if t.get("status") != "fail")
        
        print(f"Total tests run: {total_tests}")
        print(f"Tests passed: {passed}/{total_tests}")
        
        # Check citation improvements
        citation_test = next((t for t in self.test_results["tests"] if t["test"] == "blog_citations"), None)
        if citation_test:
            total_citations = sum(r.get("total_citations", 0) for r in citation_test["results"] if "error" not in r)
            print(f"Total academic citations found: {total_citations}")
        
        print(f"\nResults saved to: docs/live-site-test-results.json")
        
        return self.test_results

async def main():
    tester = LiveSiteTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())