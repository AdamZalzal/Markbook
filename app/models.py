"""
Definition of models.
"""

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from Markbook import settings
import django.contrib.auth
class Book(models.Model):
    user = models.ForeignKey(User,models.CASCADE,null = True)
    name = models.CharField(max_length = 200, null = True, blank= False)
    num_courses = models.PositiveIntegerField(null = True, blank = False)
    gpa = models.FloatField(null = True, blank = True)

class Course(models.Model):
    name = models.CharField(max_length = 200,null = True, blank = False)
    num_items = models.PositiveIntegerField(null = True, blank = False)
    current_mark = models.FloatField(null = True, blank = False, validators =[MaxValueValidator(100.0),MinValueValidator(0.0)])
    goal_mark = models.FloatField(null = True, blank = False,validators =[MaxValueValidator(100.0),MinValueValidator(0.0)])
    book = models.ForeignKey(Book,models.CASCADE,null = True, blank = False)
    completion = models.FloatField(null = True, blank = False,validators =[MaxValueValidator(100.0),MinValueValidator(0.0)])

class Item(models.Model):
    name = models.CharField(max_length = 200,null = True, blank = False)
    weight = models.FloatField(null = True, blank = False,validators =[MaxValueValidator(100.0),MinValueValidator(0.0)])
    mark = models.FloatField(null = True, blank = True,validators =[MaxValueValidator(100.0),MinValueValidator(0.0)])
    required_mark = models.FloatField(null= True, blank=True)
    course = models.ForeignKey(Course,models.CASCADE,null = True, blank = False)

    
