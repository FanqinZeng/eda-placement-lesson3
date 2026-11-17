# 三把尺子，看懂线长 · Placement Lesson 03

中文交互课程：同一组引脚，比较 BBox/HPWL、Clique 与 Star。为 [eda-learning issue #26](https://github.com/yongfu-li/eda-learning/issues/26) 制作，对应关系及主题依据见 [课程范围](docs/research/course-scope.md)。

**第一版已于 2026-11-17 12:13（Asia/Shanghai）发布并验证，早于 15:00 截止时间。**

[打开课程网站](https://fanqinzeng.github.io/eda-placement-lesson3/) · [在线学习资料](https://fanqinzeng.github.io/eda-placement-lesson3/reading/) · [中文配音动画](https://fanqinzeng.github.io/eda-placement-lesson3/media/lesson.zh.mp4) · [English narration](https://fanqinzeng.github.io/eda-placement-lesson3/media/lesson.en.mp4)

**中英文配音补齐已于 2026-11-17 12:36 发布并验证。** 在影片上方选择“中文 / English”，或使用上方两种语言的成片直链。

用户已授权按推荐静态方案全权推进。每 40 分钟的构建定时任务在网站及双语配音交付并验证后已结束；后续按具体反馈继续修改。

## 内容

- 三模型同步 SVG 实验：拖动、方向键与坐标表等价编辑，Star 中心可切换。
- 逐条 Clique 求和演示、对称/非对称/内部点反例。
- 六项实验任务、六项带解析概念检查，本地学习记录及禁用存储降级。
- 中英文两个完整配音版本：中文 5 分 46 秒，英文约 5 分 50 秒；均为 1080p/30fps 连续动画，各有对应字幕、文字稿和章节。网页可切换配音，按分镜保持进度与倍速。
- 站内资料阅读页：Python 练习与参考实现可直接查看、复制；坐标表与原始 JSON、完整讲义、中英文文字稿、复现说明全部在线阅读，可选下载保留。

## 本地运行

```bash
python3 scripts/serve.py --port 8000
```

打开 `http://localhost:8000`。网页无框架、无运行时 CDN，数据在本机计算。下载完整仓库后可离线使用已生成的影片与实验；ES modules 需要 HTTP 服务。附带服务支持 MP4 分段请求，确保离线视频章节跳转可用。

## 验证

```bash
node --test tests/*.test.mjs
python3 scripts/build_reading.py --check
python3 scripts/check-site.py
python3 scripts/verify-media.py
python3 scripts/verify-media.py --lang en
```

第三条需要 `requirements-media.txt` 中的依赖。引擎与独立 Python 对 300 组确定性输入交叉核对。真实浏览器验证报告与媒体流检查见 [docs/qa](docs/qa)。`scripts/check-browser.py` 使用隔离的已安装 Microsoft Edge 和 Playwright；修改其 URL/可执行文件路径可用于其他环境。

## 重新制作影片

使用 Python 3.12+，在隔离环境安装 `requirements-media.txt`（首版制作环境还使用 Playwright 做页面检查）。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-media.txt
node scripts/export-data.mjs
.venv/bin/python scripts/speech.py
.venv/bin/python scripts/render-film.py --stills
.venv/bin/python scripts/render-film.py
.venv/bin/python scripts/verify-media.py
.venv/bin/python scripts/speech.py --lang en
.venv/bin/python scripts/render-film.py --lang en
.venv/bin/python scripts/verify-media.py --lang en
.venv/bin/python scripts/build-versions.py
python3 scripts/build_reading.py
```

`video/story.json` 是可编辑分镜和旁白，`video/data.json` 由网页引擎导出。`video/audio/` 冻结逐段音频、来源信息和服务返回的句子时间戳；文字不变时无需再调用 TTS。中文合成声音为 `zh-CN-XiaoxiaoNeural`，英文为 `en-US-JennyNeural`；英文分镜、音频与时间轴分别在 `video/story.en.json`、`video/audio/en/`、`video/timeline.en.json`，不会覆盖中文资源。实际音频时长决定场景与字幕时间，服务返回的约 50ms 重叠句尾被裁到下一句起点，原始边界保留。

字体随源文件保留 OFL。影片无背景音乐。媒体检查覆盖流、音量、时间轴和代表帧；**尚未进行人的完整听感审评**，不将自动音量检查等同于人工试听。

## 调研与持续推进

- [32 条课程条目与逐课优点](docs/research/lesson-review.md)
- [课程设计](docs/course-design.md) · [实施计划](docs/superpowers/plans/2026-11-17-lesson03.md)
- [当前进度](PROGRESS.md) · [第三方来源与许可](THIRD_PARTY_NOTICES.md)

新增代码 MIT，新教材 CC BY 4.0；上游数据和字体等按各自许可处理。
