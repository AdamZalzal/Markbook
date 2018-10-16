"""
Definition of forms.
"""

from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import Book, Course, Item, User
from django.utils.translation import gettext_lazy as _
from app import models
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name']
        labels ={'name': _('What is the name of this markbook?'),
                  
                  }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','goal_mark']
        labels = {'name':_('What is the name of this course?'),
                  'goal_mark':_('What is your target grade for this course?')
                  }

GradeFormSet = modelformset_factory(Item, fields = ('name', 'weight','mark'))

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','weight','mark']



class GradeForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','weight','mark']
        labels = {'name':_('What is the name of this syllabus item?'),
                  'weight':_('How much is this item worth?'),
         
                  }

