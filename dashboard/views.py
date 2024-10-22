from django.shortcuts import redirect, render
from django.contrib import messages

from .models import Patient
from . import utils

def index(request):
    """
    handles the request for /dashboard/ page
    """
    if request.POST:
        """
        execute the following code only when a POST request is sent
        """
        patient_id = request.POST['patient_id'].upper()
        if Patient.objects.filter(uniq_id=patient_id).exists():
            patient = Patient.objects.get(uniq_id=patient_id)
            patient_name = patient.name
            dob = patient.dob
            gender = patient.gender

            details_formatted = utils.get_details(patient_id)
            # summary = utils.generate_summary(details_formatted)
            summary = """
<p>
</p><h2>Personalized Treatment Recommendations for John Doe</h2>
<p>Based on the provided medical records, here are personalized recommendations tailored to John Doe's unique needs:</p>
<p><strong>I. Diabetes Management:</strong></p>
<ul>
<li><strong>Diet and Exercise:</strong> John Doe requires continued effort in managing his Type 2 diabetes through diet and exercise. The previously created "diet and exercise regimen" plan from 2021 should be revisited with a doctor or registered dietitian to adjust it based on his current needs, preferences, and lifestyle.  </li>
<li><strong>Monitoring:</strong> Regular monitoring of blood sugar levels is crucial. John Doe should aim for at least weekly checkups to assess the effectiveness of medication and diet adjustments. </li>
<li><strong>Medication Review:</strong> Metformin continues to be essential. However, a thorough review with his physician may consider adjusting dosage or adding another diabetes medication based on current blood sugar control and individual needs.  </li>
</ul>
<p><strong>II. Cardiovascular Health:</strong></p>
<ul>
<li><strong>Statins:</strong> John Doe's elevated cholesterol levels require continued use of statins as prescribed. </li>
<li><strong>Blood Pressure Monitoring &amp; Lifestyle Changes:</strong> Given his history of high blood pressure, consistent monitoring and lifestyle modifications are important for long-term management.  John Doe needs to continue with the "diet and exercise regimen" plan from 2021 or explore alternative options after consulting his doctor.</li>
</ul>
<p><strong>III. Overall Health Management:</strong></p>
<ul>
<li><strong>Regular checkups:</strong> It's vital for John Doe to maintain regular appointments with his physician for a comprehensive health checkup, addressing any concerns he might have about his overall well-being.</li>
<li><strong>Holistic approach:</strong>  A holistic approach to healthcare is crucial for John Doe. This includes not just treating existing conditions but also focusing on preventive measures like stress management and healthy sleep patterns.</li>
</ul>
<p><strong>IV. Recommendations based on Age &amp; Gender:</strong></p>
<ul>
<li><strong>Age:</strong> John Doe, at age 49, presents a unique opportunity for preventative care. Addressing his high cholesterol early can significantly reduce the risk of heart disease in the long run.</li>
<li><strong>Gender:</strong>  Men are often more susceptible to cardiovascular diseases than women. Therefore, proactive management is crucial for preventing future complications.</li>
</ul>
<p><strong>V. Further Steps and Resources:</strong></p>
<ul>
<li><strong>Consult with a Doctor or Physician:</strong> John Doe should consult with his physician or healthcare provider regularly to discuss any concerns he might have about his health, medication, and treatment plan.</li>
<li><strong>Registered Dietitian:</strong> A registered dietitian can create a personalized meal plan for John Doe that will be effective in managing diabetes and improving overall nutrition. </li>
<li><strong>Physical Activity Specialist:</strong>  A certified fitness trainer or physical activity specialist can help John Doe create an exercise program tailored to his fitness level and goals, incorporating both aerobic and strength training.</li>
</ul>
<p><strong>Remember</strong>: These are general recommendations based on the information provided. It is crucial for John Doe to consult with a healthcare professional to receive personalized advice and treatment plans tailored to his specific needs. </p>
                    
                <p></p>
            
            """
            # summary = '<h1>bleh<h1>'

            if summary == None:
                messages.error(request, 'Something went wrong, Check the logs')
                return render(request, 'dash/index.html')

            request.session['summary'] = summary
            request.session['name'] = patient_name
            request.session['dob'] = dob.strftime('%d-%m-%Y')
            request.session['gender'] = gender.upper()

            return redirect('dash:result')

        messages.error(request, f"Patient ID: {patient_id} is invalid")
        return render(request, 'dash/index.html')

    return render(request, 'dash/index.html')

def result(request):
    summary = request.session.get('summary', None)
    if summary == None:
        redirect('dash:index')

    name = request.session.get('name', None)
    dob = request.session.get('dob', None)
    gender = request.session.get('gender', None)

    context = {
        'summary': summary,
        'name': name,
        'dob': dob,
        'gender': gender
    }
    return render(request, 'dash/result.html', context)
