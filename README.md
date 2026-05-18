# docker-hello

![CI](https://github.com/ZPMan10197/docker-hello/actions/workflows/ci.yml/badge.svg)

My first Docker project. A minimal Python HTTP server packaged as a container, built as the first step in my cloud security engineering portfolio.

## What it does

Runs a Python HTTP server and a Redis instance together via Docker Compose. When you hit the server, it responds with the container hostname and a persistent visit counter stored in Redis.

## Run it

```bash
docker compose up --build
```

Then in another terminal:

```bash
curl http://localhost:8000
```

Or open `http://localhost:8000` in a browser.

Stop with `Ctrl + C`, then `docker compose down` to remove the containers.

## What I learned

- **Images vs containers** — an image is an immutable template; each `docker run` creates a fresh container instance. Same image, different hostnames on every run.
- **Dockerfile basics** — `FROM` sets the base image, `WORKDIR` sets the in-container working directory, `COPY` bakes files into the image at build time, `CMD` defines the default startup command.
- **Port mapping** — `-p HOST:CONTAINER` forwards traffic from a port on the host to a port inside the container. Without it, the server inside is unreachable from outside.
- **`EXPOSE` is documentation only** — the actual port publishing happens at `docker run` time, not in the Dockerfile.
- **Binding to `0.0.0.0` inside the container** — required so the server accepts traffic routed in via Docker's port forward. Binding to `127.0.0.1` would make it unreachable from outside the container.
- **Containers ship their own runtime** — the Python interpreter running my code lives inside the container, not on my Mac. This is what makes containers portable across environments.
- **CI/CD pipelines** — GitHub Actions spins up a fresh Ubuntu runner on every push, builds the image, and runs Trivy to scan for CVEs. If a critical vulnerability is found, the build fails automatically before anything ships.
- **Secret scanning** — Gitleaks scans the full git history on every push for accidentally committed credentials (API keys, tokens, passwords). It runs before the Docker build so a leaked secret fails the pipeline immediately.
- **CVE scanning** — Trivy checks every package in the image against a database of known vulnerabilities. Pinning to `ignore-unfixed: true` avoids noise from vulnerabilities with no available patch.
- **Multi-container networking** — Docker Compose puts services on a shared private network. Containers find each other by service name (e.g. `redis`), not by IP. Docker's internal DNS resolves the name automatically.
- **Stateless app, stateful data store** — the Python server holds no state itself. The visit counter lives in Redis. Restarting the app container doesn't reset the count because the data is in a separate container.

## Next steps

- Push to AWS ECR and run on ECS Fargate

## Stack

- Python 3.12 (slim)
- Redis 7 (Alpine)
- Docker Compose
- Docker Desktop on Apple Silicon (M1)

## Design decisions

**1. Why `python:3.12-slim` as the base image?** Smaller attack surface and faster pulls than `python:3.12`. Would consider alpine or distroless for production.

**2. Why `0.0.0.0` instead of `127.0.0.1`?** Inside a container, binding to `127.0.0.1` only listens on loopback — Docker's forwarded traffic arrives on `eth0` and would be refused. `0.0.0.0` is correct for containers; the security boundary is the port-publishing rule, not the bind address.

**3. Why does `EXPOSE` appear in the Dockerfile?** Documentation for humans reading the Dockerfile. The actual port publishing happens at `docker run -p` time. `EXPOSE` does nothing to networking.

**4. Why pin the base image to a sha256 digest?** Tags like `python:3.12-slim` are mutable — the image they point to can change at any time. A sha256 digest is a cryptographic fingerprint of the exact image bytes, so every build is guaranteed to use the same image. This prevents unexpected upstream changes and supply chain attacks.

**5. Why run as a non-root user?** By default, container processes run as root. If an attacker exploits the app, they land as root inside the container. Creating an unprivileged user (`appuser`) and switching to it with `USER` limits the blast radius of any compromise.

**6. Why add a HEALTHCHECK?** Docker can't tell if your app is actually working — only that the process is running. The `HEALTHCHECK` runs a real HTTP request every 30 seconds. If it fails three times, Docker marks the container unhealthy, allowing orchestrators (ECS, Kubernetes) to restart it automatically.

**7. Why use Trivy in CI and not just locally?** Running a scan locally is easy to forget or skip. Putting it in the pipeline makes it automatic and mandatory — every push is scanned, no exceptions. This is the "shift left" security principle: catch vulnerabilities at build time before they ever reach production.

**9. Why add Gitleaks secret scanning?** Accidentally committed credentials are one of the most common causes of cloud breaches — an AWS key in a public repo can be found and abused within minutes. Gitleaks scans the full git history (not just the latest commit) on every push, so even a secret committed and "deleted" in a later commit gets caught. Running it first in the pipeline means it fails fast before wasting time on a build.

**8. Why is Redis a separate container and not just a Python library?** `import redis` is the client — the code that knows how to talk to Redis. Redis the database is a separate program that has to run somewhere. Keeping it in its own container matches how production systems work: stateless app layer, separate data layer. This also means you can restart the app without losing data.