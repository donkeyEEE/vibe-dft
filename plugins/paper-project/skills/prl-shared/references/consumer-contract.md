# 消费协议

正式内容位于 `references/knowledge-source.yaml` 指向的插件本地
`knowledge/` 目录。该目录的 `CONSUMER_CONTRACT.md` 是消费行为的
正式规则；本文件只规定 paper-project 治理端与消费端之间的责任边界。

## 消费端声明

每个消费端 skill 负责定义：

- **Trigger**：什么任务条件需要共享知识；
- **Selection**：用于选择正式卡片或模板的区域、类型、tags 或稳定名称；
- **Application**：知识及其边界在哪一步影响任务流程或输出。

消费端保留自己的任务逻辑、输出格式、安全边界和质量保证责任。

## 读取顺序

1. 读取消费 skill 自己的 `references/knowledge-source.yaml`；
2. 读取插件本地知识目录的 `CONSUMER_CONTRACT.md`；
3. 读取相关正式索引；
4. 只读取完成当前任务所需的最小相关集合；
5. 回到消费端自己的 Trigger、Selection 和 Application 流程。

正常消费只读。消费端不得读取或搜索 `candidates/`，不得无边界扫描仓库，
也不得静默修改卡片、模板、索引、状态、关系或 `updated_at`。

## 异常结果

- **冲突**：报告冲突内容和差异，不生成未经验证的合并规则；
- **有争议知识**：保留正式索引中的争议状态和不同解释；
- **知识缺口或仓库不可用**：提醒用户并继续当前任务，不使用共享知识，
  不回退到插件内旧副本；
- **新知识候选**：作为建议的 Cangjie 输入，不能在消费任务中直接写入正式区。
