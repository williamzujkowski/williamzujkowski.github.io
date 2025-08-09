#!/usr/bin/env python3
"""
Visual check of the live site to see actual button issue
"""

import asyncio
from playwright.async_api import async_playwright

async def visual_check():
    """Check visually what's on the page"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser
        page = await browser.new_page()
        
        print("=" * 70)
        print("🖼️ Visual Check of Live Site")
        print("=" * 70)
        
        url = "https://williamzujkowski.github.io/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/"
        print(f"\n📝 Opening: {url}")
        print("Browser window will open - please check visually for buttons on Mermaid diagrams")
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Scroll to first Mermaid diagram
        first_mermaid = await page.query_selector('.mermaid-container')
        if first_mermaid:
            await first_mermaid.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            print("\n✅ Scrolled to first Mermaid diagram")
            
            # Take screenshot of first diagram
            await first_mermaid.screenshot(path="first_mermaid_diagram.png")
            print("📸 Screenshot of first diagram: first_mermaid_diagram.png")
        
        # Scroll to second Mermaid diagram
        mermaid_containers = await page.query_selector_all('.mermaid-container')
        if len(mermaid_containers) > 1:
            await mermaid_containers[1].scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            print("\n✅ Scrolled to second Mermaid diagram")
            
            # Take screenshot of second diagram
            await mermaid_containers[1].screenshot(path="second_mermaid_diagram.png")
            print("📸 Screenshot of second diagram: second_mermaid_diagram.png")
        
        # Check for any visible buttons with text
        buttons_with_expand = await page.query_selector_all('button:has-text("Expand")')
        buttons_with_collapse = await page.query_selector_all('button:has-text("Collapse")')
        
        print(f"\n🔘 Buttons found:")
        print(f"   - Buttons with 'Expand': {len(buttons_with_expand)}")
        print(f"   - Buttons with 'Collapse': {len(buttons_with_collapse)}")
        
        # Check what elements have buttons
        for btn in buttons_with_expand[:3]:  # Check first 3
            parent = await btn.evaluate('''(btn) => {
                let p = btn.parentElement;
                while (p && !p.classList.contains('mermaid-container') && !p.tagName.match(/^(PRE|CODE|DIV)$/)) {
                    p = p.parentElement;
                }
                return {
                    tag: p ? p.tagName : 'unknown',
                    classes: p ? p.className : '',
                    isMermaid: p ? p.classList.contains('mermaid-container') : false
                };
            }''')
            print(f"\n   Button parent: {parent}")
        
        print("\n⏳ Keeping browser open for 10 seconds for visual inspection...")
        await page.wait_for_timeout(10000)
        
        await browser.close()
        
        print("\n" + "=" * 70)
        print("Visual check complete - check screenshot files")

if __name__ == "__main__":
    asyncio.run(visual_check())