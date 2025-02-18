from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('admin/add-train/', views.add_train, name='add_train'),
    path('trains/', views.seat_availability, name='seat_availability'),
    path('book/', views.book_seat, name='book_seat'),
    path('booking/<int:booking_id>/', views.booking_details, name='booking_details'),
]
