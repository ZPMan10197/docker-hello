# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal Python HTTP server (`app.py`) packaged as a Docker container. It responds to GET requests with the container's hostname on port 8000. This is a cloud security engineering portfolio project.

## Commands

```bash
# Build the image
docker build -t hello-zeshawn .

# Run the container
docker run -p 8000:8000 hello-zeshawn

# Test the server
curl http://localhost:8000
```

## Architecture

The entire application is a single file (`app.py`) using Python's stdlib `http.server`. There are no dependencies, no package manager files, and no test suite.

The Dockerfile runs the app as an unprivileged `appuser` (not root), includes a `HEALTHCHECK` via `urllib.request`, and pins the base image to a sha256 digest for reproducible builds.

A GitHub Actions pipeline (`.github/workflows/ci.yml`) runs on every push to `main`: builds the image, then scans it with Trivy — failing the build on CRITICAL or HIGH CVEs with no available fix ignored.

## Intended next steps

- Docker Compose with a Redis backend service
- Push to AWS ECR and run on ECS Fargate

## Hardening notes (for future work)

- Use a multi-stage build
- Switch to distroless or Alpine base image for smaller attack surface
