# Inbound Carrier Sales - FDE Technical Challenge

## 📊 Overview

This project implements an inbound use case for carrier engagement using the **HappyRobot** platform. It simulates an AI assistant that handles calls from carriers looking to book freight loads, negotiates offers, and classifies calls by outcome and sentiment.

## 🚀 Features

* Load search from internal API
* Carrier MC number validation via FMCSA API
* Load details pitching and offer negotiation (up to 3 rounds)
* Call classification (outcome and sentiment)
* Call transfer to sales rep upon agreement
* REST API built with FastAPI + SQLAlchemy
* Containerized with Docker

## 🔧 Technologies

* Python 3.10+
* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker
* Fly.io (for deployment)

## ✅ How to Run Locally

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

The API provides endpoints for managing loads, calls, and interacting with the assistant. API key authentication is required on all endpoints.

## 🌐 Deployment

Deployed using Fly.io. See `fly.toml` and Dockerfile for configuration.

## 📈 Optional Features

* [ ] Dashboard for metrics (pending or optional)

## 📢 Deliverables

1. Code Repository (this repo)
2. Link to HappyRobot configuration (see platform)
3. Video Demo (not included here)

## 🔒 Security

* API key authentication on all endpoints
* CORS enabled
* Secret handling via environment variables (recommended for production)

## 📄 License

MIT License

---

Feel free to fork, clone, and build upon this project. For any questions, reach out!
