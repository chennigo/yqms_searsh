import BaseVideoClient
import wxauto
import time
import re
import threading
import pythoncom  # 添加 COM 初始化支持
from DrissionPage import ChromiumPage
import schedule
from push_error import sc_send
# 在程序启动时初始化 COM
pythoncom.CoInitialize()

# 全局变量，用来在 main 和 子线程之间传递 page 对象
current_page = None
current_browser = None

def fetch_data():
    """获取数据，返回浏览器和页面对象"""
    print("正在获取新数据...")
    browser = ChromiumPage()
    page = browser.latest_tab
    page.listen.start('updateNum')
    page.get('https://yqms.istarshine.com/v4/warning')
    page.ele('tag:span@@class=el-tree-label@@text()=全家桶').click.multi(2)
    return browser,page
def process_loop():
    """持续运行的线程函数：只负责监听和处理"""
    global current_page, current_browser
    
    # 子线程中需要单独初始化 COM
    pythoncom.CoInitialize()
    
    while True:
        # 如果 page 还没准备好，稍微等一下
        if current_page is None:
            time.sleep(1)
            continue
        
        try:
            data_packet = current_page.listen.wait()
            
            data_body = data_packet.response.body
            fetch_records = data_body.get('data', {}).get('records', [])
            for data_detail in fetch_records:
                url = data_detail.get('url', '')
                title = data_detail.get('title', '')
                # identifier = re.search(r'/video/(\d+)', url).group(1)
                videoUrls = data_detail.get('videourl', '')
                match = re.search(r'video/(\d+)', url)

                if match:
                    identifier = match.group(1)
                else:
                    print(f"无法解析视频ID: {url}")
                    continue
                try:
                    print(f"正在处理: {identifier}. {title}")
                    # BaseVideoClient.main(url)
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
    """每30分钟执行一次，更新 current_page"""
    global current_page, current_browser
    print("=" * 50)
    print("执行定时任务：刷新数据")
    print("=" * 50)
    if current_browser is not None:
        try:
            print("关闭旧浏览器...")
            current_browser.quit()
        except Exception as e:
            print(f"关闭旧浏览器时出错: {e}")
            
    new_browser, new_page = fetch_data()
    
    # 更新全局变量
    current_browser = new_browser
    current_page = new_page
    print("数据刷新完成")

if __name__ == '__main__':
    print("程序启动...")
    main()
    t = threading.Thread(target=process_loop, daemon=True)
    t.start()
    print("数据处理线程已启动")
    schedule.every(48).minutes.do(main)
    print("调度器已启动，每48分钟刷新一次数据...")
    
    while True:
        schedule.run_pending()
        time.sleep(1)