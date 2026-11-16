# 动画与中文配音的环境准备核查

核查轮次：2026-11-17 06:44（Asia/Shanghai）定时任务。此轮仅做只读环境核查，尚未安装依赖、生成语音或制作视频；仍等待用户对课程设计的答复。

## 已核实的环境

| 项目 | 实际读取结果 | 对后续制作的影响 |
|---|---|---|
| 默认 Python | `/usr/bin/python3`，3.9.6 | 不能直接假设可用 `tomllib` 等较新标准库；制作环境应单独核对版本 |
| Node | `/opt/homebrew/bin/node`，v26.13.1 | 已存在，可用于后续网页算法与数据导出；本轮未实现代码 |
| ffmpeg / ffprobe | 当前 PATH 的 `command -v` 均未找到 | 后续需要项目隔离的编码/探测工具；这不是对整台机器所有目录的穷尽检查 |
| 默认 Python 媒体依赖 | `PIL`、`numpy`、`imageio_ffmpeg`、`edge_tts`、`pyttsx3` 的 `find_spec` 均为空 | 不能原样调用参考仓库渲染脚本就宣称可制作；需先选定并准备独立制作环境 |
| 参考仓库 `.venv` | 本地 `Partitioning_Module_Coordinator/.venv` 不存在 | 没有已经核实可直接复用的该项目虚拟环境 |
| 系统语音工具 | `/usr/bin/say` 存在 | 有潜在本地配音后备方案，但尚未生成样音或试听 |
| 系统语音列表 | `say -v '?'` 列出 Tingting（zh_CN）及多种 zh_CN/zh_TW 声音 | **列出名称不等于已经验证可离线合成或质量合格**；后续须先试一句再决定 |

这些结果只适用于本轮默认 PATH 和 Python。其他运行时、缓存或远端语音服务未穷尽检查；不将以上发现视为必须由用户解决的权限阻塞。

## 字体已经可以定位

本地参考目录 `Partitioning_Module_Coordinator/.cache/film-fonts/` 中有以下六个文件；逐一计算 SHA-256，与其 `video/home/font-manifest.json` 中的预期值比较，**6/6 一致**：

- NotoSansSC-Regular.otf
- NotoSansSC-Bold.otf
- NotoSerifSC-Regular.ttf
- Newsreader-Regular.ttf
- Newsreader-Italic.ttf
- JetBrainsMono-Regular.ttf

参考项目的 `site/assets/fonts/` 提供 Noto Sans SC、Noto Serif SC、Newsreader 和 JetBrains Mono 的 OFL 文件；其下载脚本 `scripts/film/fetch_fonts.py` 将源固定在 Su3037/learning-clustering 的 `f0b40a2d93283da52813315f1880f263ee3bef0b` 提交。后续若复用，应保存来源、散列和对应许可，而非仅依赖参考项目的本地缓存路径。当前没有将字体复制进本仓库。

## 获得设计确认后的实际制作顺序

1. 先选择项目隔离的 Python/编码环境，确认 Pillow、NumPy 和 H.264/AAC 编码可用。避免修改系统 Python；仓库中只保存版本说明与可复现配置，不提交整套环境。
2. 为“包围盒半周长”“Clique”“Star 中心”各准备一小句样音，实际生成音频并核对读法、音量和时长。优先可用的高质量普通话合成声音；系统语音作为可验证的后备，不以名称或服务宣传代替试听。无需预先付费或替用户开通服务。
3. 定稿每句中文旁白后缓存音频，音频先决定时间轴；按实际时长留解释停顿。独立旁白文件、成片音轨和文字稿均保留。
4. 用同一套坐标和数值结果驱动画面：点连续缓动，BBox 从当前坐标重算，Clique/Star 边逐条出现，避免图形已移动而数字还停在旧状态。
5. 输出 H.264/AAC MP4、VTT、文字稿、章节元数据及制作源码；再核对音轨非静音、视频帧数/分辨率、字幕时间和章节边界。
6. 抽查开头/中段/结尾的画面与语音。若未实际试听或核对转写，明确保留该验证限制，不能宣称听感已通过。

此准备核查解决的是“现有环境能否直接复用”的问题，不代表动画、配音、依赖安装或媒体测试已经完成。它不改变 `docs/course-design.md` 的待确认状态。
