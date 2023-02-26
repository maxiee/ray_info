from ray_info.db import Info, Record, UserDict, db
from ray_info.framework.browser.browser_utils import page_move_down_n_times
from ray_info.site.weibo.weibo import create_weibo_page, weibo_get_feed_data, weibo_home_send_text, weibo_home_send_text_with_images, weibo_repeat_save_feed_data_then_scroll, weibo_save_feed_data
from playwright.sync_api import sync_playwright, Page, Browser
import json
from ray_info.fenci.fenci import init_jieba

if __name__ == '__main__':
    db.connect()
    db.create_tables([Info, Record, UserDict], safe=True)

    init_jieba()
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)

        print('RayInfo REPL')

        page: Page = None # type: ignore

        while True:
            ret = input('> ')

            if ret == 'open_weibo':
                page = create_weibo_page(browser)
            elif ret == 'feed_data':
                for i in weibo_get_feed_data(page):
                    print('==============')
                    print(i)
                    print('==============')
            elif ret == 'save_feed_data':
                weibo_save_feed_data(
                    weibo_get_feed_data(page))
            elif ret == 'send_weibo':
                content = input('输入微博内容>')
                weibo_home_send_text(page, content)
            elif ret == 'send_weibo_with_img':
                content = input('输入微博内容>')
                img = input('输入图片路径>')
                weibo_home_send_text_with_images(page, content, [img])
            elif ret == 'scroll_and_save':
                weibo_repeat_save_feed_data_then_scroll(page)
            elif ret == 'quit':
                browser.close()
                exit(0)

    