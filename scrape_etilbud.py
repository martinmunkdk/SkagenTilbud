import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://etilbudsavis.dk")

        print("Ingen cookie-popup – går videre.")

try:
    felt = page.locator("input[aria-label*='Postnummer']")
    await felt.fill("9990")
    await page.keyboard.press("Enter")
    await page.wait_for_timeout(5000)
    print("Postnummer 9990 indtastet.")
    try:
        avisnavn = await page.locator("button[aria-label='Skift lokalavis']").text_content()
        print(f"Avis/lokalområde valgt: {avisnavn.strip()}")
    except:
        print("Kunne ikke aflæse avisnavn – måske allerede valgt eller element ikke synligt.")
except:
    print("Kunne ikke sætte postnummer – måske allerede sat eller felt ikke fundet.")


                await browser.close()

asyncio.run(main())
