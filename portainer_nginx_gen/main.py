import os
from pprint import pprint as pp

import docker

client = docker.DockerClient(
    base_url=os.environ.get("DOCKER_HOST", "unix://var/run/docker.sock")
)

for container in client.containers.list():
    print("*" * 40)
    pp(container.attrs)
    print("*" * 40)

for event in client.events(decode=True):
    print("*" * 40)
    pp(event)
    print("*" * 40)
