import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db_embedded = client['contracts_embedded']
db_referenced = client['contracts_reference']

def find_query_ref(pipeline):
	return db_referenced.contracts_general.aggregate(pipeline)

def find_query_emb(pipeline):
	return db_embedded.contracts.aggregate(pipeline)

match = {
		"$match": {
			"company": "HERTZ"
		}
	}

project = {
    "$project": {
      "_id": "$attachments._id",
      "company": "$attachments.company",
      "repair_shop_name": "$repair_shop_name",
      "repair_shop_p_iva": "$repair_shop_p_iva"
    }
  }

unwind = {
    "$unwind": {
      "path": "$attachments"
    }
	}

group = {
    "$group": {
      "_id": "$attachments._id",
      "company": { "$first": '$attachments.company' },
      "repair_shop_name": { "$first": '$repair_shop_name' },
      "repair_shop_p_iva": { "$first": '$repair_shop_p_iva' },
    }
  }

lookup = {
    "$lookup": {
      "from": "contracts_attachments",
      "localField": "attachments",
      "foreignField": "_id",
      "as": "attachments",
      "pipeline": [
				match
      ]
    }
  }


start_time = time.time()
c = find_query_emb([ unwind, group,	match ])
print(f"→ Find slow {len(list(c))} Embedded: {time.time() - start_time} s")

start_time = time.time()
c = find_query_emb([ unwind, project,	match ])
print(f"→ Find fast {len(list(c))} Embedded: {time.time() - start_time} s")

start_time = time.time()
c = find_query_ref([ lookup, unwind, project ])
print(f"→ Find fast {len(list(c))} Referencing: {time.time() - start_time} s")

start_time = time.time()
lookup['$lookup'].pop('pipeline')
c = find_query_ref([ lookup, unwind, project, match ])
print(f"→ Find slow {len(list(c))} Referencing: {time.time() - start_time} s")

