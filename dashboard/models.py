from django.db import models

class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = 'm'
        FEMALE = 'f'
        OTHERS = 'o'

    uniq_id = models.CharField(max_length=1024, unique=True)
    name = models.CharField(max_length=1024)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    condition = models.CharField(max_length=2056)
    notes = models.CharField(max_length=2056)

class TreatmentPlans(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    follow_up = models.DateField()
    plan = models.CharField(max_length=2056)

class Medications(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    dosage = models.IntegerField()
    frequency = models.CharField(max_length=1024)
    start_date = models.DateField()
    end_date = models.DateField()
