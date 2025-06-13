import os
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")  # This now points to Atlas
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["medicare_agent"]
patients_collection = db["patients"]

def insert_patient(patient_data):   
    result = patients_collection.insert_one(patient_data)
    return str(result.inserted_id)

def update_patient(patient_id, update_fields):
    result = patients_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": update_fields}
    )
    return {
        "matched": result.matched_count,
        "modified": result.modified_count
    }

def get_patient(patient_id):
    return patients_collection.find_one({"_id": ObjectId(patient_id)})

def get_all_patients():
    return list(patients_collection.find())


if __name__ == "__main__":
    # 1. Insert a new patient
    new_patient = {
    "name": "gagan",
    "age": 25,
    "gender": "male",
    "conditions": ["Not Well"],
    "symptoms": [
        "low blood pressure", "eye pain", "mood swings", "fatigue", "insomnia"
    ],
    "contact": {
        "phone": "987-654-3210",
        "email": "john@cena.com"
    }

}

    inserted_id = insert_patient(new_patient)
    print(f"\n✅ Inserted Patient ID: {inserted_id}")

    # 2. Update the patient
    update_fields = {
        "age": 51,
        "contact.email": "alice.updated@example.com"
    }
    update_result = update_patient(inserted_id, update_fields)
    print(f"🔄 Update Result: {update_result}")

    # 3. Get the updated patient
    fetched_patient = get_patient(inserted_id)
    print("\n📄 Fetched Patient:")
    print(fetched_patient)

    # 4. Get all patients
    print("\n📋 All Patients:")
    all_patients = get_all_patients()
    for patient in all_patients:
        print(patient)