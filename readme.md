# Inbound Carrier Sales - Internal API

## 📅 Useful Links

* [HR Project Call Link (HappyRobot)](https://platform.happyrobot.ai/deployments/u2hvt9impmce/lr4vbo9kfh5j)
* [Lovable Dashboard (Call Insights)](https://preview--call-whisper-insights-board.lovable.app/)
* [Deployed Internal API Docs (Swagger UI)](https://hr-challenge-code.fly.dev/docs)

## 📈 Overview

This repository was vibe-coded by Antonio González Ferreira as a solution to the technical challenge proposed by HappyRobot, focused on building an inbound carrier sales system.

It provides a backend API that supports the required logic for carrier interactions, call tracking, load management, and optional metrics visualization.

The following diagram provides a high-level view of the infrastructure and how this repo code interacts with the rest of the developed system. The entire system has been engineered using the following technologies and modules:

![System Overview](assets/challenge_sys.png)

This repository implements the **Internal REST API** module shown in the architecture diagram. It is responsible for managing freight load data and call interactions, supporting the inbound carrier engagement flow.


## 🚀 Features

* Load listing and filtering
* Call logging and classification (sentiment, outcome)
* Carrier verification and negotiation tracking
* Built using FastAPI and SQLAlchemy
* Docker-ready and deployable via Fly.io

## 🔧 Technologies

* Python 3.10+
* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker
* Fly.io (deployment)

## ✅ How to Run Locally

By default, the project runs with a local SQLite database for ease of development.

For production environments, it's recommended to use PostgreSQL. If deploying to Fly.io, follow the steps below to attach a managed Postgres instance and configure it properly using environment secrets.

### Requirements

* Python 3.10+
* Docker (optional, for containerized run)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the API

```bash
uvicorn api.main:app --reload
```

### Run with Docker

```bash
docker build -t carrier-inbound-api .
docker run -p 8000:8000 carrier-inbound-api
```

## 🌐 API Overview

The API has endpoints grouped in four main areas:

### `/loads` Endpoints

* `GET /loads` - Retrieve future available loads
* `POST /loads` - Create a new load
* `GET /loads/search` - Advanced search with filters (origin, destination, equipment, weight, miles, dates, etc.)

### `/calls` Endpoints

* `POST /calls` - Create a new call record
* `GET /calls` - Retrieve all call records
* `GET /calls/{call_id}` - Retrieve details of a single call
* `POST /calls/update/{call_id}` - Update a call record
* `DELETE /calls` - Delete all call records

### `/health` Endpoint

* `GET /health` - Simple health check

> Note: `/metrics/agent` is used internally to power the optional dashboard (not part of the public API contract).

All endpoints require an `x-api-key` header for authentication.

## 🌐 Deployment

### Deploy to Fly.io

1. **Install Fly CLI**

```bash
curl -L https://fly.io/install.sh | sh
```

2. **Authenticate with Fly.io**

```bash
fly auth login
```

3. **Initialize the app (only once)**

```bash
fly launch
```

* Choose a name or accept the default
* Select region
* Decline PostgreSQL if you're setting it up manually

4. **Provision a PostgreSQL Database**

```bash
fly postgres create --name carrier-db
```

* Choose a region
* Wait for the provisioning to complete

5. **Attach the Database to Your App**

```bash
fly postgres attach --app carrier-inbound-api carrier-db
```

This will automatically set the `DATABASE_URL` secret for your app.

If you need to set or override it manually, you can do so with:

```bash
fly secrets set DATABASE_URL=postgres://username:password@host:port/dbname
```

Make sure the connection string matches your Postgres configuration.

6. **Set Additional Secrets (e.g. API keys)**

```bash
fly secrets set API_KEY=your_api_key FMCSA_KEY=your_fmcsa_key
```

7. **Deploy the App**

```bash
fly deploy
```

8. **Access your deployment**
   Fly.io will provide a URL like:

```
https://carrier-inbound-api.fly.dev
```

Refer to `fly.toml` for environment configuration and port mappings.

## 🔐 Security

* API key authentication on all endpoints
* CORS enabled
* Environment variable management for secrets


---

Feel free to fork, clone, and build upon this project. For any questions, reach out!
