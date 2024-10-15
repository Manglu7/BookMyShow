import random

from django.core.handlers import exception
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, Token

from bms.models import Show, ShowSeat, ShowSeatStatus, Ticket, BookingStatus
from typing import List, Tuple


class BookShowService:

    def create_booking(self, user_id: int, show_seat_ids: List[int], show_id: int) -> Ticket:
        if len(show_seat_ids) > 10:
            raise ValueError("Show seat id must be less than 10")
        try:
            user = User.objects.get(id=user_id)
            if user is None:
                raise User.DoesNotExist

            show = Show.objects.get(id=show_id)
            if show is None:
                raise Show.DoesNotExist

            show_seats = ShowSeat.objects.filter(id__in=show_seat_ids)

            for show_seat in show_seats:
                if show_seat.show_seat_status != ShowSeatStatus.AVAILABLE:
                    raise ValueError("Show seat is not available")

            for show_seat in show_seats:
                show_seat.show_seat_status = ShowSeatStatus.LOCKED
                show_seat.save()

            booking = Ticket(
                user=user,
                show=show,
                amount=100,
                ticket_number=random.randint(1, 9999),
                booking_status=BookingStatus.PENDING,
            )
            booking.save()

            #make_payment

            for show_seat in show_seats:
                show_seat.show_seat_status = ShowSeatStatus.RESERVED
                show_seat.save()

            booking.show_seats = show_seats
            booking.save()
            return booking

        except Exception as e:
            print(e)
