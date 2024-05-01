from rest_framework import serializers
from .models import Profile, Contract, Job


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'profession', 'balance', 'user_type', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile = Profile.objects.create_user(**validated_data)
        return profile


class ContractSerializer(serializers.ModelSerializer):
    client = ProfileSerializer()
    contractor = ProfileSerializer()

    class Meta:
        model = Contract
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class BalanceDepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
