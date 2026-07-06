import os
import time

import jwt
from jwt import PyJWKClient


GITHUB_OIDC_ISSUER = "https://token.actions.githubusercontent.com"
GITHUB_OIDC_JWKS_URL = f"{GITHUB_OIDC_ISSUER}/.well-known/jwks"
DEFAULT_OIDC_AUDIENCE = "pldz-dev-site-deploy"
DEFAULT_JWKS_CACHE_SECONDS = 600


class GitHubOidcVerifier:
    _jwk_client = None
    _jwk_client_created_at = 0

    @classmethod
    def verify(cls, token: str) -> dict:
        audience = os.environ.get("DEPLOY_OIDC_AUDIENCE", DEFAULT_OIDC_AUDIENCE).strip()
        if not audience:
            raise ValueError("DEPLOY_OIDC_AUDIENCE must be configured.")

        signing_key = cls._get_jwk_client().get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=audience,
            issuer=GITHUB_OIDC_ISSUER,
        )
        cls._validate_claim_policy(claims)
        return claims

    @classmethod
    def _get_jwk_client(cls) -> PyJWKClient:
        now = time.time()
        if (
            cls._jwk_client is None
            or now - cls._jwk_client_created_at > DEFAULT_JWKS_CACHE_SECONDS
        ):
            cls._jwk_client = PyJWKClient(GITHUB_OIDC_JWKS_URL)
            cls._jwk_client_created_at = now
        return cls._jwk_client

    @classmethod
    def _validate_claim_policy(cls, claims: dict) -> None:
        allowed_owner = os.environ.get("DEPLOY_ALLOWED_OWNER", "").strip()
        if allowed_owner and claims.get("repository_owner") != allowed_owner:
            raise ValueError("OIDC repository owner is not allowed.")

        allowed_refs = cls._split_env("DEPLOY_ALLOWED_REFS")
        if allowed_refs and claims.get("ref") not in allowed_refs:
            raise ValueError("OIDC ref is not allowed.")

        allowed_workflows = cls._split_env("DEPLOY_ALLOWED_WORKFLOWS")
        if allowed_workflows and claims.get("workflow") not in allowed_workflows:
            raise ValueError("OIDC workflow is not allowed.")

        allowed_events = cls._split_env("DEPLOY_ALLOWED_EVENTS") or ["push"]
        if claims.get("event_name") not in allowed_events:
            raise ValueError("OIDC event is not allowed.")

    @classmethod
    def _split_env(cls, name: str) -> list[str]:
        value = os.environ.get(name, "")
        return [item.strip() for item in value.split(",") if item.strip()]
