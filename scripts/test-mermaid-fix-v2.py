#!/usr/bin/env python3
"""
Test the updated Mermaid fix locally
"""

import asyncio
from playwright.async_api import async_playwright

async def test_fix():
    """Test that Mermaid diagrams work without buttons"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for debugging
        page = await browser.new_page()
        
        print("=" * 70)
        print("🧪 Testing Updated Mermaid Fix Locally")
        print("=" * 70)
        
        # Enable console logging
        page.on("console", lambda msg: print(f"  Console: {msg.text}"))
        
        url = "http://localhost:8080/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/"
        print(f"\n📝 Loading: {url}")
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)  # Give scripts time to run
        
        # Check what elements exist
        print("\n📊 Element Analysis:")
        
        # Check for Mermaid elements
        mermaid_containers = await page.query_selector_all('.mermaid-container')
        mermaid_divs = await page.query_selector_all('div.mermaid')
        svg_diagrams = await page.query_selector_all('.mermaid svg, svg[id*="mermaid"]')
        pre_mermaid = await page.query_selector_all('pre code.language-mermaid')
        
        print(f"  Mermaid containers: {len(mermaid_containers)}")
        print(f"  Mermaid divs: {len(mermaid_divs)}")
        print(f"  SVG diagrams: {len(svg_diagrams)}")
        print(f"  Pre code.language-mermaid (should be 0): {len(pre_mermaid)}")
        
        # Check for buttons
        all_buttons = await page.query_selector_all('button')
        toggle_buttons = await page.query_selector_all('.code-toggle-btn')
        expand_buttons = await page.query_selector_all('button:has-text("Expand")')
        
        print(f"\n🔘 Button Analysis:")
        print(f"  Total buttons: {len(all_buttons)}")
        print(f"  Toggle buttons: {len(toggle_buttons)}")
        print(f"  Expand buttons: {len(expand_buttons)}")
        
        # Check each Mermaid container
        print(f"\n🔍 Mermaid Container Check:")
        for i, container in enumerate(mermaid_containers):
            buttons_inside = await container.query_selector_all('button')
            is_visible = await container.is_visible()
            bbox = await container.bounding_box()
            
            print(f"  Container {i+1}:")
            print(f"    - Visible: {is_visible}")
            print(f"    - Buttons inside: {len(buttons_inside)}")
            if bbox:
                print(f"    - Size: {bbox['width']}x{bbox['height']}")
            
            # Check for SVG inside
            svg_inside = await container.query_selector('svg')
            if svg_inside:
                print(f"    - ✅ Has SVG diagram")
            else:
                print(f"    - ❌ No SVG diagram")
        
        # Check regular code blocks
        print(f"\n📝 Regular Code Block Check:")
        regular_code_blocks = await page.query_selector_all('pre:not([data-mermaid])')
        print(f"  Regular code blocks: {len(regular_code_blocks)}")
        
        # Count which have buttons
        blocks_with_buttons = 0
        for block in regular_code_blocks[:5]:  # Check first 5
            buttons = await block.query_selector_all('.code-toggle-btn')
            if buttons:
                blocks_with_buttons += 1
        
        print(f"  Code blocks with toggle buttons: {blocks_with_buttons}")
        
        # Take screenshots
        await page.screenshot(path="test_mermaid_fix_v2.png", full_page=False)
        
        # Scroll to first Mermaid
        if mermaid_containers:
            await mermaid_containers[0].scroll_into_view_if_needed()
            await page.wait_for_timeout(500)
            await mermaid_containers[0].screenshot(path="mermaid_test_1.png")
            print(f"\n📸 Screenshot saved: mermaid_test_1.png")
        
        # Test result
        print("\n" + "=" * 70)
        if len(pre_mermaid) == 0 and len(svg_diagrams) > 0:
            print("✅ TEST PASSED!")
            print("  - Mermaid code blocks have been replaced with diagrams")
            print("  - SVG diagrams are rendering")
            print("  - No leftover code blocks for Mermaid")
        else:
            print("❌ TEST FAILED!")
            print("  - Check console output above for issues")
        
        await page.wait_for_timeout(3000)  # Keep open for visual check
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_fix())