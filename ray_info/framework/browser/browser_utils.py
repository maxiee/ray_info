from playwright.sync_api import Page, sync_playwright

global_playwright = sync_playwright().start()
global_browser = global_playwright.chromium.launch(headless=True)

def page_move_down(page: Page, distance=1000):
    page.mouse.wheel(0, distance)


def page_move_down_n_times(page: Page, n_times = 15, sleep=5000, distance=3000):
    for i in range(n_times):
        page_move_down(page, distance)
        page.wait_for_timeout(sleep)