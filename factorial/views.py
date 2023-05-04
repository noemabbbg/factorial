from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
import json
import math
import asyncio
import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Calculation, Users, History
from rest_framework import viewsets, status
from .serializers import UserSerializer, HistorySerializer
from rest_framework.views import APIView, Response
KAFKA_TOPIC = 'factorial'
KAFKA_SERVERS = ['localhost:9092']


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = Users.objects.filter(id = payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response

# Функция для вычисления факториала числа
def calculate_factorial(number):
    result = math.factorial(number)
    return result

# Функция для вычисления НОД
def gcd_calculator(a, b):
    while b:
        a, b = b, a % b
    return a

# Функция для отправки сообщения в Kafka
async def send_to_kafka(data):
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVERS,
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    producer.send(KAFKA_TOPIC, data)
    producer.flush()
    producer.close()

# Вьюшка для обработки запросов и вычисления факториала числа или НОД
@csrf_exempt
def calculate(request):
    if request.method == 'POST':
        # Получаем число из тела запроса
        data = json.loads(request.body.decode('utf-8'))
        number = int(data['number'])
        # Вычисляем факториал числа
        result = calculate_factorial(number)
        # Сохраняем результат в базе данных
        calculation = Calculation(number=number, result=result)
        calculation.save()
        # Отправляем число в Kafka
        asyncio.run(send_to_kafka(data))
        # Возвращаем результат в формате JSON
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    


# Вьюшка для вычисления НОД
# Вьюшка для вычисления НОД
@csrf_exempt
def calculate_gcd(request):
    if request.method == 'POST':
        # Получаем числа из тела запроса
        data = json.loads(request.body.decode('utf-8'))
        a = int(data['a'])
        b = int(data['b'])
        # Вычисляем НОД
        result = gcd_calculator(a, b)
        # Сохраняем результат в базе данных
        calculation = Calculation(a=a, b=b, result=result)
        calculation.save()
        # Отправляем числа в Kafka
        asyncio.run(send_to_kafka(data))
        # Возвращаем результат в формате JSON
        return JsonResponse({'result': result})
    else:
        return JsonResponse({'error': 'Invalid request method'})

from rest_framework import permissions
class IsLoggedInUserOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff 

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать акции компаний
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Users.objects.all().order_by('pk')
    serializer_class = UserSerializer  # Сериализатор для модели




class HistoryViewSet(viewsets.ModelViewSet):
    queryset = Calculation.objects.all().order_by('pk')
    serializer_class = HistorySerializer
    def get(self, request):
        serializer = HistorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


'''
def history(request):
    calculations = Calculation.objects.all().order_by('pk')
    print(calculations)
    data = []
    for calc in calculations:
        data.append({
            'number': calc.number,
            'result': calc.result,
            
        })
    return JsonResponse(data, safe=False)

'''





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['login'] = user.login
        token['email'] = user.email
        token['is_manager'] = user.is_manager;

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LoginView(APIView):
    def post(self, request):
        login = request.data['login']
        password = request.data['password']

        user = Users.objects.filter(login = login).first()

        if user is None:
            raise AuthenticationFailed('User not found.')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password.')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token
        }

        return response
