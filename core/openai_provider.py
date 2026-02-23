from typing import List
from core.provider import StatusProvider
from models import IncidentEvent
from config import OPENAI_STATUS_SUMMARY_URL


class OpenAIStatusProvider(StatusProvider):
    """
    Provider for OpenAI status page (incident.io powered).
    """

    def name(self) -> str:
        return "OpenAI"

    async def fetch(self, fetcher):
        return await fetcher.fetch_json(OPENAI_STATUS_SUMMARY_URL)

    def parse(self, data) -> List[IncidentEvent]:
        if not data:
            return []

        summary = data.get("summary", {})
        events = []

        for incident in summary.get("ongoing_incidents", []):
            message = incident.get("name")

            # If detailed updates exist
            updates = incident.get("incident_updates")
            if updates:
                latest = updates[-1]
                message = latest.get("body", message)

            events.append(
                IncidentEvent(
                    provider=self.name(),
                    incident_id=incident.get("id"),
                    title=incident.get("name"),
                    status=incident.get("status"),
                    message=message,
                    updated_at=incident.get("updated_at"),
                )
            )

        return events