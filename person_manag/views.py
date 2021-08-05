
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from .service import logg_try,register,generate_code,code_form,obtain_auth_token,write_to_db,GenerateExcelUser,get_person_data,post_person_data,put_person_data
'''
Класс реализует основной функционал API и стандартные методы GET,PUT, POST, DELETE
'''

class PersonView(APIView):

    # Метод получает все данные о пользователях

    def get(self, request):
        get_user = get_person_data(self, request) 
        return Response({"person_api": get_user})

    # Метод создает пользователя, чтобы активировать его,
    # необходимо зайти на указаннуб почту и перейти по ссылке

    def post(self, request):
        post_user = post_person_data(self, request)
        return Response({
        "success": "'{}', активируйте аккаунт на указанной вами почте ".format(post_user)
        })

    #Метод редактирует данные, указанного пользователя,
    #но если токен, указанный в headers не соответствует токену редактируемого пользователя 
    #метод не сработает

    def put(self, request, pk,):
        put_user = put_person_data(self, request,pk)
        return Response({
            "success": "Группа" '{}'" обновился ".format(put_user)
        })
            
    #Метод удаляет указанного пользователя
        
    def delete(self, request, pk):
        delete_user = put_person_data(self, request,pk)
        return Response({
            "message": "Челик `{}` удален".format(delete_user)
        })


#Считывает указанный excel файл, и добавляет записи в бд

def generate_users(request):
    write_to_db(request)
    return HttpResponse("Пользователи добавлены")


#Считывает указанный excel файл, и добавляет записи в бд

def generate_excel_file(request):
    GenerateExcelUser(request)
    return HttpResponse("Excel файл сгенерирован")

