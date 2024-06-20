import time
import random
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient('localhost', 27017)
db_embedded = client['contracts_embedded']
db_referenced = client['contracts_reference']

def create_attachment_ref(id, new_contrat):
	new_id = db_referenced.contracts_attachments.insert_one(new_contrat).inserted_id;
	return db_referenced.contracts_general.update_many(
		{ }, 
		{ "$push": { "attachments": new_id }}
	)

def create_attachment_emb(id, new_contrat):
	new_contrat['_id'] = ObjectId()
	return db_embedded.contracts.update_many(
		{ },
		{ "$push": { "attachments": new_contrat }}
	)


contracts_id = '66607c3714aa457d80784d78'
general_contract_id = '66607bfc14aa457d807812e0'
new_contract = {
  # "_id": "66603eb8864b00623a99220d",
  "service": "VINSURANCE",
  "company": "SOS",
  "pricing_table": {
    "price_1": random.randint(1, 100),
    "price_2": random.randint(1, 100),
    "price_3": random.randint(1, 100)
  },
  "date_signature": datetime.today(),
  "date_created": datetime.today(),
  "date_expiration": datetime.today()
}

start_time = time.time()
c = create_attachment_emb(contracts_id, new_contract)
print(f"→ Create Attachments {c.modified_count} Embedded: {time.time() - start_time} s")

start_time = time.time()
c = create_attachment_ref(contracts_id, new_contract)
print(f"→ Create Attachments {c.modified_count} Referencing: {time.time() - start_time} s")

