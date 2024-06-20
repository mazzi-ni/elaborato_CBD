import time
# from bson import ObjectId
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db_embedded = client['contracts_embedded']
db_referenced = client['contracts_reference']

def delete_attachment_emb(city, company):
	return db_embedded.contracts.update_many(
		{ "repair_shop_city": {"$eq" : city} },
		{ 
			"$pull": { 
				"attachments": { "company": company}
			}
		}
	)


def delete_attachment_ref(city, company):
	contracts = db_referenced.contracts_general.find(
		{ "repair_shop_city": {"$eq" : city} }
	)
	
	if contracts == None:
		return 'contracts not found'

	deleted = 0
	for c in contracts:
		deleted += db_referenced.contracts_attachments.delete_many({
			"_id": { "$in": c['attachments'] } , 
			"company": company 
		}).deleted_count
	
	return deleted


# contracts_id = '66607c6914aa457d807858aa'
# general_contract_id = '66607bfc14aa457d807812e0'

start_time = time.time()
c = delete_attachment_emb('Milano', 'VANFORYOU')
print(f"→ Delete {c.modified_count} Attachments Embedded: {time.time() - start_time} s")

start_time = time.time()
c = delete_attachment_ref('Milano', 'VANFORYOU')
print(f"→ Delete {c} Attachments Referencing: {time.time() - start_time} s")

