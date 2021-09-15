from django.urls import path

from sites.views import AddVisits, ListVisits

urlpatterns = [
    path('visited_links/', AddVisits.as_view()),
    path('visited_domains/', ListVisits.as_view()),
]
