import os
import pandas as pd
from pymongo import MongoClient
import math as m

        
    # CONVERTING EXCEL TO DICTIONARY
def excel_to_json(excel_file):
    excel_data = pd.read_excel(excel_file)
    dict_data = excel_data.to_dict(orient='records')
    return dict_data

# INSERTING DATA INTO DATABASE
def insert_json_to_mongodb(dict_data):
    client = MongoClient(os.getenv("MONGODB_URL"))
    db = client.userdb
    collection = db.userData



    for doc in dict_data:
        # Extract tag values

        
        tags = [str(doc[f'tag{i}']) for i in range(1, 6) if doc.get(f'tag{i}') is not None]
        
        if(tags[0]!="nan"):

            # Assigning tag values to variables
            tag1 = tags[0] if tags[0] else ''
            tag2_values = tags[1].split(';') if len(tags) > 1 else []
            tag3_values = tags[2].split(';') if len(tags) > 2 else []

            # Check if there are any non-null tags
            if tag1:
                # Query to check if any existing document has the same tags
                query = {
                    'learner_id': tag1,
                    'program_id': tag2_values[0],
                    'module_id': tag2_values[1],
                    'activity_id': tag2_values[2],
                    'super_admin': tag3_values[0],
                    'organization_id': tag3_values[1],
                }
                update_record={"$set":{"report_data":doc}}
          
                # Check if a document with matching tags exists
                existing_doc = collection.find_one({},query)
                print(existing_doc)
                if existing_doc:
                    collection.find_one_and_update(query,update_record)
                    # Skip if a document with matching tags already exists
                    # print(f"Skipping document with tags: {tags}")
                    pass
                else:
                    # Insert the document into the collection
                    # collection.insert_one(doc)
                    # print(f"Inserted document with tags: {tags}")
                    pass
            else:
                # Skip if all tags are null
                print("Skipping document with no tags")


excel_file_path = './candidates.xlsx'
dict_data = excel_to_json(excel_file_path)

# print(dict_data)

insert_json_to_mongodb(dict_data)
