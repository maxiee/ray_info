from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser, Page

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

def create_weibo_page(browser: Browser):
    context = browser.new_context(storage_state=str(WEIBO_STORAGE))
    p = context.new_page()
    p.goto("https://weibo.com")
    return p

def weibo_home_send_text(page: Page, content: str):
    textarea_locator = page.locator('textarea[placeholder="有什么新鲜事想分享给大家？"]')
    textarea_locator.fill(content)
    page.get_by_text('发送').click()

def weibo_home_send_text_with_images(page: Page, content: str, file_paths):
    textarea_locator = page.locator('textarea[placeholder="有什么新鲜事想分享给大家？"]')
    textarea_locator.fill(content)

    # 定位上传按钮并点击
    upload_button = page.locator('div[title="图片"]')
    

    with page.expect_file_chooser() as fc_info:
        upload_button.click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_paths)

    page.wait_for_timeout(30000)

    page.get_by_text('发送').click()

if __name__ == '__main__':
    login_weibo()