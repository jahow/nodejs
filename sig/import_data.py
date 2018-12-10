import os

import extractor


def importTopoToPostgis(path):
    '''Import data from the BD TOPO IGN
    into the postgis database'''
    bd_topo_extractor = extractor.Extractor(path)
    bd_topo_extractor.get_files_by_format('shp')
    bd_topo_extractor.bulk_create()
    for shapefile in bd_topo_extractor.tables:
        bd_topo_extractor.insert_data_from_shapefile(shapefile, **bd_topo_extractor.tables[shapefile])


importTopoToPostgis('/app/sig/data/')
