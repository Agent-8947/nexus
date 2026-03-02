"""
NEXUS Core API — Health & Status Tests
Validates that critical endpoints respond correctly.
"""
import pytest


@pytest.mark.anyio
async def test_root_endpoint(client):
    """GET / must return API identity and version."""
    resp = await client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "nexus" in data.get("engine", "").lower()
    assert "uptime_seconds" in data


@pytest.mark.anyio
async def test_health_check(client):
    """GET /health must return healthy status and DB health."""
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "healthy"
    assert "database" in data


@pytest.mark.anyio
async def test_metrics_endpoint(client):
    """GET /api/v1/metrics must return valid metrics structure."""
    resp = await client.get("/api/v1/metrics")
    assert resp.status_code == 200
    data = resp.json()
    # Metrics may come from pipe server or be empty — both are valid
    assert isinstance(data, dict)


@pytest.mark.anyio
async def test_available_commands(client):
    """GET /api/v1/commands/available must list dispatcher commands."""
    resp = await client.get("/api/v1/commands/available")
    assert resp.status_code == 200
    data = resp.json()
    assert "built_in" in data
    built_in = data["built_in"]
    # Core commands must always be present
    assert "SCAN_TODO" in built_in
    assert "SYS_INFO" in built_in
    assert "SYS_CLEAN" in built_in
