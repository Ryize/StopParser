from django.urls import path

from api.views import HtmlCssViewSet

urlpatterns = [
    path('html_css/', HtmlCssViewSet.as_view()),
]
