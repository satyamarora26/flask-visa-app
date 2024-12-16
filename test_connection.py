from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["visa_db"]
collection = db["visitor_600_data"]

# Fetch and print one document to test
document = collection.find_one()
if document:
    print("Connection Successful!")
    print(document)
else:
    print("No documents found!")
