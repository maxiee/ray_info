from ray_info.site.weibo.weibo import create_weibo_page, weibo_get_feed_data, weibo_home_send_text, weibo_home_send_text_with_images
from playwright.sync_api import sync_playwright, Page, Browser
import json

if __name__ == '__main__':
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)

        print('RayInfo REPL')

        page: Page = None # type: ignore

        while True:
            ret = input('> ')

            if ret == 'open_weibo':
                page = create_weibo_page(browser)
            elif ret == 'feed_data':
                print(json.dumps(weibo_get_feed_data(page)))
            elif ret == 'send_weibo':
                content = input('输入微博内容>')
                weibo_home_send_text(page, content)
            elif ret == 'send_weibo_with_img':
                content = input('输入微博内容>')
                img = input('输入图片路径>')
                weibo_home_send_text_with_images(page, content, [img])
            elif ret == 'quit':
                browser.close()
                exit(0)

    