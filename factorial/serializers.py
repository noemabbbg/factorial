# serializers.py
from rest_framework import serializers
from factorial.models import FactorialRequest, Users, History, Calculation

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        token['email'] = user.email

        return token

class FactorialRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorialRequest
        fields = ('id', 'number', 'result', 'created_at')
        read_only_fields = ('id', 'result', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Users
        # Поля, которые мы сериализуем
        fields = ["id", "login", "password", "email", "is_manager"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'calculation', 'user', 'add_date', 'calculation_result']



class CalculationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Calculation
        fields = ['pk', 'user_id', 'function', 'par_1', 'par_2', 'result', 'status', 'calc_date', 'exec_time']



