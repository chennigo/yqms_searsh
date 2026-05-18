import requests
import logging

logger = logging.getLogger(__name__)

def download_video(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        logger.info(f"视频下载成功：{file_name}")
    else:
        logger.error(f"视频下载失败：HTTP {response.status_code}")


#不搞url看，阻力太多，现在搞videodl。
#均已添加logging，方便调试和监控。