from .import views
from django.urls import path
from .views import PersonView, code_form, generate_excel_file


urlpatterns = [
    # Получить данные 
    path('person/', PersonView.as_view()), 
    # Put запрос 
    path('person/<int:pk>', PersonView.as_view()),
    # Записать в бд все данные с указанного excel файла
    path('generate_users/', views.generate_users),
    # Переход по ссылке указанной в письме(подтверждение аккаунта) 
    path('confirm_form/<random_code>/',code_form),
    #Генерирует excel файл
    path('generate_excel_file/', generate_excel_file),
]
