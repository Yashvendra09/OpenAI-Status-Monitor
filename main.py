import asyncio
import logging
from fastapi import FastAPI

from core.fetcher import HTTPFetcher
from core.openai_provider import OpenAIStatusProvider
from config import POLL_INTERVAL

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

app = FastAPI()

latest_events = []
seen_events = set()


async def monitor():
    logger.info("Background monitor started")

    fetcher = HTTPFetcher()
    providers = [OpenAIStatusProvider()]

    while True:
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
                    latest_events.append({
                        "provider": event.provider,
                        "product": event.title,
                        "status": event.status,
                        "message": event.message,
                        "updated_at": event.updated_at,
                    })

                    logger.info(
                        f"New Event | Provider={event.provider} | "
                        f"Product={event.title} | "
                        f"Status={event.status}"
                    )

        await asyncio.sleep(POLL_INTERVAL)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor())


@app.get("/health")
async def health():
    return {"status": "running"}


@app.get("/latest")
async def latest():
    return {"events": latest_events[-10:]}