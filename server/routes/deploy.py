import os

from fastapi import BackgroundTasks, Depends, Header, HTTPException, status
from fastapi.routing import APIRouter
from pydantic import BaseModel

from routes.dependencies import ensure_admin_user
from scripts.db import AuthorizedHandler
from scripts.filesystem import TemplateDeployHandler


DEPLOY_ROUTER = APIRouter(prefix="/deploy/templates", tags=["template-deploy"])


class NoticeDeployRequest(BaseModel):
    folder: str
    artifact_url: str


class RetryDeployRequest(BaseModel):
    id: str


def _check_deploy_token(authorization: str) -> None:
    scheme, _, token = authorization.partition(" ")
    expected = os.environ.get("DEPLOY_NOTICE_TOKEN", "").strip()
    if scheme.lower() != "bearer" or not token.strip() or not expected or token.strip() != expected:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid deployment token.",
        )


def _model_to_dict(model: BaseModel) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


@DEPLOY_ROUTER.post("/notice")
async def api_notice_template_deploy(
    request: NoticeDeployRequest,
    background_tasks: BackgroundTasks,
    authorization: str = Header(""),
):
    _check_deploy_token(authorization)
    record = TemplateDeployHandler.create_record(_model_to_dict(request))
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
