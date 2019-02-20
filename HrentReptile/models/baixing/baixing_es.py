from elasticsearch_dsl import connections, Document, Keyword, Text, Integer, GeoPoint, Float, Object

connections.create_connection(hosts=["localhost"])


class BaixingDoc(Document):
    pass