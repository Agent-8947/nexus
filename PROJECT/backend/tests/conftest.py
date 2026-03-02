"""
NEXUS Core API — Test Configuration
Shared fixtures for all backend tests.
"""
import pytest
from httpx import AsyncClient, ASGITransport

# Import the FastAPI app from the main module
import sys
from pathlib import Path

# Ensure backend is on the path
sys.path.insert(0, str(Path(__file__).parent.parent))
from httpx import AsyncClient, ASGITransport
from main import app, NexusDB, DB_PATH


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """Async HTTP client that talks directly to the FastAPI app (no network)."""
    # Manually initialize app.state if lifespan isn't running automatically in this environment
    if not hasattr(app.state, "db"):
        app.state.db = NexusDB(DB_PATH)
    if not hasattr(app.state, "start_time"):
        import time
        app.state.start_time = time.time()
        
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
def database():
    """Direct access to the NexusDB instance for state assertions."""
    # We can create a separate instance for tests or use the app's state if it's initialized
    return NexusDB(DB_PATH)
