# EDA 课程网站调研

调研日期：2026-11-17（Asia/Shanghai）。来源：[项目看板](https://github.com/users/yongfu-li/projects/4)及其 32 个 issue 的公开评论。看板公开页面的分组及条目分页均已完整读取；清单见 `project-inventory.json`。

## 访问范围与证据

- 23 个已提交的网站或 HTML 附件地址全部返回 HTTP 200，标题与访问记录见 `site-http-audit.json`。
- 另读取 #3 的仓库首页源码与 README，以及 #19 ZIP 内的 HTML 和文件清单。共有 25 个条目有可审阅的课程内容。
- #25–#31 尚未在 issue 正文或评论中提交网站。没有把这些课程记成已经审阅。
- 本轮审阅的是实际 HTML、部分关联课程页及 JavaScript 源码；浏览器控制连接两次超时，因此**没有完成视觉、点击、音视频播放质量验收**。HTTP 200 不代表交互已验证。
- #7、#13 是 HTML 附件；#19 是 ZIP，不能称为已经公开部署的网站。#3 提供源码，没有发现公开网站地址。
- 优点描述的是页面中实际提供的学习结构与材料，不代表所有教学断言都正确。比如 #13 对 KL 的“只看单步”描述不准确：经典 KL 也使用试探、锁定与最佳累计收益前缀。新课应吸收呈现方法并独立校核内容。

## 逐项记录

| Issue / 课程 | 审阅入口 | 可借鉴之处 | 新课的具体采用方式 |
|---|---|---|---|
| #1 Clustering 02 · Capeur | [Affinity metrics](https://capeur.github.io/eda-clustering-module-lab2/) | 评分先于合并；手算、排名、不同图的反例；实现练习与金标准 | 先定义测量口径，再让学生逐项计算和排序 |
| #2 Clustering 03 · thy031 | [Greedy pair merge](https://thy031.github.io/lab-03/) | Lab/Game/Notes 分流；单步日志；手动画边答案；容量导致停止的反例 | 演示步骤与独立答题分开，先预测再看结果 |
| #3 Clustering 04 · GateUltra | [仓库首页源码与说明](https://github.com/GateUltra/eda-clustering-lab4) | 明确容量可行、达到目标 K、全局最优是不同问题；双语字幕、可复现测试 | 区分“模型数值更小”“布局更好”“真实布线更短” |
| #4 Clustering 05 · Su3037 | [标签传播](https://su3037.github.io/clustering-lab5-label-propagation/) | 从通讯录到芯片的类比；九层解释；答案来自真实引擎；关卡与自由实验台 | 从四个地点的连接问题引入，以同一数据贯穿讲解、影片和练习 |
| #5 Clustering 06 · xingguangyaoyu | [谱二分](https://xingguangyaoyu.github.io/eda-clustering-module-lab6/) | 同时展示矩阵、向量和 sweep 表，反驳“总在中间切” | 同时展示坐标、几何图、逐项求和与结果，避免只给最终数字 |
| #6 Clustering 07 · FanqinZeng | [KL 实验课](https://fanqinzeng.github.io/eda-clustering-lab7-kl/) | 中文叙事；公式对应图中操作；前进、后退、自动演示；可编辑输入和离线资料 | 可回退的模型构造、输入校验、离线参考实现 |
| #7 Clustering 08 · stephQ-lab | [FM HTML 附件](https://github.com/user-attachments/files/33714154/eda_lab_08_fiduccia_mattheyses_fm.html) | 课堂黑板提示；增益桶、锁定池、累计曲线与当前步骤同步；投影模式 | 当前贡献项高亮，让公式中的每一项都能指向图形 |
| #8 Clustering 09 · muranfei | [RW 课程](https://muranfei.github.io/rajaraman-wong-algorithm-teaching/) | 普通话完整视频、章节、学习目标、文字稿和来源边界 | 带中文旁白的视频、章节跳转与可读文字稿 |
| #9 Clustering Coordinator · Su3037 | [Learning Clustering](https://su3037.github.io/learning-clustering/) | 公共例图、学习路径、术语、同例比较；明确编号对应存在的不确定性 | 所有模型使用同一引脚输入；记录 issue 与教材目录映射依据 |
| #10 Partitioning 02 · GateUltra | [Cutsize and balance](https://gateultra.github.io/Partitioning_Lesson2/) | 同样平衡但 cut 不同的对照；每条边只算一次；注明两种平衡指标 | Clique 只算 i<j；强调 HPWL 是半周长；明确单 net 与全网指标 |
| #11 Partitioning 03 · Capeur | [Initial bipartition](https://capeur.github.io/eda-partitioning-module-lab3/) | 五段短视频、速度控制、分步截图；幸运与不幸运种子对照 | 章节化视频、对称与非对称预设、独立反例 |
| #12 Partitioning 04 · muranfei | [KL/FM Refinement](https://muranfei.github.io/kl-fm-refinement-lab/) | 方法比较直接说明操作、评分和限制；视频章节与练习对应 | 模型比较表同时列定义、复杂度和用途边界 |
| #13 Partitioning 05 · stephQ-lab | [FM 中文 HTML 附件](https://github.com/user-attachments/files/33997214/index.html) | 长文目录、概念→伪代码→推演→自测结构；复杂度与易错点单列 | 基础阅读与进阶推导分层；教学内容独立验证 |
| #14 Partitioning 06 · thy031 | [Spectral bipartition](https://thy031.github.io/partitioning6/) | 可单步 sweep；学生手动画割边并验证；解释平票和排序规则 | 让学生预测下一条 Clique 边及贡献，再显示算式 |
| #15 Partitioning 07 · xingguangyaoyu | [Recursive bisection](https://xingguangyaoyu.github.io/EDA-Partitioning-Module-Lesson-7/) | k=2/3/4 同图对照，cut 增量有逐步解释 | 同图三模型对照；改变一个条件后解释哪些项变化 |
| #16 Partitioning 08 · FanqinZeng | [Multiway lesson](https://fanqinzeng.github.io/eda-partitioning-lesson8/) | 中文/英文配音可切；矩阵到坐标再到候选表；可导入输入 | 先测量再解释，视频数值与实验共用例子 |
| #17 Partitioning Coordinator · FanqinZeng | [Learning EDA](https://fanqinzeng.github.io/Partitioning_Module_Coordinator/) | 按学习问题选择入口；影片、实验、代码形成闭环；清楚署名 | 延续视频配色，提供“从头学”和“直接实验”两条入口 |
| #18 Floorplanning 02 · muranfei | [Fixed-outline](https://muranfei.github.io/eda-floorplanning-topic02/) | 用装箱讲边界与正面积重叠；双语音轨；合法性是门槛 | 把“线长测量”与“合法布局”分开，不将重叠零线长宣称为好解 |
| #19 Floorplanning 03 · stephQ-lab | [Area/deadspace ZIP](https://github.com/user-attachments/files/34252235/area-deadspace.zip) | 两个密度分母对照；合法性门槛；操控面板、drills 和自测 | 明确所算对象、距离与模型，避免跨口径比较 |
| #20 Floorplanning 04 · GateUltra | [Slicing floorplans](https://gateultra.github.io/floorplanning-lesson4/) | 几何→树→表达式→栈的统一视角；媒体失败保留讲义；键盘步骤 | 图形→边集合→算式的互相映射；视频不可播放时文字稿可用 |
| #21 Floorplanning 05 · Capeur | [B*-tree](https://capeur.github.io/eda-floorplanning-module-lab5/) | 小段视频与互动课对应；skyline、旋转、交换解释结果 | 每一视频章节对应一项实验任务 |
| #22 Floorplanning 06 · Su3037 | [Sequence-pair](https://su3037.github.io/floorplanning-lesson6-sequence-pair/)及其模块页 | 目标→约定→约束图→DP→挑战→Python；充分区分合法、装得下与紧凑 | 公开测量约定、独立参考实现和有解析的概念检查 |
| #23 Floorplanning 07 · thy031 | [入口及关联 lab/tool](https://thy031.github.io/floorplanning7/) | 课程与工具分离；公开页壳指向统一 pages.js 与 Anneal-O 工具 | 阅读与实验共享数据；本轮只核对页壳与资源链接，未验证动态内容 |
| #24 Floorplanning 08 · xingguangyaoyu | [Soft modules](https://xingguangyaoyu.github.io/EDA-Floorplanning-Lesson-8/) | 学习目标与前置清楚；守恒量与可变量对照；legal 不等于 good | 缩放和移动实验，解释不变量与模型差异 |
| #25 Placement 02 · Su3037 | [Issue](https://github.com/yongfu-li/eda-learning/issues/25) | 暂无提交链接 | 记录为待更新，不臆造课程优点 |
| #26 Placement 03 · FanqinZeng | [Issue](https://github.com/yongfu-li/eda-learning/issues/26) | 当前任务；正文为空，无评论 | 从上游 MODULES 与 net-models 原始材料确定范围 |
| #27 Placement 04 · thy031 | [Issue](https://github.com/yongfu-li/eda-learning/issues/27) | 暂无提交链接 | 待更新 |
| #28 Placement 05 · muranfei | [Issue](https://github.com/yongfu-li/eda-learning/issues/28) | 暂无提交链接 | 待更新 |
| #29 Placement 05 · stephQ-lab | [Issue](https://github.com/yongfu-li/eda-learning/issues/29) | 暂无提交链接；与 #28 标题重号 | 保留上游事实，不自行改号 |
| #30 Placement 06 · GateUltra | [Issue](https://github.com/yongfu-li/eda-learning/issues/30) | 暂无提交链接 | 待更新 |
| #31 Placement 07 · Capeur | [Issue](https://github.com/yongfu-li/eda-learning/issues/31) | 暂无提交链接 | 待更新 |
| #32 Floorplanning Coordinator · xingguangyaoyu | [Floorplanning Studio](https://xingguangyaoyu.github.io/Floorplanning/)及 app.mjs | 公共实例、多方法比较、中文/英文、配音驱动动画、关键处暂停预测；演示不计独立完成 | 动画和答题状态分离；支持减少动态；明确本轮为源码审阅 |

## 融合结论

1. 用一个可手算问题贯穿全课：四个引脚，三把“尺子”。
2. 图、坐标、边集合、算式、结果同步，学生能核查每一项。
3. 先预测再揭示；看演示和载入标准答案不能自动算完成挑战。
4. 必须设置反例：非对称输入的 hub 依赖、BBox 内部移动的盲区、所有点重叠时三项为零。
5. 中文旁白与字幕、章节、文字稿、可下载 MP4 独立交付；延续用户指定视频的深色配色。
6. 引用教学结构时保留作者署名，数值、公式和算法说明独立核验。
