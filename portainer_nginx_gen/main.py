import os
from pprint import pprint as pp

import docker
import requests

API_KEY = os.environ.get("PORTAINER_API_KEY")
PORTAINER_API_URL = (
    "https://portainer.uwcs.co.uk/api/endpoints/4/docker/containers/{}/json"
)

session = requests.session()
session.headers.update({"X-API-KEY": API_KEY})

client = docker.DockerClient(
    base_url=os.environ.get("DOCKER_HOST", "unix://var/run/docker.sock")
)

for container in client.containers.list():
    container_id = container.id
    data = session.get(PORTAINER_API_URL.format(container_id))
    print(data.text())


for event in client.events(decode=True):
    print("*" * 40)
    pp(event)
    print("*" * 40)
