# 课程交付验证

## 学习资料在线阅读 · 2026-11-17 13:11

- 阅读地址：https://fanqinzeng.github.io/eda-placement-lesson3/reading/
- Python 练习/参考实现可直接查看、复制，坐标表及原始 JSON、讲义、中英文文字稿、复现说明全部嵌入 HTML；下载为可选操作。
- 发布工作流 44022075413 成功，发布源 e5362667f28999c3220c2bd3f7b6ffab1328cd2d。
- 5组 Node、6组 Python、生成一致性和63项跨页资源/锚点检查通过；独立审阅无重要问题。
- 实际线上验证了入口不触发下载、代码与源文件相同、剪贴板复制、16行坐标表、无脚本完整阅读、390/768/1440布局，以及配音切换到对应在线文字稿。
- [在线阅读报告](qa/reading-deployment.json) · [双语入口回归](qa/bilingual-reading-deployment.json) · [审阅记录](qa/reading-review.md)。

## 初次交付

2026-11-17 12:13（Asia/Shanghai），第一版已部署至 https://fanqinzeng.github.io/eda-placement-lesson3/ ，早于用户的 15:00 截止时间。

- 交付源提交：df179769046c67bd573a522106a93ce6a90cb349。
- [GitHub Pages 首次工作流](https://github.com/FanqinZeng/eda-placement-lesson3/actions/runs/44015478488)：success。
- 首页、MP4、VTT：公开 HTTP 200；媒体支持 Accept-Ranges: bytes。
- 线上浏览器：标准图 4/16/8；非对称中心 B 为 11/36/22；MP4 实际时长、100 秒之后章节定位、字幕轨以及移动端无溢出均验证。
- [浏览器报告](qa/browser.json)：桌面交互、移动布局、600px SVG 变换回归、无效输入、进度、存储降级等。
- [媒体报告](qa/media.json)：346.367 秒、1080p30fps、H.264/AAC、平均 -20.1dB、峰值 -1.5dB、67 字幕段。
- [独立审阅与修复](qa/review.md)：一项重要与两项小问题均修复。
- Node 数值测试 3 组通过，含 300 组独立 Python 交叉核对；HTTP Range 回归 2 组通过；31 项资源/锚点检查通过。

真实限制：没有人的完整普通话听感审评或真实触屏设备测试。当前证据来自原始合成文本、音频流/音量与字幕时间戳、代表画面和隔离 Edge 浏览器；不扩大为对所有设备的保证。

## 中英文配音补齐 · 2026-11-17 12:36

- 用户要求两种语言均有完整配音，已交付独立中文和英文原声 MP4，并非仅增加英文字幕。
- [双语发布工作流](https://github.com/FanqinZeng/eda-placement-lesson3/actions/runs/44018165204)：success，发布源提交 15a83b42e28dd9e214702b348053410705cbf342。
- 英文影片 349.767 秒、1080p/30fps、H.264/AAC，合成声音 en-US-JennyNeural；74 段实际句子时间戳字幕。中文346.367秒及其成片哈希保持不变。
- 英文 MP4/VTT 公开 HTTP 200。网页同步切换声音、字幕、章节及下载链接，保留分镜进度、倍速、播放状态和字幕偏好；已在实际公开网址通过快速切换和旧请求竞态回归。
- 记录：[双语线上验证](qa/bilingual-deployment.json)、[英文媒体](qa/media.en.json)、[双语独立审阅](qa/bilingual-review.md)。
- 人的完整听感审评和真实触屏设备验证仍未进行，不夸大自动测试范围。
