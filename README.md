# 三把尺子，看懂线长 · Placement Lesson 03

中文交互课程：同一组引脚，比较 BBox/HPWL、Clique 与 Star。为 [eda-learning issue #26](https://github.com/yongfu-li/eda-learning/issues/26) 制作，对应关系及主题依据见 [课程范围](docs/research/course-scope.md)。

首版已完成本地实现与验证，GitHub Pages 发布验证进行中。用户已授权按推荐静态方案全权推进。每 40 分钟的定时任务继续衔接实际进度；首版截止时间为 2026-11-17 15:00（Asia/Shanghai）。

## 内容

- 三模型同步 SVG 实验：拖动、方向键与坐标表等价编辑，Star 中心可切换。
- 逐条 Clique 求和演示、对称/非对称/内部点反例。
- 六项实验任务、六项带解析概念检查，本地学习记录及禁用存储降级。
- 5 分 46 秒原创连续动画，1080p/30fps、中文合成旁白、67 段字幕及章节。
- 中文讲义、Python 练习、独立参考实现、数据与可复现媒体源文件。

## 本地运行

```bash
python3 -m http.server 8000 --directory site
```

打开 `http://localhost:8000`。网页无框架、无运行时 CDN，数据在本机计算。下载完整仓库后可离线使用已生成的影片与实验；ES modules 需要 HTTP 服务。

## 验证

```bash
node --test tests/models.test.mjs
python3 scripts/check-site.py
python3 scripts/verify-media.py
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
```

`video/story.json` 是可编辑分镜和旁白，`video/data.json` 由网页引擎导出。`video/audio/` 冻结逐段音频、来源信息和服务返回的句子时间戳；文字不变时无需再调用 TTS。中文合成声音为 `zh-CN-XiaoxiaoNeural`。实际音频时长决定场景与字幕时间，服务返回的约 50ms 重叠句尾被裁到下一句起点，原始边界保留。

字体随源文件保留 OFL。影片无背景音乐。媒体检查覆盖流、音量、时间轴和代表帧；**尚未进行人的完整听感审评**，不将自动音量检查等同于人工试听。

## 调研与持续推进

- [32 条课程条目与逐课优点](docs/research/lesson-review.md)
- [课程设计](docs/course-design.md) · [实施计划](docs/superpowers/plans/2026-11-17-lesson03.md)
- [当前进度](PROGRESS.md) · [第三方来源与许可](THIRD_PARTY_NOTICES.md)

新增代码 MIT，新教材 CC BY 4.0；上游数据和字体等按各自许可处理。
