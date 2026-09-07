# Skill Incubator

Skill Incubator 是独立安装的演示文稿插件，包含两个已发布的 skill：

- `paper2ppt`：阅读科研论文、组织证据叙事、确认重点并向 PPT Master 交付素材。
- `ppt-master`：创建、填充、增强和验证可编辑 PPTX，并维护 Brand、Style、Layout 与 Deck 模板工作区。

`paper2ppt` 使用同插件内置的 `$ppt-master` 完成渲染。处理 PDF、Office
文档或图片时还需要单独安装 `paper-project`，以调用
`paper-project:liteparse` 完成源文档规范化。

PPT Master 的完整 Python 依赖可按需安装：

```bash
python3 -m pip install -r skills/ppt-master/requirements.txt
```

安装插件后新建 Codex 对话，使两个 skills 进入新的会话上下文。
