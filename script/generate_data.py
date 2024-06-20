import json
import random
import string
import os
import threading

from datetime import datetime, timedelta
from bson import ObjectId
from pathlib import Path
from atpbar import atpbar, flushing

from data import *
from schema import *

MAX_ATTACHEMNT = 800
MAX_GENERAL_CONTRACT = 15000
PATH = 'json/'

Path(PATH).mkdir(parents=True, exist_ok=True)

def generate_random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_partita_iva():
    return ''.join(random.choices(string.digits, k=11))

def generate_random_address():
    street = f"{random.choice(street_types)} {random.choice(street_names)} {random.randint(1, 100)}"
    city = random.choice(cities)
    postal_code = ''.join(random.choices(string.digits, k=5))
    return street, city, postal_code
    # return f"{street}, {postal_code} {city}"


def generate_pricing_table():
    return {
        "price_1": round(random.uniform(100, 1000), 2),
        "price_2": round(random.uniform(100, 1000), 2),
        "price_3": round(random.uniform(100, 1000), 2),
    }


def generate_embedded_json():
    contracts_embedded = []
    count = 0

    for _ in atpbar(range(MAX_GENERAL_CONTRACT), name='embedded_json'):
        count += 1
        street, city, postalcode = generate_random_address()
        contract_embedded = {
            "contract_date_creation": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
            "contract_date_signature": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
            "repair_shop_name": generate_random_name(),        
            "repair_shop_p_iva": generate_partita_iva(),
            "repair_shop_street": street,
            "repair_shop_city": city,
            "repair_shop_postalcode": postalcode,
            "attachments": []
        }

        num_attachments = random.randint(1, MAX_ATTACHEMNT)  
        for _ in range(num_attachments):
            attachment = {
                "_id": str(ObjectId()),
                "service": random.choice(services),
                "company": random.choice(companies),
                "pricing_table": generate_pricing_table(),
                "date_signature":(datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
                "date_created": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
                "date_expiration": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
            }
            contract_embedded["attachments"].append(attachment)

        contracts_embedded.append(contract_embedded)
        # print('\r' + str(count), end='\r')


    # Save the embedded contracts data to a JSON file
    with open(os.path.join(PATH, 'contracts_embedded_data.json'), 'w') as f_out:
        json.dump(contracts_embedded, f_out, indent=2)


def generate_reference_json():
    contracts_referencing = []
    attachments_referencing = []
    count = 0

    for _ in atpbar(range(MAX_GENERAL_CONTRACT), name='reference_json'):
        count += 1
        street, city, postalcode = generate_random_address()
        contract_referencing = {
            "contract_date_creation": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
            "contract_date_signature": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
            "repair_shop_name": generate_random_name(),        
            "repair_shop_p_iva": generate_partita_iva(),
            "repair_shop_street": street,
            "repair_shop_city": city,
            "repair_shop_postalcode": postalcode,
            "attachments": []
        }

        # Create attachments
        num_attachments = random.randint(1, MAX_ATTACHEMNT)  
        for _ in range(num_attachments):
            attachment_id = str(ObjectId())
            attachment = {
                "_id": attachment_id,
                "service": random.choice(services),
                "company": random.choice(companies),
                "pricing_table": generate_pricing_table(),
                "date_signature": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
                "date_created": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
                "date_expiration": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
            }
            contract_referencing["attachments"].append(attachment_id)
            attachments_referencing.append(attachment)

        contracts_referencing.append(contract_referencing)
        # print('\r' + str(count), end='\r')

    # Save the referencing contracts data to a JSON file
    with open(os.path.join(PATH, 'contracts_referencing_data.json'), 'w') as f_out:
        json.dump(contracts_referencing, f_out, indent=2)

    # Save the attachments data to a JSON file
    with open(os.path.join(PATH, 'attachments_referencing_data.json'), 'w') as f_out:
        json.dump(attachments_referencing, f_out, indent=2)



print('>>> creating embedded json ...')
generate_embedded_json()
print('--- done.')
print('>>> creating referencing json ...')
generate_reference_json()
print('--- done.')

# if __name__ =="__main__":
#     print('>>> creating json ...')
#     with flushing():

#         t1 = threading.Thread(target=generate_embedded_json)
#         t2 = threading.Thread(target=generate_reference_json)
 
#         t1.start()
#         t2.start()
 
#     t1.join()
#     t2.join()
 
#     print("Done!")
