#!/bin/bash

git stash save static/img/*
git pull
git stash apply
chmod a+w -R static
chmod a+w -R data
sudo systemctl restart uwsgi
