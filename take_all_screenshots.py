#!/usr/bin/env python3
"""Take screenshots: dark hero, light hero, mobile view."""
import asyncio, os

async def main():
    import nodriver as uc
    out = '/home/ubuntu/mimocompare/screenshots'
    os.makedirs(out, exist_ok=True)
    
    browser = await uc.start(
        headless=True,
        browser_args=['--no-sandbox','--disable-gpu','--window-size=1920,1080']
    )
    page = await browser.get('file:///home/ubuntu/mimocompare/index.html')
    await page.sleep(2)
    
    # Desktop 1920x1080
    await page.send(uc.cdp.emulation.set_device_metrics_override(
        width=1920, height=1080, device_scale_factor=1, mobile=False
    ))
    await page.sleep(1)
    
    # Shot 1: Dark theme - hero
    await page.evaluate("document.documentElement.setAttribute('data-theme','dark')")
    await page.sleep(0.5)
    await page.save_screenshot(f'{out}/01_dark_hero.png')
    print('✅ Shot 1: Dark Hero')
    
    # Shot 2: Dark theme - fill example + priorities
    await page.evaluate("fillExample('phone')")
    await page.sleep(1)
    await page.save_screenshot(f'{out}/02_dark_priorities.png')
    print('✅ Shot 2: Dark Priorities')
    
    # Shot 3: Run comparison → results (dark)
    await page.evaluate("runComparison()")
    for i in range(30):
        await page.sleep(1)
        visible = await page.evaluate("document.getElementById('resultsSection').classList.contains('active')")
        if visible:
            break
    await page.sleep(1)
    await page.save_screenshot(f'{out}/03_dark_results.png')
    print('✅ Shot 3: Dark Results')
    
    # Shot 4: Light theme - hero
    await page.evaluate("resetAll()")
    await page.sleep(1)
    await page.evaluate("document.documentElement.setAttribute('data-theme','light')")
    await page.sleep(1)
    await page.save_screenshot(f'{out}/04_light_hero.png')
    print('✅ Shot 4: Light Hero')
    
    # Shot 5: Light theme - results
    await page.evaluate("fillExample('laptop')")
    await page.sleep(0.5)
    await page.evaluate("goToStep(2)")
    await page.sleep(0.5)
    await page.evaluate("runComparison()")
    for i in range(30):
        await page.sleep(1)
        visible = await page.evaluate("document.getElementById('resultsSection').classList.contains('active')")
        if visible:
            break
    await page.sleep(1)
    await page.save_screenshot(f'{out}/05_light_results.png')
    print('✅ Shot 5: Light Results')
    
    # Shot 6: Mobile view (375x812 - iPhone)
    await page.evaluate("document.documentElement.setAttribute('data-theme','dark')")
    await page.evaluate("resetAll()")
    await page.sleep(1)
    await page.send(uc.cdp.emulation.set_device_metrics_override(
        width=375, height=812, device_scale_factor=2, mobile=True
    ))
    await page.sleep(1)
    await page.save_screenshot(f'{out}/06_mobile_hero.png')
    print('✅ Shot 6: Mobile Hero')
    
    browser.stop()
    
    for f in sorted(os.listdir(out)):
        size = os.path.getsize(f'{out}/{f}')
        print(f'  {f}: {size//1024}KB')

asyncio.run(main())
