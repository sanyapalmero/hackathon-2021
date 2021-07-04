from fabric import task


BACKEND_IMAGE = "docker.pkg.github.com/sanyapalmero/hackathon-2021/hackathon-2021-backend"
FRONTEND_IMAGE = "docker.pkg.github.com/sanyapalmero/hackathon-2021/hackathon-2021-frontend"


@task
def build_images(c):
    c.local(f"docker build . -f Dockerfile.backend -t {BACKEND_IMAGE}")
    c.local(f"docker build . -f Dockerfile.frontend -t {FRONTEND_IMAGE}")


@task
def push_images(c):
    c.local(f"docker push {BACKEND_IMAGE}")
    c.local(f"docker push {FRONTEND_IMAGE}")


@task
def upgrade(c):
    build_images(c)
    push_images(c)

    with c.cd("hackathon"):
        c.run("docker-compose pull")
        c.run("docker-compose up -d")
        c.run("docker-compose restart frontend")
