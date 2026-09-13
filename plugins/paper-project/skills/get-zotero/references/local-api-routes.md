# Zotero local API and connector routes for Get Zotero

Base URL 由 `scripts/runtime_config.py` 解析。原生环境默认使用 `http://127.0.0.1:23119`；WSL 依次尝试 loopback 和动态发现的 Windows 主机地址。用户显式配置 host 时只使用该地址。

Every request must include:

```text
Host: 127.0.0.1:<configured-port>
Zotero-API-Version: 3
```

Zotero 验证 loopback Host header，因此 header 中的端口必须与连接端口一致。

## Desktop local API

The local API is under `/api/`. It implements Zotero Web API v3 for the local logged-in desktop user.

Important constraints:

- Use `/api/users/0/...` for the local user by default.
- Local API reads do not require an API key.
- The local API is read-only; write requests are not supported there.
- Atom output is not supported locally.
- Attachment file URLs and full text can expose local file paths or document text. Retrieve them only for a user-authorized literature task and only when the reading question requires that evidence; do not reveal local paths in normal output.

Safe read routes:

```text
/api/
/api/schema
/api/itemTypes
/api/itemFields
/api/itemTypeFields?itemType=journalArticle
/api/itemTypeCreatorTypes?itemType=journalArticle
/api/creatorFields
/api/users/0/collections
/api/users/0/collections/top
/api/users/0/items
/api/users/0/items/top
/api/users/0/items/trash
/api/users/0/items/<itemKey>
/api/users/0/items/<itemKey>/children
/api/users/0/items?format=keys
/api/users/0/items?format=versions
/api/users/0/items?format=bibtex
/api/users/0/items?include=data,citation&style=apa
/api/users/0/items?q=<query>
/api/users/0/tags
/api/users/0/searches
/api/users/0/searches/<searchKey>/items
/api/users/0/groups
/api/users/0/fulltext?since=0
/api/users/0/items/<attachmentKey>/fulltext
/api/users/0/items/<attachmentKey>/file/view/url
```

## 只读 Connector 路由

Zotero Connector 与本地 API 共用端口。Get Zotero 仅使用下列非修改性路由读取当前界面选择：

Useful routes:

```text
POST /connector/getSelectedCollection
```

其余 Connector 写入路由不属于 Get Zotero 接口。
