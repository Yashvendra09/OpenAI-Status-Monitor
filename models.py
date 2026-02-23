from dataclasses import dataclass


@dataclass(frozen=True)
class IncidentEvent:
    provider: str
    incident_id: str
    title: str
    status: str
    message: str
    updated_at: str