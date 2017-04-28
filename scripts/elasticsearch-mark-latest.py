#!/usr/bin/env python

from elasticsearch import Elasticsearch

try:
	# Initialize ES client
	es = Elasticsearch(hosts = ["localhost:9200"])

	print "Search for docs with is_latest:1"

	# Search all records where is_latest is 1
	res = es.search(index = "_all", doc_type = "dbexport-age", body = {
	        "query": {
			"match": {
				"is_latest": 1
			}
	        }
	})

	# If found
	if res["hits"]["total"] > 0:

		# For each doc
		for doc in res["hits"]["hits"]:

			print "Update doc %s set is_latest:0" % doc["_id"]

			# Update set is_latest to 0
			upd = es.update(index = doc["_index"], doc_type = "dbexport-age", id = doc["_id"], body = {
				"doc": {
					"is_latest": 0
				}
			})

	print "Search for latest doc"

	# Search for the latest doc
	lat = es.search(index = "_all", doc_type = "dbexport-age", body = {
		"query": {
			"match_all": {}
		},
		"size": 1,
		"sort": {
			"@timestamp": {
				"order": "desc"
			}
		}
	})

	# If found
	if lat["hits"]["total"] > 0:

		print "Update doc %s set is_latest:1" % lat["hits"]["hits"][0]["_id"]

		# Update the first doc found (should be only one since we specified size:1 earlier)
		upd = es.update(index = lat["hits"]["hits"][0]["_index"], doc_type = "dbexport-age", id = lat["hits"]["hits"][0]["_id"], body = {
			"doc": {
				"is_latest": 1
			}
		})

except Exception as e:

	print str(e)

print "Done"
