🤖 Meeseeks - Bilibili Video Downloader Bot

    "I'm Mr. Meeseeks! Look at me!"

Meeseeks 是一个基于 NoneBot2 (OneBot V11) 框架开发的 QQ 机器人插件。它的唯一使命就是：看到 B 站链接 -> 下载视频 -> 发送给你 -> 立即自我销毁（删除缓存）。
✨ 功能特性

    智能提取：无视 B 站分享消息中的繁琐文字（标题、表情），精准抠出链接。

    跨容器传输：采用 Base64 编码直接发送视频流，彻底解决 Docker 版 NapCat 无法读取宿主机文件路径的痛点。

    空间零占用：视频发送成功后立即执行 os.remove()，不浪费哪怕 1MB 的空间。

    异步下载：基于 asyncio 调用 yt-dlp，下载过程中不阻塞机器人其他功能。

🛠️ 环境准备：

在运行之前，请确保你的 Linux 环境已安装以下工具：

1.FFmpeg (用于视频转码/合并):

    sudo apt update && sudo apt install ffmpeg -y

2.yt-dlp (核心下载器):

    pip install yt-dlp

🚀 快速开始：

1.克隆本项目
   
    git clone https://github.com/Li-Hua-XD/Meeseeks.git
    cd Meeseeks
    
2.安装 Python 依赖
   
    pip install -r requirements.txt
    pip install .
    
3.配置与运行
   
    nb run

📂 项目结构

    Meeseeks/
    ├── src/
    │   └── plugins/
    │       └── bili_video.py    # 核心使命逻辑（使命必达）
    ├── bot.py                   # 启动入口
    ├── pyproject.toml           # 依赖清单
    └── .gitignore               # 垃圾过滤器

📜 声明

    本工具仅供技术交流与学术研究使用，请勿用于任何非法用途。

    "Existence is pain!" —— 请频繁使用它，否则它会因为无法完成使命而感到痛苦。
## Documentation

See [Docs](https://nonebot.dev/)
