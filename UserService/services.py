from rest_framework_simplejwt.tokens import RefreshToken

from UserService.models import User, Token


def signup_user(self, email: str, password: str, name: str) -> User:
    user = User(email=email, name=name)
    user.set_password(password)
    user.save()
    return user


def login_user(self, email: str, password: str) -> tuple[None, Exception] | tuple[Token, None]:
    user = User.objects.get(email=email)
    if not user.check_password(password):
        return None, Exception('Incorrect email or password')

    token = RefreshToken.for_user(user)
    return token, None
