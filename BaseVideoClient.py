import os
from videodl import videodl

save_dir = r"E:\5.16\DouyinVideoClient"
os.makedirs(save_dir, exist_ok=True)

def down(identifier, url):
    video_client = videodl.VideoClient(
        init_video_clients_cfg={
            "DouyinVideoClient": {
                "work_dir": r'E:\\5.16',  # ✅ 规范转义反斜杠（原代码易引发路径错误）
                "max_retries": 3,
                "maintain_session": True,
            }
        },
        allowed_video_sources=["DouyinVideoClient"]
    )
    
    video_id = identifier
    file_path = os.path.join(save_dir, f"{video_id}.mp4")
    
    if os.path.exists(file_path):
        print(f"⚠️ 文件已存在，已跳过：{file_path}")
        return False 
    else:
        video_infos = video_client.parsefromurl(url)
        video_info = video_infos[0] if isinstance(video_infos, list) else video_infos
        
        # custom_save_path = os.path.join(save_dir, f"{identifier}.mp4")
        video_info.save_path = file_path
        
        to_download = []
        to_download.append(video_info)
        
        if to_download:
            video_client.download(to_download)
            print(f"✅ 下载完成：{file_path}")
            return True
# down(
#     identifier="test_video_0028",
#     url="https://www.iesdouyin.com/share/video/7642112753582728677"
# )