from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView 
import uuid
import boto3
from .models import Company, Meal, Photo
from .forms import MealForm

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'anycollector'

def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def companies_index(request):
  companies = Company.objects.all()
  return render(request, 'companies/index.html', { 'companies': companies })

def companies_detail(request, company_id):
    company = Company.objects.get(id=company_id)
    if company.role == 'FoodGiver':
      company_meals = Meal.objects.filter(company_id=company.id)
      req_meals = None
    else:
      company_meals = Meal.objects.filter(available=True)
      req_meals = Meal.objects.filter(requested_by = company_id)
    meal_form = MealForm()
    return render(request, 'companies/detail.html', {
        'company': company, 'meal_form': meal_form, 
        'meals': company_meals, 'req_meals': req_meals
    })

class CompanyCreate(CreateView):
  model = Company
  fields = '__all__'
  success_url = '/companies/'

class CompanyUpdate(UpdateView):
  model = Company
  fields = ['name', 'role', 'email', 'logo', 'website']
  success_url = '/companies/'

class CompanyDelete(DeleteView):
  model = Company
  success_url = '/companies/'

def add_meal(request, company_id):
  # create the ModelForm using the data in request.POST
  meal_form = MealForm(request.POST)
  # validate the form
  if meal_form.is_valid():
    # don't save the form to the db until it
    # has the company_id assigned
    new_meal = meal_form.save(commit=False)
    new_meal.company_id = company_id
    new_meal.save()
  return redirect('detail', company_id=company_id)

def remove_meal(request, company_id, meal_id):
    Meal.objects.filter(id=meal_id).delete()
    return redirect('detail', company_id=company_id)

def request_meal(request, company_id, meal_id):
  print('meal id ', meal_id)
  meal = Meal.objects.get(id=meal_id)
  print('meal desc: ', meal)
  meal.requested_by = company_id
  meal.available = False
  meal.save()
  return redirect('detail', company_id=company_id)

def cancel_req_meal(request, company_id, meal_id):
  print('meal id ', meal_id)
  meal = Meal.objects.get(id=meal_id)
  print('meal desc: ', meal)
  meal.requested_by = 0
  meal.available = True
  meal.save()
  return redirect('detail', company_id=company_id)

def add_photo(request, company_id):
	# photo-file was the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to company_id or company (if you have a company object
            photo = Photo(url=url, company_id=company_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', company_id=company_id)