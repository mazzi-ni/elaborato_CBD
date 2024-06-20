import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db_embedded = client['contracts_embedded']
db_referenced = client['contracts_reference']

def update_query_ref(query, new_contract):
	return db_referenced.contracts_general.update_many(query, new_contract)

def update_query_emb(query, new_contract):
	return db_embedded.contracts.update_many(query, new_contract)

# query in general_contract
num_old = 48
num_new = 99
query = { 
	"repair_shop_street": f"vicolo Lodi {num_old}" 
}
new_contract = { 
	"$set": { 
		"repair_shop_street": f"via Lodi {num_new}" 
	}
}

start_time = time.time()
contract = update_query_emb(query, new_contract)
print(f"→ Update {contract.modified_count} Embedded: {time.time() - start_time} s")

start_time = time.time()
contract = update_query_ref(query, new_contract)
print(f"→ Update {contract.modified_count} Referecing: {time.time() - start_time} s")

