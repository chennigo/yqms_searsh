import BaseVideoClient
import wxauto
import time
import re
import threading
import pythoncom
from DrissionPage import ChromiumPage, ChromiumOptions
import schedule
from push_error import sc_send

# 在程序启动时初始化 COM
pythoncom.CoInitialize()

# 全局变量，用来在 main 和 子线程之间传递 page 对象
page = None
browser = None

def fetch_data():
    """获取数据，返回浏览器和页面对象"""
    print("正在获取新数据...")
    co = ChromiumOptions().headless()
    global browser, page
    browser = ChromiumPage(co)
    page = browser.latest_tab
    page.listen.start('updateNum')
    page.get('https://yqms.istarshine.com/v4/warning')
    try:
        page.ele('tag:span@@class=el-tree-label@@text()=全家桶').click.multi(2)
    except Exception as e:
        sc_send(
            'SCT354857T488CbXZlyFhaEmjbW6Uyf8JV',
            '点击全家桶失败',
            f'错误详情：{str(e)}'
        )
        print(f"❌ 点击全家桶失败：{e}")
    return browser, page

def process_loop():
    """持续运行的线程函数：只负责监听和处理"""
    
    # 子线程中需要单独初始化 COM
    pythoncom.CoInitialize()
    
    while True:
        # 等待 page 初始化完成
        if page is None:
            print("⚠️ page 尚未初始化，等待 5 秒...")
            time.sleep(5)
            continue
            
        try:
            data_packet = page.listen.wait()
            
            data_body = data_packet.response.body
            fetch_records = data_body.get('data', {}).get('records', [])
            for data_detail in fetch_records:
                url = data_detail.get('url', '')
                title = data_detail.get('title', '')
                videoUrls = data_detail.get('videourl', '')
                match = re.search(r'video/(\d+)', url)

                if match:
                    identifier = match.group(1)
                else:
                    print(f"无法解析视频ID: {url}")
                    continue
                    
                try:
                    print(f"正在处理: {identifier}. {title}")
                    downloaded = BaseVideoClient.down(identifier, url)
                    if downloaded:
                        time.sleep(3)
                        wxauto.wxchat(identifier, url, title)
                        print(f"处理完成: {identifier}")
                    else:
                        print(f"跳过微信发送: {identifier}")
                except Exception as e:
                    print(f"处理 {identifier}. {title} 时发生错误: {e}")
        except Exception as e:
            print(f"监听发生错误: {e}")
            time.sleep(5)

def main():
    print("=" * 50)
    print("执行定时任务：刷新数据")
    print("=" * 50)
    
    global browser, page
    
    # 先关闭旧的浏览器（如果存在）
    if browser is not None:
        try:
            print("关闭旧浏览器...")
            browser.quit()
            browser = None
            page = None  # 重置 page 为 None
        except Exception as e:
            print(f"关闭旧浏览器时出错: {e}")
    
    # 重新获取数据
    print("获取新数据...")
    fetch_data()  # 调用 fetch_data() 初始化 browser 和 page
    print("数据刷新完成")

if __name__ == '__main__':
    print("程序启动...")
    
    # 首次启动时先初始化浏览器和页面
    main()  # 这会调用 fetch_data() 初始化全局变量
    
    # 启动处理线程
    t = threading.Thread(target=process_loop, daemon=True)
    t.start()
    print("数据处理线程已启动")
    
    # 设置定时任务
    schedule.every(48).minutes.do(main)
    print("调度器已启动，每48分钟刷新一次数据...")
    
    while True:
        schedule.run_pending()
        time.sleep(1)