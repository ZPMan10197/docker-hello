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

The entire application is a single file (`app.py`) using Python's stdlib `http.server`. There are no dependencies, no package manager files, and no test suite. The Dockerfile uses `python:3.12-slim` as the base image.

## Intended next steps (from README)

- Add Docker Compose with a Redis backend service
- Scan image for CVEs with Trivy
- Push to AWS ECR and run on ECS Fargate

## Hardening notes (for future work)

- Pin base image to a `sha256` digest instead of a floating tag
- Add a non-root `USER` directive
- Add a `HEALTHCHECK` instruction
- Use a multi-stage build
