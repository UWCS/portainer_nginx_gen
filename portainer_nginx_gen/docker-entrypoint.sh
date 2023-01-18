#!/bin/bash

nginx
sh -c "/app/nginx_reloader.sh &"
exec "$@"
