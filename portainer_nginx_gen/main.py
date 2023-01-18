import os

import docker
import requests

from pprint import pprint as print

API_KEY = os.environ.get("PORTAINER_API_KEY")
TOP_LEVEL_DOMAIN = os.environ.get("TOP_LEVEL_DOMAIN", "local")
PORTAINER_CONTAINERS_API_URL = (
    "https://portainer.uwcs.co.uk/api/endpoints/4/docker/containers/{}/json"
)
PORTAINER_USERS_API_URL = "https://portainer.uwcs.co.uk/api/users/{}"
session = requests.session()
session.headers.update({"X-API-KEY": API_KEY})

client = docker.DockerClient(
    base_url=os.environ.get("DOCKER_HOST", "unix://var/run/docker.sock")
)

def get_username(user: id):
    data = session.get(PORTAINER_USERS_API_URL.format(user))
    try:
        info: dict = data.json()
    except:
        info = {}
    username = info.get("Username", None)
    return username

def get_portainer_container_data(container_id: str):
    data = session.get(PORTAINER_CONTAINERS_API_URL.format(container_id))
    try:
        container_info: dict = data.json()
    except:
        container_info = {}
    if not container_info.get("Id", None):
        container_info = {}
    return container_info

def generate_configs():
    for container in client.containers.list():
        container_id = container.id

        container_info = get_portainer_container_data(container_id)
        portainer_info = container_info.get("Portainer", None)
        if not portainer_info:
            print(f"Couldn't get Portainer info for container {container_id}")
            continue
        user_access = portainer_info["ResourceControl"]["UserAccesses"]
        container_env: list[str] = container.attrs["Config"]["Env"]
        virtual_host = ""
        for i in container_env:
            if i.startswith("VIRTUAL_HOST="):
                virtual_host = i.split("=", 1)[1]
        if virtual_host == "":
            continue
        if len(user_access) > 0:
            user = user_access[0]["UserId"]
            username = get_username(user)
            subdomain = f".{username}."
        else:
            subdomain = "."
        hostname = virtual_host + subdomain + TOP_LEVEL_DOMAIN
        print(hostname)


generate_configs()

for event in client.events(decode=True):
    # print(event.keys())
    generate_configs()
