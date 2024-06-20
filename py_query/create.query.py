import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db_embedded = client['contracts_embedded']
db_referenced = client['contracts_reference']

def create_query_ref(n):
	for i in range(n):
		attachments_contract = [
				{
					"_id": f"66603e2c864b006{i}3a3ead21",
					"service": "VFLEET",
					"company": "VANFORYOU",
					"pricing_table": {
						"price_1": 457.28,
						"price_2": 948.97,
						"price_3": 222.11
					},
					"date_signature": "2023-07-23T12:30:04.967352Z",
					"date_created": "2023-10-11T12:30:04.967355Z",
					"date_expiration": "2023-12-26T12:30:04.967357Z"
				}
			]		

		general_contract = {
			"contract_date_creation": time.localtime(),
			"contract_date_signature": "2024-04-14T12:30:04.967342Z",
			"repair_shop_name": "Gabriella Gentile",
			"repair_shop_p_iva": f"6208125810{i}",
			"repair_shop_street": "vicolo Lodi 48",
			"repair_shop_city": "Ancona",
			"repair_shop_postalcode": "67454",
			"attachments": []
		}
		
		general_contract['attachments'] = [ attachments_contract[0]['_id'] ]
		db_referenced.contracts_general.insert_one(general_contract)
		attachments_contract[0].pop('_id')
		db_referenced.contracts_attachments.insert_one(attachments_contract[0])

def create_query_emb(n):
	for i in range(n):
		attachments_contract = [
				{
					"_id": f"66603e2c864b006{i}3a3ead21",
					"service": "VFLEET",
					"company": "VANFORYOU",
					"pricing_table": {
						"price_1": 457.28,
						"price_2": 948.97,
						"price_3": 222.11
					},
					"date_signature": "2023-07-23T12:30:04.967352Z",
					"date_created": "2023-10-11T12:30:04.967355Z",
					"date_expiration": "2023-12-26T12:30:04.967357Z"
				}
			]		

		general_contract = {
			"contract_date_creation": time.localtime(),
			"contract_date_signature": "2024-04-14T12:30:04.967342Z",
			"repair_shop_name": "Gabriella Gentile",
			"repair_shop_p_iva": f"6208125810{i}",
			"repair_shop_street": "vicolo Lodi 48",
			"repair_shop_city": "Ancona",
			"repair_shop_postalcode": "67454",
			"attachments": []
		}
		
		general_contract['attachments'] = attachments_contract
		db_embedded.contracts.insert_one(general_contract)

stop = 10000
step = 100
for i in range(0, stop, step):
	start_time = time.time()
	create_query_emb(i)
	print(f"→ Selezione Embedded {i}: {time.time() - start_time} s")

for i in range(0, stop, step):
	start_time = time.time()
	create_query_ref(i)
	print(f"→ Selezione Referencing {i}: {time.time() - start_time} s")

