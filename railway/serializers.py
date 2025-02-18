from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Train, Booking

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)
    train_id = serializers.PrimaryKeyRelatedField(
        queryset=Train.objects.all(), source='train', write_only=True
    )
    
    class Meta:
        model = Booking
        fields = ('id', 'user', 'train', 'train_id', 'booked_at')
        read_only_fields = ('id', 'user', 'train', 'booked_at')
