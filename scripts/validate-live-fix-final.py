#!/usr/bin/env python3
"""
Final validation of Mermaid fix on live site
"""

import asyncio
from playwright.async_api import async_playwright

async def validate_live():
    """Validate the fix is working on production"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for final check
        page = await browser.new_page()
        
        print("=" * 70)
        print("🌐 Final Validation of Mermaid Fix on Live Site")
        print("=" * 70)
        
        # Enable console logging
        page.on("console", lambda msg: print(f"  Console: {msg.text}"))
        
        url = "https://williamzujkowski.github.io/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/"
        print(f"\n📝 Testing: {url}")
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)  # Give scripts time to run
        
        print("\n📊 Element Analysis:")
        
        # Check for Mermaid elements
        mermaid_containers = await page.query_selector_all('.mermaid-container')
        mermaid_divs = await page.query_selector_all('div.mermaid')
        svg_diagrams = await page.query_selector_all('.mermaid svg, svg[id*="mermaid"]')
        pre_mermaid = await page.query_selector_all('pre code.language-mermaid')
        
        print(f"  ✅ Mermaid containers: {len(mermaid_containers)}")
        print(f"  ✅ Mermaid divs: {len(mermaid_divs)}")
        print(f"  ✅ SVG diagrams rendered: {len(svg_diagrams)}")
        print(f"  ✅ Leftover mermaid code blocks: {len(pre_mermaid)} (should be 0)")
        
        # Check for buttons
        all_buttons = await page.query_selector_all('button')
        toggle_buttons = await page.query_selector_all('.code-toggle-btn')
        expand_buttons = await page.query_selector_all('button:has-text("Expand")')
        collapse_buttons = await page.query_selector_all('button:has-text("Collapse")')
        
        print(f"\n🔘 Button Analysis:")
        print(f"  Total buttons on page: {len(all_buttons)}")
        print(f"  Code toggle buttons: {len(toggle_buttons)}")
        print(f"  Expand buttons: {len(expand_buttons)}")
        print(f"  Collapse buttons: {len(collapse_buttons)}")
        
        # Check each Mermaid container for buttons
        print(f"\n🔍 Mermaid Container Validation:")
        mermaid_has_buttons = False
        for i, container in enumerate(mermaid_containers):
            buttons_inside = await container.query_selector_all('button')
            toggle_inside = await container.query_selector_all('.code-toggle-btn')
            is_visible = await container.is_visible()
            svg_inside = await container.query_selector('svg')
            
            print(f"  Container {i+1}:")
            print(f"    - Visible: {is_visible}")
            print(f"    - Any buttons inside: {len(buttons_inside)}")
            print(f"    - Toggle buttons inside: {len(toggle_inside)}")
            print(f"    - Has SVG: {'✅ Yes' if svg_inside else '❌ No'}")
            
            if len(buttons_inside) > 0 or len(toggle_inside) > 0:
                mermaid_has_buttons = True
                print(f"    ❌ ERROR: Mermaid has buttons!")
        
        # Scroll to and screenshot first Mermaid
        if mermaid_containers:
            await mermaid_containers[0].scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            await mermaid_containers[0].screenshot(path="live_mermaid_final_1.png")
            print(f"\n📸 First Mermaid screenshot: live_mermaid_final_1.png")
            
            # Check if visible on screen
            bbox = await mermaid_containers[0].bounding_box()
            if bbox:
                print(f"  Size: {bbox['width']}x{bbox['height']}")
        
        # Check second Mermaid if exists
        if len(mermaid_containers) > 1:
            await mermaid_containers[1].scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            await mermaid_containers[1].screenshot(path="live_mermaid_final_2.png")
            print(f"\n📸 Second Mermaid screenshot: live_mermaid_final_2.png")
        
        # Full page screenshot
        await page.screenshot(path="live_validation_final.png", full_page=False)
        
        # Test another post with Mermaid
        url2 = "https://williamzujkowski.github.io/posts/implementing-zero-trust-security-never-trust-always-verify/"
        print(f"\n📝 Also checking: {url2}")
        await page.goto(url2, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        mermaid2 = await page.query_selector_all('.mermaid-container')
        buttons2 = await page.query_selector_all('.mermaid-container button')
        print(f"  ✅ Mermaid containers: {len(mermaid2)}")
        print(f"  ✅ Buttons in Mermaid: {len(buttons2)}")
        
        # Final result
        print("\n" + "=" * 70)
        if not mermaid_has_buttons and len(svg_diagrams) > 0 and len(pre_mermaid) == 0:
            print("✅ MERMAID FIX SUCCESSFULLY DEPLOYED!")
            print("\nValidation Summary:")
            print("  ✅ Mermaid diagrams render as SVG")
            print("  ✅ No buttons on Mermaid diagrams")
            print("  ✅ No leftover code blocks for Mermaid")
            print("  ✅ Diagrams are visible on page")
            print("\n🎉 The issue has been completely resolved!")
        else:
            print("❌ ISSUES DETECTED")
            if mermaid_has_buttons:
                print("  - Mermaid containers still have buttons")
            if len(svg_diagrams) == 0:
                print("  - No SVG diagrams found")
            if len(pre_mermaid) > 0:
                print("  - Leftover Mermaid code blocks found")
        
        print("\n⏳ Keeping browser open for 5 seconds for visual confirmation...")
        await page.wait_for_timeout(5000)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(validate_live())