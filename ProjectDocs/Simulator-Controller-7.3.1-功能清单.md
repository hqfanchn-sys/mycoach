# Simulator Controller 7.3.1 功能清单

本清单用于选择个人精简版保留哪些功能，以及哪些功能接入 Live、Sol 或继续使用本地程序。按可独立讨论的用途拆成 **15 组、156 项**，覆盖原版主要应用和插件；同义语音命令、每个配置参数、翻译资源及开发测试程序合并到对应功能。

**版本基准：2026 年 10 月 29 日核对的最新正式版 7.3.1.0-release，发布于 2026 年 10 月 23 日。** 源码固定为正式版提交 [ed4799fe](https://github.com/SeriousOldMan/Simulator-Controller/tree/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/)。现有安装与旧版本不作为约束，后续按全新安装考虑。主分支 7.3.2 开发版的变化单列在文末。[版本文件](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/VERSION)

这里的“原版实现”描述现有软件。精简版已确认分析用 Sol、语音用 Live；各组具体保留项继续讨论。功能来自对应版本文档与关键源码的静态审查，尚未在游戏中逐项运行验证。

## 已确认的首版方向

截至 2026 年 10 月 30 日，首版围绕 A 游戏接入与赛道数据、B 驾驶教练、M 语音与大模型功能展开；组内细项尚未全部确定。所需的共用分析、存储、配置和运行能力随所选功能保留，其他模块的完整界面不因此自动纳入。

| 环节 | 分工 | 具体职责 |
| --- | --- | --- |
| 遥测采集与数值计算 | 本地程序 | 读取游戏数据、定位和分段，计算圈速及遥测指标，保存和加载参考圈。 |
| 驾驶分析与专业建议 | GPT-6.1 Sol（gpt-6.1-sol） | 根据已获得的数据分析整圈、弯道和参考圈差异，解释问题并形成训练建议。 |
| 语音交流 | GPT-Live 1（gpt-live-1） | 听取问题、澄清需求、处理语音轮替与打断，围绕 Sol 的结果进行口头解释；需要新的驾驶诊断时交给 Sol。 |

典型流程：用户语音提问 → Live 接收需求 → 本地程序提供对应遥测与指标 → Sol 分析 → Live 说明结果并承接追问。已有结果可以复用；新增分析按问题需要触发。

Live 语音交流和 B07 到弯前主动提示已纳入首版。逐弯提示拟由 Sol 根据已获得的遥测与参考圈提前形成建议，本地程序根据赛道位置触发，再由 Live 播报；提示时机与延迟需要实际验证。B08 指定弯道专项练习尚未单独确定，B09 刹车点训练与倒计时仍为备选。

本人实际线路与参考线路叠图暂不纳入首版，保留为后续扩展；图像辅助分析仍为备选。线路叠图是将本人和参考圈的实际驾驶轨迹画在同一张赛道俯视图上，用不同颜色展示入弯位置、经过弯心的位置和出弯展开程度的差异；需要真实的每圈轨迹数据，与速度、油门、刹车等遥测曲线对比是不同的展示能力。暂不做线路叠图不影响教练使用参考圈数据进行分析，也不影响已选的主动逐弯提醒。

OpenAI 官方文档说明 Live 可将推理与工具工作委托给后端模型；Sol 支持推理、工具调用和结构化输出。上述分工为本项目的设计决定，接入与联调尚未实施。[GPT-Live 1](https://developers.openai.com/api/docs/models/gpt-live-1) · [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)

## 如何选择

可以按整组或具体编号回复，例如“B04 保留，用 Sol；B08 待讨论；K 整组删除”。也可以指定“分析用 Sol，语音用 Live”，因为同一功能的分析与说话是两个不同环节。

选择项可用：**保留、删除、备选、待讨论**。模型分工可用：**Live、Sol、两者配合、本地程序、待讨论**。下面保留原版功能的完整列表，已确认的范围和模型分工见上节。

| 分组 | 功能范围 | 编号 | 项数 |
| --- | --- | --- | --- |
| A | 游戏接入与赛道数据 | A01 至 A09 | 9 |
| B | 驾驶教练 Driving Coach | B01 至 B12 | 12 |
| C | 遥测查看与参考圈比较 | C01 至 C10 | 10 |
| D | 车辆工程师 Race Engineer | D01 至 D12 | 12 |
| E | 比赛策略师 Race Strategist | E01 至 E09 | 9 |
| F | 赛道观察员 Race Spotter | F01 至 F14 | 14 |
| G | 车辆调校 Setup Workbench | G01 至 G12 | 12 |
| H | 个人练习管理 Solo Center | H01 至 H07 | 7 |
| I | 赛前策略规划 Strategy Workbench | I01 至 I09 | 9 |
| J | 赛后报告 Race Reports | J01 至 J08 | 8 |
| K | 车队协作 Team Center 和 Team Server | K01 至 K10 | 10 |
| L | 数据库与轮胎资料 | L01 至 L10 | 10 |
| M | 语音与大模型公共功能 | M01 至 M12 | 12 |
| N | 硬件控制与自动化 | N01 至 N12 | 12 |
| O | 安装设置与维护 | O01 至 O10 | 10 |

## 原版 AI 教练如何工作

原版把工作分成数据采集、数值处理、规则判断、大模型分析／表达和语音输出。驾驶教练先把遥测按弯道和直道提取为刹车、弯中、加速等摘要，再与参考圈比较；规则可以给出“早一点刹车”等候选提示，模型结合这些数据及作者编写的驾驶指令生成解释或短建议。其知识不是一套已验证的专业参考线路库。[教练源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Libraries/DrivingCoach.ahk#L1918) · [遥测分析源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Libraries/TelemetryAnalyzer.ahk)

逐弯指导主要利用上一完成圈，重点弯道训练还会检查刚驶过赛段的改善。刹车倒计时由本地位置触发程序承担。原版语音采用识别、文字处理和语音合成的组合；接入原生 Live 双向语音需要改造这条链路。[教练说明](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/AI%20Driving%20Coach.md) · [语音管理源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Libraries/VoiceManager.ahk)

原版还区分两类分析：驾驶教练主要接收分段摘要和规则提示；Setup Workbench 的 GPT 调校工程师会接收抽样后的数值遥测表格，再给出分析或通过工具修改受支持的调校文件。[调校工程师说明](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Setup%20Workbench.md)

“本地”表示原版主要通过普通程序、数值计算或规则完成；“大模型”表示该项依赖所配置模型；“混合”表示两者配合。播报本地计算的结果仍可能使用外部语音服务。工程师、策略师和观察员可以额外叠加 M 组的大模型功能。

## A 游戏接入与赛道数据

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| A01 | 多款赛车游戏接入 | iRacing、AC、ACC、ACE、AMS2、PCARS2、rFactor 2、LMU、RaceRoom、PMR、F1 25；各游戏的数据和控制能力不同。 | 本地 |
| A02 | 自动识别当前驾驶环境 | 识别游戏、车辆、赛道、练习／排位／比赛状态、圈数和天气，为助手提供上下文。 | 本地 |
| A03 | 读取车辆状态 | 读取油量、车速、踏板、方向、挡位、转速、轮胎、刹车、损伤等可用数据；并非每个游戏都提供所有字段。 | 本地 |
| A04 | 读取比赛与对手数据 | 收集排名、组别、圈速、差距和进站等数据，供策略、观察员及报表使用。 | 本地 |
| A05 | 原生详细遥测录制 | 按圈记录随赛道位置变化的驾驶输入及车辆动态；与低频的比赛状态更新是两条不同处理路径。 | 本地 |
| A06 | Second Monitor 遥测接入 | 可改用外部 Second Monitor 提供遥测；需要另行运行该软件。 | 外部 |
| A07 | 远程游戏数据接入 | 支持通过网络连接 PMR、F1 25 等已提供相应接口的游戏；不等于所有游戏都能远程连接。 | 本地＋外部 |
| A08 | 赛道地图生成 | 驾驶时记录赛道轮廓；支持环形赛道及受支持游戏的开放赛段。iRacing 使用专门的轨迹推算过程。 | 本地 |
| A09 | 弯道和直道划分 | 手动划分、命名和移动赛道段，也可根据遥测扫描生成分段，供分析和教练使用。 | 本地 |

依据：[Plugins & Modes 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Plugins%20%26%20Modes.md) · [Session Database 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Session%20Database.md) · [AI Race Spotter 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/AI%20Race%20Spotter.md) · [IRC Plugin.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Plugins/IRC%20Plugin.ahk) · [Track Mapper.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Track%20Mapper.ahk) · [TelemetryCollector.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Libraries/TelemetryCollector.ahk)

## B 驾驶教练 Driving Coach

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| B01 | 赛车知识问答 | 讨论驾驶技术、车辆物理、驾驶习惯及调校原理。知识来自所连接模型和教练指令。 | 大模型 |
| B02 | 结合当前状态对话 | 把当前车辆、赛道、比赛、驾驶段及已识别的问题带入问答；可控制哪些信息进入对话。 | 混合 |
| B03 | 讨论操控和悬挂问题 | 结合本地检测出的转向不足、转向过度、悬挂问题，解释可能原因与驾驶调整方向。 | 混合 |
| B04 | 整圈复盘 | 根据已采集遥测分析整圈表现，讨论时间损失和改进方法。 | 混合 |
| B05 | 指定弯道复盘 | 询问某个弯的刹车、弯中、出弯表现，获得针对该弯的分析。 | 混合 |
| B06 | 参考圈比较指导 | 可参考上一圈、当前最快圈、数据库最快圈或指定参考圈；可使用他人保存的有效数据。 | 混合 |
| B07 | 到弯前主动提示 | 接近弯道时，结合上一圈表现与参考圈给出简短刹车／油门等建议；提示距离和间隔可配置。 | 混合 |
| B08 | 指定弯道专项练习 | 只练选定弯道，并在通过弯道及后续赛段后，将本圈与上一圈比较，给出反馈。 | 混合 |
| B09 | 刹车点训练 | 根据参考数据给出刹车方式、倒计时、踩刹车和开始松刹车的声音提示。与逐弯指导模式二选一。 | 本地 |
| B10 | 比赛中的专注和激励 | 在配速下降时提醒集中注意力，对表现给出鼓励；内容和啰嗦程度可配置。 | 混合 |
| B11 | 无大模型的基础教练 | 保留规则驱动的简短逐弯提示及刹车点训练；不具备完整自由问答能力。 | 本地 |
| B12 | 自动开启训练与赛后讨论 | 可按启动配置自动开始录制和训练、保存最快圈；本场记忆保留到下一场开始前，供赛后讨论。 | 混合 |

依据：[AI Driving Coach 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/AI%20Driving%20Coach.md) · [DrivingCoach.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Libraries/DrivingCoach.ahk) · [TelemetryAnalyzer.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Libraries/TelemetryAnalyzer.ahk)

## C 遥测查看与参考圈比较

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| C01 | 按圈选择和浏览 | 浏览本次录制和已保存圈，查看车手、圈速及相关信息。 | 本地 |
| C02 | 两圈遥测曲线叠加 | 比较速度、刹车、油门、方向、挡位、转速及其他可用通道。 | 本地 |
| C03 | 距离对齐与偏移校正 | 按赛道距离比较两圈，必要时水平移动数据改善对齐。 | 本地 |
| C04 | 地图与曲线联动 | 点击地图定位对应遥测采样点，也能由曲线查看所在赛道位置。地图定位不等于真实走线叠加。 | 本地 |
| C05 | 分段表现摘要 | 按弯道／直道汇总时间、速度、刹车距离、加速位置等信息，并与参考段比较。 | 本地 |
| C06 | 驾驶输入质量指标 | 统计刹车建立、踏板与方向平顺性、修正次数及可用的 ABS／TC 触发信息。iRacing 原生录制的 ABS／TC 两列为缺失值。 | 本地 |
| C07 | 参考圈保存和加载 | 从本地文件或会话数据库保存、加载、移除遥测圈；可用于以后分析和教练参考。 | 本地 |
| C08 | iRacing IBT 导入 | 拆分 IBT 内的各圈后选择导入；需要赛道地图。原版导入结果的圈内时间字段留空，限制后续部分分析。 | 本地 |
| C09 | 外部遥测导入 | 支持自身 telemetry 文件、Second Monitor JSON、MoTeC 导出 CSV 和符合字段要求的通用 CSV。 | 本地 |
| C10 | 通道布局与缩放 | 选择显示通道、组织曲线布局、缩放图表，并查看指定位置的数据。 | 本地 |

依据：[Session Database 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Session%20Database.md) · [Setup Workbench 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Setup%20Workbench.md) · [TelemetryViewer.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Libraries/TelemetryViewer.ahk) · [SessionDatabase.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Libraries/SessionDatabase.ahk)

## D 车辆工程师 Race Engineer

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| D01 | 燃油与剩余圈数 | 估算油耗、可跑圈数、需补油量，提醒低油量，并可计算目标节油用量。 | 本地 |
| D02 | 虚拟能量提醒 | 处理受支持游戏的能量余量和不足提醒；例如 LMU 的虚拟能量。 | 本地 |
| D03 | 轮胎和刹车状态查询 | 播报胎压、胎温、轮胎磨损、刹车温度和磨损；以游戏实际提供的字段为准。 | 本地 |
| D04 | 发动机温度查询 | 查询水温、油温等发动机状态。 | 本地 |
| D05 | 损伤与异常预警 | 提醒悬挂、车身、发动机损伤、胎压损失、轮胎或刹车磨损等异常。 | 本地 |
| D06 | 维修得失分析 | 估算损伤导致的圈速损失与维修时间，判断是否值得进站维修。 | 本地 |
| D07 | 天气与换胎提醒 | 观察天气变化、抓地力和轮胎适用性，提出换干胎／雨胎等建议。 | 本地 |
| D08 | 制定和调整进站计划 | 规划目标圈、补油、轮胎、维修与换车手；支持对已规划项目作修改。 | 本地 |
| D09 | 自动计算补油 | 结合比赛剩余长度、油耗和安全余量，设置进站补油数量。 | 本地 |
| D10 | 轮胎选择和胎压调整 | 选择胎种、胎组或单轮换胎，设置胎压；有足够可靠数据时可修正冷胎压。依游戏而异。 | 本地 |
| D11 | 维修和换车手选项 | 按支持情况设置维修项目、刹车服务及车手交接；部分游戏只能使用较粗的维修开关。 | 本地 |
| D12 | 准备并执行进站设置 | 提醒本圈进站，将计划写入游戏的进站选项，记录实际服务；可人工确认，也可配置自动处理。 | 本地 |

依据：[AI Race Engineer 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/AI%20Race%20Engineer.md) · [Customizing Assistants 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Customizing%20Assistants.md) · [RaceEngineer.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Libraries/RaceEngineer.ahk)

## E 比赛策略师 Race Strategist

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| E01 | 比赛形势查询 | 查询当前排名、组别、圈速、差距和剩余比赛长度。 | 本地 |
| E02 | 未来排名预测 | 根据当前节奏及比赛模型，估计之后或进站后的排名变化。 | 本地 |
| E03 | 进站时机和 undercut 分析 | 模拟不同进站圈，比较交通影响和出站位置，为提前／延后进站提供依据。 | 本地 |
| E04 | 载入并执行赛前策略 | 使用 Strategy Workbench 或数据库中的策略，追踪驾驶段和下一次进站。 | 本地 |
| E05 | 比赛中生成或重算策略 | 根据当前数据、比赛规则、油耗和轮胎等条件提出策略，也可解释变化。 | 本地 |
| E06 | 天气和意外后的策略调整 | 天气变化、临时进站或比赛情况偏离计划时，重新评估剩余赛程。 | 本地 |
| E07 | 全场黄旗策略 | 在全场黄旗条件下重新考虑是否进站及其收益。 | 本地 |
| E08 | 与工程师协同和自主模式 | 把选定进站方案交给工程师准备；可配置自动接受和执行策略决策。 | 本地 |
| E09 | 赛后评价与资料保存 | 评价配速、一致性和比赛表现，保存比赛报告及有关设置。 | 本地 |

依据：[AI Race Strategist 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/AI%20Race%20Strategist.md) · [RaceStrategist.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Libraries/RaceStrategist.ahk)

## F 赛道观察员 Race Spotter

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| F01 | 左右并排和三车并行提醒 | 报告左侧、右侧有车、保持车道及某一侧已经清空。 | 本地 |
| F02 | 后车接近和超车方向提示 | 报告后方近车，部分情形预测对方可能从哪一侧尝试超车。 | 本地 |
| F03 | 黄旗和绿旗播报 | 报告分区黄旗、全场黄旗、危险解除和比赛开始。 | 本地 |
| F04 | 事故和慢车提示 | 利用位置、运动和速度信息识别异常慢车、事故及大致距离；可提示身后事故。 | 本地 |
| F05 | 蓝旗和多组别交通 | 提示被套圈、较快组别接近、前方较慢组别，以及是否夹带直接竞争对手。 | 本地 |
| F06 | 重新回到赛道提醒 | 7.3.1 已有事故／出界后的安全回场提醒；来车还差多少秒的细化播报属于 7.3.2 开发版变化。 | 本地 |
| F07 | 前后车差距与趋势 | 提供直接差距或动态追踪，判断正在追近还是被拉开。 | 本地 |
| F08 | 指定对手跟踪 | 选择重点观察车辆，跟踪其圈速、差距、进站和问题。 | 本地 |
| F09 | 对手动态和分段优劣 | 报告对手进站、表现异常，以及你在哪些计时段更快或更慢等信息。 | 本地 |
| F10 | 超车、防守和跟车建议 | 识别部分典型战况，给出防守、利用慢车、跟尾流或处理套圈车的建议。 | 本地 |
| F11 | 切弯和处罚通知 | 游戏提供相应数据时，通知赛道限制、处罚和取消资格。 | 本地 |
| F12 | 比赛进程提醒 | 播报进站窗口、驾驶段剩余时间、最后几圈、练习／排位剩余时间和比赛过半信息。 | 本地 |
| F13 | 成绩和环境变化播报 | 提示起步得失、个人最快圈／速度，以及空气和赛道温度变化。 | 本地 |
| F14 | 提醒频率与类别控制 | 各类提醒可单独开启、关闭和调整频率；可区分本组与总排名。 | 本地 |

依据：[AI Race Spotter 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/AI%20Race%20Spotter.md) · [RaceSpotter.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Libraries/RaceSpotter.ahk)

## G 车辆调校 Setup Workbench

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| G01 | 手动描述车辆问题 | 按快／慢弯、入弯／弯中／出弯等选择问题，设置严重程度和改进优先级。 | 本地 |
| G02 | 规则式调校建议 | 根据问题推荐悬挂、空气动力、胎压、刹车等调整方向，并权衡互相冲突的需求。 | 本地 |
| G03 | 实时转向不足和过度检测 | 用车辆几何、方向输入和运动数据估计操控问题，按发生位置和严重程度统计。 | 本地 |
| G04 | 操控阈值校准和声音反馈 | 按车辆／赛道保存检测阈值，可通过校准驾驶确定阈值，并用声音提示操控问题。 | 本地 |
| G05 | 悬挂触底事件分析 | 由悬挂行程及其变化推断冲击事件，分级并汇总；属于计算推断，依赖通道与采样质量。 | 本地 |
| G06 | 轮胎、刹车和发动机温度诊断 | 按目标温度、上下限及轮胎内外温差识别问题；原版不对保存的圈遥测执行此温度分析。 | 本地 |
| G07 | 离线操控与悬挂分析 | 从已保存遥测重新计算操控及悬挂问题，送入调校建议流程。 | 本地 |
| G08 | 悬挂详细图表 | 查看阻尼速度直方图、行程、速度、加速度和高速／低速阻尼分布，支持选轮及局部赛段。 | 本地 |
| G09 | GPT 调校工程师分析 | 把抽样后的数值遥测、车辆几何和可选的问题描述交给模型，生成性能与操控分析。 | 大模型 |
| G10 | 调校文件编辑和应用建议 | 载入车辆调校文件、手动编辑或应用规则／模型建议，检查改动后保存新文件；受支持游戏不包含 iRacing。 | 混合 |
| G11 | 调校差异比较和混合 | 比较两个调校，并按权重混合参数形成新方案；受调校文件编辑器支持范围限制。 | 本地 |
| G12 | 调校日志和车型扩展 | 记录问题、分析、调校修改、圈速及个人笔记；可新增车型、参数定义和建议规则。 | 本地 |

依据：[Setup Workbench 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Setup%20Workbench.md) · [Setup Workbench.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Garage/Setup%20Workbench.ahk)

## H 个人练习管理 Solo Center

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| H01 | 个人场次与驾驶段管理 | 跟踪练习或个人比赛中的场次、各段和各圈，提供概要与备注。 | 本地 |
| H02 | 驾驶中更新的数据面板 | 查看本车、对手、轮胎、消耗品和成绩报告；更新频率由配置决定。 | 本地 |
| H03 | 轮胎组和练习方案管理 | 记录胎组、已使用圈数和冷胎压，手动或自动建立新的练习段。 | 本地 |
| H04 | 建议补充哪些练习数据 | Run Sheet 找出当前数据库缺少的车辆状态组合，提示有价值的数据采集练习。 | 本地 |
| H05 | 历史数据探索 | 按车手、天气、胎种等查看油耗、圈速和轮胎数据，识别已有覆盖及空白。 | 本地 |
| H06 | 整场保存和恢复查看 | 保存完整场次状态，之后重新打开复盘；与向统计数据库导出有效数据是两件事。 | 本地 |
| H07 | 筛选有效圈并入库 | 选择哪些圈写入统计数据库；支持自动保存、自动导出等配置。详细遥测使用 C 组共用查看器。 | 本地 |

依据：[Solo Center 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Solo%20Center.md) · [Solo Center.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Solo%20Center.ahk)

## I 赛前策略规划 Strategy Workbench

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| I01 | 比赛规则建模 | 设置按时间／圈数比赛、编队圈、额外圈、驾驶段限制、必停次数、进站窗口及加油换胎规则。 | 本地 |
| I02 | 进站损失和服务时间 | 配置进出站时间、补油速度、换胎时间、服务能否同时进行及安全油量。 | 本地 |
| I03 | 固定进站安排 | 预设某次进站的圈数、补油和换胎；原版可能形成不满足油量或规则约束的方案，需要检查。 | 本地 |
| I04 | 多人车手安排 | 按车手轮值顺序及其各自圈速、油耗、轮胎数据模拟驾驶段。 | 本地 |
| I05 | 天气与轮胎场景 | 输入天气变化和可用胎种／胎组，模拟换胎及可用轮胎寿命。 | 本地 |
| I06 | 历史数据或手工数据模拟 | 可用历史遥测，也可输入固定圈速和油耗；考虑车重降低及轮胎衰减对圈速的影响。 | 本地 |
| I07 | 策略方案优化 | 比较起步油量、补油量、胎种、轮胎使用程度、首段和末段长度等变化。 | 本地 |
| I08 | 策略规则和脚本校验 | 定义额外约束，过滤不符合赛事要求的模拟方案。 | 本地 |
| I09 | 策略比较、图表和交接 | 比较多个方案，查看油量／轮胎消耗曲线，保存并交给策略师或车队中心使用。 | 本地 |

依据：[Strategy Workbench 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Strategy%20Workbench.md) · [Strategy Workbench.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Strategy%20Workbench.ahk)

## J 赛后报告 Race Reports

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| J01 | 比赛总览 | 查看发车位置、最终成绩、最佳与平均圈速，支持多组别结果。 | 本地 |
| J02 | 车辆报告 | 按圈查看轮胎、电子设置、天气和圈速等技术信息。 | 本地 |
| J03 | 车手能力比较 | 用原版定义的指标评价潜力、比赛技巧、速度、一致性和车辆控制；是统计评分。 | 本地 |
| J04 | 排名变化 | 查看各车在比赛过程中名次的变化。 | 本地 |
| J05 | 全场圈速表 | 查看和筛选自己与对手的各圈成绩。 | 本地 |
| J06 | 性能对比图 | 把选定车手和圈段的圈速画成图表比较。 | 本地 |
| J07 | 一致性分析 | 比较圈速分布、波动、最慢／最快／平均值等。 | 本地 |
| J08 | 比赛配速图 | 用配速图比较不同车辆和车手；这些报告也嵌入 Solo Center 和 Team Center。 | 本地 |

依据：[Race Reports 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Race%20Reports.md)

## K 车队协作 Team Center 和 Team Server

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| K01 | 多人共享的比赛控制台 | 通过 Team Server 连接正在进行的车队比赛，提供完整模式和简化驾驶员模式。 | 本地＋服务器 |
| K02 | 远程查看车队状态 | 查看当前车手、圈速、排名、车辆状态、遥测、驾驶段和进站记录；可在另一台电脑使用。 | 本地＋服务器 |
| K03 | 耐力赛轮值安排 | 创建驾驶段时间表、分配车手，或从策略生成计划并向队员同步。 | 本地＋服务器 |
| K04 | 车队实时策略调整 | 结合当前比赛与历史数据重算策略，并用 Monte Carlo 交通模拟评估出站交通。 | 本地＋服务器 |
| K05 | 车手专属胎压资料 | 保存不同车手、天气和胎种的胎压方案，供换车手和进站准备使用。 | 本地＋服务器 |
| K06 | 远程安排和准备进站 | 由场外人员配置补油、换胎、胎压和维修，再将方案传给当前驾驶员的系统。 | 本地＋服务器 |
| K07 | 下一位车手选择 | 按计划或手工选择交接车手；实际游戏内换人操作取决于该游戏支持。 | 本地＋服务器 |
| K08 | 换人后延续助手状态 | 在队员间传递比赛状态与助手知识，让下一位车手延续本场油耗、计划等信息。 | 本地＋服务器 |
| K09 | 车队比赛保存和复盘 | 保留团队场次，提供车手统计、轮值、进站及比赛总结报告。 | 本地＋服务器 |
| K10 | 服务器和队伍管理 | 自建或连接托管服务器；管理账户、队伍、车手、会话、访问令牌、额度、连接与保存的数据。 | 本地＋服务器 |

依据：[Team Center 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Team%20Center.md) · [Team Server 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Team%20Server.md) · [Team Center.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Team%20Center.ahk) · [Server Administration.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Server%20Administration.ahk)

## L 数据库与轮胎资料

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| L01 | 集中管理赛车资料 | 保存和浏览场次、遥测圈、策略、调校、胎压及有关备注。 | 本地 |
| L02 | 按环境继承默认设置 | 按游戏、车辆、赛道、单人／车队、天气组合保存设置，具体配置覆盖通用默认值。 | 本地 |
| L03 | 历史圈速、油耗和磨损库 | 积累统计数据，供工程师、策略规划和练习管理复用；不同于逐采样点的遥测文件。 | 本地 |
| L04 | 胎压浏览和编辑 | 查看与维护冷／热胎压记录及其温度条件，用于适用游戏的胎压估算。 | 本地 |
| L05 | 轮胎配方和寿命定义 | 维护游戏胎种编号、颜色、干湿适用范围、目标胎压、寿命和可用胎组，支持适用游戏的逐轮胎种。 | 本地 |
| L06 | 文件整理与命名 | 对场次、遥测、策略和调校进行命名、重命名、导入、导出和删除。 | 本地 |
| L07 | 数据清理与范围管理 | 按游戏／车／赛道／车手筛选资料，管理异常统计数据和不再需要的条目。 | 本地 |
| L08 | 资料和配置交换 | 导出、导入自己的设置及数据库内容，保留原始车手归属，支持符合规定结构的外部数据。 | 本地 |
| L09 | 车队数据库同步 | 通过 Database Synchronizer 与 Team Server 同步资料，供队员共享和策略规划。 | 本地＋服务器 |
| L10 | 社区资料和分享控制 | 按自己的授权分享或使用社区胎压、遥测、策略和调校；可分别控制共享类别及条目。 | 本地＋服务器 |

依据：[Session Database 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Session%20Database.md) · [Tyre Compounds 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Tyre%20Compounds.md) · [Session Database.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Session%20Database.ahk) · [SessionDatabase.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Libraries/SessionDatabase.ahk)

## M 语音与大模型公共功能

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| M01 | 语音识别 | 把麦克风输入转成命令或文字；可用本地或云端识别方案，覆盖语言因引擎而异。 | 本地／外部语音服务 |
| M02 | 语音播报 | 把助手文字变成语音；支持本地和多种云端声音，并可调整不同助手的声音。 | 本地／外部语音服务 |
| M03 | 呼叫助手和按键通话 | 使用助手名字、唤醒短语或 Push To Talk 激活交互，也可给控制器本身起呼叫名。 | 本地 |
| M04 | 多语言和翻译 | 各助手可使用不同语言／声音；内置中文等语言资源，并提供翻译服务接入。 | 本地＋外部 |
| M05 | 麦克风、输出设备和音量分配 | 按助手、提示类型、游戏和场次分配音频设备及音量。 | 本地＋外部 |
| M06 | 静音、停听、确认和自主模式 | 独立控制主动播报、语音输入和行动确认，允许按钮确认或配置自主执行。 | 本地 |
| M07 | 大模型服务选择 | 接入 OpenAI、Anthropic、Google、Azure、Mistral、Yandex、OpenRouter、通用接口及本地运行方案。 | 大模型 |
| M08 | 输出话术改写 | Rephrasing Booster 把预设台词改写得更多样；紧急且时间敏感的观察员提醒绕过此改写。 | 大模型 |
| M09 | 自由表达识别为已有命令 | Understanding Booster 把不同说法匹配到原有操作，例如把自然表达理解为查询刹车磨损。 | 大模型 |
| M10 | 带比赛数据的自由对话 | Conversation Booster 让工程师、策略师等基于自身可获得的车辆／比赛信息对话，并可调用允许的动作。 | 大模型 |
| M11 | 事件触发的推理和工具调用 | Reasoning Booster 接收比赛事件和状态，判断是否调用行动；可与对话功能使用不同模型。 | 大模型 |
| M12 | 角色、上下文、脚本与记录 | 可编辑提示词、事件和动作、Lua 回复过滤器，记录模型交互文本；过滤器主要处理文字，不自动证明分析正确。 | 混合 |

依据：[Using Simulator Controller 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Using%20Simulator%20Controller.md) · [Installation & Configuration 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Installation%20%26%20Configuration.md) · [Customizing Assistants 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Customizing%20Assistants.md) · [AI Driving Coach 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/AI%20Driving%20Coach.md) · [LLMConnector.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Framework/Extensions/LLMConnector.ahk) · [LLMBooster.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Framework/Extensions/LLMBooster.ahk) · [LLMAgent.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Framework/Extensions/LLMAgent.ahk) · [VoiceManager.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Assistants/Libraries/VoiceManager.ahk)

## N 硬件控制与自动化

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| N01 | 方向盘、按钮盒和键盘绑定 | 把按钮、旋钮、拨杆和热键映射到游戏、助手及外部程序动作。 | 本地 |
| N02 | Stream Deck 支持 | 配置按键布局、标签、图标和动态显示规则，触发助手及控制动作。 | 本地 |
| N03 | 多层控制模式 | 同一个按钮在不同模式执行不同动作；支持多个控制器各自使用不同模式及自动切换。 | 本地 |
| N04 | 控制器布局与触发识别 | 图形化布局、动作标签／图标编辑及输入检测；支持新版多 USB 设备识别。 | 本地 |
| N05 | 程序启动面板和联动 | 启动、停止赛车游戏及周边应用；按配置执行前后置操作，也可提供系统关机动作。 | 本地 |
| N06 | 游戏进站菜单控制 | 通过游戏接口或按键／菜单自动化修改进站设置；部分游戏用图像匹配辨认菜单选项。 | 本地 |
| N07 | 预设聊天消息 | 用按钮发送游戏内预设聊天内容；7.3.1 还支持在 ACC、rFactor 2、LMU 用语音给出聊天消息。 | 本地＋语音服务 |
| N08 | 外部程序和脚本触发 | 通过热键、命令文件、动作函数和脚本与其他软件联动；包含 RST Telemetry 等外部工具启动辅助。 | 本地＋外部 |
| N09 | SimHub 踏板和车架震动控制 | 启停或调整踏板、前后车架及相关效果强度；震动效果由 SimHub 和硬件实现。 | 外部 |
| N10 | SimFeedback 动态平台控制 | 控制动态平台开关、效果及强度；需要对应软件、连接方式和硬件。 | 外部 |
| N11 | Heusinkveld 踏板曲线切换 | 通过 SmartControl 集成切换踏板校准方案；不代表通用支持所有品牌。 | 外部 |
| N12 | 按赛道位置触发动作 | 在指定位置调 TC／ABS 等车内设置、播放声音、说提示或运行自定义动作；可切换、导入／导出多套规则。 | 本地 |

依据：[Plugins & Modes 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Plugins%20%26%20Modes.md) · [Action Functions 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Action%20Functions.md) · [Installation & Configuration 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Installation%20%26%20Configuration.md) · [AI Race Spotter 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/AI%20Race%20Spotter.md) · [Controller Plugins.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Plugins/Controller%20Plugins.ahk) · [RSP Plugin.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Plugins/RSP%20Plugin.ahk) · [RST Plugin.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Plugins/RST%20Plugin.ahk)

## O 安装设置与维护

| 编号 | 功能 | 用途与边界 | 原版实现 |
| --- | --- | --- | --- |
| O01 | 在线和离线安装 | 下载组件、首次安装、自动更新和卸载；可选择稳定版或开发版渠道。 | 本地＋下载服务 |
| O02 | 初次设置向导 | 检测游戏和外部软件、选择模块、语音和控制设备，生成可用配置。 | 本地 |
| O03 | 完整配置与赛事设置 | 提供高级配置、运行设置及本场比赛设置工具，管理插件和助手行为。 | 本地 |
| O04 | 启动配置组合 | 为练习、比赛等保存不同助手／功能组合，启动时切换。 | 本地 |
| O05 | 扩展组件与配置预设 | 安装附加组件、语言或控制器预设，并支持导入团队共享配置及配置补丁。 | 本地 |
| O06 | 界面语言、单位和主题 | 选择语言、单位、格式、颜色及窗口偏好；可编辑翻译资源。 | 本地 |
| O07 | 启动画面和声音编辑 | 自定义启动图片、GIF 动画、音乐与确认提示音。 | 本地 |
| O08 | 工具入口和功能开关 | 统一打开数据库、调校、策略、个人／车队中心等工具，启停对应模块。 | 本地 |
| O09 | 运行状态和进程监控 | 查看游戏、助手、会话、服务器连接及模块健康，管理后台进程并检查日志。 | 本地 |
| O10 | 开发扩展接口 | 提供插件、规则引擎、脚本模块、动作函数、配置资源及开发测试支持，供定制新的行为或接入。 | 本地 |

依据：[Installation & Configuration 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Installation%20%26%20Configuration.md) · [Using Simulator Controller 文档](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Using%20Simulator%20Controller.md) · [Simulator Setup.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Configuration/Simulator%20Setup.ahk) · [Simulator Startup.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Controller/Simulator%20Startup.ahk) · [System Monitor.ahk 源码](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Controller/System%20Monitor.ahk)

## iRacing 需要单独考虑的边界

| 项目 | 7.3.1 原版情况 | 对精简版的影响 |
| --- | --- | --- |
| 真正的驾驶线路对比 | 实时详细遥测中的地图坐标，由圈内进度映射到事先记录的固定地图；不同圈同一进度会取得同一地图点。 | 不能把这个点直接当作本圈实际横向位置；你要的本人走线与参考走线对比，需要独立确认坐标来源及实现。 |
| IBT 导入后的圈内时间 | 原版导入代码明确向该字段写入空值。 | 原样复用会限制需要时间轴的教练和悬挂分析；这是导入实现的限制，不等于 IBT 的全部时间信息都无法利用。 |
| ABS 和 TC 触发分析 | 所审查 iRacing 原生详细遥测写入路径把这两个通道写为 n/a。 | 不能把缺失值解释为没有触发，也不能照搬其他游戏的 ABS／TC 分析。 |
| 胎压和温度 | 官方特别提示行驶中的胎压数据有缺口；进站控制支持设置胎压并不等于能实时读到准确热胎压。 | 查询、估算、自动修正和写入设置必须分开判断。 |
| 自动修改调校文件 | 原版编辑器支持 AC、ACC、ACE、LMU、rFactor 2，不包括 iRacing。 | 可以保留分析和文字建议；直接改 iRacing 调校属于额外工作。 |
| 即时语音建议 | 通用状态更新、详细遥测采集和紧急观察员提醒有不同频率；云端分析及合成还会增加等待。 | 不能把原版“实时”理解为每个采样点都交给模型处理。 |

依据：[iRacing 地图坐标映射](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Special/IRC%20SHM%20Spotter/IRC%20SHM%20Spotter/IRC%20SHM%20Spotter.cpp#L320) · [iRacing 遥测写入](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Special/IRC%20SHM%20Spotter/IRC%20SHM%20Spotter/IRC%20SHM%20Spotter.cpp#L1516) · [IBT 导入处理](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Database/Libraries/SessionDatabase.ahk#L2212) · [游戏插件限制](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Plugins%20%26%20Modes.md) · [调校编辑器支持范围](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Setup%20Workbench.md) · [更新频率与延迟说明](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Using%20Simulator%20Controller.md)

## 你提出的扩展需求

这些是精简版的候选需求，未计入上面的 156 项原版功能。

| 编号 | 需求 | 目前理解 |
| --- | --- | --- |
| X01 | Live 语音对话与实时指导 | 语音交流已选定 GPT-Live 1，B07 到弯前主动提示已纳入首版；驾驶分析由 Sol 提供，本地程序负责位置触发。 |
| X02 | Sol 数据分析 | 驾驶分析与专业建议已选定 GPT-6.1 Sol；遥测采集和精确指标计算继续由本地程序承担。 |
| X03 | 本人线路与参考线路对比 | 线路叠图暂不纳入首版，留待后续扩展；教练使用参考圈数据进行分析照常保留。 |
| X04 | 图像辅助识别问题及对比展示 | 图像辅助分析仍为备选。原版部分进站菜单的图像匹配，不等于这种驾驶画面分析。 |

## 模块之间的主要依赖

| 要保留的能力 | 需要连带考虑的组件 |
| --- | --- |
| B 驾驶教练和 C 遥测比较 | A 的游戏数据、地图／分段，以及参考圈的加载与保存；语音交互再接 M。 |
| D 工程师 | A 的车辆与会话数据、L 的设置和历史统计；自动进站再接 N06。 |
| E 策略师与 I 策略规划 | A 的比赛数据、L 的历史统计与轮胎资料；落实进站再接 D。 |
| F 观察员 | A 的交通及位置数据、快速本地事件判断和播报通道；可独立于深度教练分析保留。 |
| G 调校分析 | A／C 的遥测、车辆几何与参数资料；自动改文件另需该游戏的调校编辑器。 |
| H 个人练习中心与 J 报告 | A 的比赛数据、C 的遥测组件及 L 的存储；多处共用同一套报表组件。 |
| K 车队功能 | Team Server、同步、账户及会话管理；只做单人功能时是否保留由你决定。 |
| Live 或 Sol 接入 | 数据和本地动作接口仍需存在；替换模型不自动替代采集、计时、绘图和游戏控制。 |

## 支持的游戏范围

7.3.1 文档与插件提供主要助手接入的游戏包括：**iRacing、Assetto Corsa、Assetto Corsa Competizione、Assetto Corsa EVO、Automobilista 2、Project CARS 2、rFactor 2、Le Mans Ultimate、RaceRoom Racing Experience、Project Motor Racing、F1 25**。支持深度、可读取字段及进站控制随游戏变化。

另外保留了 **Rennsport** 的简单启动／停止插件，不能据此认定具有完整遥测或 AI 助手支持。[游戏插件总览](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Docs/Plugins%20%26%20Modes.md) · [Rennsport 插件](https://github.com/SeriousOldMan/Simulator-Controller/blob/ed4799fe23161767dcfc44b0b7fdb0c1ad1c3a25/Sources/Plugins/RSP%20Plugin.ahk)

## 7.3.2 开发版的额外变化

截至本次核对，主分支是 **7.3.2.0-dev，2026 年 10 月 27 日构建**，固定提交 [27a46f5c](https://github.com/SeriousOldMan/Simulator-Controller/tree/27a46f5c6bc581f47a610666ca4a80c32553aa27)。主要功能变化如下，未混入正式版功能描述：

- **V01 回场来车间隔：** 在事故或出界后，还可报告接近车辆的秒数间隔，并增加相关阈值／校正设置。
- **V02 固定进站扩展：** 扩展策略规划中预设固定进站的能力。
- 另有圈时归一化、调校工作台菜单、波兰语提示等修复及运行环境更新。

开发版说明列出的 10 月 30 日是计划发布日，截至 10 月 29 日不能当作已经正式发布。[开发版版本文件](https://github.com/SeriousOldMan/Simulator-Controller/blob/27a46f5c6bc581f47a610666ca4a80c32553aa27/VERSION) · [对应更新说明](https://github.com/SeriousOldMan/Simulator-Controller/blob/27a46f5c6bc581f47a610666ca4a80c32553aa27/Docs/Releases.md)

后续精简以选定源码版本为基础，按全新安装交付；功能取舍和 Live／Sol 分工以你的选择为准。

