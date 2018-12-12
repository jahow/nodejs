

### Information

Application with :

- postgres/postgis
- geoserver
- gistools
- angular 7


### Installation

Build application:

`docker-compose build`

Start application:

`docker-compose up`

### Insert Data into postgis & geoserver

copy the data dir into `/sig`

Then execute the following:

`sudo docker exec -ti nodejs_gistools_1 python /app/sig/scripts/import_data.py`


### Links

Geoserver:
http://localhost:8600/geoserver/web/

Angular:
http://localhost:4004/
