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
            summary = utils.generate_summary(details_formatted)

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
