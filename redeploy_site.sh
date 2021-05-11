#!/bin/bash

git pull
chmod a+w -R static
chmod a+w -R data
sudo systemctl restart uwsgi
