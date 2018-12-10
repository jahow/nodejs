import psycopg2
import logging
import os
from pathlib import Path
import osgeo.ogr


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
            import ipdb; ipdb.set_trace()
            schema = ''.join(s.lower() for s in os.path.basename(subdir) if not s.isspace())
            self.schemas.append(schema)
            print (schema)
            for file in files:
               if file.endswith(".{}".format(format)):
                    table_name = ''.join(s.lower() for s in file if not s.isspace())
                    self.tables[Path(table_name).resolve().stem] = {'schema': schema, 'path': '{}/{}'.format(subdir, file)}


    def bulk_create(self):
        for schema in self.schemas:
            self._push_to_database(self._build_create_schema_query(schema))
            for table in self.tables:
                import ipdb ; ipdb.set_trace()
                self._push_to_database(self._build_create_table_query(self.tables[table]['schema'], table))
                logging.info('Created TABLE {}'.format(table))
        logging.info('Done creating TABLES total : {}'.format(len(self.tables.keys())))


    @staticmethod
    def insert_data_from_shapefile(table, **kwargs):
        schema = kwargs['schema']
        path = kwargs['path']
        shapefile = osgeo.ogr.Open(path)
        import ipdb ; ipdb.set_trace()
        layer = shapefile.GetLayer(0)

        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            name = feature.GetField("NAME").decode("Latin-1")
            wkt = feature.GetGeometryRef().ExportToWkt()
            cursor.execute("INSERT INTO countries (name,outline) " +"VALUES (%s, ST_GeometryFromText(%s, " +"4326))", (name.encode("utf8"), wkt))
    @staticmethod
    def _build_create_table_query(dirname, shapefile):
        return 'CREATE TABLE {}.{}'.format(dirname, shapefile)

    @staticmethod
    def _build_create_schema_query(schema):
        return 'CREATE SCHEMA {}'.format(schema)

    def _push_to_database(self, query):
        #self.cur.commit(query)
        print (query)
