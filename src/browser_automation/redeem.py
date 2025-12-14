from typing import Any, List, Dict
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def perform_giftcode_redeem(player_id: str, gift_code: str, page: Any) -> Dict[str, Any]:
    await page.fill("input[placeholder='Player ID']", player_id)
    await page.click("div.btn.login_btn")
    await page.wait_for_timeout(2000)

    player_nick = await page.inner_text("p.name")
    print("Trying to redeem for player:", player_nick)

    await page.fill("input[placeholder='Enter Gift Code']", gift_code)
    await page.click("div.btn.exchange_btn")
    await page.wait_for_timeout(2000)

    try:
        await page.wait_for_selector("div.message_modal", timeout=5000)
        modal_text = await page.inner_text("div.modal_content .msg")
        print("Redemption result:", modal_text)

        await page.click("div.confirm_btn")

        return {
            "player_nick": player_nick,
            "success": "success" in modal_text.lower(),
            "message": modal_text,
        }
    except (PlaywrightTimeoutError, TimeoutError):
        return {"success": False, "message": "No confirmation modal appeared."}
    finally:
        # Attempt to close the modal or exit
        try:
            await page.click("div.exit_con")
        except Exception:
            pass

async def redeem_giftcode_for_all_players(player_ids: List[str], gift_code: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://ks-giftcode.centurygame.com/")

        for player_id in player_ids:
            result = await perform_giftcode_redeem(player_id, gift_code, page)
            results.append({"player_id": player_id, "result": result, "success": result.get("success", False)})

        await browser.close()
        return results
