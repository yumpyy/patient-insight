import ollama
import markdown

from .models import Patient

def convert_to_html(text: str):
    md = markdown.Markdown()

    return md.convert(text)

def generate_summary(text: str):
    try:
        response = ollama.chat(
            model='gemma2:2b',
            messages= [
                {
                    'role': 'system',
                    'content': 'You will receive the medical records of a patient, which include detailed information about their medical history, demographics, current health conditions, and any previous treatment plans. Your task is to thoroughly analyze this data to generate personalized treatment recommendations tailored to the patient\'s unique needs. Consider factors such as the patient\'s age, gender, medical history, and any relevant conditions when formulating your recommendations.' # give instruction to the model, what are they supposed to do with the data
                },
                {
                    'role': 'user',
                    'content': text # feed the model with data in order to proeed with summarization process
                }
            ]
        )
        return convert_to_html(response['message']['content']) # print the response from the model
        
    except Exception as e:
        # handle exceptions
        print(f"An error occurred: {e}")
        return "Something went wrong. Chech logs"

def get_details(patient_id: str):
    patient = Patient.objects.get(uniq_id=patient_id)
    patient_name = patient.name
    dob = patient.dob
    gender = patient.gender
    
    medical_history = [
        {
            'date': entry.date,
            'condition': entry.condition,
            'notes': entry.notes,
        }
        for entry in patient.medicalhistory_set.all()
    ] 
    
    treatment_plans = [
        {
            'date': plans.date,
            'follow_up': plans.follow_up,
            'plan': plans.plan
        }
        for plans in patient.treatmentplans_set.all()
    ]
    
    medications = [
        {
            'name': meds.name,
            'dosage': meds.dosage,
            'frequency': meds.frequency,
            'start_date': meds.start_date,
            'end_date': meds.end_date
        }
        for meds in patient.medications_set.all()
    ]

    format_text = f"""
    Name: {patient_name}
    Date of Birth: {dob}
    Gender: {gender}

    Medical History: {medical_history}
    Treatment Plans: {treatment_plans}
    Medications: {medications}
    """

    return format_text
