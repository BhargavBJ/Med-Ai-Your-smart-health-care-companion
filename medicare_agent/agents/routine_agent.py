from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import db

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

def suggest_routine(name: str, email: str):

    patient = db.patients_collection.find_one(
        {"name": name, "email": email},
        {"_id": 0, "name": 1, "symptoms": 1, "conditions": 1}
    )
    if not patient:
        print(f"No patient found with name '{name}' and email '{email}'.")
        return
    symptoms = patient.get("symptoms", [])
    conditions = patient.get("conditions", [])
    name = patient.get("name", "Unknown")

    print(f"Name: {name} | Symptoms: {', '.join(symptoms)} | Conditions: {', '.join(conditions)}")
    system_prompt = """
    You are a doctor by profession and have excellent knowledge about the Human Body and all the diseases with their cures. 
    Give the routine for the patient based on the symptoms and conditions. Use the patient's name instead of their pronouns and be specific.
    """
    human_prompt = (
        "Give the routine for the patient name: {name} based on the symptoms provided in: {symptoms} and the conditions provided in: {conditions}. "
        "Make sure you just give the disease name and not what to do later on."
    )
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
    chat = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)
    chain = prompt | chat
    print("\nRecommended Routine:")
    for chunk in chain.stream({
        "name": name,
        "symptoms": symptoms,
        "conditions": conditions
    }):
        print(chunk.content, end="", flush=True)

# Example call:
suggest_routine("Alice Smith", "alicesmith@gmail.com")
