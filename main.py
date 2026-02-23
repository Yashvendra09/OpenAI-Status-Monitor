import asyncio
import logging

from core.fetcher import HTTPFetcher
from core.openai_provider import OpenAIStatusProvider
from config import POLL_INTERVAL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def monitor():
    logger.info("Monitor started")

    fetcher = HTTPFetcher()

    # 🔁 Switch provider here for testing if needed
    providers = [
        OpenAIStatusProvider(),
    ]

    seen_events = set()

    while True:

        # Fetch all providers concurrently
        tasks = [provider.fetch(fetcher) for provider in providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for provider, data in zip(providers, results):

            if isinstance(data, Exception):
                logger.error(f"{provider.name()} error: {data}")
                continue

            events = provider.parse(data)

            for event in events:
                unique_key = (
                    f"{event.provider}-"
                    f"{event.incident_id}-"
                    f"{event.status}-"
                    f"{event.message}"
                )

                if unique_key not in seen_events:
                    seen_events.add(unique_key)

                    logger.info(
                        f"New Event | Provider={event.provider} | "
                        f"Product={event.title} | "
                        f"Status={event.status} | "
                        f"Message={event.message}"
                    )

        await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(monitor())