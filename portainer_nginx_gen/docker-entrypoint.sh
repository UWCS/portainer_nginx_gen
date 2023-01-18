#!/bin/bash

sh -c "/app/nginx_reloader.sh &"
exec "$@"
