---
author: pldz1
category: ai-industrial-report
csdn: ''
date: '2026-07-15'
gitee: ''
github: ''
juejin: ''
serialNo: 1
status: publish
summary: 以 2026 年上半年具体产品、工厂项目、行业数据和研究报告为证据，分析 Physical AI、工业机器人、具身智能与智能制造的八个关键趋势。
tags:
  - Physical AI
  - 工业机器人
  - 具身智能
  - 智能制造
  - 行业趋势
thumbnail: /api/v1/website/image/ai-industrial-report/2026-industrial-report-half-thumbnail.jpg
title: 2026 年上半年 Physical AI 与工业机器人行业趋势报告
---

# 2026 年上半年 Physical AI 与工业机器人行业趋势报告

> **核心判断：**2026 年上半年，机器人行业最重要的变化并不是“人形机器人突然成熟”，而是模型、仿真、边缘计算、工业数据和传统自动化开始被组织成一套更完整的 Physical AI 技术栈。行业竞争也因此从单台机器人展示，转向数据闭环、平台集成、可靠性验证和规模化交付。

本文不讨论机器人应用软件是否易用，也不围绕示教器、低代码编程或 UI 设计展开，而是关注产业层面的技术路线、产品发布、商业部署与区域竞争。

---

## 一、先说明：什么才算“2026 年最新数据”

机器人行业的数据发布具有明显滞后性。2026 年发布的权威资料中：

- 全球工业机器人完整装机数据通常只统计到 2024 年；
- 2025 年数据在 2026 年上半年仍多为区域性初步统计；
- 2026 年最及时的信息主要来自产品发布、工厂试点、开发平台更新和研究论文。

因此，本文将证据分为三层：

1. **市场底盘：**IFR《World Robotics 2025》以及 Stanford《2026 AI Index》整理的 2024 年完整数据；
2. **市场拐点：**IFR 在 2026 年上半年公布的 2025 年局部初步结果；
3. **产业趋势：**2026 年 1—6 月的具体产品、项目与报告。

---

## 二、市场底盘：工业机器人仍处于历史高位，但增长极度不均衡

IFR 的完整统计显示，2024 年全球新增工业机器人约 **54.2 万台**，连续第四年超过 50 万台；全球在役工业机器人达到约 **466.4 万台**。工业机器人安装市场价值达到 **167 亿美元的历史高位**。

- IFR 原始报道：[World Robotics 2025：全球机器人需求十年翻倍](https://ifr.org/ifr-press-releases/news/global-robot-demand-in-factories-doubles-over-10-years)
- IFR 报告入口：[World Robotics](https://ifr.org/worldrobotics/)
- Stanford 汇总入口：[2026 AI Index Report](https://hai.stanford.edu/ai-index/2026-ai-index-report)

![全球主要工业机器人市场](/api/v1/website/image/ai-industrial-report/industrial-robot-installations-2024.png)

中国在 2024 年安装约 **29.5 万台**工业机器人，占全球新增安装量约 **54%**。日本、美国、韩国和德国仍是重要市场，但与中国之间已经形成明显规模差距。

![区域安装量占比](/api/v1/website/image/ai-industrial-report/regional-share-2024.png)

亚洲占全球新增安装量的 **74%**，欧洲占 16%，美洲占 9%。这不仅是需求分布，也意味着供应链、集成经验、工厂数据和制造人才正在进一步向亚洲集中。

与此同时，2026 年 6 月公布的初步数据表明，美国 2025 年工业机器人安装量约 **3.8 万台**，同比增长 11%。其中食品与非制造行业增长明显，而汽车行业仍是最大客户。

- IFR 2026 年 6 月报道：[US Robot Industry Returns to Double Digit Growth](https://ifr.org/ifr-press-releases/news/us-robot-industry-returns-to-double-digit-growth)

![美国市场初步恢复](/api/v1/website/image/ai-industrial-report/us-robot-installations-2025-preliminary.png)

**判断：**机器人行业不是简单的全球同步增长，而是由中国规模化、美国市场恢复、欧洲工业升级以及新行业渗透共同构成的结构性增长。

---

# 三、八个关键趋势

## 趋势一：Physical AI 已经从概念变成一套“云—仿真—边缘—机器”的产品栈

过去企业谈机器人，通常分别讨论机器人本体、控制器、视觉和软件。2026 年上半年，领先平台厂商开始把这些部分作为一个连续系统来发布。

### 1. NVIDIA 把 Physical AI 产品线组织成完整开发链

在 CES 2026 与 GTC 2026，NVIDIA 连续发布和更新了以下产品：

| 产品 | 作用 | 为什么重要 |
|---|---|---|
| **Cosmos 3** | 世界模型、场景生成、物理推理与动作模拟 | 用统一模型覆盖合成数据、环境理解和策略测试 |
| **Isaac GR00T N1.7** | 面向人形机器人的视觉—语言—动作模型 | 将自然语言、视觉理解和机器人动作联系起来 |
| **Isaac Lab-Arena** | 机器人策略评测环境 | 让不同模型在统一环境中比较，而不是只看厂商演示 |
| **OSMO** | 边缘到云端的机器人工作流编排 | 连接数据生成、训练、仿真和部署任务 |
| **Isaac Sim / Isaac Lab** | 高保真仿真与强化学习环境 | 形成从虚拟训练到真实机器人部署的核心工具链 |
| **Factory Operations Blueprint** | 工厂运营 Physical AI 蓝图 | 将数字孪生、运营数据和 AI 决策连接到工厂层面 |

直接资料：

- [NVIDIA CES 2026：Cosmos、GR00T、Isaac Lab-Arena 与 OSMO](https://nvidianews.nvidia.com/news/nvidia-releases-new-physical-ai-models-as-global-partners-unveil-next-generation-robots)
- [NVIDIA GTC 2026：Cosmos 3 与 GR00T N1.7](https://nvidianews.nvidia.com/news/nvidia-expands-open-model-families-to-power-the-next-wave-of-agentic-physical-and-healthcare-ai)
- [NVIDIA：Physical AI 进入现实世界](https://nvidianews.nvidia.com/news/nvidia-and-global-robotics-leaders-take-physical-ai-to-the-real-world)
- [GTC 2026 端到端 Physical AI 开发流程](https://www.nvidia.com/en-us/on-demand/session/gtc26-s81478/)

这里最值得注意的不是单个模型版本，而是产品之间的接口关系：Cosmos 负责生成和理解世界，Isaac 负责模拟和训练，GR00T 负责机器人策略，边缘计算平台负责部署。

### 2. Arm 新设 Physical AI 业务方向，押注边缘实时计算

2026 年 CES 期间，Arm 将机器人、汽车与相关边缘计算能力更明确地归入 Physical AI 方向。Arm 强调的并不是一个机器人模型，而是四项底层能力：

- 较低功耗；
- 实时响应；
- 长生命周期平台支持；
- 软件在不同设备间的可迁移性。

直接资料：

- [Reuters：Arm 成立 Physical AI 业务部门](https://www.reuters.com/business/autos-transportation/arm-launches-physical-ai-division-expand-robotics-market-2026-01-07/)
- [Arm：The Next Platform Shift — Physical and Edge AI](https://newsroom.arm.com/blog/the-next-platform-shift-physical-and-edge-ai-powered-by-arm)
- [Arm Physical AI 产品与市场页面](https://www.arm.com/markets/physical-ai)

### 这说明了什么

Physical AI 的竞争边界已经被扩大。未来客户采购的不只是机器人本体，而是：

**训练计算 + 世界模型 + 仿真环境 + 边缘芯片 + 控制系统 + 数据运营平台。**

单一机器人公司的产品能力可能很强，但如果缺少训练、验证与部署基础设施，就很难形成大规模持续交付。

---

## 趋势二：工业 AI 正从 Copilot 走向能够执行工程任务的 Agent

2024—2025 年，工业 AI 的典型产品是文档问答、代码补全和维修助手。2026 年上半年，产品开始向“多步骤规划与执行”推进。

### 1. Siemens Eigen Engineering Agent：从建议走向执行

Siemens 在 Hannover Messe 2026 发布 **Eigen Engineering Agent**。它被定位为面向工业自动化工程的 AI Agent，不仅回答问题，还能够：

- 拆解工程任务；
- 规划多步骤工作；
- 调用工程工具；
- 生成或修改自动化工程内容；
- 检查结果并进行自我修正。

直接资料：

- [Siemens：Eigen Engineering Agent 发布](https://press.siemens.com/global/en/pressrelease/siemens-brings-ai-physical-world-eigen-engineering-agent)
- [Siemens：2026 年 6 月增加两项新能力](https://press.siemens.com/global/en/pressrelease/siemens-takes-ai-physical-world-next-level-two-new-eigen-engineering-agent)
- [Siemens Hannover Messe 2026 专题](https://press.siemens.com/global/en/event/siemens-hannover-messe-2026)

这与普通 Copilot 的差异在于：Copilot 给出文本建议，Agent 则试图完成一个带有状态、工具调用与校验环节的工程流程。

### 2. Siemens Fuse EDA AI Agent：Agent 开始进入专业工程软件

2026 年 3 月，Siemens 在 NVIDIA GTC 发布 **Fuse EDA AI Agent**，将 Agent 应用到电子设计自动化领域。EDA 工作本身包含大量规则、工具链和验证步骤，因此比一般办公 Agent 更接近真实工业工程。

- [Siemens Fuse EDA AI Agent 发布](https://news.siemens.com/en-us/siemens-fuse-eda-ai-agent/)
- [Fuse EDA AI System 产品页](https://www.siemens.com/en-us/products/fuse-eda-ai-system/agent/)

### 3. Industrial AI Suite：Agent 必须接入工厂数据和边缘运行环境

Siemens 同期宣布 **Industrial AI Suite** 正式可用，并基于 Industrial Edge 扩大 IT 与 OT 数据整合能力。

- [Siemens Industrial Edge 与 Industrial AI Suite](https://press.siemens.com/global/en/pressrelease/siemens-industrial-edge-ecosystem-strengthens-data-and-ai-integration)

### 这说明了什么

工业 Agent 的核心不是聊天，而是能否获得：

- 可信的设备与工程数据；
- 对工业软件的工具调用权限；
- 有约束的执行范围；
- 可回滚和可审计机制。

短期内，Agent 最可能首先改变的是 PLC 工程、产线调试、EDA、运维与工艺优化，而不是直接替代安全 PLC 或机器人实时控制器。

---

## 趋势三：仿真与数字孪生正在从“辅助工具”升级为训练基础设施

机器人行业长期使用仿真做离线编程和碰撞检查。2026 年上半年的变化是：仿真开始同时承担数据生产、策略训练、模型评估与工厂运营优化。

### 1. Cosmos 3：把“生成场景”和“理解物理世界”合并

NVIDIA 将 Cosmos 3 定义为能够统一处理：

- 合成世界生成；
- Physical AI 推理；
- 动作模拟。

这与传统 3D 场景工具不同。它的目标不是只生成漂亮画面，而是产生可用于训练、评估和决策的数据。

- [NVIDIA Cosmos 3 产品发布](https://nvidianews.nvidia.com/news/nvidia-expands-open-model-families-to-power-the-next-wave-of-agentic-physical-and-healthcare-ai)
- [GTC 2026 Virtual Worlds 与 Physical AI](https://blogs.nvidia.com/blog/gtc-2026-virtual-worlds-physical-ai/)

### 2. Isaac Lab-Arena：机器人模型开始需要公开评测基础设施

CES 2026 发布的 **Isaac Lab-Arena** 面向机器人学习与评估。其重要意义在于，行业开始意识到：单个精心设计的演示不能代表模型能力，模型需要在统一任务、扰动和评估指标下进行比较。

- [NVIDIA CES 2026 机器人产品发布](https://nvidianews.nvidia.com/news/nvidia-releases-new-physical-ai-models-as-global-partners-unveil-next-generation-robots)

### 3. Siemens Tecnomatix：工厂级仿真正在接入 AI

Siemens 在 Hannover Messe 2026 展示 Tecnomatix 组合中的：

- **Process Simulate**：机器人、人员和制造流程仿真；
- **Plant Simulation**：产线、物流、节拍和资源流仿真。

- [Siemens Tecnomatix at Hannover Messe 2026](https://blogs.sw.siemens.com/tecnomatix/siemens-tecnomatix-portfolio-at-hannover-messe-the-digital-factory-live/)
- [Siemens Hannover Messe：AI in Manufacturing](https://www.siemens.com/en-us/events/hannover-messe/)

这表明仿真不再只是机器人部门的工具，也开始成为工厂数据、生产规划和 AI 优化的共同运行环境。

### 4. 一条正在成形的数据闭环

现实机器人开发逐渐形成如下路径：

**真实数据采集  
→ 数字孪生重建  
→ 合成数据扩充  
→ 模型训练  
→ 仿真评估  
→ 小规模实机验证  
→ 生产数据回流**

其中每一层都有具体产品：

- 真实数据：相机、力传感器、遥操作系统；
- 数字孪生：Omniverse、Tecnomatix、Process Simulate；
- 合成数据：Cosmos、Isaac Sim；
- 模型训练：Isaac Lab、GR00T；
- 工作流编排：OSMO；
- 实机部署：Jetson、机器人控制器和工业 Edge。

### 这说明了什么

机器人企业的资产不只是机械结构和算法代码。更难复制的是：

- 高质量数字孪生；
- 真实失败数据；
- 仿真与实机之间的校准能力；
- 持续更新的数据闭环。

---

## 趋势四：机器人基础模型进入产品化阶段，但“评测与恢复”比模型规模更重要

2026 年上半年，机器人基础模型继续从单任务策略转向长时序、多模态和跨机器人能力。

### 1. Isaac GR00T N1.7：面向人形机器人的开放 VLA 模型

NVIDIA 在 GTC 2026 发布 **Isaac GR00T N1.7**，将其定位为面向人形机器人的视觉—语言—动作模型。它要解决的不是单一抓取，而是让机器人根据视觉观察和语言目标生成动作序列。

- [GR00T N1.7 官方发布](https://nvidianews.nvidia.com/news/nvidia-expands-open-model-families-to-power-the-next-wave-of-agentic-physical-and-healthcare-ai)
- [NVIDIA National Robotics Week 2026](https://blogs.nvidia.com/blog/national-robotics-week-2026/)

### 2. NVIDIA Isaac GR00T Reference Humanoid Robot：平台开始配套标准硬件

2026 年 5 月，NVIDIA 发布 **Isaac GR00T Reference Humanoid Robot**，并宣布该参考机器人预计由 Unitree 在 2026 年晚些时候提供。

- [NVIDIA Isaac GR00T Reference Humanoid Robot](https://nvidianews.nvidia.com/news/nvidia-open-humanoid-robot-reference-design)

这说明基础模型厂商正在补齐硬件基准。没有统一或参考硬件，研究者很难复现实验，数据也难以跨团队比较。

### 3. Unitree G1-D：厂商开始出售“机器人 + 数据 + 训练工具”平台

Unitree 的 **G1-D End-to-End Platform** 不只包含机器人本体，还包括：

- 数据采集；
- 数据处理与标注；
- 数据资产管理；
- 分布式训练；
- 模型开发；
- 推理与部署工具。

- [Unitree G1-D 端到端平台](https://www.unitree.com/mobile/G1-D)
- [Unitree G1 产品页](https://www.unitree.com/g1)

这类产品说明机器人供应商正在从卖硬件转向卖“数据生产和模型训练入口”。

### 4. RoCo Challenge：工业装配评测开始关注失败恢复

AAAI 2026 的 **RoCo Challenge** 聚焦工业装配任务。相关研究强调，复杂装配不仅需要任务成功率，还需要：

- 长时序规划；
- 双臂或多机器人协同；
- 精细接触操作；
- 失败后的恢复能力。

- [RoCo Challenge at AAAI 2026](https://arxiv.org/abs/2603.15469)

### 这说明了什么

机器人基础模型的产品竞争将逐渐从参数规模转向四个指标：

1. 能否迁移到不同机器人本体；
2. 是否有足够多的真实与合成数据；
3. 失败后是否能恢复；
4. 升级模型后是否仍能通过回归测试。

机器人模型最终必须在物理世界持续运行，因此“平均成功率”远远不够。长时间运行中的偶发错误，往往才是商业部署的决定因素。

---

## 趋势五：人形机器人正在进入真实工厂，但行业仍处于可靠性验证期

2026 年上半年，人形机器人已经不只是舞台演示。一些项目开始进入真实工厂，并披露更具体的任务和运行数据。但这些项目仍然主要属于试点，而不是全面替代传统自动化。

### 1. BMW Leipzig + AEON：在欧洲现有汽车生产体系中试点

BMW 于 2026 年 2 月宣布，在德国莱比锡工厂部署 Hexagon Robotics 的 **AEON** 人形机器人，并建立 Physical AI 生产能力中心。

试点方向包括：

- 电池与零部件生产；
- 与现有量产系统整合；
- 单调、人体工学负担较高或安全风险较高的任务。

直接资料：

- [BMW：首次在德国生产体系部署人形机器人](https://www.press.bmwgroup.com/global/article/detail/T0455864EN/bmw-group-to-deploy-humanoid-robots-in-production-in-germany-for-the-first-time?language=en)
- [BMW：AEON 在莱比锡工厂组装电池模组](https://www.bmwgroup.com/en/news/general/2026/humanoid-robot-in-leipzig.html)

### 2. BMW Spartanburg + Figure：开始披露实际产线贡献

BMW 在 2026 年 6 月披露，Figure 02 曾在 Spartanburg 工厂参与超过 **3 万辆 BMW X3** 的生产，在车身车间执行将金属板件放入焊接工位的任务。BMW 同时推进新一代 **Figure 03** 项目。

- [BMW：Figure 03 Physical AI 项目](https://www.press.bmwgroup.com/global/article/detail/T0458778EN/bmw-group-advances-the-use-of-physical-ai-in-production-with-figure-03-project-in-spartanburg?language=en)

这类数据比“机器人可以搬箱子”的演示更有价值，因为它至少说明机器人已经被放入真实生产节拍和质量体系中。

### 3. Mercedes-Benz + Apptronik Apollo：从搬运与质检切入

Mercedes-Benz 与 Apptronik 合作，在工厂测试 **Apollo** 人形机器人，目标任务包括：

- 将零部件送到生产线；
- 搬运周转箱；
- 进行初步质量检查。

- [Mercedes-Benz：Apollo 工厂试验](https://group.mercedes-benz.com/unternehmen/produktion/produktionsnetzwerk/mbdfc-humanoide-roboter.html)
- [Reuters：Mercedes-Benz 投资 Apptronik 并扩大试验](https://www.reuters.com/business/autos-transportation/mercedes-benz-takes-stake-robotics-maker-apptronik-tests-robots-factories-2025-03-18/)

虽然项目启动早于 2026 年，但它仍是 2026 年观察人形机器人真实工业落地的重要基线。

### 4. UBTECH Walker S2：从样机进入千台级小规模量产

UBTECH 在 2025 年底开始 Walker S2 的量产与交付，并在 2026 年年报中称其进入 **千台级小规模量产与交付**。

Walker S2 的产品特点包括：

- 工业场景设计；
- 自主换电；
- 面向多任务、多场景协同；
- 重点进入汽车工厂训练与部署。

- [UBTECH 公司里程碑：Walker S2 量产与交付](https://www.ubtrobot.com/en/about/company-profile)
- [UBTECH 2025 年年报（2026 年发布）](https://owebsite-cdn.ubtrobot.com/resources/file/2026/04/21/797179114676293.pdf)

### 应如何判断人形机器人是否真正商业化

应重点看以下指标，而不是看舞蹈、奔跑或单次搬运视频：

| 指标 | 含义 |
|---|---|
| 每小时完成任务数 | 是否达到产线节拍 |
| 无干预连续运行时间 | 是否真正具备自主性 |
| 远程接管频率 | 是否隐藏大量人工成本 |
| 平均故障间隔 | 能否稳定运行 |
| 电池更换与充电时间 | 是否能覆盖完整班次 |
| 单任务成本 | 是否优于人力或专用机器人 |
| 对现有工厂改造量 | 是否真的发挥“通用形态”价值 |

**判断：**人形机器人已从纯演示进入工业试点，但 2026 年仍主要是可靠性验证期。真正的分水岭不是厂商宣布多少订单，而是能否持续数月披露可审计的运行数据。

---

## 趋势六：中国、美国和欧洲形成三条不同的产业路线

### 中国：用供应链、成本和出货速度扩大规模

中国在传统工业机器人安装量上已经占全球一半以上。进入人形机器人阶段后，供应链优势继续体现为：

- 自研电机、减速器、编码器和执行器；
- 更低硬件价格；
- 更快产品迭代；
- 大量工厂、研究机构和政府项目提供试点场景。

具体例子：

- **Unitree G1**：面向研究和开发市场的通用人形机器人；
- **Unitree G1-D**：将机器人、数据采集、标注、训练和部署整合成平台；
- **UBTECH Walker S2**：进入千台级小规模量产；
- **Unitree IPO**：2026 年 3 月提交上海上市计划，反映资本市场开始检验人形机器人收入质量。

资料：

- [Unitree G1](https://www.unitree.com/g1)
- [Unitree G1-D](https://www.unitree.com/mobile/G1-D)
- [Reuters：Unitree 上海 IPO 与 2025 年出货情况](https://www.reuters.com/world/asia-pacific/unitree-plans-shanghai-ipo-testing-interest-humanoid-robots-2026-03-20/)
- [UBTECH Walker S2 量产信息](https://www.ubtrobot.com/en/about/company-profile)

这里也出现了一个新的产业问题：**中国已经证明可以快速制造机器人，但真实买方与可持续需求是否足够，仍需观察。**

### 美国：掌握基础模型、GPU 和机器人软件平台

美国的优势集中在：

- NVIDIA 的 Cosmos、Isaac 与 GR00T；
- Figure、Apptronik 等创业公司；
- GPU 与云训练资源；
- 资本市场与开发者生态。

美国公司的目标更接近于定义机器人“操作系统和模型层”，让不同硬件接入相同训练与部署平台。

### 欧洲：把 AI 接入既有自动化与工程体系

欧洲的强项不是消费级 AI 模型，而是：

- PLC 与控制系统；
- 工业网络；
- EDA 与工程软件；
- 数字孪生；
- 功能安全；
- 大型制造企业的集成能力。

具体例子：

- Siemens **Eigen Engineering Agent**；
- Siemens **Industrial AI Suite**；
- Tecnomatix **Process Simulate / Plant Simulation**；
- BMW 的 AEON 与 Figure 工厂项目；
- Mercedes-Benz 的 Apollo 项目。

**判断：**未来可能不是某一地区“全面获胜”，而是形成跨区域组合：中国提供机器人硬件和规模，美国提供模型与计算，欧洲提供工业集成、安全和客户场景。

---

## 趋势七：机器人增长开始从汽车行业扩展到食品、物流、建筑与重型设备

### 1. IFR 数据：美国增长已出现行业扩散

IFR 2026 年 6 月的初步统计明确指出，美国 2025 年机器人市场增长不仅来自汽车，也来自：

- 食品行业；
- 其他非制造领域。

- [IFR：美国机器人行业恢复两位数增长](https://ifr.org/ifr-press-releases/news/us-robot-industry-returns-to-double-digit-growth)

这很重要，因为汽车行业擅长大批量、固定节拍和高资本投入，而食品、物流与中小制造往往具有：

- SKU 多；
- 环境变化大；
- 工件柔软或形状不规则；
- 人员流动率高；
- 自动化预算更有限。

这些条件正好推动 AI 视觉、移动操作和柔性抓取。

### 2. NVIDIA 生态伙伴：从电子装配扩展到建筑和重型设备

NVIDIA 在 2026 年的 Physical AI 发布中列举了多类合作方向：

- 高精度电子装配；
- 自主施工设备；
- 面向中小制造商的 AI 自动化；
- 移动机器人和人形机器人。

- [NVIDIA 与全球机器人企业推进 Physical AI 实际部署](https://nvidianews.nvidia.com/news/nvidia-and-global-robotics-leaders-take-physical-ai-to-the-real-world)
- [Arm CES 2026：Caterpillar 与 NVIDIA 展示重型设备 Physical AI](https://newsroom.arm.com/blog/arm-ces-2026-takeaways)

### 3. Boston Dynamics Spot：从巡检继续向物流作业延伸

Spot 过去主要用于能源、工厂和危险环境巡检。2026 年，其产品探索继续向配送和物流辅助扩展，包括利用附件完成卸货和短距离搬运。

虽然这类场景距离规模化仍有距离，但它说明机器人产品的商业边界正在从“移动传感器”转向“移动作业平台”。

### 4. 为什么新行业会改变机器人产品形态

在汽车行业，专用固定机器人通常具有最好经济性；但在高混合、低批量场景中，固定自动化的改造成本过高。因此，新行业更容易采用：

- 协作机器人；
- 自主移动机器人；
- 视觉引导机器人；
- 移动操作机器人；
- 可通过模型快速换任务的机器人。

**判断：**下一轮机器人增量市场，很可能来自过去自动化率较低、难以为单一产品设计专机的行业，而不是只来自更多汽车焊装机器人。

---

## 趋势八：安全、治理与可验证性开始成为 Physical AI 的独立产品层

随着机器人从固定程序转向模型驱动，传统机械安全已经不足以覆盖全部风险。

### 1. ISO 10218:2025：工业机器人安全开始加入网络与数字风险

2025 年修订的 ISO 10218 标准被 2026 年研究进一步分析。新版本扩展了：

- 功能安全；
- 网络安全；
- 未授权访问防护；
- 协作机器人应用分类；
- ISO/TS 15066 的规范性整合。

- [ISO Robotics Standards 入口](https://www.iso.org/sectors/engineering/robotics)
- [2026 年 ISO 10218 新旧版本比较研究](https://arxiv.org/abs/2602.17822)

这说明机器人安全不再只讨论围栏、急停和碰撞力，也必须讨论软件更新、网络攻击和访问控制。

### 2. SAE World Congress 2026：将具身 AI 视为生命周期系统工程

SAE World Congress 2026 相关白皮书提出，具身 AI 的安全需要覆盖：

- 系统工程；
- 生命周期治理；
- 人类监督；
- 运行可靠性；
- 持续更新后的风险管理。

- [Embodied AI in Action：SAE World Congress 2026 白皮书](https://arxiv.org/abs/2605.10653)

### 3. EmbodiedGovBench：开始评估机器人是否“可治理”

2026 年提出的 **EmbodiedGovBench** 不只测任务成功率，而是评估：

- 是否调用未经授权的能力；
- 运行状态漂移后是否仍安全；
- 是否能恢复；
- 是否有完整审计记录；
- 人类能否及时接管；
- 模型升级后是否破坏既有安全边界。

- [EmbodiedGovBench](https://arxiv.org/abs/2604.11174)

### 4. 安全研究开始覆盖完整攻击链

2026 年的 Embodied AI 安全综述整理了 400 多篇论文，风险覆盖：

- 视觉与传感器攻击；
- 多模态融合脆弱性；
- 后门与越狱；
- 规划阶段失控；
- 硬件层攻击；
- 人机交互中的信任问题。

- [Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses](https://arxiv.org/abs/2605.02900)

### 这会催生哪些新产品

Physical AI 的安全产品层可能包括：

- 机器人行为运行监控；
- 模型版本与策略审批；
- 回归测试平台；
- 仿真红队测试；
- 权限与能力边界管理；
- 事件录像与审计日志；
- 人工接管和安全降级系统。

**判断：**未来工业客户不会只问“机器人能不能完成任务”，还会问“它为什么做这个动作、谁允许它做、升级后是否仍然安全、出错后能不能回溯”。

---

# 四、2026 年下半年值得持续观察的指标

| 观察指标 | 对应产品或项目 | 为什么重要 |
|---|---|---|
| BMW Figure 03、AEON 项目的连续运行数据 | Figure 03、AEON | 判断人形机器人是否从试点进入生产 |
| Walker S2 实际交付量与客户复购 | UBTECH Walker S2 | 验证千台级量产是否对应真实需求 |
| Cosmos 3 与 GR00T N1.7 的第三方评测 | NVIDIA Physical AI 栈 | 区分官方演示与可复现能力 |
| Isaac Lab-Arena 是否形成行业基准 | Isaac Lab-Arena | 决定机器人模型能否客观比较 |
| Eigen Engineering Agent 是否获得执行权限 | Siemens Eigen | 判断工业 Agent 是否真正进入闭环 |
| G1-D 等数据平台的开发者采用量 | Unitree G1-D | 判断硬件厂商能否建立软件与数据生态 |
| 食品与非制造行业安装增长 | IFR 2025/2026 数据 | 判断机器人是否摆脱汽车周期 |
| ISO 10218:2025 的产业落地 | 机器人厂商与集成商 | 判断网络安全和 AI 安全是否进入验收流程 |
| 远程接管与人工标注成本 | 各人形机器人项目 | 识别被隐藏的运营成本 |
| 每任务总成本 | 所有 Physical AI 项目 | 决定最终商业可行性 |

---

# 五、结论

2026 年上半年的机器人行业并不是由一个单一爆款产品推动，而是由多条产品线同时成熟：

- NVIDIA 用 Cosmos、Isaac、GR00T 和 OSMO 建立 Physical AI 开发栈；
- Siemens 用 Eigen Engineering Agent 与 Industrial AI Suite 将 Agent 接入工业工程与 OT 数据；
- BMW、Mercedes-Benz 开始把 AEON、Figure 和 Apollo 放入真实汽车工厂；
- Unitree 与 UBTECH 从机器人本体延伸到数据平台和规模制造；
- ISO、SAE 与研究机构开始建立新的安全和治理框架。

真正的行业趋势可以浓缩为一句话：

> **机器人产业正在从“卖一台会动的机器”，转向“交付一套能够持续学习、仿真验证、边缘部署、稳定运行并接受治理的物理智能系统”。**

对企业而言，2026 年最重要的并不是追逐所有人形机器人新闻，而是判断一个项目是否同时具备：

1. 明确且高频的任务；
2. 可持续获得的数据；
3. 可量化的节拍与成本；
4. 仿真到实机的验证路径；
5. 安全降级和人工接管机制；
6. 可以规模复制的部署架构。

只有这些条件同时成立，Physical AI 才会从展示项目变成真正的生产力。
