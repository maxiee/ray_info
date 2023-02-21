import base64
from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser, Page

from ray_info.common import WEIBO_STORAGE


def login_weibo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://weibo.com")
        print(page.title())

        ret = input("请登录微博，完成后输入 save 回车，保存登录信息到本地> ")

        if ret == "save":
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
    page.get_by_text("发送").click()


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

    page.get_by_text("发送").click()


def weibo_get_feed_data(page: Page):
    # 获取所有的资讯卡片
    feed_cards = page.query_selector_all("article")

    feed_data = []
    for card in feed_cards:
        # 获取卡片的文本信息
        text = card.inner_text()
        # 获取卡片的图片信息
        images = []
        image_elements = card.query_selector_all("img")
        for image_element in image_elements:
            images.append(image_element.get_attribute('src'))
        # 获取卡片的用户信息
        user_img = card.query_selector(".woo-avatar-img").get_attribute("src")
        user_name = card.query_selector_all("a")[0].inner_text()

        feed_data.append(
            {
                "text": text,
                "images": images,
                "user_img": user_img,
                "user_name": user_name,
            }
        )

    return feed_data


if __name__ == "__main__":
    login_weibo()
