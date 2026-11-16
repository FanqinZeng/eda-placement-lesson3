# Lesson 03 主题与数值口径

## 主题对应依据

[Issue #26](https://github.com/yongfu-li/eda-learning/issues/26) 标题为 Placement - Lesson 03，assignee 为 FanqinZeng，正文为空且无评论。不能说 issue 本文已经明确写出 net-models。

上游 [MODULES.md](https://github.com/yongfu-li/eda-learning/blob/main/courses/learn_placement/docs/MODULES.md) 的教学顺序为 intro → HPWL metrics → Net models → Force-directed。#25 叫 Placement - Lab 02，#26 叫 Lesson 03。结合此前课程的“intro 之后 Lab 02”编号惯例，**将 #26 对应到第三个教学单元 Net models for wirelength 是有教材支持的映射推断**，而不是 issue 内的明确说明。

任务分配时的历史版本 `4fb4083379d066325384023af074f7bf59e98e09`（2026-11-10 之前最后一次相关提交）中，MODULES 的对应顺序相同。当前主分支调研版本 `003bcd49e3794e6cfd2680181cdbd347d673ad07`。

直接教学依据：

- [Net models README](https://github.com/yongfu-li/eda-learning/blob/main/courses/learn_placement/module01-03-net-models/README.md)：在同一多引脚 net 比较 bbox、clique、star。
- [EXAMPLES](https://github.com/yongfu-li/eda-learning/blob/main/courses/learn_placement/module01-03-net-models/EXAMPLES.md)：golden clique=16、star-from-A=8。
- [原始讲稿](https://github.com/yongfu-li/eda-learning/blob/main/courses/learn_placement/module01-03-net-models/transcript.md)：bbox=4；明确使用哪个模型。
- [浏览器实验](https://github.com/yongfu-li/eda-learning/blob/main/platform/tools/net-models/net-models.js)：同图移动引脚、十项挑战。
- [placement-core.js](https://github.com/yongfu-li/eda-learning/blob/main/platform/assets/placement-core.js) 与 [tiny_place.json](https://github.com/yongfu-li/eda-learning/blob/main/courses/learn_placement/common/tiny_place.json)：坐标与求值约定。

## 三个模型

本课以单个 net、单位权重、二维曼哈顿距离 d(i,j)=|xi−xj|+|yi−yj| 为主。

| 模型 | 定义 | 实际表达 | 复杂度 |
|---|---|---|---|
| BBox / HPWL | (max x−min x)+(max y−min y) | 包围盒**半**周长，线长估计 | O(p) |
| Clique | Σ(i<j) d(i,j) | 每对引脚一次，共 p(p−1)/2 条边，未经归一化 | O(p²) |
| Star-from-h | Σ(i≠h) d(h,i) | 以指定现有引脚 h 为中心，共 p−1 条辐条 | O(p) |

不把 Clique 的未加权曼哈顿总和与二次布局中的加权平方距离混为一谈；不把 Star 的现有引脚中心与虚拟中心混为一谈；不把图上边的 L 形示意当作实际共享布线。

## 标准例与反例

| 输入 | BBox | Clique | Star-from-A | 作用 |
|---|---:|---:|---:|---|
| Starter：A(0,0), B(8,0), C(0,8), D(8,8) | 16 | 64 | 32 | 对齐教师 spread 例子 |
| Golden：A(2,2), B(4,2), C(2,4), D(4,4) | 4 | 16 | 8 | 对齐教师 goldens；Clique 项 2+2+4+4+2+2 |
| 非对称：A(0,0), B(6,0), C(1,2), D(2,5) | 11 | 36 | 16 | Star-from-B=22、from-C=14、from-D=20，说明中心依赖 |
| 内部点：A(0,0), B(8,0), C(0,8), D(4,4) | 16 | 56 | 24 | D→(2,2) 后 BBox=16、Clique=52、Star-from-A=20 |
| 全部重叠于一点 | 0 | 0 | 0 | 线长小不能保证布局合法 |

Golden 正方形的四个角作 Star 中心时都得到 8，**不能用这张对称图证明 hub 不重要**。

## 教师数据中的易混点

- 六个 net 的总 HPWL 是 starter 52、golden 14；这与单个 ABCD net 的 16→4 是两个对象。采用 net 权重 [1,1,1,1,5,1] 后总和则是 116→30。主实验应只显示 ABCD，扩展资料单列全网口径。
- `fixed_pads` A、D 用于后续布局求解，不用于把本课当作带固定约束的优化器。本课是测量实验，若允许移动 A、D，应明确写出这一约定。
- 本课不求生产布局，不保证消除重叠、满足密度或找到最优布线路径。
- 空输入、缺坐标、NaN、重复 pin、非法 hub 需要明确拒绝或说明处理规则。推荐拒绝无效输入；单 pin 返回零；两个 pin 的三模型值相同。
