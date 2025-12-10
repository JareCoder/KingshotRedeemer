from playwright.sync_api import sync_playwright

def redeem_giftcode(player_id: str, gift_code: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://ks-giftcode.centurygame.com/")

        page.fill("input[placeholder='Player ID']", player_id)
        page.click("div.btn.login_btn")
        page.wait_for_timeout(2000)

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
                "success": "success" in modal_text.lower(),
                "message": modal_text
            }

        except TimeoutError:
            return {"success": False, "message": "No confirmation modal appeared."}

        finally:
            browser.close()


if __name__ == "__main__":
    # Example test run
    print("Starting test redemption...")
    res = redeem_giftcode("48666532", "KSFB15K")
    print("Test redemption result:", res)
