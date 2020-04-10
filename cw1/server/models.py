from django.db import models
import json
# Create your models here.
class Professor(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

class Module(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    taughtBy = models.ManyToManyField(Professor)

class Student(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
