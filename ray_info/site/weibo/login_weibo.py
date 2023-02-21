from playwright.sync_api import sync_playwright

from ray_info.common import WEIBO_STORAGE

def login_weibo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://weibo.com")
        print(page.title())

        ret = input('请登录微博，完成后输入 save 回车，保存登录信息到本地> ')

        if ret == 'save':
            page.context.storage_state(path=str(WEIBO_STORAGE))

        browser.close()

if __name__ == '__main__':
    login_weibo()