from datetime import datetime
import json
import re
from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser, Page
import tempfile
from ray_info.common import WEIBO_STORAGE
import pathlib
import jieba
from ray_info.db import Info
from ray_info.fenci.fenci import get_word
from peewee import DoesNotExist

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
            # print(f'拦截到请求 {url=}')
            if re.findall(r'\.png|jpg|gif', url, re.IGNORECASE):
                # print(f'拦截到图片: {url=}')
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

    page.wait_for_timeout(5000)

    page.get_by_text("发送").click()


def weibo_get_feed_data(page: Page):
    # 获取所有的资讯卡片
    feed_cards = page.query_selector_all("article")

    feed_data = []
    for card in feed_cards:
        # 获取卡片的用户信息
        user_img = card.query_selector(".woo-avatar-img").get_attribute("src")
        user_img = dir.joinpath(url_to_file_name(user_img))

        user_name = card.query_selector('header').query_selector_all('a')[1].inner_text()

        print('======================================================================')
        print(f'{user_name=}')
        print(f'{user_img}')

        # 获取卡片的文本信息
        text = ''
        text_part_one = card.query_selector('.wbpro-feed-content')
        text_part_two = card.query_selector('.wbpro-feed-reText')
        if text_part_one != None:
            text = text + text_part_one.inner_text() + '\n\n'
        if text_part_two != None:
            text = text + text_part_two.inner_text()
        # 获取卡片的图片信息
        images = []
        element_picture = card.query_selector('.picture')
        if element_picture == None:
            print('未发现图片区，请与网页比对')
        if element_picture != None:
            image_elements = element_picture.query_selector_all("img")
            print(f'图片区原始链接数量 = {len(image_elements)}')
            for index, image_element in enumerate(image_elements):
                img_url = image_element.get_attribute('src')
                print(f'图片{index}的 url：{img_url=}')
                if img_url is None:
                    continue
                img_name = url_to_file_name(img_url)
                temp_path = dir.joinpath(img_name)
                if temp_path.exists():
                    images.append(f'file://{temp_path}')
                else:
                    print(f'图片缓存未命中 {temp_path=} {img_url=}')
        if len(images) > 0:
            print(f'图片列表：{images}')
        print('======================================================================')
        feed_data.append(
            {
                "text": text,
                "images": images,
                "user_img": user_img,
                "user_name": user_name,
            }
        )

    return feed_data

def weibo_save_feed_data(feed_data):
    for data in feed_data:
        text = data['text']
        images = data['images']
        user_img = data['user_img']
        user_name = data['user_name']

        cut_ret = jieba.cut(text)
        like_score = 0
        for fc in cut_ret:
            w = get_word(fc)
            if w != None:
                    like_score += w.like
        
        try:
            info = Info.get(Info.description == text)
            print(f'\t微博已存在')
        except DoesNotExist:
            info = Info.create(
                title='',
                updated=datetime.now(),
                site=user_name,
                site_img=user_img,
                url='',
                description=text,
                images=json.dumps(images),
                like=like_score
            )



if __name__ == "__main__":
    login_weibo()
