import psycopg2
import logging
import os
from pathlib import Path
import osgeo.ogr
import subprocess


EPSG = '2154'

class Extractor:
    def __init__(self, input_dir):
        logging.basicConfig(filename='extractor.log', level=logging.INFO)
        self.table_count = 0
        self.working_dir = input_dir
        self.schemas = []
        self.tables = {}
        # pg connexion
        conn = psycopg2.connect(dbname="gis", user="docker", password="docker", host="db")
        self.cur = conn.cursor()


    def get_files_by_format(self, format):
        logging.info('Started')
        for subdir, dirs, files in os.walk(self.working_dir):
            # lower and remove spaces
            schema = ''.join(s.lower() for s in os.path.basename(subdir) if not s.isspace())
            self.schemas.append(schema)
            for file in files:
               if file.endswith(".{}".format(format)):
                    table_name = ''.join(s.lower() for s in file if not s.isspace())
                    self.tables[Path(table_name).resolve().stem] = {'schema': schema, 'path': '{}/{}'.format(subdir, file)}


    def bulk_create(self):
        for schema in self.schemas:
            self._push_to_database(self._build_create_schema_query(schema))
            for table in self.tables:
                self._push_to_database(self._build_create_table_query(self.tables[table]['schema'], table))
                logging.info('Created TABLE {}'.format(table))
        logging.info('Done creating TABLES total : {}'.format(len(self.tables.keys())))

    @staticmethod
    def insert_data_from_shapefile(table, **kwargs):
        schema = kwargs['schema']
        path = kwargs['path']
        cmd = 'shp2pgsql -s {} {} {} | psql -h hostname -d databasename -U username'.format(EPSG, path, schema+table)
        import ipdb ; ipdb.set_trace()
        subprocess.call(cmd, shell=True)

    @staticmethod
    def _build_create_table_query(dirname, shapefile):
        return 'CREATE TABLE {}.{}'.format(dirname, shapefile)

    @staticmethod
    def _build_create_schema_query(schema):
        return 'CREATE SCHEMA {}'.format(schema)

    def _push_to_database(self, query):
        self.cur.commit(query)
