import httpx

from app.core.config import get_settings

settings = get_settings()


class OPAClient:
    """docs/deccission.md ADR-006/ADR-024: role-based access control is a policy
    decision delegated to OPA's Rego policies (infra/opa/policies/authz.rego),
    not re-implemented as a Python `in` check. Fails closed — any error talking
    to OPA (timeout, connection refused, non-2xx) denies the request rather than
    allowing it."""

    def __init__(self, base_url: str, timeout: float = 2.0):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def allow_role(self, role: str, allowed_roles: list[str]) -> bool:
        return self._decide(
            "globalcare/authz/allow_role",
            {"role": role, "allowed_roles": allowed_roles},
        )

    def _decide(self, policy_path: str, input_doc: dict) -> bool:
        try:
            response = httpx.post(
                f"{self._base_url}/v1/data/{policy_path}",
                json={"input": input_doc},
                timeout=self._timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError:
            return False
        return bool(response.json().get("result", False))


_opa_client = OPAClient(settings.opa_url)


def get_opa_client() -> OPAClient:
    return _opa_client
