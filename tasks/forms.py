from django import forms
from django.forms import ModelForm
from .models import Task



# Crear formulario personalizado 

class taskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets={
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control'}),
            'important' : forms.CheckboxInput(attrs={'class' : 'form-check-input'}),

        }