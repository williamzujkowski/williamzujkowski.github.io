#!/usr/bin/env python3
"""
Diagnose the duplicate expand button issue on long code blocks
"""

import asyncio
from playwright.async_api import async_playwright

async def diagnose_issue():
    """Check duplicate button issue on blockchain post"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser
        page = await browser.new_page()
        
        print("=" * 70)
        print("🔍 Diagnosing Duplicate Button Issue")
        print("=" * 70)
        
        # Enable console logging
        page.on("console", lambda msg: print(f"  Console [{msg.type}]: {msg.text}"))
        
        url = "https://williamzujkowski.github.io/posts/blockchain-beyond-cryptocurrency-building-the-trust-layer-of-the-internet/"
        print(f"\n📝 Checking: {url}")
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)  # Give scripts time to run
        
        # Check all code blocks and buttons
        pre_elements = await page.query_selector_all('pre')
        code_blocks = await page.query_selector_all('pre code')
        all_buttons = await page.query_selector_all('button')
        toggle_buttons = await page.query_selector_all('.code-toggle-btn')
        copy_buttons = await page.query_selector_all('.code-copy-btn')
        
        print(f"\n📊 Element counts:")
        print(f"  Pre elements: {len(pre_elements)}")
        print(f"  Code blocks: {len(code_blocks)}")
        print(f"  All buttons: {len(all_buttons)}")
        print(f"  Toggle buttons: {len(toggle_buttons)}")
        print(f"  Copy buttons: {len(copy_buttons)}")
        
        # Check each pre element for multiple buttons
        print(f"\n🔍 Checking each code block for duplicate buttons:")
        problem_blocks = []
        
        for i, pre in enumerate(pre_elements):
            # Get all buttons in this pre element
            buttons_in_pre = await pre.query_selector_all('button')
            toggle_in_pre = await pre.query_selector_all('.code-toggle-btn')
            copy_in_pre = await pre.query_selector_all('.code-copy-btn')
            
            # Get code language
            code = await pre.query_selector('code')
            lang_class = ""
            if code:
                classes = await code.get_attribute('class') or ""
                lang_class = classes
            
            # Check parent structure
            parent = await pre.evaluate_handle('(el) => el.parentElement')
            parent_class = await parent.evaluate('(el) => el.className')
            
            if len(buttons_in_pre) > 0:
                print(f"\n  Pre block {i+1}:")
                print(f"    Language: {lang_class}")
                print(f"    Parent class: {parent_class}")
                print(f"    Total buttons: {len(buttons_in_pre)}")
                print(f"    Toggle buttons: {len(toggle_in_pre)}")
                print(f"    Copy buttons: {len(copy_in_pre)}")
                
                if len(toggle_in_pre) > 1:
                    print(f"    ❌ DUPLICATE TOGGLE BUTTONS FOUND!")
                    problem_blocks.append(i)
                    
                    # Get button details
                    for j, btn in enumerate(toggle_in_pre):
                        text = await btn.inner_text()
                        position = await btn.evaluate('(el) => el.style.position')
                        print(f"      Button {j+1}: '{text}' (position: {position})")
        
        # Find the long code block mentioned
        print(f"\n🔍 Looking for long code blocks (>30 lines):")
        for i, pre in enumerate(pre_elements):
            code = await pre.query_selector('code')
            if code:
                text = await code.inner_text()
                lines = text.split('\n')
                if len(lines) > 30:
                    buttons = await pre.query_selector_all('.code-toggle-btn')
                    print(f"  Long block {i+1}: {len(lines)} lines, {len(buttons)} toggle buttons")
                    
                    # Scroll to it and screenshot
                    await pre.scroll_into_view_if_needed()
                    await page.wait_for_timeout(500)
                    await pre.screenshot(path=f"long_code_block_{i}.png")
                    print(f"    📸 Screenshot: long_code_block_{i}.png")
        
        # Check for wrapper elements
        print(f"\n🔍 Checking for code-block-wrapper elements:")
        wrappers = await page.query_selector_all('.code-block-wrapper')
        print(f"  Code block wrappers: {len(wrappers)}")
        
        for i, wrapper in enumerate(wrappers[:3]):  # Check first 3
            buttons_in_wrapper = await wrapper.query_selector_all('button')
            containers = await wrapper.query_selector_all('.code-block-container')
            pre_in_wrapper = await wrapper.query_selector_all('pre')
            
            print(f"\n  Wrapper {i+1}:")
            print(f"    Containers inside: {len(containers)}")
            print(f"    Pre elements inside: {len(pre_in_wrapper)}")
            print(f"    Buttons: {len(buttons_in_wrapper)}")
        
        # Check script loading order
        scripts = await page.evaluate('''() => {
            const scripts = Array.from(document.querySelectorAll('script'));
            return scripts.map(s => ({
                src: s.src || 'inline',
                type: s.type || 'text/javascript'
            })).filter(s => s.src.includes('code-collapse') || s.src.includes('mermaid') || s.type === 'module');
        }''')
        
        print(f"\n📜 Script loading order:")
        for script in scripts:
            print(f"  - {script['src']} ({script['type']})")
        
        # Take full page screenshot
        await page.screenshot(path="duplicate_buttons_diagnosis.png", full_page=False)
        
        print(f"\n" + "=" * 70)
        if problem_blocks:
            print(f"❌ Found {len(problem_blocks)} blocks with duplicate buttons")
            print("Issue: Code-collapse.js is being initialized multiple times")
        else:
            print("✅ No duplicate buttons found")
        
        await page.wait_for_timeout(5000)  # Keep open for inspection
        await browser.close()

if __name__ == "__main__":
    asyncio.run(diagnose_issue())