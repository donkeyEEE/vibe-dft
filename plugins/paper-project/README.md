# Paper Project

Paper Project 是面向科研论文阅读、写作、引用核验和科学图件的
Codex 插件。插件中的技能通过 `paper-project:<skill-name>` 命名空间提供。

## 主要技能

- `big-paper-helper`：规划、起草、修改和审计材料计算类中文博士论文。
- [pr-intro](skills/pr-intro/SKILL.md)：撰写或重构以证据为基础的 Physical Review 论文引言。
- `prl-figure`：创建、修改和审查投稿级科学图件。
- `citation-validator`：检查 DOCX 稿件中的引用是否真正支持相邻主张。
- `get-zotero`：从 Zotero 只读获取题录、索引正文或本地 PDF。
- `get-notes`：通过 `get-zotero` 获取选定文献并生成项目内中文研究笔记。
其余可用技能以安装后 `codex plugin list` 和 Codex 技能列表为准。

Paper Project 的写作参考资料均位于对应 skill 的 `references/`，插件根目录不维护共享 `resources/`。通用物理论文逐段润色已迁移到 Skill Incubator 的 `prl-polishing`。

## 运行依赖

```bash
python3 -m pip install PyMuPDF Pillow
```

LibreOffice/`soffice` 用于 Office 文档解析；涉及 Zotero、PDF OCR 或学术检索的技能可能还需要相应的
本地应用、CLI 或连接器；技能会在实际使用时报告缺失项。

## 从 marketplace 发布包首次安装

将完整发布包解压到一个长期不变的绝对路径，例如：

```text
/home/user/codex-marketplaces/paper-project/
├── .agents/plugins/marketplace.json
└── plugins/paper-project/
```

注册并安装：

```bash
codex plugin marketplace add /home/user/codex-marketplaces/paper-project
codex plugin add paper-project@paper-project-release
codex plugin list
```

安装完成后新建 Codex 对话，使新技能进入新的会话上下文。

## 使用新版发布包更新

1. 校验发布者提供的 SHA-256。
2. 把新包解压到临时目录。
3. 备份旧的固定 marketplace 目录。
4. 用新目录替换固定目录，保持绝对路径和 marketplace 名称不变。
5. 重新安装并检查版本：

```bash
codex plugin add paper-project@paper-project-release
codex plugin list
```

本地压缩包 marketplace 不使用 `codex plugin marketplace upgrade`；该命令只
刷新已配置的 Git marketplace 快照。

`.codex-plugin/plugin.json` 中的版本必须带有新的 `+codex.<cachebuster>`，
否则 Codex 可能继续使用旧缓存。更新完成后请新建对话。

## 回滚

把备份目录恢复到同一个固定路径，然后重新执行：

```bash
codex plugin add paper-project@paper-project-release
```

回滚包也必须拥有与目标内容对应的版本标识。恢复后用 `codex plugin list`
确认版本，并新建对话。

## 发布包边界

正式发布包只应包含可安装插件内容，不得包含：

- `tests/`
- `.ingest-staging/`
- `__pycache__/`、`.pytest_cache/`、`*.pyc` 或 `*.pyo`
- 本地论文、解析中间文件或用户数据

发布包内的 `MANIFEST.sha256` 校验各文件，压缩包旁的 `.sha256` 文件校验
整个归档。

## 发布者构建流程

只有获得明确发布授权后，才在开发仓库根执行。先确认待发布范围；每个准备
分发的新版本更新一次 cachebuster，再重新运行两组测试和插件校验：

```bash
python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py paper-project
pytest tests -q
pytest paper-project/tests -q
python3 /home/donk/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py paper-project
python3 paper-project/scripts/build_marketplace_release.py
```

构建器不会自行改变版本，也不会注册 marketplace 或重装插件。默认输出到
开发仓库的 `dist/`，并拒绝覆盖同一版本的已有归档。只有获得明确确认且确实
需要重建同一版本时才使用 `--force`。更新或注册 marketplace、替换固定
marketplace 目录和重装插件属于独立外部操作，必须再次获得明确授权。
