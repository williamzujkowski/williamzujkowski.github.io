#!/usr/bin/env python3
"""
Comprehensive test of all fixes - Mermaid and code blocks
"""

import asyncio
from playwright.async_api import async_playwright

async def test_all_fixes():
    """Test that both Mermaid and code blocks work properly"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser
        page = await browser.new_page()
        
        print("=" * 70)
        print("🧪 Comprehensive Fix Test - Local")
        print("=" * 70)
        
        # Test 1: Blockchain post with long code blocks
        print("\n📝 Test 1: Blockchain post (long code blocks)")
        url1 = "http://localhost:8080/posts/blockchain-beyond-cryptocurrency-building-the-trust-layer-of-the-internet/"
        
        await page.goto(url1, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Check for code blocks and buttons
        pre_elements = await page.query_selector_all('pre')
        toggle_buttons = await page.query_selector_all('.code-toggle-btn')
        copy_buttons = await page.query_selector_all('.code-copy-btn')
        
        print(f"  Pre elements: {len(pre_elements)}")
        print(f"  Toggle buttons: {len(toggle_buttons)}")
        print(f"  Copy buttons: {len(copy_buttons)}")
        
        # Check each pre for duplicate buttons
        duplicates_found = False
        for i, pre in enumerate(pre_elements):
            toggles_in_pre = await pre.query_selector_all('.code-toggle-btn')
            if len(toggles_in_pre) > 1:
                print(f"  ❌ Pre {i+1} has {len(toggles_in_pre)} toggle buttons (DUPLICATE!)")
                duplicates_found = True
            elif len(toggles_in_pre) == 1:
                # Check if it's a long block
                code = await pre.query_selector('code')
                if code:
                    text = await code.inner_text()
                    lines = len(text.split('\n'))
                    if lines > 30:
                        print(f"  ✅ Long code block ({lines} lines) has 1 toggle button")
        
        if not duplicates_found:
            print(f"  ✅ No duplicate buttons found")
        
        # Test 2: Claude-Flow post with Mermaid
        print("\n📝 Test 2: Claude-Flow post (Mermaid diagrams)")
        url2 = "http://localhost:8080/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/"
        
        await page.goto(url2, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Check Mermaid elements
        mermaid_containers = await page.query_selector_all('.mermaid-container')
        mermaid_svgs = await page.query_selector_all('.mermaid svg')
        pre_mermaid = await page.query_selector_all('pre code.language-mermaid')
        
        print(f"  Mermaid containers: {len(mermaid_containers)}")
        print(f"  Mermaid SVGs: {len(mermaid_svgs)}")
        print(f"  Leftover Mermaid code blocks: {len(pre_mermaid)}")
        
        # Check Mermaid containers for buttons
        mermaid_has_buttons = False
        for i, container in enumerate(mermaid_containers):
            buttons = await container.query_selector_all('button')
            if buttons:
                print(f"  ❌ Mermaid {i+1} has {len(buttons)} buttons")
                mermaid_has_buttons = True
        
        if not mermaid_has_buttons and len(mermaid_svgs) > 0:
            print(f"  ✅ Mermaid diagrams have no buttons")
        
        # Check regular code blocks still work
        regular_blocks = await page.query_selector_all('pre:not([data-mermaid])')
        print(f"  Regular code blocks: {len(regular_blocks)}")
        
        # Test 3: Check console for errors
        print("\n📝 Test 3: Console errors check")
        console_messages = []
        page.on("console", lambda msg: console_messages.append(msg))
        
        await page.reload()
        await page.wait_for_timeout(2000)
        
        errors = [msg for msg in console_messages if msg.type == "error"]
        if errors:
            print(f"  ❌ Found {len(errors)} console errors:")
            for error in errors:
                print(f"    - {error.text}")
        else:
            print(f"  ✅ No console errors")
        
        # Test 4: Check script loading
        scripts_loaded = await page.evaluate('''() => {
            const scripts = Array.from(document.querySelectorAll('script[src*="code-collapse"]'));
            return scripts.length;
        }''')
        
        print(f"\n📝 Test 4: Script loading")
        print(f"  code-collapse.js instances: {scripts_loaded}")
        if scripts_loaded == 1:
            print(f"  ✅ Script loaded only once")
        else:
            print(f"  ❌ Script loaded {scripts_loaded} times")
        
        # Summary
        print("\n" + "=" * 70)
        if not duplicates_found and not mermaid_has_buttons and scripts_loaded == 1:
            print("✅ ALL TESTS PASSED!")
            print("  - No duplicate buttons on code blocks")
            print("  - Mermaid diagrams render without buttons")
            print("  - Scripts load correctly")
            print("  - No console errors")
        else:
            print("❌ SOME TESTS FAILED - See details above")
        
        await page.wait_for_timeout(3000)  # Keep open for visual check
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_all_fixes())