from core.provider import StatusProvider
from models import IncidentEvent


class TestProvider(StatusProvider):
    def __init__(self):
        self.counter = 0

    def name(self):
        return "TestProvider"

    async def fetch(self, fetcher):
        return {}

    def parse(self, data):
        self.counter += 1

        if self.counter == 1:
            return [
                IncidentEvent(
                    provider=self.name(),
                    incident_id="TEST1",
                    title="Chat Completions",
                    status="investigating",
                    message="Initial degradation detected",
                    updated_at="2026-02-24T00:00:00Z",
                )
            ]

        elif self.counter == 2:
            return [
                IncidentEvent(
                    provider=self.name(),
                    incident_id="TEST1",
                    title="Chat Completions",
                    status="resolved",
                    message="Issue resolved",
                    updated_at="2026-02-24T00:05:00Z",
                )
            ]

        return []