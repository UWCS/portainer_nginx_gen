import os

import docker
import requests

from pprint import pprint as print

API_KEY = os.environ.get("PORTAINER_API_KEY")
PORTAINER_API_URL = (
    "https://portainer.uwcs.co.uk/api/endpoints/4/docker/containers/{}/json"
)

session = requests.session()
session.headers.update({"X-API-KEY": API_KEY})

client = docker.DockerClient(
    base_url=os.environ.get("DOCKER_HOST", "unix://var/run/docker.sock")
)


def generate_configs():
    for container in client.containers.list():
        container_id = container.id
        data = session.get(PORTAINER_API_URL.format(container_id))
        try:
            container_info: dict = data.json()
        except:
            print(f"Couldn't get info for container {container_id}")
            continue
        portainer_info = container_info["Portainer"]
        print(portainer_info)


generate_configs()

for event in client.events(decode=True):
    print(event.keys())
