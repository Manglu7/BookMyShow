from django.shortcuts import render
from rest_framework import viewsets

from .serializers import BookingRequestSerializer


# Create your views here.


class BookingViewSet(viewsets.ViewSet):

    def create_booking(self, request):
        req = BookingRequestSerializer(request.data)
        req.is_valid(raise_exception=True)
        
