import re
from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser, Page
import tempfile
from ray_info.common import WEIBO_STORAGE
import pathlib

from ray_info.utils.html_utils import url_to_file_name

dir = pathlib.Path(tempfile.gettempdir()).joinpath('ray_info_weibo')
dir.mkdir(exist_ok=True)
print(f'临时文件目录 {dir=}')

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

    def img_saver(*args, **kw):
        try:
            response = args[0]
            url = response.url
            print(f'拦截到请求 {url=}')
            if re.findall(r'\.png|jpg|gif', url, re.IGNORECASE):
                print(f'拦截到图片: {url=}')
                img_name = url_to_file_name(url)
                p = pathlib.Path(dir).joinpath(img_name)
                print(p)
                with open(p, 'wb') as f:
                    f.write(response.body())
        except Exception:
            pass

    p.on('response', img_saver)
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
        # fixme 现在方法太粗暴了，尽管把头像（0号图片）过滤掉了，但是文本中的表情还是会采下来
        #       要把范围缩小至图片区内的图片
        images = []
        element_picture = card.query_selector('.picture')
        if element_picture != None:
            image_elements = element_picture.query_selector_all("img")
            for index, image_element in enumerate(image_elements):
                if index == 0:
                    continue
                img_url = image_element.get_attribute('src')
                if img_url is None:
                    continue
                img_name = url_to_file_name(img_url)
                temp_path = dir.joinpath(img_name)
                if temp_path.exists():
                    images.append(str(temp_path))
            
        # 获取卡片的用户信息
        user_img = card.query_selector(".woo-avatar-img").get_attribute("src")
        user_name = card.query_selector('header').query_selector_all('a')[1].inner_text()

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
