from elasticsearch import Elasticsearch


class ELK:
    def __init__(self, host) -> None:
        self.es = Elasticsearch(host)

    def put(self, doc, indexName):
        try:
            res = self.es.index(index=indexName, document=doc)
            return res
        except Exception as e:
            print(f"Error cannot put data into Elasticsearch: {e}")
