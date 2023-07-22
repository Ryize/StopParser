from django.urls import path

from api.views import OnlyHtmlViewSet


urlpatterns = [
    path('html/', OnlyHtmlViewSet.as_view())
]
