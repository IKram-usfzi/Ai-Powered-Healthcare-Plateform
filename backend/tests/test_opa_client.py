import httpx

from app.core.opa_client import OPAClient


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("error", request=None, response=self)

    def json(self) -> dict:
        return self._payload


def test_allow_role_true_when_opa_allows(monkeypatch):
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _FakeResponse(200, {"result": True}))
    client = OPAClient("http://opa:8181")
    assert client.allow_role("administrator", ["administrator"]) is True


def test_allow_role_false_when_opa_denies(monkeypatch):
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _FakeResponse(200, {"result": False}))
    client = OPAClient("http://opa:8181")
    assert client.allow_role("patient", ["administrator"]) is False


def test_allow_role_fails_closed_on_connection_error(monkeypatch):
    def _raise(*args, **kwargs):
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(httpx, "post", _raise)
    client = OPAClient("http://opa:8181")
    assert client.allow_role("administrator", ["administrator"]) is False


def test_allow_role_fails_closed_on_non_2xx(monkeypatch):
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _FakeResponse(500, {}))
    client = OPAClient("http://opa:8181")
    assert client.allow_role("administrator", ["administrator"]) is False


def test_allow_role_fails_closed_on_missing_result_key(monkeypatch):
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _FakeResponse(200, {}))
    client = OPAClient("http://opa:8181")
    assert client.allow_role("administrator", ["administrator"]) is False
