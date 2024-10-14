import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BookingStatus
from .serializers import BookingRequestSerializer, BookingResponseSerializer
from services import UserService


# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_service = UserService()
        user = user_service.signup_user(data['email'], data['password'], data['name'])

        if user:
            refresh_token = RefreshToken.for_user(user)

            return JsonResponse({
                'user': user.name,
                'email': user.email,
                'user_id': user.id,
                'roles': [roles.name for roles in user.roles.all()],
                'token': str(refresh_token.access_token),
                'refresh_token': str(refresh_token),
            }, status=201)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_service = UserService()
            token, err = user_service.login_user(data['email'], data['password'])
            if err:
                return JsonResponse({'token': None}, status=401)
            return JsonResponse({'token': str(token.access_token), 'refresh_token': str(token)}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'token': None}, status=500)


class BookingViewSet(viewsets.ViewSet):

    def __init__(self, service, **kwargs):
        self.service = service
        super().__init__(**kwargs)

    def create_booking(self, request):
        req = BookingRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        try:
            booking = self.service.create_booking(
                user_id=req.validated_data['user_id'],
                show_seat_ids=req.validated_data['show_seat_ids'],
                show_id=req.validated_data['show_id'],
            )
            data = {
                'booking_id': booking.id,
                'status': booking.booking_status,
            }
            return BookingResponseSerializer(data=data)
        except Exception as e:
            print(e)
            return BookingResponseSerializer({'status': 'ERROR'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def say_hello(request):
    return JsonResponse({'hello': 'world'}, status=200)