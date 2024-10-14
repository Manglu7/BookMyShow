import uuid
from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=50)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    roles = models.ManyToManyField(Role)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def generate_auth_token(self, expiration=3600):
        expires = timezone.now() + timedelta(seconds=expiration)
        token = Token.objects.create(user=self, uuid=str(uuid.uuid4()), expiration=expires)
        return token


class Token(models.Model):
    value = models.CharField(max_length=50, unique=True)
    expires = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_valid(self):
        return self.expires < timezone.now() and self.is_active


class Region(BaseModel):
    name = models.CharField(max_length=50)


class Theater(BaseModel):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Feature(BaseModel):
    name = models.CharField(max_length=50)


class Screen(BaseModel):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature)


class Movie(BaseModel):
    title = models.CharField(max_length=50)
    release_date = models.DateField()
    runtime = models.IntegerField()


class Show(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    features = models.ForeignKey(Feature, on_delete=models.CASCADE)


class ShowFeature(BaseModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)


class SeatType(models.TextChoices):
    GOLD = 'Gold', 'Gold'
    SILVER = 'Silver', 'Silver'
    PLATINUM = 'Platinum', 'Platinum'


class Seat(BaseModel):
    row_number = models.IntegerField()
    col_number = models.IntegerField()
    number = models.IntegerField()
    seat_type = models.TextField(choices=SeatType.choices)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, default=None)


class ShowSeatStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Available'
    MAINTENANCE = 'MAINTENANCE', 'Maintenance'
    RESERVED = 'RESERVED', 'Reserved'
    LOCKED = 'LOCKED', 'Locked'


class ShowSeat(BaseModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show_seat_status = models.TextField(choices=ShowSeatStatus.choices)


class ShowSeatType(BaseModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat_type = models.TextField(choices=SeatType)
    price = models.IntegerField()


class BookingStatus(models.TextChoices):
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    PENDING = 'PENDING', 'Pending'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Ticket(BaseModel):
    ticket_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    show_seats = models.ManyToManyField(ShowSeat)
    amount = models.IntegerField()
    booking_status = models.CharField(max_length=100, choices=BookingStatus.choices)
    booking_time = models.DateTimeField(default=timezone.now)


class PaymentMode(models.TextChoices):
    UPI = 'UPI'
    BANK = 'BANK', 'Bank'
    WALLET = 'WALLET', 'Wallet'
    CARD = 'CARD', 'Card'


class PaymentStatus(models.TextChoices):
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    PENDING = 'PENDING', 'Pending'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Payment(BaseModel):
    ref_number = models.IntegerField()
    mode = models.TextField(choices=PaymentMode.choices)
    status = models.TextField(choices=PaymentStatus.choices)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
