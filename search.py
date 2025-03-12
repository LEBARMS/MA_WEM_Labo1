from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "wiki_headings"

# Define a query that boosts the title field over headings
query_body = {
    "query": {
        "multi_match": {
            "query": "transformation de Fourier",
            "fields": ["title^3", "headings"]
        }
    }
}

# Execute the search
response = es.search(index=index_name, body=query_body)

# Print the total number of hits
total_hits = response["hits"]["total"]["value"]
print("Total hits:", total_hits)

# Iterate through the hits and print the score and source
for hit in response["hits"]["hits"]:
    print(f"Score: {hit['_score']}")
    print("Document:", hit["_source"])
    print("---------------------------")
