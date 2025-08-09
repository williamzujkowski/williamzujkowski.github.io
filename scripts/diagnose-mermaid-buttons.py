#!/usr/bin/env python3
"""
Diagnose the duplicate button issue on Mermaid diagrams
"""

import asyncio
from playwright.async_api import async_playwright

async def diagnose_issue():
    """Check what's happening with Mermaid buttons on live site"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for debugging
        page = await browser.new_page()
        
        print("=" * 70)
        print("🔍 Diagnosing Mermaid Button Issue")
        print("=" * 70)
        
        url = "https://williamzujkowski.github.io/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/"
        print(f"\n📝 Checking: {url}")
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)  # Give time for all scripts to run
        
        # Check all Mermaid-related elements
        mermaid_containers = await page.query_selector_all('.mermaid-container')
        mermaid_divs = await page.query_selector_all('div.mermaid')
        pre_elements = await page.query_selector_all('pre')
        code_mermaid = await page.query_selector_all('pre code.language-mermaid')
        
        print(f"\n📊 Element counts:")
        print(f"   Mermaid containers: {len(mermaid_containers)}")
        print(f"   Mermaid divs: {len(mermaid_divs)}")
        print(f"   Pre elements total: {len(pre_elements)}")
        print(f"   Code.language-mermaid: {len(code_mermaid)}")
        
        # Check for buttons in different contexts
        all_toggle_buttons = await page.query_selector_all('.code-toggle-btn')
        print(f"\n🔘 Total toggle buttons on page: {len(all_toggle_buttons)}")
        
        # Check each Mermaid container for buttons
        print(f"\n🔍 Checking Mermaid containers for buttons:")
        for i, container in enumerate(mermaid_containers):
            buttons_in_container = await container.query_selector_all('.code-toggle-btn')
            parent = await container.evaluate_handle('(el) => el.parentElement')
            parent_html = await parent.evaluate('(el) => el.outerHTML.substring(0, 200)')
            
            print(f"\n   Container {i+1}:")
            print(f"   - Buttons inside: {len(buttons_in_container)}")
            print(f"   - Parent HTML preview: {parent_html}...")
            
            # Check if container has any pre/code elements
            pre_in_container = await container.query_selector_all('pre')
            code_in_container = await container.query_selector_all('code')
            print(f"   - Pre elements inside: {len(pre_in_container)}")
            print(f"   - Code elements inside: {len(code_in_container)}")
        
        # Check for any pre elements with mermaid code
        print(f"\n🔍 Checking for lingering mermaid code blocks:")
        for pre in pre_elements:
            code = await pre.query_selector('code.language-mermaid')
            if code:
                buttons = await pre.query_selector_all('.code-toggle-btn')
                pre_html = await pre.evaluate('(el) => el.outerHTML.substring(0, 150)')
                print(f"   Found pre with mermaid code:")
                print(f"   - Has {len(buttons)} buttons")
                print(f"   - HTML: {pre_html}...")
        
        # Get page HTML around mermaid sections
        mermaid_section_html = await page.evaluate('''() => {
            const containers = document.querySelectorAll('.mermaid-container');
            const results = [];
            containers.forEach((container, i) => {
                const parent = container.parentElement;
                results.push({
                    index: i,
                    containerHTML: container.outerHTML.substring(0, 200),
                    hasButtons: container.querySelectorAll('.code-toggle-btn').length,
                    parentTag: parent.tagName,
                    siblingCount: parent.children.length
                });
            });
            return results;
        }''')
        
        print(f"\n📋 Mermaid container analysis:")
        for item in mermaid_section_html:
            print(f"   Container {item['index'] + 1}:")
            print(f"   - Has {item['hasButtons']} buttons")
            print(f"   - Parent tag: {item['parentTag']}")
            print(f"   - Siblings: {item['siblingCount']}")
        
        # Take screenshot
        await page.screenshot(path="mermaid_button_diagnosis.png", full_page=False)
        
        # Check console for errors
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"{msg.type}: {msg.text}"))
        await page.reload()
        await page.wait_for_timeout(3000)
        
        if console_logs:
            print(f"\n📝 Console messages:")
            for log in console_logs[:10]:  # First 10 messages
                print(f"   {log}")
        
        await browser.close()
        
        print("\n" + "=" * 70)
        print("Diagnosis complete - check mermaid_button_diagnosis.png")

if __name__ == "__main__":
    asyncio.run(diagnose_issue())