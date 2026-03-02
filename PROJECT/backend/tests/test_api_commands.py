"""
NEXUS Core API — Command Execution Tests
Validates command dispatch, history logging, and error handling.
"""
import pytest


@pytest.mark.anyio
async def test_execute_scan_todo(client):
    """POST /api/v1/command with SCAN_TODO must return SUCCESS."""
    resp = await client.post("/api/v1/command", json={"cmd": "SCAN_TODO"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "SUCCESS"
    assert "data" in data


@pytest.mark.anyio
async def test_execute_sys_info(client):
    """POST /api/v1/command with SYS_INFO must return CPU/RAM metrics."""
    resp = await client.post("/api/v1/command", json={"cmd": "SYS_INFO"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "SUCCESS"
    assert any("CPU" in item for item in data.get("data", []))


@pytest.mark.anyio
async def test_execute_unknown_command(client):
    """POST /api/v1/command with unknown command must return UNKNOWN status."""
    resp = await client.post("/api/v1/command", json={"cmd": "NONEXISTENT_CMD_XYZ"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "UNKNOWN"


@pytest.mark.anyio
async def test_execute_missing_cmd_field(client):
    """POST /api/v1/command without cmd field must return 422 validation error."""
    resp = await client.post("/api/v1/command", json={"arg": "test"})
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_command_history_after_execution(client):
    """After executing a command, /api/v1/commands/history must contain it."""
    # Execute a command first
    await client.post("/api/v1/command", json={"cmd": "SYS_CLEAN"})

    # Check history
    resp = await client.get("/api/v1/commands/history", params={"limit": 5})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # At least one entry should exist after execution
    assert len(data) >= 1


@pytest.mark.anyio
async def test_command_history_limit(client):
    """History limit parameter must be respected."""
    resp = await client.get("/api/v1/commands/history", params={"limit": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) <= 1
