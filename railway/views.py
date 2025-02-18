from django.shortcuts import render

from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication


from .models import Train, Booking
from .serializers import UserRegistrationSerializer, TrainSerializer, BookingSerializer
from .decorators import admin_api_required

# 1. Registration of the user
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. Login of the user
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# 3. Adding a new train
@api_view(['POST'])
@admin_api_required
def add_train(request):
    serializer = TrainSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(available_seats=serializer.validated_data.get('total_seats'))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4. Check for sseat availability
@api_view(['GET'])
def seat_availability(request):
    source = request.query_params.get('source')
    destination = request.query_params.get('destination')
    if not source or not destination:
        return Response({"error": "Please provide both source and destination"}, status=status.HTTP_400_BAD_REQUEST)
    
    trains = Train.objects.filter(source__iexact=source, destination__iexact=destination)
    serializer = TrainSerializer(trains, many=True)
    return Response(serializer.data)

# 5. Booking seat
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_seat(request):
    train_no = request.data.get('train_no')
    if not train_no:
        return Response({"error": "Train No is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Use transaction.atomic and select_for_update to prevent multiple users from booking the same seat.
        with transaction.atomic():
            train = Train.objects.select_for_update().get(train_no=train_no)
            if train.available_seats <= 0:
                return Response(data={"error": "No seats available"}, status=status.HTTP_400_BAD_REQUEST)
        
            train.available_seats -= 1
            train.save()

            booking = Booking.objects.create(user=request.user, train=train)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Train.DoesNotExist:
        return Response({"error": "Train not found"}, status=status.HTTP_404_NOT_FOUND)

# 6. Getting booking details
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def booking_details(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
