FROM camptocamp/python-gis:3.6
ADD data /tmp
RUN pip install psycopg2-binary && apt-get update && apt-get -y install postgis
# we need shp2pgsql
