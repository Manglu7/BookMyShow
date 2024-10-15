import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from UserService.services import signup_user, login_user


# Create your views here.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = signup_user(data['email'], data['password'], data['name'])

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
            token, err = login_user(data['email'], data['password'])
            if err:
                return JsonResponse({'token': None}, status=401)
            return JsonResponse({'token': str(token.access_token), 'refresh_token': str(token)}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'token': None}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def say_hello(request):
    return JsonResponse({'hello': 'world'}, status=200)