from django.shortcuts import render
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
            text = utils.get_details(patient_id)
            summary = utils.generate_summary(text)
            print(summary)

            context = {
                'summary': summary
            }
            return render(request, 'dash/index.html', context)

        messages.error(request, f"Patient ID: {patient_id} is invalid")
        return render(request, 'dash/index.html')

    return render(request, 'dash/index.html')
