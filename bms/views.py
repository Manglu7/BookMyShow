from django.shortcuts import render
from rest_framework import viewsets

from .models import BookingStatus
from .serializers import BookingRequestSerializer, BookingResponseSerializer


# Create your views here.


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
