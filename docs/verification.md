# 首版交付验证

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
