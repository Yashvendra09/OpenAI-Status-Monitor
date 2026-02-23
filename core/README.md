
# OpenAI Status Monitor

A lightweight, asynchronous monitoring service that tracks the OpenAI Status Page and logs incident updates in real time.

Designed with scalability, efficiency, and extensibility in mind, this service can be easily adapted to monitor multiple status pages across providers.

✨ Overview

This project continuously monitors the OpenAI status API and automatically detects:

New incidents

Service degradations

Outages

Status transitions (e.g., investigating → resolved)

Message-level updates

It logs only meaningful changes, avoiding duplicate output and unnecessary processing.

The system is built to scale cleanly to 100+ providers.

🏗 Architecture

The system follows a modular, provider-agnostic architecture:

bolna-status-tracker/
│
├── main.py
├── config.py
├── models.py
│
├── core/
│   ├── fetcher.py
│   ├── provider.py
│   ├── openai_provider.py
│
└── requirements.txt
🔹 1. Provider Abstraction

All monitoring targets implement a common StatusProvider interface:

fetch() → retrieves raw provider data

parse() → transforms provider-specific payload into a unified event format

name() → identifies provider

This abstraction allows seamless extension to other services (e.g., Stripe, AWS, etc.) without modifying the monitoring loop.

🔹 2. Efficient HTTP Fetching (ETag-Based)

The system uses conditional HTTP requests:

Sends If-None-Match

Handles 304 Not Modified

Avoids re-downloading unchanged payloads

This ensures:

Reduced bandwidth usage

Minimal processing overhead

Scalability across many providers

This approach is significantly more efficient than naive polling.

🔹 3. Unified Event Model

All providers return standardized IncidentEvent objects:

IncidentEvent(
    provider,
    incident_id,
    title,
    status,
    message,
    updated_at
)

This keeps the monitoring engine provider-independent and easy to extend.

🔹 4. Concurrent Monitoring

Providers are fetched concurrently using:

asyncio.gather(...)

This allows scalable monitoring of multiple status pages without blocking execution.

⚡ Change Detection Logic

An event is logged only when there is a meaningful change:

New incident appears

Status changes

Message content changes

Deduplication key:

provider + incident_id + status + message

This guarantees:

No duplicate logs

Accurate detection of real updates

Message-level granularity

🖥 Example Output
2026-02-24 00:54:58 | INFO | New Event | Provider=OpenAI | Product=Chat Completions | Status=investigating | Message=Elevated error rates detected
▶ Running Locally
1️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Start monitoring
python main.py

If incidents are active, updates will be logged automatically.

🌍 Deployment

This service can be deployed as a background worker on:

Render

Railway

Fly.io

Any container-based environment

Start command:

python main.py
📈 Extending the System

To add a new provider:

Implement a new class extending StatusProvider

Add it to the providers list in main.py

No architectural changes required.

🧠 Design Principles

Asynchronous execution

Efficient network usage

Provider abstraction

Clean separation of concerns

Minimal dependencies

Production-style logging

No unnecessary complexity

✅ Why This Matters

Monitoring external service health is critical for:

Incident response systems

Reliability engineering

Observability pipelines

Operational dashboards

This project demonstrates how to build a scalable, event-driven monitoring loop without overengineering.