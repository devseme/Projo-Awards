from django import forms
from django.db.models import fields
from awards.models import Project,Profile


class ShowProjectForm(forms.ModelForm):
    class Meta:
        model=Project        
        fields=['image',
                 'link',
                 'name',
                 'description',
                 'category',
                 'location',
                 'user',
        ] 