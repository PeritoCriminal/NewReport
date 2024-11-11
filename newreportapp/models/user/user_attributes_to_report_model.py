# newreportapp/models/user/user_attributes_to_report_model.py

from django.db import models
from newreportapp.models import CustomUserModel

class UserAttributesToReportModel(models.Model):
    registration_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="user_reports")
    director = models.CharField(max_length=150, blank=False, default='')
    state = models.CharField(max_length=150, blank=False, default='')
    city = models.CharField(max_length=150, blank=False, default='')
    unit = models.CharField(max_length=150, blank=False, default='')
    team = models.CharField(max_length=150, blank=False, default='')

    class Meta:
        verbose_name = "User Attribute to Report"
        verbose_name_plural = "User Attributes to Report"

    def __str__(self):
        return f"{self.user} - {self.city} ({self.registration_date})"
