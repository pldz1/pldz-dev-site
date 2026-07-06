import os
import shutil

from fastapi import BackgroundTasks, Depends, File, Form, Header, HTTPException, Query, UploadFile, status
from fastapi.routing import APIRouter
from pydantic import BaseModel

from routes.dependencies import ensure_admin_user
from scripts.db import AuthorizedHandler
from scripts.filesystem import TemplateDeployHandler
from scripts.security import GitHubOidcVerifier


DEPLOY_ROUTER = APIRouter(prefix="/deploy/templates", tags=["template-deploy"])
DEFAULT_MAX_UPLOAD_BYTES = 100 * 1024 * 1024


def _check_deploy_token(deploy_token: str) -> None:
    expected = os.environ.get("DEPLOY_NOTICE_TOKEN", "").strip()
    if not expected or deploy_token != expected:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid deployment token.",
        )


def _extract_bearer_token(authorization: str) -> str:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing GitHub OIDC bearer token.",
        )
    return token.strip()


def _verify_oidc_request(authorization: str, repo: str, sha: str, ref: str, run_id: str, run_attempt: str) -> dict:
    try:
        claims = GitHubOidcVerifier.verify(_extract_bearer_token(authorization))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid GitHub OIDC token: {exc}",
        )

    expected = {
        "repository": repo,
        "sha": sha,
        "ref": ref,
    }
    for claim_name, expected_value in expected.items():
        if claims.get(claim_name) != expected_value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"OIDC claim '{claim_name}' does not match request metadata.",
            )

    optional_expected = {
        "run_id": run_id,
        "run_attempt": run_attempt,
    }
    for claim_name, expected_value in optional_expected.items():
        claim_value = claims.get(claim_name)
        if claim_value is not None and str(claim_value) != str(expected_value):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"OIDC claim '{claim_name}' does not match request metadata.",
            )

    return claims


def _max_upload_bytes() -> int:
    raw_value = os.environ.get("DEPLOY_MAX_UPLOAD_BYTES", "").strip()
    if not raw_value:
        return DEFAULT_MAX_UPLOAD_BYTES
    try:
        return max(1, int(raw_value))
    except ValueError:
        return DEFAULT_MAX_UPLOAD_BYTES


@DEPLOY_ROUTER.get("/notice")
async def api_notice_template_deploy(
    background_tasks: BackgroundTasks,
    repo: str = Query(...),
    sha: str = Query(...),
    ref: str = Query(...),
    run_id: str = Query(...),
    run_attempt: str = Query(...),
    artifact_name: str = Query(...),
    artifact_url: str = Query(...),
    deploy_token: str = Query(""),
):
    _check_deploy_token(deploy_token)
    record = TemplateDeployHandler.create_record({
        "repo": repo,
        "sha": sha,
        "ref": ref,
        "run_id": run_id,
        "run_attempt": run_attempt,
        "artifact_name": artifact_name,
        "artifact_url": artifact_url,
    })
    background_tasks.add_task(TemplateDeployHandler.run_deploy, record["id"])
    return {"data": {"id": record["id"], "status": record["status"]}}


@DEPLOY_ROUTER.post("/upload")
async def api_upload_template_deploy(
    background_tasks: BackgroundTasks,
    repo: str = Form(...),
    sha: str = Form(...),
    ref: str = Form(...),
    run_id: str = Form(...),
    run_attempt: str = Form(...),
    artifact_name: str = Form(...),
    file: UploadFile = File(...),
    authorization: str = Header(""),
):
    claims = _verify_oidc_request(authorization, repo, sha, ref, run_id, run_attempt)
    record = TemplateDeployHandler.create_record({
        "repo": repo,
        "sha": sha,
        "ref": ref,
        "run_id": run_id,
        "run_attempt": run_attempt,
        "artifact_name": artifact_name,
        "artifact_url": "",
        "oidc_sub": claims.get("sub", ""),
        "workflow": claims.get("workflow", ""),
        "event_name": claims.get("event_name", ""),
        "actor": claims.get("actor", ""),
        "repository_id": str(claims.get("repository_id", "")),
    })

    artifact_path = TemplateDeployHandler.get_artifact_path(record["id"])
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    max_bytes = _max_upload_bytes()
    total_bytes = 0
    try:
        with open(artifact_path, "wb") as file_obj:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > max_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        detail="Uploaded artifact is too large.",
                    )
                file_obj.write(chunk)
    except Exception:
        shutil.rmtree(artifact_path.parent, ignore_errors=True)
        raise

    if total_bytes <= 0:
        shutil.rmtree(artifact_path.parent, ignore_errors=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded artifact is empty.",
        )

    TemplateDeployHandler.set_artifact_path(record["id"], artifact_path)
    background_tasks.add_task(TemplateDeployHandler.run_deploy, record["id"])
    return {"data": {"id": record["id"], "status": record["status"]}}


@DEPLOY_ROUTER.get("/all")
async def api_get_template_deployments(user: dict = Depends(AuthorizedHandler.get_current_user)):
    ensure_admin_user(
        user,
        login_detail="You must be logged in to access template deployments.",
        forbidden_detail="You do not have permission to access template deployments.",
    )
    return {"data": TemplateDeployHandler.list_records()}


class RetryDeployRequest(BaseModel):
    id: str


@DEPLOY_ROUTER.post("/retry")
async def api_retry_template_deployment(
    request: RetryDeployRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(AuthorizedHandler.get_current_user),
):
    ensure_admin_user(
        user,
        login_detail="You must be logged in to retry template deployments.",
        forbidden_detail="You do not have permission to retry template deployments.",
    )
    record = TemplateDeployHandler.retry_record(request.id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment record not found.",
        )
    background_tasks.add_task(TemplateDeployHandler.run_deploy, record["id"])
    return {"data": record}
