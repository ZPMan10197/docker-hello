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