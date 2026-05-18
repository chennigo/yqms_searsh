import os
from videodl import videodl

def main(url, file_id=None):
    video_client = videodl.VideoClient(
        init_video_clients_cfg={
            "DouyinVideoClient": {
                "work_dir": f'H:\\5.16',
                "max_retries": 3,
                "maintain_session": True,
            }
        },
        allowed_video_sources=["DouyinVideoClient"]
    )
    
    acfun_url = url
    video_infos = video_client.parsefromurl(acfun_url)

    # 用于存储实际需要下载的视频信息
    to_download = []
    skipped = []

    for info in video_infos:
        # 假设 info.save_path 是最终保存的完整路径（包括文件名）
        # 如果 save_path 只是目录，你可能需要结合 info.title 和扩展名来构造完整路径
        # 这里根据你的实际情况调整，下面是一种常见情况的处理：
        
        # 情况1：如果 info.save_path 已经是完整文件路径
        if hasattr(info, 'save_path') and info.save_path:
            file_path = info.save_path
        else:
            # 情况2：如果 save_path 是目录，或者没有 save_path，则需要根据 work_dir 和标题来构造
            # 注意：你需要知道文件扩展名，或者从 download_url 推断，这里假设为 .mp4
            # 另外，注意标题中可能包含非法文件名字符，需要处理（这里简单示例，未处理）
            file_name = f"{file_id}.mp4" if file_id else f"{info.title}.mp4"
            # 替换掉可能非法字符，简单示例
            illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
            for char in illegal_chars:
                file_name = file_name.replace(char, '_')
            file_path = os.path.join('H:\\5.16', file_name)
        
        # 检查文件是否存在
        if os.path.exists(file_path):
            skipped.append((info.title, file_path))
            print(f"跳过已存在文件: {file_path}")
        else:
            to_download.append(info)
    
    # 如果有需要下载的视频，才调用下载
    if to_download:
        video_client.download(to_download)
        for info in to_download:
            print(info.title)
            print(info.source)
            print(info.download_url)
            print(info.save_path)
    else:
        print("所有文件均已存在，无需下载。")
    
    # 打印跳过的文件信息（可选）
    if skipped:
        print("\n以下文件已存在，被跳过:")
        for title, path in skipped:
            print(f"  {title} -> {path}")

if __name__ == "__main__":
    # 假设你有一个URL传入，这里只是示例
    # main("某个视频URL")
    pass