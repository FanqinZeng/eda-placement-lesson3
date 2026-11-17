# 源码与复现说明

## 先在网站中验证

返回课程的交互实验，载入标准正方形。三个结果应为 HPWL 4、Clique 16、Star-from-A 8。切换非对称图并更换中心，再对照阅读页中的数据表。

网页实验在浏览器本地计算，不需要登录。阅读 Python 和 JSON 也不需要安装任何软件。下面的本机操作仅在你希望自己运行或修改时使用。

## 自己运行 Python

练习模板和参考实现已经完整显示在本页。可复制代码到编辑器，也可选择下载原文件。

将参考实现保存为 reference.py 后，在同一目录用以下例子核对：

```python
from reference import evaluate

pins = [
    {"id": "A", "x": 2, "y": 2},
    {"id": "B", "x": 4, "y": 2},
    {"id": "C", "x": 2, "y": 4},
    {"id": "D", "x": 4, "y": 4},
]
print(evaluate(pins, "A"))  # [4, 16, 8]
```

参考实现只使用 Python 标准库。坐标文件 examples.json 按预设名称组织；evaluate 接收其中某个预设的引脚列表，例如 data["golden"]，而不是整个预设字典。

## 离线运行整站

获取完整课程仓库后，在仓库根目录运行：

```bash
python3 scripts/serve.py --port 8000
```

在浏览器打开 http://localhost:8000。这个本地服务支持视频分段请求，章节跳转可以正常工作。视频、双语字幕、文字稿和所有实验资源都随仓库提供，播放已生成影片无需再次调用语音服务。

## 修改课程或重新制作影片

- 网页与算法：site/index.html、site/assets/models.mjs、site/assets/app.mjs。
- 在线阅读页：scripts/build_reading.py 从原始讲义、代码、数据和文字稿生成，修改内容后运行 python3 scripts/build_reading.py。
- 中文分镜：video/story.json；英文分镜：video/story.en.json。
- 冻结语音与实际句子时间戳：video/audio/ 和 video/audio/en/。
- 语音和渲染：scripts/speech.py、scripts/render-film.py，使用 --lang zh 或 --lang en。
- 双语字幕：scripts/build-bilingual-captions.py --mux，在两部影片渲染完成后运行，生成同屏字幕并嵌入 MP4。

完整运行命令、依赖与许可可在[课程源码与 README](https://github.com/FanqinZeng/eda-placement-lesson3)中直接查看。

## 检查结果

```bash
node --test tests/*.test.mjs
python3 scripts/check-site.py
python3 scripts/build_reading.py --check
```

媒体流、音量与字幕验证需要制作依赖，分别运行 scripts/verify-media.py 和 scripts/verify-media.py --lang en。自动测试不等于人的完整听感审评或所有真实设备的验证。

新增代码 MIT，新教材 CC BY 4.0。教师教材、字体与合成语音来源见仓库 THIRD_PARTY_NOTICES.md。
