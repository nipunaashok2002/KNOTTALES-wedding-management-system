from django import forms
from .models import PlanningTask

class TaskForm(forms.ModelForm):
    class Meta:
        model = PlanningTask
        fields = ["period", "text", "completed"]
