"""
NEXUS Core API — State & Memory Tests
Validates key-value state management and fault registry endpoints.
"""
import pytest
import time


@pytest.mark.anyio
async def test_get_state(client):
    """GET /api/v1/state must return a dict."""
    resp = await client.get("/api/v1/state")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


@pytest.mark.anyio
async def test_set_and_get_state(client):
    """PUT /api/v1/state must persist a key-value pair."""
    test_key = f"test_key_{int(time.time())}"
    test_value = "nexus_test_value"

    # Set state
    resp = await client.put("/api/v1/state", json={"key": test_key, "value": test_value})
    assert resp.status_code == 200

    # Read state back
    resp = await client.get("/api/v1/state")
    assert resp.status_code == 200
    state = resp.json()
    assert state.get(test_key) == test_value


@pytest.mark.anyio
async def test_get_faults(client):
    """GET /api/v1/faults must return the fault registry as a list."""
    resp = await client.get("/api/v1/faults")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # At least the initial placeholder entry
    if len(data) > 0:
        assert "id" in data[0]
        assert "fault_type" in data[0]


@pytest.mark.anyio
async def test_get_assets(client):
    """GET /api/v1/assets must return list of output files."""
    resp = await client.get("/api/v1/assets")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # outputs/ directory has 25+ files, should return some
    assert len(data) > 0
