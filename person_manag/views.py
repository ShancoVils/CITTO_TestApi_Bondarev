from rest_framework.generics import  get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests,random,string




   

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
        return Response({"person_api": serializer.data})

# Метод создает пользователя, что бы активировать его,
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
        return Response({
        "success": "'{}', активируйте аккаунт на указанной вами почте ".format(email)
        })

  #Метод редактирует данные, указанного пользователя,
  #но если токен, указанный в headers не соответствует токену редактируемого пользователя 
  #метод не сработает

    def put(self, request, pk,):
        resp = requests.get('http://127.0.0.1:8000', headers={'Token': '338d404253f7d2d65ff3664f2ebc2771f6a96402'})
        token_get =  resp.request.headers['Token']
        tokens_set = Token.objects.filter(key=token_get)

        if not tokens_set:
            return Response({"Иди": "на хрен"})
        else:
            token_user_id = tokens_set.values('user_id')
            first_orb_tocken =  token_user_id.first()
            id_user =  first_orb_tocken.get('user_id')
            CustomUser.objects.filter(id =id_user)
            main_id=pk
            if  id_user != main_id:
                return Response({"Меняй": " СВОЙ аккаунт, пес"})
            else:
                person_save = get_object_or_404(CustomUser.objects.all(), pk=pk)
                data = request.data.get('person_api')
                serializer = CustomUserSerializer(instance=person_save, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    personal_save = serializer.save()
                return Response({
                    "success": "Челик '{}' обновился ".format(personal_save)
                })
        
   #Метод удаляет указанного пользователя
    
    def delete(self, request, pk):
            person_obj = get_object_or_404(CustomUser.objects.all(), pk=pk)
            person_obj.delete()
            return Response({
                "message": "Челик `{}` удален".format(pk)
            })



# Метод отправляет письмо на указанную почту со ссылкой на активацию аккаунта

def register(email, code):
    message ="Ссылка для подтверждения аккаунта"+"  "+"http://127.0.0.1:8000/confirm_form/"+code
    send_mail('Код подтверждения', message,
    settings.EMAIL_HOST_USER,
    [email], 
    fail_silently=False)  


# Метод активирует аккаунт, который перешел по ссылке

def code_form(request, random_code):
    profile = CustomUser.objects.get(activate_code=random_code)
    profile.is_active = True
    profile.save()
    return HttpResponse("Аккаунт '{}' активирован".format(profile))



# Метод выдает токен при регистрации каждого пользоватля

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def obtain_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
