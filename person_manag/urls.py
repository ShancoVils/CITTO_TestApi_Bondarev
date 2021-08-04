from .import views
from django.urls import path
from .views import PersonView, code_form
from .RandomUserGenerate import GenerateExcelUser


urlpatterns = [
    # Получить данные 
    path('person/', PersonView.as_view()), 
    # Put запрос 
    path('person/<int:pk>', PersonView.as_view()),
    # Записать в бд все данные с указанного excel файла
    path('write_to_db/', views.write_to_db),
    # Переход по ссылке указанной в письме(подтверждение аккаунта) 
    path('confirm_form/<random_code>/',code_form),
    #Генерирует excel файл
    path('generate_excel/', GenerateExcelUser),

]
