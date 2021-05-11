#!/bin/bash

git pull
chmod a+w -R static
sudo systemctl restart uwsgi
