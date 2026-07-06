import json
import zipfile
from pathlib import Path


def _write_livedemo(root: Path, folder: str = "demo") -> None:
    config_dir = root / "data" / "resources" / "website"
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "livedemo.json", "w", encoding="utf-8") as file_obj:
        json.dump(
            {
                "data": [
                    {
                        "folder": folder,
                        "sourcelink": "https://github.com/acme/demo",
                    }
                ]
            },
            file_obj,
        )


def _write_zip(path: Path, files: dict[str, str]) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)


def _setup_project(monkeypatch, tmp_path: Path):
    from core import ProjectConfig

    monkeypatch.setattr(ProjectConfig, "PROJECT_ROOT", str(tmp_path))
    monkeypatch.setenv("DEPLOY_NOTICE_TOKEN", "secret")
    _write_livedemo(tmp_path)
    (tmp_path / "data" / "db").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data" / "cache").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data" / "templates").mkdir(parents=True, exist_ok=True)


def _notice_params(artifact_url: str, token: str = "secret") -> dict:
    return {
        "repo": "acme/demo",
        "sha": "1234567890abcdef",
        "ref": "main",
        "run_id": "1",
        "run_attempt": "1",
        "artifact_name": "site",
        "artifact_url": artifact_url,
        "deploy_token": token,
    }


def _upload_data() -> dict:
    return {
        "repo": "acme/demo",
        "sha": "1234567890abcdef",
        "ref": "refs/heads/main",
        "run_id": "1",
        "run_attempt": "1",
        "artifact_name": "site",
    }


def _oidc_claims(**overrides) -> dict:
    claims = {
        "sub": "repo:acme/demo:ref:refs/heads/main",
        "repository": "acme/demo",
        "repository_owner": "acme",
        "repository_id": "123",
        "sha": "1234567890abcdef",
        "ref": "refs/heads/main",
        "run_id": "1",
        "run_attempt": "1",
        "workflow": "deploy",
        "event_name": "push",
        "actor": "octocat",
    }
    claims.update(overrides)
    return claims


def _records(tmp_path: Path) -> list[dict]:
    with open(tmp_path / "data" / "db" / "template_deployments.json", "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def test_template_deploy_notice_rejects_missing_or_wrong_token(client, monkeypatch, tmp_path):
    _setup_project(monkeypatch, tmp_path)
    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"index.html": "hello"})

    missing = _notice_params(zip_path.as_uri())
    missing.pop("deploy_token")
    assert client.get("/api/v1/deploy/templates/notice", params=missing).status_code == 403

    wrong = _notice_params(zip_path.as_uri(), token="bad")
    assert client.get("/api/v1/deploy/templates/notice", params=wrong).status_code == 403


def test_template_deploy_upload_with_oidc_success(client, monkeypatch, tmp_path):
    from routes import deploy

    _setup_project(monkeypatch, tmp_path)
    target = tmp_path / "data" / "templates" / "demo"
    target.mkdir(parents=True)
    (target / "index.html").write_text("old", encoding="utf-8")
    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"index.html": "new"})
    monkeypatch.setattr(deploy.GitHubOidcVerifier, "verify", lambda token: _oidc_claims())

    with open(zip_path, "rb") as file_obj:
        response = client.post(
            "/api/v1/deploy/templates/upload",
            data=_upload_data(),
            files={"file": ("site.zip", file_obj, "application/zip")},
            headers={"Authorization": "Bearer oidc-token"},
        )

    assert response.status_code == 200
    assert (target / "index.html").read_text(encoding="utf-8") == "new"
    record = _records(tmp_path)[-1]
    assert record["status"] == "success"
    assert record["artifact_path"]
    assert record["oidc_sub"] == "repo:acme/demo:ref:refs/heads/main"
    assert record["workflow"] == "deploy"


def test_template_deploy_upload_rejects_oidc_metadata_mismatch(client, monkeypatch, tmp_path):
    from routes import deploy

    _setup_project(monkeypatch, tmp_path)
    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"index.html": "new"})
    monkeypatch.setattr(deploy.GitHubOidcVerifier, "verify", lambda token: _oidc_claims(repository="evil/demo"))

    with open(zip_path, "rb") as file_obj:
        response = client.post(
            "/api/v1/deploy/templates/upload",
            data=_upload_data(),
            files={"file": ("site.zip", file_obj, "application/zip")},
            headers={"Authorization": "Bearer oidc-token"},
        )

    assert response.status_code == 403
    assert "repository" in response.json()["detail"]


def test_template_deploy_upload_rejects_large_file(client, monkeypatch, tmp_path):
    from routes import deploy

    _setup_project(monkeypatch, tmp_path)
    monkeypatch.setenv("DEPLOY_MAX_UPLOAD_BYTES", "4")
    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"index.html": "new"})
    monkeypatch.setattr(deploy.GitHubOidcVerifier, "verify", lambda token: _oidc_claims())

    with open(zip_path, "rb") as file_obj:
        response = client.post(
            "/api/v1/deploy/templates/upload",
            data=_upload_data(),
            files={"file": ("site.zip", file_obj, "application/zip")},
            headers={"Authorization": "Bearer oidc-token"},
        )

    assert response.status_code == 413


def test_template_deploy_success_replaces_target_and_creates_backup(client, monkeypatch, tmp_path):
    _setup_project(monkeypatch, tmp_path)
    target = tmp_path / "data" / "templates" / "demo"
    target.mkdir(parents=True)
    (target / "index.html").write_text("old", encoding="utf-8")

    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"dist/index.html": "new", "dist/app.js": "console.log(1)"})

    response = client.get("/api/v1/deploy/templates/notice", params=_notice_params(zip_path.as_uri()))

    assert response.status_code == 200
    assert (target / "index.html").read_text(encoding="utf-8") == "new"
    assert (target / "app.js").is_file()
    backups = list((tmp_path / "data" / "templates" / ".backups").glob("demo-*"))
    assert backups
    records = _records(tmp_path)
    assert records[-1]["status"] == "success"
    assert records[-1]["folder"] == "demo"


def test_template_deploy_unknown_repo_records_failure(client, monkeypatch, tmp_path):
    _setup_project(monkeypatch, tmp_path)
    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"index.html": "hello"})
    params = _notice_params(zip_path.as_uri())
    params["repo"] = "acme/unknown"

    response = client.get("/api/v1/deploy/templates/notice", params=params)

    assert response.status_code == 200
    record = _records(tmp_path)[-1]
    assert record["status"] == "failed"
    assert "does not match" in record["error"]


def test_template_deploy_rejects_unsafe_folder(client, monkeypatch, tmp_path):
    _setup_project(monkeypatch, tmp_path)
    _write_livedemo(tmp_path, folder="../bad")
    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"index.html": "hello"})

    response = client.get("/api/v1/deploy/templates/notice", params=_notice_params(zip_path.as_uri()))

    assert response.status_code == 200
    record = _records(tmp_path)[-1]
    assert record["status"] == "failed"
    assert "safe template folder" in record["error"]


def test_template_deploy_rejects_zip_path_traversal(client, monkeypatch, tmp_path):
    _setup_project(monkeypatch, tmp_path)
    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"../index.html": "bad"})

    response = client.get("/api/v1/deploy/templates/notice", params=_notice_params(zip_path.as_uri()))

    assert response.status_code == 200
    record = _records(tmp_path)[-1]
    assert record["status"] == "failed"
    assert "unsafe path" in record["error"]


def test_template_deploy_rejects_missing_index(client, monkeypatch, tmp_path):
    _setup_project(monkeypatch, tmp_path)
    zip_path = tmp_path / "site.zip"
    _write_zip(zip_path, {"app.js": "console.log(1)"})

    response = client.get("/api/v1/deploy/templates/notice", params=_notice_params(zip_path.as_uri()))

    assert response.status_code == 200
    record = _records(tmp_path)[-1]
    assert record["status"] == "failed"
    assert "index.html" in record["error"]


def test_template_deploy_retry_creates_new_record(monkeypatch, tmp_path):
    from core import ProjectConfig
    from scripts.filesystem import TemplateDeployHandler

    monkeypatch.setattr(ProjectConfig, "PROJECT_ROOT", str(tmp_path))
    (tmp_path / "data" / "db").mkdir(parents=True, exist_ok=True)

    original = TemplateDeployHandler.create_record({
        "repo": "acme/demo",
        "sha": "123",
        "ref": "main",
        "run_id": "1",
        "run_attempt": "1",
        "artifact_name": "site",
        "artifact_url": "file:///tmp/site.zip",
        "folder": "demo",
    })

    retry = TemplateDeployHandler.retry_record(original["id"])

    assert retry["id"] != original["id"]
    assert retry["artifact_url"] == original["artifact_url"]
    assert retry["folder"] == "demo"
