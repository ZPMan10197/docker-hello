# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal Python HTTP server (`app.py`) packaged as a Docker container. It responds to GET requests with the container's hostname on port 8000. This is a cloud security engineering portfolio project.

## Commands

```bash
# Run both services (app + Redis)
docker compose up --build

# Test the server
curl http://localhost:8000

# Tear down
docker compose down
```

## Architecture

`app.py` uses Python's stdlib `http.server` and the `redis` client library to increment a visit counter on every GET request. Redis runs as a separate container on the same Compose network; the app connects to it by service name (`host="redis"`).

The Dockerfile installs dependencies via `requirements.txt`, runs the app as an unprivileged `appuser`, includes a `HEALTHCHECK` via `urllib.request`, and pins the base image to a sha256 digest.

A GitHub Actions pipeline (`.github/workflows/ci.yml`) runs on every push to `main`: builds the image, then scans it with Trivy — failing on CRITICAL or HIGH CVEs with no available fix ignored.

## Intended next steps

- Push to AWS ECR and run on ECS Fargate

## Hardening notes (for future work)

- Use a multi-stage build
- Switch to distroless or Alpine base image for smaller attack surface
