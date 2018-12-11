import extractor


def import_topo_to_postgis(path):
    '''Import data from the BD TOPO IGN
    into the postgis database'''
    bd_topo_extractor = extractor.Extractor(path)
    bd_topo_extractor.get_files_by_format('shp')
    #bd_topo_extractor.bulk_create()
    #for shapefile in bd_topo_extractor.tables:
    #    bd_topo_extractor.insert_data_from_shapefile(shapefile, **bd_topo_extractor.tables[shapefile])

    #bd_topo_extractor.commit_to_database()
    import_to_geoserver(bd_topo_extractor)


def import_to_geoserver(bd_topo_extractor):
    workspace_name = 'bd_topo_ign'
    bd_topo_extractor.gs_connect_geoserver()
    # create stores == schemas
    for schema in bd_topo_extractor.schemas:
        bd_topo_extractor.gs_create_store(schema, workspace_name)
    for table in bd_topo_extractor.tables:
        bd_topo_extractor.gs_publish_feature_type(table, bd_topo_extractor.tables[table]['schema'])





import_topo_to_postgis('/app/sig/data/')
