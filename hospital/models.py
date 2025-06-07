from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import date
from django.utils import timezone

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import date

from django.utils import timezone  # ensure this is at the top

class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescriptions')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescriptions')
    patient_age = models.PositiveIntegerField()
    patient_address = models.TextField()
    date = models.DateField(default=timezone.now)
    medicines = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    share_id = models.CharField(max_length=100, default=uuid.uuid4)
