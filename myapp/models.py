from django.db import models

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100)
  published_on = models.DateField()

  def __str__(self):
    return self.title

class Student(models.Model):
  name = models.CharField(max_length=100)
  roll_number = models.CharField(max_length=20, unique=True)
  class_name = models.CharField(max_length=10)
  age = models.IntegerField()
  enrolled_on = models.DateField()

  def __str__(self):
    return self.name
  
class Employee(models.Model):
  name = models.CharField(max_length=100)
  empId = models.CharField(max_length=10)
  department = models.CharField(max_length=20)
  designation = models.CharField(max_length=20)
  salary = models.IntegerField()
  joining_date = models.DateField()