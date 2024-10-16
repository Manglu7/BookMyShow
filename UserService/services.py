from rest_framework_simplejwt.tokens import RefreshToken

from UserService.models import User, Token
from UserService.producer import send_email_event


def signup_user(self, email: str, password: str, name: str) -> User:
    user = User(email=email, name=name)
    user.set_password(password)

    user.save()

    user_email_data = {
        'to': user.email,
        'from': 'abc@gmail.com',
        'subject': 'welcome',
        'body': f'welcome {name}',
    }

    send_email_event(user_email_data)

    return user


def login_user(self, email: str, password: str) -> tuple[None, Exception] | tuple[Token, None]:
    user = User.objects.get(email=email)
    if not user.check_password(password):
        return None, Exception('Incorrect email or password')

    token = RefreshToken.for_user(user)
    return token, None
