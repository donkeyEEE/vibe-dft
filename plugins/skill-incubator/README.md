# Skill Incubator

Skill Incubator 是可独立安装和发布的通用 skill 试验场。它允许不同领域和成熟度的 skill 正常进入发布包；是否将某个 skill 留在这里或升级为独立插件，由维护者逐项决定。

当前包含以下试验中 skill：

- `paper2ppt`：阅读科研论文、组织证据叙事、确认重点并向 PPT Master 交付素材。
- `ppt-master`：创建、填充、增强和验证可编辑 PPTX，并维护 Brand、Style、Layout 与 Deck 模板工作区。
- `nature-response`：起草和审校 Nature 风格的审稿回复与返修材料。
- `scholar-evaluation`：按结构化框架评价学术成果。
- `scientific-critical-thinking`：批判性评估材料物理与计算研究主张。
- `cangjie-skill`：仅限显式调用的待重设计知识蒸馏入口。
- `prl-polishing`：按 claim、evidence、boundary 和 consequence 逻辑逐段审阅、重构或翻译物理论文。

`paper2ppt` 使用同插件内置的 `$ppt-master` 完成渲染。处理 PDF、Office
文档或图片时还需要单独安装 `paper-project`，以调用
`paper-project:liteparse` 完成源文档规范化。

PPT Master 的完整 Python 依赖可按需安装：

```bash
python3 -m pip install -r skills/ppt-master/requirements.txt
```

安装插件后新建 Codex 对话，使这些 skills 进入新的会话上下文。
