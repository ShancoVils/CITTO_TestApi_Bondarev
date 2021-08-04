from rest_framework.generics import  get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests,random,string, os
from .logs import logger
import xlrd

   

def generate_code():
    letters_and_digits = string.ascii_letters + string.digits
    random_char = ''.join(random.sample(letters_and_digits, 16 ))
    return str(random_char)

'''
Класс реализует основной функционал API и стандартные методы GET,PUT, POST, DELETE


'''

class PersonView(APIView):

    # Метод получает все данные о пользователях

    def get(self, request):
        person_api = CustomUser.objects.all()
        serializer = CustomUserSerializer(person_api, many=True)
        logg_try()
        logger.debug("Получение данных")
        return Response({"person_api": serializer.data})

    # Метод создает пользователя, чтобы активировать его,
    # необходимо зайти на указаннуб почту и перейти по ссылке

    def post(self, request):

        person_api = request.data.get("person_api")
        email =person_api['email']
        code = generate_code()
        person_api["activate_code"] = code
        register(email,code)
        serializer = CustomUserSerializer(data=person_api)
        if serializer.is_valid(raise_exception=True):
            person_save = serializer.save()
        obtain_auth_token(sender=settings.AUTH_USER_MODEL)
        logg_try()
        logger.debug("Пользователь '{}' создан (не активирован)".format(email))
        return Response({
        "success": "'{}', активируйте аккаунт на указанной вами почте ".format(email)
        })

    #Метод редактирует данные, указанного пользователя,
    #но если токен, указанный в headers не соответствует токену редактируемого пользователя 
    #метод не сработает

    def put(self, request, pk,):
            resp = requests.get('http://127.0.0.1:8000', headers={'Token': '014582855f7ba31ec6a9e026c261c77bd041d681'})
            token_get =  resp.request.headers['Token']
            tokens_set = Token.objects.filter(key=token_get)

            if not tokens_set:
                logg_try()
                logger.error("Токен '{}' не существует".format(token_get))
                return Response({"Токен": "не действительный"})
            else:
                token_user_id = tokens_set.values('user_id')
                first_orb_tocken =  token_user_id.first()
                id_user =  first_orb_tocken.get('user_id')
                CustomUser.objects.filter(id =id_user)
                main_id=pk
                if  id_user != main_id:
                    logg_try()
                    logger.error("Не достаточно прав для редактирование аккаунта")
                    return Response({"Не": " достаточно прав"})
                else:
                    person_save = get_object_or_404(CustomUser.objects.all(), pk=pk)
                    data = request.data.get('person_api')
                    serializer = CustomUserSerializer(instance=person_save, data=data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        personal_save = serializer.save()
                        logg_try()
                        logger.debug("Профиль пользователя '{}' обновлен".format(personal_save.email))
                    return Response({
                        "success": "Группа" '{}'" обновился ".format(personal_save.email)
                    })
            
    #Метод удаляет указанного пользователя
        
    def delete(self, request, pk):
            person_obj = get_object_or_404(CustomUser.objects.all(), pk=pk)
            person_obj.delete()
            logg_try()
            logger.debug("Профиль пользователя '{}' удален".format(person_obj.email))
            return Response({
                "message": "Челик `{}` удален".format(person_obj.email)
            })


# Метод отправляет письмо на указанную почту со ссылкой на активацию аккаунта

def register(email, code):
    try:
        message ="Ссылка для подтверждения аккаунта"+"  "+"http://127.0.0.1:8000/confirm_form/"+code
        send_mail('Код подтверждения', message,
        settings.EMAIL_HOST_USER,
        [email], 
        fail_silently=False) 
        logg_try()
        logger.debug("Письмо подтверждение отправлено на '{}' ".format(email))
    except:
        logger.error("Почты '{}' не существует ".format(email))


# Метод активирует аккаунт, который перешел по ссылке

def code_form(request, random_code):
    profile = CustomUser.objects.get(activate_code=random_code)
    profile.is_active = True
    profile.save()
    logg_try()
    logger.debug("Пользователь '{}'активирован".format(profile))
    return HttpResponse("Аккаунт '{}' активирован".format(profile))



# Метод выдает токен при регистрации каждого пользоватля

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def obtain_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) 
    logg_try()
    logger.debug("Пользователю  на '{}' был выдан токен  ".format(instance))

#Если размер основного лог-файла больше 500б, создается новый, а записи в этом перекидывются в хранилище

def logg_try():
    if  int(os.path.getsize('logs/logs.log'))  <  int(500):
        print(os.path.getsize('logs/logs.log'))
    else:    
        log_file =  open('logs/logs.log', 'r')
        log_info = log_file.read()
        other_log_file =  open('logs/other_logs.log', 'a')
        other_log_file.write(log_info)
        open('logs/logs.log', 'w').close()

#Считывает указанный excel файл, и добавляет записи в бд

def write_to_db(self):
    # Получаю файл
    excel_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'teams.xls')
    excel_dict = {}
    excel_file = xlrd.open_workbook(excel_file_path)
    excel_sheet = excel_file.sheet_by_index(0)
    # Считывание файла
    for i in range(excel_sheet.nrows):
        x = excel_sheet.row_values(i) 
        if i not in excel_dict:
            excel_dict[i] = x
    num_user = 1


    # Добавление в базу данных
    while (num_user < int((excel_sheet.nrows))):
        one_per = excel_dict[num_user]
        email_excel_obj = one_per[1]
        password_excel_obj = one_per[2]
        person_ge_excel_obj = int(one_per[3])
        ex_user = CustomUser.objects.create_user(email = email_excel_obj,
                                                password=  password_excel_obj,
                                                person_group_id = person_ge_excel_obj)
        ex_user.save()
        print("Юзер '{}' добавлен".format(num_user))
        num_user = num_user+1
    return HttpResponse(excel_sheet.nrows)


