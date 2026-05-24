#!/usr/bin/env python3
"""Take 5 screenshots of MiMoCompare at 1920x1080."""
import asyncio, os, time

async def main():
    import nodriver as uc
    browser = await uc.start(
        headless=True,
        browser_args=['--no-sandbox','--disable-gpu','--window-size=1920,1080']
    )
    page = await browser.get('file:///home/ubuntu/mimocompare/index.html')
    await page.sleep(2)
    
    await page.send(uc.cdp.emulation.set_device_metrics_override(
        width=1920, height=1080, device_scale_factor=1, mobile=False
    ))
    await page.sleep(1)
    
    out = '/home/ubuntu/mimocompare/screenshots'
    os.makedirs(out, exist_ok=True)
    
    # Shot 1: Hero + form (clean)
    await page.save_screenshot(f'{out}/01_hero_form.png')
    print('✅ Shot 1: Hero + Form')
    
    # Shot 2: Fill example → priorities
    await page.evaluate("fillExample('phone')")
    await page.sleep(1)
    await page.save_screenshot(f'{out}/02_priorities.png')
    print('✅ Shot 2: Priorities')
    
    # Shot 3: Run comparison → results
    await page.evaluate("runComparison()")
    # Wait for MiMo API response (poll for results section)
    for i in range(30):
        await page.sleep(1)
        visible = await page.evaluate("document.getElementById('resultsSection').classList.contains('active')")
        if visible:
            print(f'  Results loaded after {i+1}s')
            break
    
    await page.sleep(1)
    await page.save_screenshot(f'{out}/03_results_top.png')
    print('✅ Shot 3: Results Top')
    
    # Shot 4: Scroll to verdict cards + comparison table
    await page.evaluate("window.scrollTo(0, 500)")
    await page.sleep(1)
    await page.save_screenshot(f'{out}/04_verdict.png')
    print('✅ Shot 4: Verdict + Table')
    
    # Shot 5: Scroll to AI analysis + chat widget
    await page.evaluate("window.scrollTo(0, 1100)")
    await page.sleep(1)
    # Open chat
    await page.evaluate("toggleChat()")
    await page.sleep(1)
    await page.save_screenshot(f'{out}/05_chat_analysis.png')
    print('✅ Shot 5: Analysis + Chat')
    
    browser.stop()
    
    for f in sorted(os.listdir(out)):
        size = os.path.getsize(f'{out}/{f}')
        print(f'  {f}: {size//1024}KB')

asyncio.run(main())
