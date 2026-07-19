# Devix

A network device monitoring and management platform — connects to network devices over SSH/SNMP/ICMP, collects telemetry on a schedule, and surfaces it through a real-time dashboard.

## Overview

Devix is a full-stack platform for managing and monitoring network infrastructure. The FastAPI backend talks directly to network devices (via Netmiko/Paramiko for SSH, PySNMP for SNMP, ping3/python-nmap for reachability and discovery), polls them on a schedule, and stores results across a relational store (device inventory, users, config) and a time-series store (metrics/telemetry). The React dashboard presents that data with live updates, filtering, and export.

## Features

- **Multi-protocol device connectivity** — SSH (Netmiko, Paramiko), SNMP (PySNMP), ICMP reachability (ping3), network discovery (python-nmap)
- **Scheduled polling** — background jobs via APScheduler
- **Time-series telemetry storage** — InfluxDB for device metrics history
- **Relational data layer** — PostgreSQL via SQLAlchemy/SQLModel, migrations via Alembic
- **Caching & queuing** — Redis / aioredis
- **Real-time updates** — WebSocket support for live dashboard data
- **Authentication** — JWT-based auth (python-jose, passlib, bcrypt)
- **Alerting** — email notifications via FastAPI-Mail
- **Geolocation** — device location support via Geopy
- **Cloud storage** — S3 integration via boto3
- **Data export** — Excel export from the dashboard (xlsx)

## Tech Stack

**Backend** — FastAPI, SQLAlchemy/SQLModel, PostgreSQL, Alembic, Redis, InfluxDB, APScheduler, Netmiko, Paramiko, PySNMP, WebSockets, JWT, boto3
**Frontend** — React 18, Material UI, Ant Design, Redux Toolkit + redux-persist, Tailwind CSS, React Hook Form + Yup, xlsx

## Project Structure

```
Devix/
├── fast_backend/   # FastAPI service — device connectivity, polling, telemetry, auth
└── frontend/       # React dashboard
```

## Getting Started

### Backend

```bash
cd fast_backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

### Environment Variables

Create a `.env` file in `fast_backend/` with:

```
DATABASE_URL=
REDIS_URL=
INFLUXDB_URL=
INFLUXDB_TOKEN=
JWT_SECRET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
SMTP_HOST=
SMTP_USER=
SMTP_PASS=
```

## License

MIT
