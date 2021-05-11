#!/bin/bash

git stash save static/img/*
git pull
chmod a+w -R static
chmod a+w -R data
sudo systemctl restart uwsgi
