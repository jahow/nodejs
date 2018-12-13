

### Information

Application with :

- postgres/postgis
- geoserver
- gistools
- angular 7 through node 10


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

Data:
http://localhost:8600/geoserver/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities


Angular:
http://localhost:4004/
