from typing import Any
from playwright.sync_api import sync_playwright

def perform_giftcode_redeem(player_id: str, gift_code: str, page: Any):
    page.fill("input[placeholder='Player ID']", player_id)
    page.click("div.btn.login_btn")
    page.wait_for_timeout(2000)

    player_nick = page.inner_text("p.name")
    print("Trying to redeem for player:", player_nick)

    page.fill("input[placeholder='Enter Gift Code']", gift_code)
    page.click("div.btn.exchange_btn")
    page.wait_for_timeout(2000)


    # Handle confirmation modal
    try:
        page.wait_for_selector("div.message_modal", timeout=5000)
        modal_text = page.inner_text("div.modal_content .msg")
        print("Redemption result:", modal_text)

        page.click("div.confirm_btn")

        return {
            "player_nick": player_nick,
            "success": "success" in modal_text.lower(),
            "message": modal_text
        }

    except TimeoutError:
        return {"success": False, "message": "No confirmation modal appeared."}

    finally:
        page.click("div.exit_con")

def redeem_giftcode_for_all_players(player_ids: list, gift_code: str):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://ks-giftcode.centurygame.com/")

        for player_id in player_ids:
            result = perform_giftcode_redeem(player_id, gift_code, page)
            result_message = result.get("message")
            
            #if result_message == "Gift Code not found, this is case-sensitive!":
            #    return "Gift code not found, stopping further attempts."
            
            results.append({"player_id": player_id, "result": result})

        browser.close()
        return results

if __name__ == "__main__":
    # Example test run
    print("Starting test redemption...")
    player_list = ["48666532", "46864326"]
    res = redeem_giftcode_for_all_players(player_list, "KSFB15K")
    print("Test redemption result:", res)
