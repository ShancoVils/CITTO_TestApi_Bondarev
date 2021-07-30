from .import views
from django.urls import path
from .views import PersonView, generate_code, code_form,register
from rest_framework.authtoken import views 

urlpatterns = [
    path('person/', PersonView.as_view()),
    path('person/<int:pk>', PersonView.as_view()),
    path('confirm_form/<random_code>/',code_form),
]
