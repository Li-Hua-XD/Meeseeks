import os
import re
import asyncio
import base64
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, Bot
from nonebot.log import logger

bili_video = on_regex(r"(video/BV|b23\.tv/|BV[a-zA-Z0-9]{10})")

@bili_video.handle()
async def handle_bili(bot: Bot, event: MessageEvent):
    raw_msg = event.get_plaintext().strip()
    url_match = re.search(r'(https?://[^\s]+)', raw_msg)
    url = url_match.group(1) if url_match else raw_msg
    
    # 路径依然设在当前插件目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, f"video_{event.user_id}.mp4")
    
    if os.path.exists(file_path):
        os.remove(file_path)

    await bili_video.send("🎬 正在下载并转换视频，请稍候...")

    try:
        process = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-f", "b[ext=mp4]/bv[ext=mp4]+ba[ext=m4a]/b",
            "--max-filesize", "50M",
            "--no-playlist",
            "-o", file_path,
            url
        )
        await process.wait()

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            # --- 关键修改：将视频转为 Base64 字符串 ---
            with open(file_path, "rb") as f:
                video_data = f.read()
            video_base64 = base64.b64encode(video_data).decode()
            
            # 发送 Base64 格式的视频
            await bili_video.send(MessageSegment.video(f"base64://{video_base64}"))
            
            os.remove(file_path)
            logger.info(f"视频发送成功（Base64 模式）")
        else:
            await bili_video.send("❌ 下载失败，请检查链接或视频大小。")

    except Exception as e:
        logger.error(f"插件运行异常: {e}")
        await bili_video.send(f"⚠️ 错误: {str(e)}")
