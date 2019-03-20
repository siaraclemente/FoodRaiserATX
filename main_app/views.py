from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

# @login_required
# def companies_index(request):
#   companies = Company.objects.filter(user=request.user)
#   # You could also retrieve the logged in user's cats like this
#   # cats = request.user.cat_set.all()
#   return render(request, 'companies/index.html', { 'companies': companies })
#   # companies = Company.objects.all()
#   # return render(request, 'companies/index.html', { 'companies': companies })

@login_required
def companies_detail(request):
    company = Company.objects.get(user = request.user)
    print('company: ', company)
    if company.role == 'FoodGiver':
      company_meals = Meal.objects.filter(company_id=company.id)
      req_meals = None
    else:
      company_meals = Meal.objects.filter(available=True)
      req_meals = Meal.objects.filter(requested_by = company.id)
    meal_form = MealForm()
    return render(request, 'companies/detail.html', {
        'company': company, 'meal_form': meal_form, 
        'meals': company_meals, 'req_meals': req_meals
    })


class CompanyCreate(LoginRequiredMixin, CreateView):
  model = Company
  fields = ['role', 'name', 'email', 'phone', 'address', 'website']
  
  # This method is called when a valid
  # cat form has being submitted
  def form_valid(self, form):
    # Assign the logged in user
    form.instance.user = self.request.user
    # Let the CreateView do its job as usual
    return super().form_valid(form)  
  # model = Company
  # fields = '__all__'
  success_url = '/companies/'

class CompanyUpdate(LoginRequiredMixin, UpdateView):
  model = Company
  fields = ['name', 'role', 'email', 'phone', 'website']
  success_url = '/companies/'

class CompanyDelete(LoginRequiredMixin, DeleteView):
  model = Company
  success_url = '/companies/'

@login_required
def add_meal(request):
  company = Company.objects.get(user = request.user)
  # create the ModelForm using the data in request.POST
  meal_form = MealForm(request.POST)
  # validate the form
  if meal_form.is_valid():
    # don't save the form to the db until it
    # has the company_id assigned
    new_meal = meal_form.save(commit=False)
    new_meal.company_id = company.id
    new_meal.save()
  return redirect('detail')

@login_required
def remove_meal(request, meal_id):
    company = Company.objects.get(user = request.user)
    Meal.objects.filter(id=meal_id).delete()
    return redirect('detail')

@login_required
def request_meal(request, meal_id):
  company = Company.objects.get(user = request.user)
  print('meal id ', meal_id)
  meal = Meal.objects.get(id=meal_id)
  print('meal desc: ', meal)
  meal.requested_by = company.id
  meal.available = False
  meal.save()
  return redirect('detail')

@login_required
def cancel_req_meal(request, meal_id):
  print('meal id ', meal_id)
  meal = Meal.objects.get(id=meal_id)
  print('meal desc: ', meal)
  meal.requested_by = 0
  meal.available = True
  meal.save()
  return redirect('detail')

@login_required
def add_photo(request):
    company = Company.objects.get(user = request.user)
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
            photo = Photo(url=url, company_id=company.id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('company_create')
    else:
      error_message = 'Invalid credentials - Please try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)