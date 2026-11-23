from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.conf import settings
from .utils import *

class ClinicalData(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Patient"
    )

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name="Sex")

    age = models.PositiveIntegerField(verbose_name="Age")
    cough = models.BooleanField(default=False, verbose_name="Cough")
    rasp = models.BooleanField(default=False, verbose_name="Wheezing")
    cancer = models.BooleanField(default=False, verbose_name="Cancer")
    liver_disease = models.BooleanField(default=False, verbose_name="Liver disease")
    heart_disease = models.BooleanField(default=False, verbose_name="Heart failure")
    cerebrovascular_disease = models.BooleanField(default=False, verbose_name="Cerebrovascular disease (stroke)")
    renal_disease = models.BooleanField(default=False, verbose_name="Kidney disease")
    nursing_home = models.BooleanField(default=False, verbose_name="Nursing home resident")
    altered_mental_status = models.BooleanField(default=False, verbose_name="Confusion")

    respiratory_rate = models.PositiveIntegerField(
        verbose_name="Respiratory rate (breaths/min)",
        default=18,
        validators=[MinValueValidator(5), MaxValueValidator(80)]
    )
    systolic_bp = models.PositiveIntegerField(
        verbose_name="Systolic blood pressure (mmHg)",
        default=120,
        validators=[MinValueValidator(40), MaxValueValidator(300)]
    )
    pulse = models.PositiveIntegerField(
        verbose_name="Pulse (beats/min)",
        default=70,
        validators=[MinValueValidator(30), MaxValueValidator(250)]
    )
    temperature = models.FloatField(
        verbose_name="Temperature (°C)",
        validators=[MinValueValidator(30.0), MaxValueValidator(45.0)]
    )
    hemoglobin = models.FloatField(
        verbose_name="Hemoglobin (g/L)",
        validators=[MinValueValidator(20.0), MaxValueValidator(250.0)]
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Analysis date")

    psi_score = models.IntegerField(
        null=True, blank=True,
        verbose_name="PSI score"
    )
    risk_class = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name="Risk class"
    )
    mortality_prediction = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name="Predicted mortality"
    )

    def __str__(self):
        return f"Analysis for {self.user.username} on {self.created_at.strftime('%d.%m.%Y')}"

class XRayData(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to=user_directory_path,
        verbose_name="X-ray",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    confidence = models.FloatField(blank=True, null=True)
    result = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Analysis date")

    def __str__(self):
        return f"Image {self.id} for {self.user.username}"