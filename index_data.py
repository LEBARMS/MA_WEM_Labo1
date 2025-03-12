import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Connect to the Elasticsearch instance
es = Elasticsearch("http://localhost:9200")
index_name = "wiki_headings"

# Create the index with mapping if it doesn't exist
if not es.indices.exists(index=index_name):
    mapping_body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "french_custom": {
                        "type": "french",
                        "stopwords": "_french_"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "title": {"type": "text", "analyzer": "french_custom"},
                "headings": {"type": "text", "analyzer": "french_custom"}
            }
        }
    }
    es.indices.create(index=index_name, body=mapping_body)

# Load JSON file
with open("wikipedia_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

actions = []
for i, doc in enumerate(data):
    actions.append({
        "_index": index_name,
        "_id": i,
        "_source": doc
    })

bulk(es, actions)
print(f"Indexed {len(actions)} documents into '{index_name}'")
