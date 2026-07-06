import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi.testclient import TestClient
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVER_ROOT = PROJECT_ROOT / "server"

if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from core import ProjectConfig  # noqa: E402


ProjectConfig.PROJECT_ROOT = str(PROJECT_ROOT)
load_dotenv(PROJECT_ROOT / ".env", override=False)

from routes.app import app  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)
