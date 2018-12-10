 #!/bin/bash
set -e

pip install psycopg2-binary
pip install ipdb
apt-get update
apt-get -y install postgis