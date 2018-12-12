import psycopg2
import logging
import os
from pathlib import Path
import subprocess
import config
from geoserver.catalog import Catalog


EPSG = config.EPSG

class Extractor:
    def __init__(self, input_dir):
        logging.basicConfig(filename='extractor.log', level=logging.INFO)
        self.table_count = 0
        self.working_dir = input_dir
        self.schemas = []
        self.tables = {}
        # pg connexion
        self.conn = psycopg2.connect\
            (dbname=config.PGDATABASE, user=config.PGUSER,
             password=config.PGPASSWORD, host=config.PGHOST)
        self.cur = self.conn.cursor()
        self.sql_commands = []
        #gs config
        self.cat = None


    def get_files_by_format(self, format):
        logging.info('Started')
        for subdir, dirs, files in os.walk(self.working_dir):
            # lower and remove spaces
            schema = ''.join(s.lower() for s in os.path.basename(subdir) if os.path.basename(subdir) and not s.isspace())
            if schema != '': self.schemas.append(schema)
            for file in files:
               if file.endswith(".{}".format(format)):
                    table_name = ''.join(s.lower() for s in file if not s.isspace())
                    self.tables[Path(table_name).resolve().stem] = {'schema': schema,
                                                                    'path': '{}/{}'.format(subdir, file)}

    def bulk_create(self):
        for schema in self.schemas:
            if schema == '': continue
            self._push_to_database(self._build_create_schema_query(schema))
        self.commit_to_database()


    def gs_connect_geoserver(self):
        self.cat = Catalog(config.GSREST, username=config.GSUSER, password=config.GSPASSWORD)

    def gs_create_workspace(self, ws):
        if self.cat.get_workspace(ws): logging.info('workspace {} exists skipping...'.format(ws))
        else: self.cat.create_workspace(ws)

    def gs_get_data_store(self, store):
        return self.cat.get_store(store)

    def gs_create_store(self, schema, workspace_name):
        try:
            self.cat.get_store(schema)
        except:
            ds = self.cat.create_datastore(schema, workspace_name)
            ds.connection_parameters.update({
                'host': config.PGHOST,
                'port':config.PGPORT,
                'database': config.PGDATABASE,
                'user': config.PGUSER,
                'passwd': config.PGPASSWORD, 'dbtype':'postgis',
                'schema': schema,
                'Expose primary keys': 'true'
            })
            self.cat.save(ds)

    def gs_publish_feature_type(self, table, store_name):
        try:
            data_store = self.gs_get_data_store(store_name)
        except:
            self.cat.publish_featuretype(table, data_store, 'EPSG:2154', srs='EPSG:2154')


    @staticmethod
    def insert_data_from_shapefile(table, **kwargs):
        schema = kwargs['schema']
        path = kwargs['path']
        cmd = 'shp2pgsql -s {} {} "{}"."{}" | ' \
              'PGPASSWORD={} psql -h {} -d {} -U {}'.format(
            EPSG, path, schema, table, config.PGPASSWORD, config.PGHOST, config.PGDATABASE, config.PGUSER)
        subprocess.call(cmd, shell=True)

    @staticmethod
    def _build_create_table_query(dirname, shapefile):
        return 'CREATE TABLE {}.{};'.format(dirname, shapefile)

    @staticmethod
    def _build_create_schema_query(schema):
        return 'CREATE SCHEMA {};'.format(schema)

    def _push_to_database(self, query):
        self.cur.execute(query)


    def commit_to_database(self):
        self.conn.commit()