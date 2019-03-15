from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('companies/', views.companies_index, name='index'),
    path('companies/<int:company_id>/', views.companies_detail, name='detail'),
    path('companies/create/', views.CompanyCreate.as_view(), name='company_create'),
    path('companies/<int:pk>/update/', views.CompanyUpdate.as_view(), name='company_update'),
    path('companies/<int:pk>/delete/', views.CompanyDelete.as_view(), name='company_delete'),
    path('companies/<int:company_id>/add_meal/', views.add_meal, name='add_meal'),
    path('companies/<int:company_id>/meals/<int:meal_id>/delete/', views.remove_meal, name='remove_meal'),
    path('companies/<int:company_id>/meals/<int:meal_id>/request/', views.request_meal, name='request_meal'),
    path('companies/<int:company_id>/meals/<int:meal_id>/cancel_request/', views.cancel_req_meal, name='cancel_req_meal'),
    path('companies/<int:company_id>/add_photo/', views.add_photo, name='add_photo'),
]