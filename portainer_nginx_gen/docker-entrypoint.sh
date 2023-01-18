#!/bin/bash

service nginx start
sh -c "/app/nginx_reloader.sh &"
exec "$@"
