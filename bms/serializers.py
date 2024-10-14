from rest_framework import serializers

from bms.models import BookingStatus

from rest_framework_simplejwt.serializers import TokenObtainSerializer

class CustomTokenObtainSerializer(TokenObtainSerializer):




class BookingRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    show_id = serializers.IntegerField()
    show_seat_ids = serializers.ListField(child=serializers.IntegerField())


class BookingResponseSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField(required=False)
    status = serializers.CharField(max_length=100)