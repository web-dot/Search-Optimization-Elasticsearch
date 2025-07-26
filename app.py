from flask import Flask, jsonify
from elasticsearch import Elasticsearch
import json

app = Flask(__name__)

# Connect to your local Elasticsearch 7
es = Elasticsearch("http://localhost:9200")

@app.route('/')
def home():
    return "Flask App Running with Elasticsearch 🚀"

@app.route('/load-products')
def load_products():
    with open("products.json", "r") as f:
        products = json.load(f)
    
    for product in products:
        es.index(index="products", id=product["id"], body=product)
    
    return jsonify({"message": "Products loaded into Elasticsearch"}), 200

@app.route('/search/<term>')
def search(term):
    body = {
        "query": {
            "multi_match": {
                "query": term,
                "fields": ["title", "description", "category"]
            }
        }
    }

    res = es.search(index="products", body=body)
    hits = res['hits']['hits']
    return jsonify([hit["_source"] for hit in hits])

if __name__ == '__main__':
    app.run(debug=True)
