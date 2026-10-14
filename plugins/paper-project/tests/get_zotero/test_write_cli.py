"""Exercise write commands at the CLI/HTTP boundary, without a live library."""

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
from urllib.error import HTTPError

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "skills/get-zotero/scripts"
sys.path.insert(0, str(SCRIPTS))
import zotero
from runtime_config import Endpoint, RuntimeConfig


@pytest.fixture(autouse=True)
def isolate_authorization_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("GET_ZOTERO_AUTH_DIR", str(tmp_path / "auth"))


class Reply:
    def __init__(self, body=None, status=200, headers=None):
        self.body = json.dumps(body).encode() if body is not None else b""
        self.status = status
        self.headers = {
            "Content-Type": "application/json",
            "Zotero-Server-ID": "test-instance",
            **(headers or {}),
        }

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self):
        return self.body


class Library:
    def __init__(self):
        self.objects = {
            "/api/users/0/items/ABCD2345": {
                "key": "ABCD2345",
                "version": 4,
                "data": {
                    "itemType": "journalArticle",
                    "title": "Original",
                    "tags": [{"tag": "keep"}],
                    "collections": ["BCDE3456"],
                },
            }
        }
        self.calls = []

    def open(self, request, timeout):
        from urllib.parse import urlsplit

        path = urlsplit(request.full_url).path
        self.calls.append((request.method, path, request))
        if path == "/api/":
            return Reply("not necessarily JSON")
        if path == "/api/local/authorize":
            return Reply({"key": "secret-runtime-key", "remember": True})
        if request.method == "GET":
            if path not in self.objects:
                raise HTTPError(request.full_url, 404, "missing", {}, io.BytesIO())
            return Reply(self.objects[path])
        assert request.get_header("Zotero-server-id") == "test-instance"
        assert request.get_header("Zotero-api-key") == "secret-runtime-key"
        current = self.objects[path]
        assert request.get_header("If-unmodified-since-version") == str(
            current["version"]
        )
        current["data"].update(json.loads(request.data))
        current["version"] += 1
        return Reply(status=204)


def cli(library, argv):
    args = zotero.build_parser().parse_args(argv)
    config = RuntimeConfig(
        mode="native",
        host=None,
        port=23119,
        timeout_seconds=5,
        path_mappings=(),
        sources={},
    )
    client = zotero.ZoteroClient(
        config,
        (Endpoint("http://127.0.0.1:23119", "127.0.0.1:23119", "test"),),
        opener=library.open,
    )
    output = io.StringIO()
    with redirect_stdout(output):
        args.func(args, client)
    return json.loads(output.getvalue())


def prepare(tmp_path, library, operations=None):
    request = tmp_path / "request.json"
    request.write_text(
        json.dumps(
            {
                "operations": operations
                or [
                    {
                        "action": "update",
                        "resource": "items",
                        "key": "ABCD2345",
                        "set": {"title": "Corrected"},
                        "add_tags": ["new"],
                    }
                ]
            }
        )
    )
    plan = tmp_path / "plan.json"
    result = cli(library, ["write-plan", str(request), "--out", str(plan)])
    return plan, result


def test_preview_is_read_only_and_apply_preserves_fields_and_verifies(tmp_path):
    library = Library()
    plan, preview = prepare(tmp_path, library)
    assert all(method == "GET" for method, _, _ in library.calls)
    assert preview["operations"][0]["after"]["tags"] == [
        {"tag": "keep"},
        {"tag": "new"},
    ]
    report = cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert report["results"][0]["status"] == "verified"
    data = library.objects["/api/users/0/items/ABCD2345"]["data"]
    assert data["title"] == "Corrected"
    assert data["collections"] == ["BCDE3456"]
    assert "secret-runtime-key" not in json.dumps(report) + plan.read_text()


def test_tampered_or_unapproved_plan_never_requests_runtime_authorization(tmp_path):
    library = Library()
    plan, preview = prepare(tmp_path, library)
    for approval in ("wrong-digest",):
        with pytest.raises(ValueError, match="digest"):
            cli(library, ["write-apply", str(plan), "--approve", approval])
    payload = json.loads(plan.read_text())
    payload["operations"][0]["after"]["title"] = "unapproved change"
    plan.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="digest"):
        cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert not any(method != "GET" for method, _, _ in library.calls)


def test_conflicting_target_is_reported_and_other_approved_item_continues(tmp_path):
    from copy import deepcopy

    library = Library()
    second = deepcopy(library.objects["/api/users/0/items/ABCD2345"])
    second["key"] = "BCDE3456"
    library.objects["/api/users/0/items/BCDE3456"] = second
    operations = [
        {"action": "update", "key": k, "set": {"title": "Corrected"}}
        for k in ("ABCD2345", "BCDE3456")
    ]
    plan, preview = prepare(tmp_path, library, operations)
    library.objects["/api/users/0/items/ABCD2345"]["data"]["title"] = "Edited by user"
    args = zotero.build_parser().parse_args(
        ["write-apply", str(plan), "--approve", preview["digest"]]
    )
    config = RuntimeConfig(
        mode="native",
        host=None,
        port=23119,
        timeout_seconds=5,
        path_mappings=(),
        sources={},
    )
    client = zotero.ZoteroClient(
        config,
        (Endpoint("http://127.0.0.1:23119", "127.0.0.1:23119", "test"),),
        opener=library.open,
    )
    output = io.StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as error:
        args.func(args, client)
    assert error.value.code == 1
    report = json.loads(output.getvalue())
    assert [r["status"] for r in report["results"]] == ["failed", "verified"]
    assert "new authorization" in report["results"][0]["message"]


def test_reapplying_verified_plan_is_read_only(tmp_path):
    library = Library()
    plan, preview = prepare(tmp_path, library)
    cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    library.calls.clear()
    report = cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert report["results"][0]["status"] == "already-applied"
    assert all(method == "GET" for method, _, _ in library.calls)


def test_trash_requires_separate_approval_and_uses_soft_delete(tmp_path):
    library = Library()
    plan, preview = prepare(tmp_path, library, [{"action": "trash", "key": "ABCD2345"}])
    with pytest.raises(ValueError, match="separate"):
        cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert all(method == "GET" for method, _, _ in library.calls)
    report = cli(
        library,
        [
            "write-apply",
            str(plan),
            "--approve",
            preview["digest"],
            "--approve-destructive",
            preview["digest"],
        ],
    )
    assert report["ok"]
    assert library.objects["/api/users/0/items/ABCD2345"]["data"]["deleted"] == 1
    assert not any(method == "DELETE" for method, _, _ in library.calls)


def test_unrelated_field_changes_are_preserved(tmp_path):
    library = Library()
    plan, preview = prepare(tmp_path, library)
    library.objects["/api/users/0/items/ABCD2345"]["data"][
        "abstractNote"
    ] = "User addition"
    library.objects["/api/users/0/items/ABCD2345"]["version"] = 7
    report = cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert report["ok"]
    assert (
        library.objects["/api/users/0/items/ABCD2345"]["data"]["abstractNote"]
        == "User addition"
    )


class ExtendedLibrary(Library):
    def __init__(self):
        super().__init__()
        self.revision = 4
        self.index = None

    def open(self, request, timeout):
        from urllib.parse import urlsplit, parse_qs

        url = urlsplit(request.full_url)
        path = url.path
        if path == "/api/items/new":
            item_type = parse_qs(url.query)["itemType"][0]
            return Reply(
                {
                    "itemType": item_type,
                    "title": "",
                    "tags": [],
                    "relations": {},
                    **(
                        {"note": "", "parentItem": False}
                        if item_type == "note"
                        else {"collections": []}
                    ),
                }
            )
        if path == "/api/users/0/items" and request.method == "GET":
            return Reply(
                list(self.objects.values()),
                headers={"Last-Modified-Version": str(self.revision)},
            )
        if request.method == "POST" and path in {
            "/api/users/0/items",
            "/api/users/0/collections",
            "/api/users/0/searches",
        }:
            self.calls.append((request.method, path, request))
            data = json.loads(request.data)[0]
            if path + "/" + data["key"] not in self.objects:
                assert data["version"] == 0
            object_path = path + "/" + data["key"]
            old = self.objects.get(object_path, {"data": {}})
            old["data"].update(data)
            self.revision += 1
            self.objects[object_path] = {
                "key": data["key"],
                "version": self.revision,
                "data": old["data"],
            }
            return Reply(
                {"successful": {"0": self.objects[object_path]}},
                headers={"Last-Modified-Version": str(self.revision)},
            )
        if request.method == "DELETE":
            self.calls.append((request.method, path, request))
            assert request.get_header("If-unmodified-since-version") == str(
                self.revision
            )
            object_key = next(iter(parse_qs(url.query).values()))[0]
            del self.objects[path + "/" + object_key]
            self.revision += 1
            return Reply(
                status=204, headers={"Last-Modified-Version": str(self.revision)}
            )
        if (
            path.endswith("/children")
            or "/collections/" in path
            and path.endswith("/items")
        ):
            return Reply([])
        if path == "/api/users/0/fulltext" and request.method == "POST":
            self.calls.append((request.method, path, request))
            assert request.get_header("If-unmodified-since-version") == str(
                self.revision
            )
            self.index = {
                k: v for k, v in json.loads(request.data)[0].items() if k != "key"
            }
            return Reply({"successful": {"0": "ABCD2345"}})
        if path.endswith("/fulltext"):
            self.calls.append((request.method, path, request))
            if request.method == "GET":
                return Reply(self.index) if self.index else self.missing(request)
            self.index = json.loads(request.data)
            return Reply(status=204)
        return super().open(request, timeout)

    def missing(self, request):
        raise HTTPError(request.full_url, 404, "missing", {}, io.BytesIO())


@pytest.mark.parametrize(
    "resource,data",
    [
        (
            "items",
            {
                "itemType": "note",
                "note": "<p>Reading note</p>",
                "parentItem": "ABCD2345",
            },
        ),
        ("collections", {"name": "Research", "parentCollection": False}),
        (
            "searches",
            {
                "name": "Title search",
                "conditions": [
                    {"condition": "title", "operator": "contains", "value": "Research"}
                ],
            },
        ),
    ],
)
def test_create_verify_and_permanently_delete_explicit_objects(
    tmp_path, resource, data
):
    library = ExtendedLibrary()
    plan, preview = prepare(
        tmp_path,
        library,
        [{"action": "create", "resource": resource, "key": "CDEF4567", "data": data}],
    )
    report = cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert report["ok"]
    if resource == "collections":
        library.objects["/api/users/0/collections"] = []
    plan, preview = prepare(
        tmp_path,
        library,
        [{"action": "delete", "resource": resource, "key": "CDEF4567"}],
    )
    report = cli(
        library,
        [
            "write-apply",
            str(plan),
            "--approve",
            preview["digest"],
            "--approve-destructive",
            preview["digest"],
        ],
    )
    assert report["ok"]
    assert f"/api/users/0/{resource}/CDEF4567" not in library.objects


def test_fulltext_write_reads_back_content(tmp_path):
    library = ExtendedLibrary()
    library.objects["/api/users/0/items/ABCD2345"]["data"].update(
        itemType="attachment", contentType="application/pdf"
    )
    plan, preview = prepare(
        tmp_path,
        library,
        [
            {
                "action": "fulltext",
                "key": "ABCD2345",
                "data": {
                    "content": "Verified text",
                    "indexedPages": 1,
                    "totalPages": 1,
                },
            }
        ],
    )
    report = cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert report["ok"]
    assert library.index["content"] == "Verified text"


def test_codex_remembered_grant_is_shared_across_cli_processes(tmp_path):
    library = Library()
    plan, preview = prepare(tmp_path, library)
    cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    library.calls.clear()
    plan, preview = prepare(
        tmp_path,
        library,
        [
            {
                "action": "update",
                "key": "ABCD2345",
                "set": {"title": "Second authorized edit"},
            }
        ],
    )
    cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert not any(path == "/api/local/authorize" for _, path, _ in library.calls)
    auth_file = next((tmp_path / "auth").glob("*.json"))
    assert auth_file.stat().st_mode & 0o077 == 0
    assert json.loads(auth_file.read_text())["app_name"] == "Codex"


def test_create_uses_local_schema_when_template_route_is_unavailable(tmp_path):
    class SchemaLibrary(ExtendedLibrary):
        def open(self, request, timeout):
            from urllib.parse import urlsplit

            path = urlsplit(request.full_url).path
            if path == "/api/items/new":
                return self.missing(request)
            if path == "/api/itemTypeFields":
                return Reply([{"field": "title"}])
            return super().open(request, timeout)

    library = SchemaLibrary()
    plan, preview = prepare(
        tmp_path,
        library,
        [
            {
                "action": "create",
                "data": {"itemType": "journalArticle", "title": "Schema-created"},
            }
        ],
    )
    report = cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert report["ok"]


def test_fulltext_write_uses_atomic_library_precondition(tmp_path):
    class FulltextLibrary(ExtendedLibrary):
        def open(self, request, timeout):
            from urllib.parse import urlsplit

            path = urlsplit(request.full_url).path
            if path == "/api/users/0/fulltext" and request.method == "POST":
                self.calls.append((request.method, path, request))
                assert request.get_header("If-unmodified-since-version") == str(
                    self.revision
                )
                self.index = {
                    k: v for k, v in json.loads(request.data)[0].items() if k != "key"
                }
                return Reply({"successful": {"0": "ABCD2345"}})
            return super().open(request, timeout)

    library = FulltextLibrary()
    library.objects["/api/users/0/items/ABCD2345"]["data"]["itemType"] = "attachment"
    plan, preview = prepare(
        tmp_path,
        library,
        [
            {
                "action": "fulltext",
                "key": "ABCD2345",
                "data": {"content": "Frozen index", "indexedPages": 1, "totalPages": 1},
            }
        ],
    )
    report = cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert report["ok"]
    assert any(
        path == "/api/users/0/fulltext" and method == "POST"
        for method, path, _ in library.calls
    )


class UploadLibrary(ExtendedLibrary):
    def __init__(self):
        super().__init__()
        self.objects["/api/users/0/items/ABCD2345"]["data"].update(
            itemType="attachment", linkMode="imported_file", md5=None
        )
        self.uploaded = None
        self.registration = None

    def open(self, request, timeout):
        from urllib.parse import urlsplit, parse_qs

        path = urlsplit(request.full_url).path
        if path == "/api/local/uploads/abc123":
            self.calls.append((request.method, path, request))
            self.uploaded = request.data
            return Reply(status=201)
        if path.endswith("/file") and request.method == "POST":
            self.calls.append((request.method, path, request))
            data = parse_qs(request.data.decode())
            assert request.get_header("If-none-match") == "*"
            if "upload" in data:
                import hashlib

                assert (
                    hashlib.md5(self.uploaded).hexdigest()
                    == self.registration["md5"][0]
                )
                self.objects["/api/users/0/items/ABCD2345"]["data"]["md5"] = (
                    self.registration["md5"][0]
                )
                return Reply(status=204)
            self.registration = data
            return Reply(
                {
                    "url": "http://127.0.0.1:23119/api/local/uploads/abc123",
                    "uploadKey": "abc123",
                    "contentType": "application/octet-stream",
                }
            )
        return super().open(request, timeout)


def test_upload_freezes_source_and_verifies_committed_file_hash(tmp_path):
    library = UploadLibrary()
    source = tmp_path / "source.pdf"
    source.write_bytes(b"%PDF-test original")
    plan, preview = prepare(
        tmp_path,
        library,
        [{"action": "upload", "key": "ABCD2345", "file": str(source)}],
    )
    source.write_bytes(b"%PDF-unapproved replacement")
    with pytest.raises(SystemExit):
        cli(
            library,
            [
                "write-apply",
                str(plan),
                "--approve",
                preview["digest"],
                "--approve-destructive",
                preview["digest"],
            ],
        )
    assert library.uploaded is None
    assert not any(path == "/api/local/authorize" for _, path, _ in library.calls)
    source.write_bytes(b"%PDF-test original")
    report = cli(
        library,
        [
            "write-apply",
            str(plan),
            "--approve",
            preview["digest"],
            "--approve-destructive",
            preview["digest"],
        ],
    )
    assert report["ok"] and library.uploaded == b"%PDF-test original"


def test_batch_collection_selection_is_frozen_before_apply(tmp_path):
    class SelectionLibrary(ExtendedLibrary):
        def open(self, request, timeout):
            from urllib.parse import urlsplit

            if (
                urlsplit(request.full_url).path
                == "/api/users/0/collections/BCDE3456/items/top"
            ):
                return Reply([self.objects["/api/users/0/items/ABCD2345"]])
            return super().open(request, timeout)

    library = SelectionLibrary()
    request = tmp_path / "request.json"
    request.write_text(
        json.dumps(
            {
                "selection": {"collection_key": "BCDE3456"},
                "change": {"action": "update", "add_tags": ["selected"]},
            }
        )
    )
    plan = tmp_path / "plan.json"
    preview = cli(library, ["write-plan", str(request), "--out", str(plan)])
    assert [op["key"] for op in preview["operations"]] == ["ABCD2345"]
    library.calls.clear()
    report = cli(library, ["write-apply", str(plan), "--approve", preview["digest"]])
    assert report["ok"]
    assert not any("/collections/" in path for _, path, _ in library.calls)


def test_batch_deletion_accepts_only_version_changes_from_its_own_writes(tmp_path):
    from copy import deepcopy

    library = ExtendedLibrary()
    second = deepcopy(library.objects["/api/users/0/items/ABCD2345"])
    second["key"] = "BCDE3456"
    library.objects["/api/users/0/items/BCDE3456"] = second
    plan, preview = prepare(
        tmp_path,
        library,
        [{"action": "delete", "key": k} for k in ("ABCD2345", "BCDE3456")],
    )
    report = cli(
        library,
        [
            "write-apply",
            str(plan),
            "--approve",
            preview["digest"],
            "--approve-destructive",
            preview["digest"],
        ],
    )
    assert report["ok"]
