from codecs import ignore_errors
from elasticsearch import Elasticsearch
import os


class ELK:
    def __init__(self, host) -> None:
        self.es = Elasticsearch(host)
        self.mapping = {"mappings": {"properties": {"date_time": {"type": "date"}}}}

    def ping(self):
        connection = self.es.ping()
        return connection

    def create_index(self, indexName):
        res = self.es.indices.create(index=indexName, ignore=400, body=self.mapping)
        return res

    def put(self, doc, indexName):
        try:
            res = self.es.index(index=indexName, document=doc)
            return res
        except Exception as e:
            print(f"Error cannot put data into Elasticsearch: {e}")
