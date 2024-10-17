from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path("create_review/<int:order_id>", create_review, name="create_review"),
]