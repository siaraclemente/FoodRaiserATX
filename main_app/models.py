from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

ROLES = (
    ('FoodGiver', 'FoodGiver'),
    ('FoodTaker', 'FoodTaker'),
)

class Company(models.Model):
    role = models.CharField(
        max_length = 12,
        choices = ROLES,
        default = ROLES[0][1]
    )
    name = models.CharField(max_length=100) #this will be deleted to use django User name
    email = models.CharField(max_length=100)
    logo = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'company_id': self.id})

class Meal(models.Model):
    description = models.CharField(max_length=200)
    available_on = models.DateField('availability date')
    available = models.BooleanField(default=True)
    requested_by = models.IntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('meals_detail', kwargs={'pk': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for company_id: {self.company_id} @{self.url}"
    