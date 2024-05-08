from rest_framework import serializers
from .models import Profile, Contract, Job


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'profession', 'balance', 'type', 'password']
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


class AmountSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)


class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='contract__client__id')
    fullName = serializers.CharField()
    paid = serializers.DecimalField(source='total_paid', max_digits=10, decimal_places=2)
