from django import forms
from .models import Dashboard

class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome do Dashboard',
                'autofocus': True
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'url-unica-do-dashboard'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Descrição do dashboard (opcional)',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.organization:
            instance.organization = self.organization
        if commit:
            instance.save()
        return instance