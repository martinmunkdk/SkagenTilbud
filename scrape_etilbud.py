import asyncio
from playwright.async_api import async_playwright

SØGEORD = ["Gevalia kaffe", "toiletpapir", "38% fløde", "Coca Cola 24"]
BUTIKKER_SKAGEN = ["SuperBrugsen", "Netto", "Rema 1000", "Lidl", "Fakta"]

async def find_tilbud(playwright):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto("https://etilbudsavis.dk")

    # Cookie-popup
    try:
        await page.locator("text=Acceptér alle").click(timeout=3000)
    except:
        print("Ingen cookie-popup – går videre.")

    # Skift lokalavis
    try:
        await page.click("button[aria-label='Skift lokalavis']", timeout=3000)
    except:
        print("Kunne ikke finde 'Skift lokalavis' – måske allerede sat.")

    try:
        await page.locator("input").first.fill("9990")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)
    except:
        print("Kunne ikke indtaste postnummer – muligvis allerede sat.")

    tilbud = []

    for søgeord in SØGEORD:
        await page.goto("https://etilbudsavis.dk")
        try:
            await page.locator("input").first.fill(søgeord)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(4000)
        except:
            print(f"Kunne ikke søge efter: {søgeord}")
            continue

        cards = page.locator(".sc-bcXHqe")
        count = await cards.count()
        for i in range(count):
            try:
                title = await cards.nth(i).locator("h3").text_content()
                price = await cards.nth(i).locator(".sc-cpmKsF").text_content()
                store = await cards.nth(i).locator(".sc-jXbUNg").text_content()
                validity = await cards.nth(i).locator(".sc-dKfzgJ").text_content()
                link = await cards.nth(i).locator("a").get_attribute("href")

                if any(butik in store for butik in BUTIKKER_SKAGEN):
                    tilbud.append({
                        "produkt": title.strip(),
                        "pris": price.strip(),
                        "butik": store.strip(),
                        "gyldig": validity.strip(),
                        "link": f"https://etilbudsavis.dk{link}"
                    })
            except:
                continue

    await browser.close()
    return tilbud

async def main():
    async with async_playwright() as playwright:
        tilbud = await find_tilbud(playwright)
        tilbud.sort(key=lambda x: x["pris"].replace(",", ".").replace("kr", "").strip()[:5])
        for t in tilbud:
            print(f"{t['produkt']} – {t['pris']} hos {t['butik']} ({t['gyldig']})")
            print(f"{t['link']}")
            print("")

asyncio.run(main())
