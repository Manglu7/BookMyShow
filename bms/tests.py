from unittest.mock import Mock

from django.test import TestCase, TransactionTestCase
from django.utils import timezone

from bms.models import User, Movie, Region, Theater, Screen, Seat, SeatType, Show, Feature, ShowSeat, ShowSeatStatus, \
    ShowSeatType
from bms.services import BookShowService
from bms.views import BookingViewSet


# Create your tests here.

class BookingTestCase(TransactionTestCase):

    def setUp(self):
        self.user, created = User.objects.get_or_create(
            id=1,
            email='abc@gmail.com',
            password='password'
        )

        self.movie, created = Movie.objects.get_or_create(
            title='asd',
            release_date='2024-07-27',
            runtime=200
        )

        self.region, created = Region.objects.get_or_create(
            name='Delhi'
        )

        self.theater, created = Theater.objects.get_or_create(
            name='inox',
            region=self.region
        )

        self.screen, created = Screen.objects.get_or_create(
            region=self.region,
            name='audi1',
            theater=self.theater
        )

        self.seat1, created = Seat.objects.get_or_create(
            row_number=1,
            col_number=1,
            number="11",
            seat_type=SeatType.PLATINUM,
            screen=self.screen
        )

        self.seat2, created = Seat.objects.get_or_create(
            row_number=1,
            col_number=2,
            number="12",
            seat_type=SeatType.PLATINUM,
            screen=self.screen
        )

        self.feature, created = Feature.objects.get_or_create(
            name='2D'
        )

        self.show, created = Show.objects.get_or_create(
            movie=self.movie,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            screen=self.screen,
            features=self.feature
        )

        self.show_seat1, created = ShowSeat.objects.get_or_create(
            show=self.show,
            seat=self.seat1,
            show_seat_status=ShowSeatStatus.AVAILABLE
        )

        self.show_seat2, created = ShowSeat.objects.get_or_create(
            show=self.show,
            seat=self.seat2,
            show_seat_status=ShowSeatStatus.AVAILABLE
        )

        self.show_seat_type, created = ShowSeatType.objects.get_or_create(
            show=self.show,
            seat_type=SeatType.PLATINUM,
            price=250
        )

    def test_create_booking(self):
        self.service = BookShowService()
        self.view = BookingViewSet(service=self.service)

        request_data = {
            'user_id': 1,
            'show_id': 1,
            'show_seat_ids': [1, 2]
        }

        request = Mock()
        request.data = request_data
        booking = self.view.create_booking(request)
