from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import db

# Load environment variables once
load_dotenv()
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
def diagnose_patient(name: str, email: str):

    patient = db.patients_collection.find_one({"name": name, "email": email}, {"_id": 0, "name": 1, "symptoms": 1})
    if not patient:
        print(f"No patient found with name '{name}' and email '{email}'.")
        return

    symptoms = patient.get("symptoms", [])
    print(f"Name: {name} | Symptoms: {', '.join(symptoms)}")

    system_prompt = (
        "You are a doctor by profession and have excellent knowledge about the Human Body "
        "and all the diseases with their cures. Just give the name of the possible disease "
        "and make sure it is comma separated if there are more than one."
    )
    human_prompt = (
        "Give the diagnosis report based on the symptoms provided in: {topic}. "
        "Make sure you just give the top 3 disease names and not what to do later on."
    )

    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
    chat = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)
    chain = prompt | chat

    print("Possible Diagnosis: ", end="", flush=True)
    for chunk in chain.stream({"topic": symptoms}):
        print(chunk.content, end="", flush=True)

name=input("Enter the patient name : ")
mail=input("Enter the patient email : ")
diagnose_patient(name,mail)
# diagnose_patient("Alice Smith", "alicesmith@gmail.com")
