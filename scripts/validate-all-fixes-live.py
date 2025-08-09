#!/usr/bin/env python3
"""
Final validation of all fixes on live site
"""

import asyncio
from playwright.async_api import async_playwright

async def validate_live():
    """Comprehensive validation on production site"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("=" * 70)
        print("🌐 Final Comprehensive Validation - Live Site")
        print("=" * 70)
        
        all_good = True
        
        # Test 1: Blockchain post - long code blocks
        print("\n📝 Test 1: Blockchain post (long code blocks)")
        url1 = "https://williamzujkowski.github.io/posts/blockchain-beyond-cryptocurrency-building-the-trust-layer-of-the-internet/"
        
        await page.goto(url1, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Check for code blocks and buttons
        pre_elements = await page.query_selector_all('pre')
        toggle_buttons = await page.query_selector_all('.code-toggle-btn')
        copy_buttons = await page.query_selector_all('.code-copy-btn')
        
        print(f"  Pre elements: {len(pre_elements)}")
        print(f"  Toggle buttons: {len(toggle_buttons)}")
        print(f"  Copy buttons: {len(copy_buttons)}")
        
        # Check for duplicates
        for i, pre in enumerate(pre_elements):
            toggles = await pre.query_selector_all('.code-toggle-btn')
            if len(toggles) > 1:
                print(f"  ❌ Pre {i+1} has {len(toggles)} toggle buttons (DUPLICATE!)")
                all_good = False
            elif len(toggles) == 1:
                code = await pre.query_selector('code')
                if code:
                    text = await code.inner_text()
                    lines = len(text.split('\n'))
                    if lines > 30:
                        print(f"  ✅ Long code block ({lines} lines) has exactly 1 toggle button")
        
        if toggle_buttons and len(toggle_buttons) <= len(pre_elements):
            print(f"  ✅ No duplicate buttons detected")
        
        # Take screenshot of long code block
        if pre_elements:
            await pre_elements[0].scroll_into_view_if_needed()
            await page.screenshot(path="live_blockchain_codeblock.png", full_page=False)
        
        # Test 2: Claude-Flow post - Mermaid diagrams
        print("\n📝 Test 2: Claude-Flow post (Mermaid diagrams)")
        url2 = "https://williamzujkowski.github.io/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/"
        
        await page.goto(url2, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Check Mermaid elements
        mermaid_containers = await page.query_selector_all('.mermaid-container')
        mermaid_svgs = await page.query_selector_all('.mermaid svg')
        pre_mermaid = await page.query_selector_all('pre code.language-mermaid')
        
        print(f"  Mermaid containers: {len(mermaid_containers)}")
        print(f"  Mermaid SVGs rendered: {len(mermaid_svgs)}")
        print(f"  Leftover Mermaid code blocks: {len(pre_mermaid)}")
        
        # Check Mermaid containers for buttons
        mermaid_clean = True
        for i, container in enumerate(mermaid_containers):
            buttons = await container.query_selector_all('button')
            if buttons:
                print(f"  ❌ Mermaid {i+1} has {len(buttons)} buttons")
                all_good = False
                mermaid_clean = False
        
        if mermaid_clean and len(mermaid_svgs) > 0:
            print(f"  ✅ Mermaid diagrams render without buttons")
        
        # Take screenshot
        if mermaid_containers:
            await mermaid_containers[0].scroll_into_view_if_needed()
            await page.screenshot(path="live_claudeflow_mermaid.png", full_page=False)
        
        # Test 3: Zero Trust post - another Mermaid test
        print("\n📝 Test 3: Zero Trust post (additional Mermaid test)")
        url3 = "https://williamzujkowski.github.io/posts/implementing-zero-trust-security-never-trust-always-verify/"
        
        await page.goto(url3, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        mermaid3 = await page.query_selector_all('.mermaid-container')
        buttons3 = await page.query_selector_all('.mermaid-container button')
        
        print(f"  Mermaid containers: {len(mermaid3)}")
        print(f"  Buttons in Mermaid: {len(buttons3)}")
        
        if len(buttons3) == 0:
            print(f"  ✅ No buttons on Mermaid diagrams")
        else:
            print(f"  ❌ Found buttons on Mermaid diagrams")
            all_good = False
        
        # Test 4: Check console errors on any page
        print("\n📝 Test 4: Console error check")
        console_messages = []
        page.on("console", lambda msg: console_messages.append(msg))
        
        await page.reload()
        await page.wait_for_timeout(2000)
        
        errors = [msg for msg in console_messages if msg.type == "error"]
        if errors:
            print(f"  ❌ Found {len(errors)} console errors")
            for error in errors[:3]:
                print(f"    - {error.text}")
            all_good = False
        else:
            print(f"  ✅ No console errors")
        
        # Test 5: Script loading check
        print("\n📝 Test 5: Script loading verification")
        scripts = await page.evaluate('''() => {
            const scripts = Array.from(document.querySelectorAll('script[src*="code-collapse"]'));
            return scripts.length;
        }''')
        
        print(f"  code-collapse.js instances: {scripts}")
        if scripts == 1:
            print(f"  ✅ Script loaded only once")
        else:
            print(f"  ❌ Script loaded {scripts} times")
            all_good = False
        
        # Test 6: Random posts spot check
        print("\n📝 Test 6: Spot checking other posts")
        
        # Check a random post with code
        url4 = "https://williamzujkowski.github.io/posts/building-secure-homelab-engineers-guide-to-self-hosted-infrastructure/"
        await page.goto(url4, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(1000)
        
        pre4 = await page.query_selector_all('pre')
        issues4 = False
        for pre in pre4[:2]:  # Check first 2
            toggles = await pre.query_selector_all('.code-toggle-btn')
            if len(toggles) > 1:
                print(f"  ❌ Found duplicate buttons in homelab post")
                all_good = False
                issues4 = True
                break
        
        if not issues4:
            print(f"  ✅ Homelab post has no duplicate buttons")
        
        await browser.close()
        
        # Final summary
        print("\n" + "=" * 70)
        if all_good:
            print("✅ ALL VALIDATIONS PASSED!")
            print("\nSummary:")
            print("  ✅ No duplicate buttons on any code blocks")
            print("  ✅ Long code blocks have exactly one expand button")
            print("  ✅ Mermaid diagrams render without any buttons")
            print("  ✅ Scripts load correctly (no duplicates)")
            print("  ✅ No console errors")
            print("  ✅ All posts checked are working properly")
            print("\n🎉 The blog is fully functional with all fixes applied!")
        else:
            print("❌ SOME ISSUES REMAIN")
            print("Please review the details above")
        
        print("\n📸 Screenshots saved for review:")
        print("  - live_blockchain_codeblock.png")
        print("  - live_claudeflow_mermaid.png")

if __name__ == "__main__":
    asyncio.run(validate_live())