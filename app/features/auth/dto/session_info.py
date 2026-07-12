from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SessionInfo:
    user_agent: str | None
    ip_address: str | None
    device_name: str | None