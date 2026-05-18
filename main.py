import BaseVideoClient
import wxauto
import time
import re
import logging
from DrissionPage  import Chromium
import schedule
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
#     handlers=[
#         logging.FileHandler('app.log', encoding='utf-8'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)



# 2. 封装获取数据的逻辑
def fetch_data():
    page = Chromium().latest_tab
    page.listen.start('updateNum')
    page.get('https://yqms.istarshine.com/v4/warning')
    page.ele('tag:span@@class=el-tree-label@@text()=全家桶').click.multi(2)
    
    data_packet = page.listen.wait()
    data_body = data_packet.response.body
    records = data_body.get('data', {}).get('records', [])
    print(f"获取到 {len(records)} 条数据")
    return records

# 3. 封装下载和发送的逻辑
def process_and_send(fetch_records):
    if not fetch_records:
        print("没有获取到新数据。")
        return
        
    for data_detail in fetch_records:
        url = data_detail.get('url', '')
        title = data_detail.get('title', '')
        videourl = data_detail.get('videourl', '')
        id = data_detail.get('id', '')
        if not videourl:
            continue
            
        try:
            print(f"正在处理: {id}. {title}")
            BaseVideoClient.main(url)
            time.sleep(2)
            wxauto.wxchat(id, url, title)
            print(f"处理完成: {id}. {title}")
        except Exception as e:
            print(f"处理 {id}. {title} 时发生错误: {e}")

def main():
    print("程序启动")
    records = fetch_data()
    process_and_send(records)


schedule.every(0.5).hours.do(main)


# if __name__ == '__main__':
#     schedule.run_pending()
#     time.sleep(1)  # 避免CPU占用过高

if __name__ == '__main__':
    print("调度器已启动，每30分钟执行一次...")
    
    # 2. 立即执行一次（可选，方便测试）
    main()
    
    # 3. 开启死循环，保持脚本运行
    while True:
        schedule.run_pending() # 检查是否有任务到期
        time.sleep(1)    