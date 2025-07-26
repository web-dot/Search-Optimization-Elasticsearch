from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
es.indices.delete(index="products", ignore=[400, 404])
print("Index deleted")
