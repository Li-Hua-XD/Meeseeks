import os
import re
import asyncio
import base64
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, Bot
from nonebot.log import logger

# 更新正则表达式：支持 B站 (BV/b23)、YouTube (youtube/youtu.be)、X/Twitter (twitter/x.com)
video_download = on_regex(
    r"(video/BV|b23\.tv/|\bBV1[a-zA-Z0-9]{9}\b|youtube\.com|youtu\.be|twitter\.com|x\.com)"
)

@video_download.handle()
async def handle_video(bot: Bot, event: MessageEvent):
    raw_msg = event.get_plaintext().strip()
    
    # 提取链接
    url_match = re.search(r'(https?://[^\s]+)', raw_msg)
    url = url_match.group(1) if url_match else raw_msg
    
    # 路径处理
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, f"video_{event.user_id}.mp4")
    
    # 清理旧文件
    if os.path.exists(file_path):
        os.remove(file_path)

    await video_download.send("🚀 正在解析多平台视频，请稍候...")

    try:
        # 使用 yt-dlp 进行下载
        # 参数解释：
        # -f: 优先下载 mp4 格式，确保 QQ 兼容性
        # --max-filesize: 限制 50M，防止内存溢出
        # --merge-output-format: 强制合并为 mp4
        process = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-f", "b[ext=mp4]/bv[ext=mp4]+ba[ext=m4a]/b",
            "--max-filesize", "50M",
            "--no-playlist",
            "--merge-output-format", "mp4",
            "-o", file_path,
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            # 读取并转为 Base64
            with open(file_path, "rb") as f:
                video_data = f.read()
            video_base64 = base64.b64encode(video_data).decode()
            
            # 发送视频
            await video_download.send(MessageSegment.video(f"base64://{video_base64}"))
            
            # 成功后删除本地文件
            os.remove(file_path)
            logger.info(f"视频发送成功：来自用户 {event.user_id}")
        else:
            error_log = stderr.decode()
            if "File is larger than max-filesize" in error_log:
                await video_download.send("❌ 视频太大了（超过50MB），Armbian 撑不住啦！")
            else:
                await video_download.send("❌ 下载失败，可能视频受限或链接无效。")
                logger.error(f"下载出错: {error_log}")

    except Exception as e:
        logger.error(f"插件运行异常: {e}")
        await video_download.send(f"⚠️ 发生错误: {str(e)}")
    
    finally:
        # 兜底清理
        if os.path.exists(file_path):
            os.remove(file_path)