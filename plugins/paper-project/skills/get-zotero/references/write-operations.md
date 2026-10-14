# Zotero 写入方案与授权

## 用户授权与应用授权

每份写入方案明确库、对象 key、操作、字段前后值及影响。用户直接指定对象和具体修改时，该指令就是授权；宽泛整理或自主修正先展示方案，再等待批准。自主修正题录提供论文原文、出版社或 DOI 注册信息等依据；来源冲突列出候选。类型转换展示字段迁移和 `cleared_fields`。

Zotero 技术授权统一使用应用名 **Codex**。首次在 Zotero 弹窗选择 **Always Allow** 后，所有使用本技能的 Codex 工作流复用授权，不重复请求弹窗。持久密钥按 Zotero Server ID 与端点绑定，保存在用户配置目录 `get-zotero/write-auth/`，文件权限为 0600；Windows 使用 APPDATA 下对应目录并继承用户目录权限。只缓存 remembered grant，单次 Allow 不持久化。密钥不进入仓库、项目、方案、输出或日志。Zotero 撤销授权后，下次收到 401 会清除失效缓存并重新请求一次授权。更换 Zotero 数据库、操作系统用户或运行环境可能需要重新授权。

应用授权不替代每次具体变更的用户授权。删除与附件文件覆盖须单独说明后果并获得授权；“整理”不隐含删除。原始明确删除指令可以作为单独授权。范围内可重试；扩大对象、字段或后果需新授权。

## 两步 CLI

```bash
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py write-plan /tmp/request.json --out /tmp/plan.json
# 展示具体差异并确认其已获用户授权后，传递方案输出的 digest：
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py write-apply /tmp/plan.json --approve <digest>
# 删除和附件上传还需单独授权：
python3 <plugin-root>/skills/get-zotero/scripts/zotero.py write-apply /tmp/plan.json --approve <digest> --approve-destructive <digest>
```

`write-plan` 只有 GET，不申请技术授权。`--approve` 表达智能体已经取得的用户授权，并非证明用户批准的安全凭证；智能体必须先完成上述授权判断。digest 绑定整个方案，修改后必须重新生成并批准。默认个人库；组库用 `library: "/api/groups/<id>"`，仍受 Zotero 本身的编辑权限约束。

## 请求格式

```json
{
  "library": "/api/users/0",
  "operations": [
    {
      "action": "update",
      "resource": "items",
      "key": "ABCD2345",
      "set": {"DOI": "10.1234/example"},
      "add_tags": ["已阅读"],
      "remove_tags": ["待阅读"],
      "add_collections": ["BCDE3456"],
      "evidence": "用户明确指定 DOI；或核对来源及原文位置"
    }
  ]
}
```

| action | resource | 请求内容及含义 |
| --- | --- | --- |
| `update` | `items` | `set` 修改题录、作者、类型、笔记、`parentItem`、`relations` 等可编辑字段；增删标签和集合用独立字段 |
| `update` | `collections` | `set.name`、`set.parentCollection`，重命名与调整层级 |
| `update` | `searches` | `set.name`、`set.conditions`，修改保存搜索 |
| `create` | 三种资源 | `data` 为创建数据；条目必须有 `itemType`，集合有 `name`，搜索有 `name` 与 `conditions`；key 可省略，由方案固定生成 |
| `trash` | `items` | 移入回收站；`update` 设置 `deleted: 0` 恢复 |
| `delete` | 三种资源 | 永久删除；条目子项也受影响；集合及子集合的归属移除，库内文献保留；方案列出影响并固定库版本 |
| `upload` | `items` | `file` 指定现有本地文件，上传至已存在的 stored-file 附件；固定文件 SHA-256、MD5、大小和时间，执行三阶段上传 |
| `fulltext` | `items` | `data.content` 及 PDF 页数或文本字符计数，写入该附件的全文索引 |

`set.tags`、`set.collections`、`set.creators`、`set.relations` 均是完整结果，不能把单个新增值直接当作完整列表。标签与集合的增删辅助字段会合并已有值，保留未涉及内容。

创建笔记：`data: {"itemType":"note", "parentItem":"ABCD2345", "note":"<p>内容</p>"}`。更新同一笔记使用 `update/set.note`，变更挂接使用 `set.parentItem`。关联关系使用 Zotero `relations` JSON，保留其他已有关系。

创建附件先提交 `create`：`itemType: attachment`、`linkMode: imported_file`、`parentItem`、`title`、`contentType`、`filename`；再针对新附件 key 生成 `upload` 方案。链接附件使用 Zotero 支持的 `linked_url`/`linked_file` 类型及其合法字段。需要下载的文件先说明来源并在授权范围内取得，再执行上传；写入接口不自动追踪或下载 URL。附件条目创建成功而上传失败时报告残留附件 key，不能报告为文件写入成功。相同对象分步骤操作需逐步生成新方案；前一步生成的对象 key 和版本必须真实读回，不猜测后续状态。

## 批量选择

```json
{
  "selection": {"collection_key": "BCDE3456", "recursive": false},
  "change": {"action": "update", "resource": "items", "add_tags": ["已核对"]}
}
```

也可使用 `selection.item_keys` 或 `selection.query`，三者择一。默认集合只含直接成员；递归必须明确指定。选择只在预览时解析；执行固定对象清单，不追随集合或搜索的新结果。批量选择支持条目 update/trash，其他操作明确列入 operations。

## 冲突与完成条件

执行前确认 Server ID、当前字段、对象版本和文件摘要；条件写入拒绝竞态。只有无关字段变化时可保留该变化继续；目标字段或类型转换前提变化需重新授权。删除和全文索引按库版本冻结可能影响范围；库变更后重新生成方案。

每个对象返回 `verified`、`already-applied`、`verification-failed` 或 `failed`；部分失败非零退出，保留成功结果。POST 的 HTTP 200 不能代替逐对象成功检查。写后 GET 核对指定字段、删除结果、附件 MD5 或全文内容。超时属于结果可能未知，先读回协调再重试；不盲目重新创建。恢复或撤销先提供具体方案，禁止用全量旧对象覆盖新的人工修改。

Zotero 10+ 才支持本地写入；缺少 Server ID 时保留读取能力并报告不支持。API 拒绝的字段、类型或权限明确报告；不直接写 SQLite、profile 或使用 Connector 写入绕过限制。跨库复制和重复条目合并未承诺支持。

官方依据（核对于 2026-10-14）：[Local API](https://www.zotero.org/support/dev/web_api/v3/local_api)、[Write Requests](https://www.zotero.org/support/dev/web_api/v3/write_requests)、[File Uploads](https://www.zotero.org/support/dev/web_api/v3/file_upload)、[Full-Text Content](https://www.zotero.org/support/dev/web_api/v3/fulltext_content)。
