# MyCoach 开发入口

本仓库基于官方 Simulator Controller 7.3.2 源码快照：
https://github.com/SeriousOldMan/Simulator-Controller/tree/9aa662664d83bce31151d1036fb32460e4023b06

`main` 保存导入的上游基线，`codex/coach-lite-v1` 保存精简版开发。
这是源码快照导入，不含上游完整 Git 历史。保留原版 License 及署名。
上游自带第三方工具属于源码包内容；本地密钥、个人遥测及旧 LapCompare 项目未纳入。

## 需求与状态

- [需求与验收规范](ProjectDocs/Simulator-Controller-首版需求与验收规范-v1.0.md)
- [开发进度](ProjectDocs/Simulator-Controller-开发进度.md)
- [背景交接](ProjectDocs/Simulator-Controller-精简版-交接文档.md)
- [模块说明](Sources/CoachLite/README.md)

第一版：iRacing 接入、可信遥测分析、参考圈导入与自动选择、Sol 分析、Live 语音和主动逐弯提醒。不包含线路叠图。不要改用旧 LapCompare 项目作为基础。

当前仅完成文件解析、参考选择、证据摘要、本地 SQLite 归档和圈生命周期模块。
20 项合成数据测试通过；尚未完成原版构建、真实游戏接入、模型调用、音频或产品界面，正式验收未执行。

## 测试

使用 Python 3.12，无额外 Python 依赖：

```powershell
cd Sources/CoachLite
python -m unittest discover -v
```

## 后续工作

1. 验证官方构建环境及 iRacing 原生采集器；确认 AHK 2.1-alpha.37 和原生构建依赖。
2. 接入可信的场次、车辆、布局、圈有效性和条件信息。不得通过文件名推断场次或把读文件成功当作有效圈认证。
3. 把采集事件接到 Pipeline。原版采集文件完成后从 `Lap N.tmp` 重命名为 `Lap N.telemetry`；读取入口已存在，真实事件连接尚未实现。
4. 接入 Sol 的证据约束分析、Live 语音以及本地提醒调度，再做真实游戏验收。

模型名称是已确认的产品需求，API 可用性尚未验证。密钥仅使用本机安全配置，禁止提交或输出。文档中的绝对本机路径用于历史记录；仓库内开发以本入口的相对路径为准。
