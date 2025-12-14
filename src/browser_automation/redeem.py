from typing import Any, List, Dict
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from config.config import TIMEOUT_MS

async def perform_giftcode_redeem(player_id: str, gift_code: str, page: Any) -> Dict[str, Any]:
    await page.fill("input[placeholder='Player ID']", player_id)
    await page.click("div.btn.login_btn")
    await page.wait_for_timeout(TIMEOUT_MS)

    # Handle failed login with busy server message
    try:
        await page.wait_for_selector("div.message_modal", timeout=TIMEOUT_MS*5)
        login_modal_text = await page.inner_text("div.modal_content .msg", timeout=TIMEOUT_MS)
        if "Server busy. Please try again later." in login_modal_text:
            await page.click("div.confirm_btn")
            return {
                "success": False, 
                "message": "Problem with logging in. Double check player ID."
            }
    except (PlaywrightTimeoutError, TimeoutError):
        pass

    player_nick = await page.inner_text("p.name")
    print("Trying to redeem for player:", player_nick)

    await page.fill("input[placeholder='Enter Gift Code']", gift_code)
    await page.click("div.btn.exchange_btn")
    await page.wait_for_timeout(TIMEOUT_MS)

    try:
        await page.wait_for_selector("div.message_modal", timeout=TIMEOUT_MS*5)
        modal_text = await page.inner_text("div.modal_content .msg", timeout=TIMEOUT_MS)
        print("Redemption result:", modal_text)

        await page.click("div.confirm_btn")

        return {
            "player_nick": player_nick,
            "success": "Redeemed, please claim the rewards in your mail!".lower() in modal_text.lower(),
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

async def redeem_giftcode_for_all_players(players: List[Dict[str, str]], gift_code: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://ks-giftcode.centurygame.com/")

        for player in players:
            player_id = player.get("player_id", "")
            stored_nick = player.get("player_nick")

            result = await perform_giftcode_redeem(player_id, gift_code, page)
            page_nick = result.get("player_nick")
            result_message = result.get("message")

            if result_message == "Gift Code not found, this is case-sensitive!":
                results.append({
                    "success": False,
                    "errorCode": "INVALID_CODE",
                    "message": "Invalid gift code.",
                })

                return results
            
            elif result_message == "The same Gift Code type can only be redeemed once!" or result_message == "Already claimed, unable to claim again.":
                results.append({
                    "player_id": player_id,
                    "stored_player_nick": stored_nick,
                    "page_player_nick": page_nick,
                    "result": result,
                    "success": True,
                })
            else:
                results.append({
                    "player_id": player_id,
                    "stored_player_nick": stored_nick,
                    "page_player_nick": page_nick,
                    "result": result,
                    "success": result.get("success", False),
                })

        await browser.close()
        return results
