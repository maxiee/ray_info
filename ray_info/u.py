from playwright.sync_api import sync_playwright

pw = sync_playwright().start()
b = pw.chromium.launch(headless=False)
p = b.new_page()


def done():
    b.close()
    pw.stop()
    exit(0)
