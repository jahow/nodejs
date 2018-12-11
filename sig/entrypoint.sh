#!/bin/bash

pip install psycopg2-binary
pip install ipdb
pip install gsconfig-py3
# params in undefined so we force to null in our case
sed -i 's/# What is the use of this request?/params = None/g' /usr/local/lib/python3.6/site-packages/geoserver/catalog.py
apt-get update
apt-get -y install postgis
python