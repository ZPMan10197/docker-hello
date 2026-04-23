# docker-hello

My first Docker project. A minimal Python HTTP server packaged as a container, built as the first step in my cloud security engineering portfolio.

## What it does

Runs a Python HTTP server on port 8000 inside a container. When you hit it, it responds with the container's hostname — showing that each container gets its own isolated identity.

## Run it

```bash
docker build -t hello-zeshawn .
docker run -p 8000:8000 hello-zeshawn
```

Then in another terminal:

```bash
curl http://localhost:8000
```

Or open `http://localhost:8000` in a browser.

Stop the container with `Ctrl + C`.

## What I learned

- **Images vs containers** — an image is an immutable template; each `docker run` creates a fresh container instance. Same image, different hostnames on every run.
- **Dockerfile basics** — `FROM` sets the base image, `WORKDIR` sets the in-container working directory, `COPY` bakes files into the image at build time, `CMD` defines the default startup command.
- **Port mapping** — `-p HOST:CONTAINER` forwards traffic from a port on the host to a port inside the container. Without it, the server inside is unreachable from outside.
- **`EXPOSE` is documentation only** — the actual port publishing happens at `docker run` time, not in the Dockerfile.
- **Binding to `0.0.0.0` inside the container** — required so the server accepts traffic routed in via Docker's port forward. Binding to `127.0.0.1` would make it unreachable from outside the container.
- **Containers ship their own runtime** — the Python interpreter running my code lives inside the container, not on my Mac. This is what makes containers portable across environments.

## Next steps

- Add Docker Compose with a second service (e.g., Redis backend)
- Scan the image for CVEs with Trivy
- Push to AWS ECR and run it on ECS Fargate

## Stack

- Python 3.12 (slim)
- Docker Desktop on Apple Silicon (M1)

## Design decisions

**1. Why `python:3.12-slim` as the base image?** Smaller attack surface and faster pulls than `python:3.12`. Would consider alpine or distroless for production.

**2. Why `0.0.0.0` instead of `127.0.0.1`?** Inside a container, binding to `127.0.0.1` only listens on loopback — Docker's forwarded traffic arrives on `eth0` and would be refused. `0.0.0.0` is correct for containers; the security boundary is the port-publishing rule, not the bind address.

**3. Why does `EXPOSE` appear in the Dockerfile?** Documentation for humans reading the Dockerfile. The actual port publishing happens at `docker run -p` time. `EXPOSE` does nothing to networking.

**4. Why pin the base image to a sha256 digest?** Tags like `python:3.12-slim` are mutable — the image they point to can change at any time. A sha256 digest is a cryptographic fingerprint of the exact image bytes, so every build is guaranteed to use the same image. This prevents unexpected upstream changes and supply chain attacks.

**5. Why run as a non-root user?** By default, container processes run as root. If an attacker exploits the app, they land as root inside the container. Creating an unprivileged user (`appuser`) and switching to it with `USER` limits the blast radius of any compromise.

**6. Why add a HEALTHCHECK?** Docker can't tell if your app is actually working — only that the process is running. The `HEALTHCHECK` runs a real HTTP request every 30 seconds. If it fails three times, Docker marks the container unhealthy, allowing orchestrators (ECS, Kubernetes) to restart it automatically.